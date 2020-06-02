import asyncio
import sys

from proxybroker import Broker


async def save(proxies, filename):
    """Save proxies to a file."""
    with open(filename, 'w') as f:
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            proto = 'https' if 'HTTPS' in proxy.types else 'http'
            row = '%s://%s:%d\n' % (proto, proxy.host, proxy.port)
            f.write(row)


def get_proxy(count=20):
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(broker.find(types=['HTTP', 'HTTPS'], limit=count),
                           save(proxies, filename='proxies.txt'))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)


def read_proxies(file='proxies.txt'):
    """Read proxies from file."""
    # comment this line if you have own proxy
    #     get_proxy(20)  # generate new proxy
    with open('proxies.txt', 'r', encoding='utf8') as file:
        proxies = file.read().split('\n')[:-1]
    return proxies


