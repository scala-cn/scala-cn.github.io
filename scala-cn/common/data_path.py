

from typing import List


class DpPort():
    
    def __init__(self) -> None:
        self.id: int = None
        self.name: str = None

class DpItem:
    def __init__(self, dp_item: 'DpItem'=None) -> None:
        if dp_item is None:
            self.lookups_hit: int = None
            self.lookups_missed: int = None
            self.lookups_lost: int = None
            self.flows: int = None
            self.masks_hit: int = None
            self.masks_total: int = None
            self.masks_hit_pkt: int = None
            self.ports: List[DpPort] = []
        else:
            self.lookups_hit: int = dp_item.lookups_hit
            self.lookups_missed: int = dp_item.lookups_missed
            self.lookups_lost: int = dp_item.lookups_lost
            self.flows: int = dp_item.flows
            self.masks_hit: int = dp_item.masks_hit
            self.masks_total: int = dp_item.masks_total
            self.masks_hit_pkt: int = dp_item.masks_hit_pkt
            self.ports: List[DpPort] = dp_item.ports
            self.timestamp: float = dp_item.timestamp