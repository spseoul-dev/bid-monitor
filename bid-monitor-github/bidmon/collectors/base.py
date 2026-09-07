import logging
from abc import ABC, abstractmethod
from ..models import Notice

log = logging.getLogger(__name__)


class BaseCollector(ABC):
    name: str = "base"

    @abstractmethod
    def collect(self, lookback_days: int) -> list[Notice]:
        ...

    def safe_collect(self, lookback_days: int) -> list[Notice]:
        try:
            items = self.collect(lookback_days)
            log.info("[%s] %d건 수집", self.name, len(items))
            return items
        except Exception as e:  # 한 소스가 죽어도 나머지는 계속
            log.exception("[%s] 수집 실패: %s", self.name, e)
            return []
