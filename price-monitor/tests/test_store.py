import json
from pathlib import Path

from price_monitor.models import Product
from price_monitor.store import PriceStore


class TestPriceStore:
    def test_compare_first_run_all_new(self, tmp_path: Path) -> None:
        store = PriceStore(tmp_path / "prices.json")
        products = [
            Product(id="1", name="Item A", price=10.0),
            Product(id="2", name="Item B", price=20.0),
        ]
        diff = store.compare("shop1", products)

        assert len(diff.new_products) == 2
        assert len(diff.changes) == 0
        assert len(diff.removed_product_ids) == 0

    def test_compare_detects_price_change(self, tmp_path: Path) -> None:
        path = tmp_path / "prices.json"
        path.write_text(
            json.dumps(
                {
                    "shop1": {
                        "products": {
                            "1": {"name": "Item A", "price": 10.0},
                            "2": {"name": "Item B", "price": 20.0},
                        },
                        "last_checked": "2026-01-01T00:00:00Z",
                    }
                }
            )
        )
        store = PriceStore(path)
        products = [
            Product(id="1", name="Item A", price=8.0),
            Product(id="2", name="Item B", price=25.0),
        ]
        diff = store.compare("shop1", products)

        assert len(diff.changes) == 2
        assert diff.changes[0].old_price == 10.0
        assert diff.changes[0].new_price == 8.0
        assert diff.changes[1].old_price == 20.0
        assert diff.changes[1].new_price == 25.0

    def test_compare_detects_removed_products(self, tmp_path: Path) -> None:
        path = tmp_path / "prices.json"
        path.write_text(
            json.dumps(
                {
                    "shop1": {
                        "products": {
                            "1": {"name": "Item A", "price": 10.0},
                            "2": {"name": "Item B", "price": 20.0},
                        },
                        "last_checked": "2026-01-01T00:00:00Z",
                    }
                }
            )
        )
        store = PriceStore(path)
        products = [Product(id="1", name="Item A", price=10.0)]
        diff = store.compare("shop1", products)

        assert diff.removed_product_ids == ["2"]

    def test_update_and_load(self, tmp_path: Path) -> None:
        store = PriceStore(tmp_path / "prices.json")
        products = [Product(id="1", name="Item A", price=10.0)]
        store.update("shop1", products)

        data = store.load()
        assert "shop1" in data
        shop = data["shop1"]
        assert isinstance(shop, dict)
        shop_dict: dict[str, object] = shop  # type: ignore[assignment]
        products = shop_dict["products"]
        assert isinstance(products, dict)
        assert "1" in products

    def test_compare_no_changes(self, tmp_path: Path) -> None:
        path = tmp_path / "prices.json"
        path.write_text(
            json.dumps(
                {
                    "shop1": {
                        "products": {
                            "1": {"name": "Item A", "price": 10.0},
                        },
                        "last_checked": "2026-01-01T00:00:00Z",
                    }
                }
            )
        )
        store = PriceStore(path)
        products = [Product(id="1", name="Item A", price=10.0)]
        diff = store.compare("shop1", products)

        assert len(diff.changes) == 0
        assert len(diff.new_products) == 0
        assert len(diff.removed_product_ids) == 0
