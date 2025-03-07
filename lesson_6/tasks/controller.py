from py_eth_async.client import Client
from py_eth_async.data.models import Networks
from py_eth_async.exceptions import HTTPException

from tasks.base import Base
from tasks.coredao import CoredaoBridge
from tasks.stargate import Stargate
from tasks.testnetbridge import Testnetbridge
from tasks.uniswap import Uniswap
from tasks.woofi import WooFi
from data.models import Contracts

from loguru import logger
class Controller(Base):
    def __init__(self, client: Client):
        super().__init__(client=client)
        self.coredao = CoredaoBridge(client=client)
        self.stargate = Stargate(client=client)
        self.testnetbridge = Testnetbridge(client=client)
        self.uniswap = Uniswap(client=client)
        self.woofi = WooFi(client=client)

    async def count_coredao_swaps(self) -> int:
        client = Client(private_key='', network=Networks.BSC)
        try:
            txs = await client.transactions.find_txs(
                contract=Contracts.BSC_COREDAO_BRIDGE,
                function_name='bridge',
                address=self.client.account.address,
            )
        except HTTPException as err:
            return 0
        return len(txs)

    async def count_testnetbridge_swaps(self) -> int:
        client = Client(private_key='', network=Networks.Arbitrum)
        try:
            txs = await client.transactions.find_txs(
                contract=Contracts.ARBITRUM_TESTNETBRIDGE,
                function_name='sendFrom',
                address=self.client.account.address,
            )
        except HTTPException as err:
            return 0
        return len(txs)

    async def count_stargate_swaps(self) -> int:
        tx_counter = 0
        for network in Stargate.supported_networks:
            client = Client(private_key='', network=network)
            print(network.name)
            try:
                contract = Stargate.contract_data[network.name]['stargate_contract']
                txs = await client.transactions.find_txs(
                    contract=contract,
                    methodId='0x9fbf10fc',
                    address=self.client.account.address,
                )
                tx_counter += len(txs)
            except HTTPException as err:
                return 0
        return tx_counter
