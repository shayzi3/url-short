import random

from string import ascii_letters, digits


symbols = ascii_letters + digits

def generate_prefix() -> str:
     return "".join([random.choice(symbols) for _ in range(7)])


async def generate_api_key(prefix: str) -> str:
     return prefix + "".join([random.choice(symbols) for _ in range(10)])