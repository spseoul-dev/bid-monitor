# -*- coding: utf-8 -*-
"""LH 수집기 단독 테스트: 용역 공고 전체 수집 + 2603342 확인 + 상세페이지 원본 저장"""
import logging, sys, json
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
sys.path.insert(0, ".")
from bidmon.collectors.lh import LHCollector, DETAIL_URL

c = LHCollector({})
# 상세페이지 원본 저장 (파서 보정용)
r = c.sess.get(DETAIL_URL["20"], params={"bidNum": "2603342", "bidDegree": "00"}, timeout=60)
r.encoding = r.apparent_encoding
open("lh_detail_2603342.html", "w", encoding="utf-8").write(r.text)
print("상세 원본 저장: lh_detail_2603342.html", len(r.text), "chars")
print("상세 추출 결과:", c._detail("2603342", "00", "20"))

items = c.collect(30)
print(f"\nLH 용역 공고 {len(items)}건")
hit = [n for n in items if n.notice_no == "2603342"]
print("2603342 노후청사:", "✓ 있음" if hit else "✗ 없음")
lines = []
for n in sorted(items, key=lambda x: x.close_date):
    lines.append(f"{n.notice_no}-{n.ord} | 공고 {n.notice_date or '-'} | 마감 {n.close_date} | {n.estimated_price or '-'} | {n.notice_kind} | {n.title}")
open("lhtest2_result.txt", "w", encoding="utf-8").write("\n".join(lines))
print("\n".join(lines[:15]))
print("\n→ lhtest2_result.txt, lh_detail_2603342.html 저장")
