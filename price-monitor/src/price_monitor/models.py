from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    price: float


class Scraper(Protocol):
    name: str

    def scrape(self) -> list[Product]: ...
