import random

from string import ascii_letters, digits


def generate_prefix() -> str:
     symbols = ascii_letters + digits
     return "".join([random.choice(symbols) for _ in range(7)])