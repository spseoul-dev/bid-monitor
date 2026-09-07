"""
나라장터 API → docs/index.html 생성 (GitHub Actions 가 매일 실행)
로컬 테스트: .env 에 키 넣고  python build.py
"""
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

from bidmon.config import load_config, ROOT
from bidmon.filters import tag_institutions, categorize
from bidmon.collectors import G2BCollector, G2BPrespecCollector

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("build")

DOCS = ROOT / "docs"
SEEN = DOCS / "seen.json"
KEEP = ["title", "institution", "demand_institution", "notice_date", "close_date",
        "estimated_price", "budget", "award_method", "notice_kind", "url", "tags", "category"]


def main():
    cfg = load_config()
    days = int(cfg.get("lookback_days", 30))
    collectors = [G2BCollector(cfg["g2b"])]
    if (cfg.get("g2b_prespec") or {}).get("enabled"):
        collectors.append(G2BPrespecCollector({**cfg["g2b"], **cfg["g2b_prespec"]}))

    notices = []
    for c in collectors:
        notices += c.safe_collect(days)
    for n in notices:
        tag_institutions(n, cfg["institutions"])
        categorize(n)

    # 처음 본 날짜 기록 (NEW 표시용). 60일 지난 항목은 정리
    seen = json.loads(SEEN.read_text(encoding="utf-8")) if SEEN.exists() else {}
    today = datetime.now().strftime("%Y-%m-%d")
    cutoff = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")
    seen = {k: v for k, v in seen.items() if v >= cutoff}
    data = []
    for n in notices:
        first = seen.setdefault(n.key, today)
        d = {k: getattr(n, k) for k in KEEP}
        d["first_seen"] = first
        data.append(d)
    data.sort(key=lambda r: r["notice_date"] or "", reverse=True)

    kw = {"include": cfg["filters"]["include_keywords"], "exclude": cfg["filters"]["exclude_keywords"]}
    now = datetime.now()
    html = ((ROOT / "bidmon" / "page.html").read_text(encoding="utf-8")
            .replace("__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
            .replace("__KW__", json.dumps(kw, ensure_ascii=False))
            .replace("__DATE__", now.strftime("%Y-%m-%d %H:%M"))
            .replace("__NOW__", now.strftime("%Y-%m-%dT%H:%M:%S")))
    DOCS.mkdir(exist_ok=True)
    (DOCS / "index.html").write_text(html, encoding="utf-8")
    SEEN.write_text(json.dumps(seen, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    log.info("index.html 생성: 공고 %d건, %.1f MB", len(data), (DOCS / "index.html").stat().st_size / 1e6)


if __name__ == "__main__":
    main()
