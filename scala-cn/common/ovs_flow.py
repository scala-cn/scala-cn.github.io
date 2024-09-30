

from enum import Enum
from ipaddress import IPv4Interface, IPv6Interface
from typing import Dict, List


class OVSFlowActionType(Enum):
    SET_TUNNEL = 'SET_TUNNEL',
    SET_ETH = 'SET_ETH',
    SET_SKB_MARK = 'SET_SKB_MARK',
    USERSPACE = 'USERSPACE',
    REDIRECT = 'REDIRECT',

class OVSFlowAction():
    def __init__(self) -> None:
        self.action_order: int = None
        self.action_type: OVSFlowActionType = None
        self.tunnel_src_ip: IPv4Interface = IPv4Interface('0.0.0.0/0.0.0.0')
        self.tunnel_dst_ip: IPv4Interface = IPv4Interface('0.0.0.0/0.0.0.0')
        self.tunnel_dst_port: int = None
        self.redirect_target: str = None
        self.eth_dst: str = None
        self.others: str = None

class OVSFlowItem():
    def __init__(self, flow_item: 'OVSFlowItem'=None) -> None:
        from common.matcher import FlowEthType
        if flow_item is None:
            self.ufid: str = None
            self.tunnel_id: str = None
            self.tunnel_src: IPv4Interface = IPv4Interface('0.0.0.0/0.0.0.0')
            self.tunnel_dst: IPv4Interface = IPv4Interface('0.0.0.0/0.0.0.0')
            self.tunnel_tp_dst: int = None
            self.in_port: str = None
            self.eth_src: str = None
            self.eth_dst: str = None
            self.eth_type: FlowEthType = None
            self.ipv4_src: IPv4Interface = IPv4Interface('0.0.0.0/0.0.0.0')
            self.ipv4_dst: IPv4Interface = IPv4Interface('0.0.0.0/0.0.0.0')
            self.ipv6_src: IPv6Interface = IPv6Interface('0000:0000:0000:0000:0000:0000:0000:0000/0')
            self.ipv6_dst: IPv6Interface = IPv6Interface('0000:0000:0000:0000:0000:0000:0000:0000/0')
            self.packets: int = None
            self.byte: int = None
            self.used: float = None
            self.offloaded: str = None
            self.dp: str = None
            self.actions: List[OVSFlowAction] = []
            self.flow_history_bytes: List[Dict] = []
            self.flow_history_packets: List[Dict] = []
            self.raw_item: str = ''
        else:
            self.ufid: str = flow_item.ufid
            self.tunnel_id: str = flow_item.tunnel_id
            self.tunnel_src: IPv4Interface = flow_item.tunnel_src
            self.tunnel_dst: IPv4Interface = flow_item.tunnel_dst
            self.tunnel_tp_dst: int = flow_item.tunnel_tp_dst
            self.in_port: str = flow_item.in_port
            self.eth_src: str = flow_item.eth_src
            self.eth_dst: str = flow_item.eth_dst
            self.eth_type: FlowEthType = flow_item.eth_type
            self.ipv4_src: IPv4Interface = flow_item.ipv4_src
            self.ipv4_dst: IPv4Interface = flow_item.ipv4_dst
            self.ipv6_src: IPv6Interface = flow_item.ipv6_src
            self.ipv6_dst: IPv6Interface = flow_item.ipv6_dst
            self.packets: int = flow_item.packets
            self.byte: int = flow_item.byte
            self.used: float = flow_item.used
            self.offloaded: str = flow_item.offloaded
            self.dp: str = flow_item.dp
            self.actions: List[OVSFlowAction] = flow_item.actions
            self.flow_history_bytes: List[Dict] = flow_item.flow_history_bytes
            self.flow_history_packets: List[Dict] = flow_item.flow_history_packets
            self.raw_item: str = flow_item.raw_item
    
    def matched_by_other_flow(self, new_flow_item: 'OVSFlowItem'=None) -> bool:
        if new_flow_item is None:
            return False
        if self.tunnel_id != new_flow_item.tunnel_id:
            return False
        if (self.tunnel_src is None and new_flow_item.tunnel_src is not None) or \
            (self.tunnel_src is not None and new_flow_item.tunnel_src is None) or \
            (self.tunnel_src is not None and new_flow_item.tunnel_src is not None and \
             not self.tunnel_src.network.subnet_of(new_flow_item.tunnel_src.network)):
            return False
        if (self.tunnel_dst is None and new_flow_item.tunnel_dst is not None) or \
            (self.tunnel_dst is not None and new_flow_item.tunnel_dst is None) or \
            (self.tunnel_dst is not None and new_flow_item.tunnel_dst is not None and \
             not self.tunnel_dst.network.subnet_of(new_flow_item.tunnel_dst.network)):
            return False
        if self.tunnel_tp_dst != new_flow_item.tunnel_tp_dst:
            return False
        if self.in_port != new_flow_item.in_port:
            return False
        if self.eth_src != new_flow_item.eth_src:
            return False
        if self.eth_dst != new_flow_item.eth_dst:
            return False
        if self.eth_type != new_flow_item.eth_type:
            return False
        if (self.ipv4_src is None and new_flow_item.ipv4_src is not None) or \
            (self.ipv4_src is not None and new_flow_item.ipv4_src is None) or \
            (self.ipv4_src is not None and new_flow_item.ipv4_src is not None and \
             not self.ipv4_src.network.subnet_of(new_flow_item.ipv4_src.network)):
            return False
        if (self.ipv4_dst is None and new_flow_item.ipv4_dst is not None) or \
            (self.ipv4_dst is not None and new_flow_item.ipv4_dst is None) or \
            (self.ipv4_dst is not None and new_flow_item.ipv4_dst is not None and \
             not self.ipv4_dst.network.subnet_of(new_flow_item.ipv4_dst.network)):
            return False
        if (self.ipv6_src is None and new_flow_item.ipv6_src is not None) or \
            (self.ipv6_src is not None and new_flow_item.ipv6_src is None) or \
            (self.ipv6_src is not None and new_flow_item.ipv6_src is not None and \
             not self.ipv6_src.network.subnet_of(new_flow_item.ipv6_src.network)):
            return False
        if (self.ipv6_dst is None and new_flow_item.ipv6_dst is not None) or \
            (self.ipv6_dst is not None and new_flow_item.ipv6_dst is None) or \
            (self.ipv6_dst is not None and new_flow_item.ipv6_dst is not None and \
             not self.ipv6_dst.network.subnet_of(new_flow_item.ipv6_dst.network)):
            return False
        
        for action in self.actions:
            for new_action in new_flow_item.actions:
                if action.action_type == new_action.action_type:
                    if action.eth_dst != new_action.eth_dst:
                        return False
                    if action.redirect_target != new_action.redirect_target:
                        return False
                    if action.tunnel_dst_port != new_action.tunnel_dst_port:
                        return False
                    if (action.tunnel_src_ip is None and new_action.tunnel_src_ip is not None) or \
                        (action.tunnel_src_ip is not None and new_action.tunnel_src_ip is None) or \
                        (action.tunnel_src_ip is not None and new_action.tunnel_src_ip is not None and \
                        not action.tunnel_src_ip.network.subnet_of(new_action.tunnel_src_ip.network)):
                        return False
                    if (action.tunnel_dst_ip is None and new_action.tunnel_dst_ip is not None) or \
                        (action.tunnel_dst_ip is not None and new_action.tunnel_dst_ip is None) or \
                        (action.tunnel_dst_ip is not None and new_action.tunnel_dst_ip is not None and \
                        not action.tunnel_dst_ip.network.subnet_of(new_action.tunnel_dst_ip.network)):
                        return False
        return True