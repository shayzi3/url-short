import random

from string import ascii_letters, digits


symbols = ascii_letters + digits


def generate_prefix_for_model() -> str:
     return "".join([random.choice(symbols) for _ in range(10)])