from typing import Optional, Union
from dataclasses import dataclass

from pretty_utils.type_functions.classes import Singleton, AutoRepr
from py_eth_async.data.models import RawContract, DefaultABIs
from pretty_utils.miscellaneous.files import read_json

from data.config import ABIS_DIR, SETTINGS_PATH


class Contracts(Singleton):
    ARBITRUM_WOOFI = RawContract(
        address='0x9aed3a8896a85fe9a8cac52c9b402d092b629a30', abi=read_json(path=(ABIS_DIR, 'woofi.json'))
    )

    ARBITRUM_USDC = RawContract(
        address='0xaf88d065e77c8cC2239327C5EDb3A432268e5831', abi=DefaultABIs.Token
    )

    ARBITRUM_USDC_e = RawContract(
        address='0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8', abi=DefaultABIs.Token
    )

    ARBITRUM_WBTC = RawContract(
        address='0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f', abi=DefaultABIs.Token
    )

    ARBITRUM_STARGATE = RawContract(
        address='0x53bf833a5d6c4dda888f69c22c88c9f356a41614', abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    ARBITRUM_ETH = RawContract(
        address='0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE', abi=DefaultABIs.Token
    )

    POLYGON_USDC = RawContract(
        address='0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174', abi=DefaultABIs.Token
    )

    POLYGON_STARGATE = RawContract(
        address='0x45a01e4e04f14f7a4a6702c74187c5f6222033cd', abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    AVALANCHE_STARGATE = RawContract(
        address='0x45a01e4e04f14f7a4a6702c74187c5f6222033cd', abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    AVALANCHE_USDC = RawContract(
        address='0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E', abi=DefaultABIs.Token
    )

    OPTIMISM_USDC = RawContract(
        address='0x7F5c764cBc14f9669B88837ca1490cCa17c31607', abi=DefaultABIs.Token
    )

    OPTIMISM_STARGATE = RawContract(
        address='0xb0d502e938ed5f4df2e681fe6e419ff29631d62b', abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    BSC_COREDAO_BRIDGE = RawContract(
        address='0x52e75D318cFB31f9A2EdFa2DFee26B161255B233', abi=read_json(path=(ABIS_DIR, 'coredao_bridge.json'))
    )

    BSC_USDT = RawContract(
        address='0x55d398326f99059ff775485246999027b3197955', abi=DefaultABIs.Token
    )

    ARBITRUM_UNISWAP_ROUTER = RawContract(
        address='0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad', abi=read_json(path=(ABIS_DIR, 'uniswap.json'))
    )

    ARBITRUM_GETH = RawContract(
        address='0xdD69DB25F6D620A7baD3023c5d32761D353D3De9', abi=DefaultABIs.Token
    )

    ARBITRUM_TESTNETBRIDGE = RawContract(
        address='0xdd69db25f6d620a7bad3023c5d32761d353d3de9', abi=read_json(path=(ABIS_DIR, 'testnetbridge.json'))
    )



class InitialCsvData:
    HEADER = ['private_key', 'name', 'proxy']

    def __init__(self, private_key: str, name: str = '', proxy: str = ''):
        self.private_key = private_key
        self.name = name
        self.proxy = proxy


@dataclass
class FromTo:
    from_: Union[int, float]
    to_: Union[int, float]


class Settings(Singleton, AutoRepr):
    def __init__(self):
        json = read_json(path=SETTINGS_PATH)

        self.stargate_swaps: FromTo = FromTo(
            from_=json['stargate_swaps']['from'], to_=json['stargate_swaps']['to']
        )
        self.stargate_swaps_usdc_amount: FromTo = FromTo(
            from_=json['stargate_swaps_usdc_amount']['from'], to_=json['stargate_swaps_usdc_amount']['to']
        )
        self.coredao_swaps: FromTo = FromTo(
            from_=json['coredao_swaps']['from'], to_=json['coredao_swaps']['to']
        )
        self.coredao_swaps_amount: FromTo = FromTo(
            from_=json['coredao_swaps_amount']['from'], to_=json['coredao_swaps_amount']['to']
        )

        self.uniswap_geth_amount: FromTo = FromTo(
            from_=json['uniswap_geth_amount']['from'], to_=json['uniswap_geth_amount']['to']
        )

        self.testnetbridge_swaps: FromTo = FromTo(
            from_=json['testnetbridge_swaps']['from'], to_=json['testnetbridge_swaps']['to']
        )
        self.testnetbridge_swaps_amount: FromTo = FromTo(
            from_=json['testnetbridge_swaps_amount']['from'], to_=json['testnetbridge_swaps_amount']['to']
        )
        self.initial_actions_delay: FromTo = FromTo(
            from_=json['initial_actions_delay']['from'], to_=json['initial_actions_delay']['to']
        )
        self.activity_actions_delay: FromTo = FromTo(
            from_=json['activity_actions_delay']['from'], to_=json['activity_actions_delay']['to']
        )

        self.max_fee = float(json['max_fee'])
