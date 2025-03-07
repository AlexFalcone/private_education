import asyncio

from web3 import Web3

from sdk.data.models import Networks
from sdk.client import Client

import os
from loguru import logger

# from private_data import private_key1, private_key2, private_key3, proxy


async def main():
    # Generate Address and Private Key
    client = Client(network=Networks.Ethereum)
    num = int(input('Enter Number of Wallets to Generate:'))
    tasks = []
    for i in range(1, num+1):
        tasks.append(
            asyncio.create_task(generate_addr(client, i))
        )
    await asyncio.wait(tasks)


async def generate_addr(client, wallet_number):
    network = client.network.name
    address = client.account.address
    private_key = client.account.key.hex()
    balance = await client.wallet.balance()

    wallet_info = {
        f'wallet{wallet_number}': {
            'network': str(network),
            'address': str(address),
            'private_key': str(private_key),
            'balance': balance.Ether,
        }
    }

    save_directory = r'C:\Users\under\Desktop\Alex Gray\Python\private_education_web3\lesson_2\files'

    # Create or append to the "New Wallets.py" file
    file_path = os.path.join(save_directory, "New Wallets.py")

    with open(file_path, "a") as file:
        file.write(f"{wallet_info}\n")

<<<<<<< HEAD
    return logger.success(f'Address Generated | Please check in files/New Wallets.py')
=======
    return return logger.success(f'Address Generated | Please check in files/New Wallets.py')
>>>>>>> fbf7f91bbc1e9b57e3df004526f12b1994f46d97


'''
token_address = Web3.to_checksum_address('0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8')

tasks = []
for private_key in [private_key1, private_key2, private_key3]:
    client = Client(private_key=private_key, network=Networks.Arbitrum)
    tasks.append(asyncio.create_task(client.wallet.balance(token_address=token_address)))

await asyncio.gather(*tasks)
await asyncio.wait([*tasks])

for task in tasks:
    print(task.result())
'''
'''
asyncio.gather() принимает список асинхронных задач (coroutines) в качестве аргументов и запускает их одновременно.
Она возвращает список результатов, соответствующих выполненным задачам в том же порядке, в котором задачи были переданы в функцию.
Если во время выполнения задачи возникает исключение, asyncio.gather() прекращает выполнение остальных задач и сразу же выбрасывает исключение.

asyncio.wait() принимает список асинхронных задач (coroutines) в качестве аргументов и запускает их одновременно.
Она возвращает кортеж из двух множеств: множество выполненных задач и множество невыполненных задач.
Если во время выполнения задачи возникает исключение, asyncio.wait() продолжает выполнение остальных задач и не выбрасывает исключение.
'''


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
