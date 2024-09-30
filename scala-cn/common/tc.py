from enum import Enum
from ipaddress import IPv4Interface, IPv6Interface
import re
from typing import List

class TCEventType(Enum):
    UNKNOWN = ''
    ADDED = 'added'
    REPLACE = 'replaced'
    DELETE = 'deleted'

class TCDirection(Enum):
    INGRESS = 'ingress'
    EGRESS = 'egress'

class TCActionType(Enum):
    TUNNEL_KEY_SET = 'TUNNEL_KEY_SET'
    TUNNEL_KEY_UNSET = 'TUNNEL_KEY_UNSET'
    EGRESS_REDIRECT = 'EGRESS_REDIRECT'
    INGRESS_REDIRECT = 'INGRESS_REDIRECT'
    ETH_PEDIT = 'ETH_PEDIT'

class TCAction():
    def __init__(self) -> None:
        self.action_order: int = None
        self.action_type: TCActionType = None
        self.tunnel_src_ip: IPv4Interface = IPv4Interface('0.0.0.0/0.0.0.0')
        self.tunnel_dst_ip: IPv4Interface = IPv4Interface('0.0.0.0/0.0.0.0')
        self.tunnel_dst_port: int = None
        self.redirect_target: str = None
        self.eth_pedit: str = None
        self.cookie: str = None
        self.others: str = None

class TCItem():

    def __init__(self, tc_item: 'TCItem'=None) -> None:
        from common.matcher import FlowEthType
        if tc_item is None:
            self.event_type: TCEventType = None
            self.dev: str = None
            self.direction: TCDirection = None
            self.protocol: str = None
            self.priority: int = None
            self.chain: int = None
            self.handle: int = None
            self.eth_type: FlowEthType = None
            self.src_mac: str = None
            self.dst_mac: str = None
            self.src_ipv4: IPv4Interface = IPv4Interface('0.0.0.0/0.0.0.0')
            self.dst_ipv4: IPv4Interface = IPv4Interface('0.0.0.0/0.0.0.0')
            self.src_ipv6: IPv6Interface = IPv6Interface('0000:0000:0000:0000:0000:0000:0000:0000/0')
            self.dst_ipv6: IPv6Interface = IPv6Interface('0000:0000:0000:0000:0000:0000:0000:0000/0')
            self.enc_src_ip: IPv4Interface = IPv4Interface('0.0.0.0/0.0.0.0')
            self.enc_dst_ip: IPv4Interface = IPv4Interface('0.0.0.0/0.0.0.0')
            self.enc_key_id: str = None
            self.enc_dst_port: int = None
            self.hw_flag: str = None
            self.others: str = None
            self.actions: List[TCAction] = []
            self.raw_item: str = ''
        else:
            self.event_type: TCEventType = tc_item.event_type
            self.dev: str = tc_item.dev
            self.direction: TCDirection = tc_item.direction
            self.protocol: str = tc_item.protocol
            self.priority: int = tc_item.priority
            self.chain: int = tc_item.chain
            self.handle: int = tc_item.handle
            self.eth_type: FlowEthType = tc_item.eth_type
            self.src_mac: str = tc_item.src_mac
            self.dst_mac: str = tc_item.dst_mac
            self.src_ipv4: IPv4Interface = tc_item.src_ipv4
            self.dst_ipv4: IPv4Interface = tc_item.dst_ipv4
            self.src_ipv6: IPv6Interface = tc_item.src_ipv6
            self.dst_ipv6: IPv6Interface = tc_item.dst_ipv6
            self.enc_src_ip: IPv4Interface = tc_item.enc_src_ip
            self.enc_dst_ip: IPv4Interface = tc_item.enc_dst_ip
            self.enc_key_id: str = tc_item.enc_key_id
            self.enc_dst_port: int = tc_item.enc_dst_port
            self.hw_flag: str = tc_item.hw_flag
            self.others: str = tc_item.others
            self.actions: List[TCAction] = tc_item.actions
            self.raw_item: str = tc_item.raw_item
    
    @staticmethod
    def get_param_after_key(tc_line: str, key: str) -> str:
        matches = re.findall(rf'{key}\s+(\S+)', tc_line)
        if matches:
            return matches[-1]
        else:
            return None
    
    @staticmethod
    def trim_mac(origin: str) -> str:
        origin = origin[0:12]
        return ':'.join([origin[i: i+2] for i in range(0, len(origin), 2)])