'''
eth -> usdc (0.001): https://explorer.zksync.io/tx/0x4d2215efd2a054fa4d0d0f40d3d7b73006613d955ff55b8e80b1b883af8ba006
usdc -> eth: https://explorer.zksync.io/tx/0x4dbbe7154c3f164dfab0dfeb3d2f31f25668d49b4dd6258b0234b26179d3f9b8
'''

from py_eth_async.data.models import Network, Networks, GWei, RawContract, DefaultABIs
import time
import asyncio
import random
from web3.types import TxParams
from web3 import Web3

from tasks.base import Base
from py_eth_async.data.models import Ether, TxArgs, TokenAmount
from pretty_utils.type_functions.floats import randfloat

from data.models import Settings, Contracts


class SyncSwap(Base):
    async def swap_eth_to_usdc(self) -> str:
        settings = Settings()
        slippage = 1

        to_token = Contracts.USDC

        to_token = await self.client.contracts.default_token(contract_address=to_token)
        to_token_name = await to_token.functions.symbol().call()

        failed_text = f'Failed swap ETH to {to_token_name} via SyncSwap'

        amount = Ether(randfloat(
            from_=settings.eth_amount_for_swap.from_,
            to_=settings.eth_amount_for_swap.to_,
            step=0.0000001
        ))
        contract = await self.client.contracts.get(contract_address=Contracts.SYNCSWAP)

        eth_price = await self.get_token_price(token='ETH')
        amount_out_min = TokenAmount(
            amount=float(amount.Ether) * eth_price * (1 - slippage / 100),
            decimals=await self.get_decimals(contract_address=to_token.address)
        )

        pool = Web3.to_checksum_address('0x80115c708e12edd42e504c1cd52aea96c547c05c')

        params = TxArgs(
            paths=[
                TxArgs(
                    steps=[
                        TxArgs(
                            pool=pool,
                            data=f'0x{Contracts.WETH.address[2:].zfill(64)}'
                                 f'{str(self.client.account.address)[2:].zfill(64)}'
                                 f'{"2".zfill(64)}',
                            callback='0x0000000000000000000000000000000000000000',
                            callbackData='0x'
                        ).tuple()
                    ],
                    tokenIn='0x0000000000000000000000000000000000000000',
                    amountIn=amount.Wei,
                ).list()
            ],
            amountOutMin=amount_out_min.Wei,
            deadline=int(time.time() + 20 * 60)
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swap', args=params.tuple()),
            value=amount.Wei
        )

        # self.parse_params(tx_params['data'])

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'{amount.Ether} ETH was swapped to {to_token_name} via SyncSwap: {tx.hash.hex()}'
        return f'{failed_text}!'

    async def swap_usdc_to_eth(self, slippage: float = 1.) -> str:
        from_token = await self.client.contracts.default_token(contract_address=Contracts.USDC.address)
        from_token_name = await from_token.functions.symbol().call()
        to_token = await self.client.contracts.default_token(contract_address=Contracts.WETH.address)
        to_token_name = await to_token.functions.symbol().call()

        failed_text = f'Failed swap USDC to {to_token_name} via SyncSwap'

        token_balance = await self.client.wallet.balance(token=from_token)

        if not token_balance.Wei:
            return f'{failed_text}: {self.client.account.address} | SpaceFi | swap_token | ' \
                   f'not enough {from_token_name} balance ({token_balance.Ether})'

        contract = await self.client.contracts.get(
            contract_address=Contracts.SYNCSWAP.address,
            abi=Contracts.SYNCSWAP.abi
        )

        if await self.approve_interface(
                token_address=from_token.address,
                spender=contract.address,
                amount=token_balance
        ):
            await asyncio.sleep(random.randint(5, 10))
        else:
            return f'{failed_text} | can not approve'

        eth_price = await self.get_token_price(token='ETH')
        amount_out_min = TokenAmount(
            amount=float(token_balance.Ether) / eth_price * (1 - slippage / 100),
        )

        pool = Web3.to_checksum_address('0x80115c708e12edd42e504c1cd52aea96c547c05c')

        params = TxArgs(
            paths=[
                TxArgs(
                    steps=[
                        TxArgs(
                            pool=pool,
                            data=f'0x{Contracts.USDC.address[2:].zfill(64)}'
                                 f'{str(self.client.account.address)[2:].zfill(64)}'
                                 f'{"1".zfill(64)}',
                            callback='0x0000000000000000000000000000000000000000',
                            callbackData='0x'
                        ).tuple()
                    ],
                    tokenIn='0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4',
                    amountIn=token_balance.Wei,
                ).list()
            ],
            amountOutMin=amount_out_min.Wei,
            deadline=int(time.time() + 20 * 60)
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swap', args=params.tuple()),

        )

        self.parse_params(tx_params['data'])

        tx_params = await self.client.transactions.auto_add_params(tx_params)
        return (await self.client.transactions.estimate_gas(self.client.w3, tx_params)).Wei

        # tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        # receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        # if receipt:
        #     return f'{amount.Ether} ETH was swapped to {to_token_name} via SpaceFi: {tx.hash.hex()}'
        # return f'{failed_text}!'