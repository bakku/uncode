import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from price_monitor.models import Product


@dataclass(frozen=True)
class PriceChange:
    product_id: str
    product_name: str
    old_price: float
    new_price: float

    @property
    def diff(self) -> float:
        return self.new_price - self.old_price


@dataclass(frozen=True)
class PriceDiff:
    shop_name: str
    changes: list[PriceChange]
    new_products: list[Product]
    removed_product_ids: list[str]


class PriceStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> dict[str, object]:
        if not self.path.exists():
            return {}
        with open(self.path) as f:
            result: object = json.load(f)
            if isinstance(result, dict):
                return result
            return {}

    def save(self, data: dict[str, object]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")

    def compare(
        self, shop_name: str, current_products: list[Product]
    ) -> PriceDiff:
        data = self.load()
        shop_entry = data.get(shop_name)
        old_products: dict[str, object] = {}
        if isinstance(shop_entry, dict):
            shop_dict: dict[str, object] = shop_entry  # type: ignore[assignment]
            products_data = shop_dict.get("products")
            if isinstance(products_data, dict):
                old_products = products_data  # type: ignore[assignment]

        changes: list[PriceChange] = []
        new_products: list[Product] = []
        current_map = {p.id: p for p in current_products}

        for product in current_products:
            old = old_products.get(product.id)
            if old is None:
                new_products.append(product)
            elif isinstance(old, dict):
                old_price = float(old.get("price", 0))  # type: ignore[arg-type]
                if old_price != product.price:
                    changes.append(
                        PriceChange(
                            product_id=product.id,
                            product_name=product.name,
                            old_price=old_price,
                            new_price=product.price,
                        )
                    )

        removed = [
            pid for pid in old_products if pid not in current_map
        ]

        return PriceDiff(
            shop_name=shop_name,
            changes=changes,
            new_products=new_products,
            removed_product_ids=removed,
        )

    def update(self, shop_name: str, products: list[Product]) -> None:
        data = self.load()
        data[shop_name] = {
            "products": {
                p.id: {"name": p.name, "price": p.price}
                for p in products
            },
            "last_checked": datetime.now(UTC).isoformat(),
        }
        self.save(data)
