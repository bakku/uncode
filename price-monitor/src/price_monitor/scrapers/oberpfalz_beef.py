import json
import re

import httpx

from price_monitor.models import Product

_DATA_LAYER_PATTERN = re.compile(r"onEventDataLayer\s*=\s*JSON\.parse\('(.+?)'\)")


class OberpfalzBeefLammScraper:
    name = "oberpfalz-beef-lamm"

    def __init__(
        self,
        url: str = "https://www.oberpfalz-beef.de/wild-lamm/lamm/",
    ) -> None:
        self.url = url

    def scrape(self) -> list[Product]:
        response = httpx.get(self.url, follow_redirects=True, timeout=30)
        response.raise_for_status()
        return self._parse(response.text)

    def _parse(self, html: str) -> list[Product]:
        match = _DATA_LAYER_PATTERN.search(html)
        if not match:
            raise ValueError(f"Could not find dataLayer JSON on {self.url}")

        raw = match.group(1).replace("\\/", "/")
        data = json.loads(raw)

        # data is a list; first element contains ecommerce.items
        items = data[0]["ecommerce"]["items"]
        products: list[Product] = []
        for item in items:
            products.append(
                Product(
                    id=str(item["item_id"]),
                    name=item["item_name"],
                    price=float(item["price"]),
                )
            )
        return products
