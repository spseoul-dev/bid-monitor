"""
나라장터 사전규격 수집기 - 용역
API: 조달청_나라장터 사전규격정보서비스 / getPublicPrcureThngInfoServcPPSSrch
※ 입찰공고정보서비스와 별개 서비스라 data.go.kr 에서 따로 활용신청 필요 (같은 인증키 사용)
- inqryDiv=1 : 접수일시 기준
"""
import json

from ..models import Notice
from .g2b import G2BCollector, _fmt_dt, _to_int


def _first(it: dict, *keys):
    for k in keys:
        v = it.get(k)
        if v not in (None, ""):
            return str(v).strip()
    return ""


class G2BPrespecCollector(G2BCollector):
    name = "g2b_prespec"

    @staticmethod
    def _to_notice(it: dict) -> Notice:
        no = _first(it, "bfSpecRgstNo", "refNo")
        title = _first(it, "prdctClsfcNoNm", "bfSpecNm", "dtilPrdctClsfcNoNm")
        return Notice(
            source="g2b_prespec",
            notice_no=no,
            ord="00",
            title=title,
            institution=_first(it, "orderInsttNm", "ntceInsttNm"),
            demand_institution=_first(it, "rlDminsttNm", "dminsttNm"),
            notice_date=_fmt_dt(_first(it, "rcptDt", "rgstDt")),
            close_date=_fmt_dt(_first(it, "opninRgstClseDt")),   # 의견등록 마감
            budget=_to_int(it.get("asignBdgtAmt")),
            notice_kind="사전규격",
            service_div=_first(it, "bsnsDivNm"),
            url=_first(it, "bfSpecDtlUrl", "specDocUrl"),
            raw=json.dumps(it, ensure_ascii=False),
        )
