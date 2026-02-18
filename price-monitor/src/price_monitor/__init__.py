import os
import sys
from pathlib import Path

from price_monitor.models import Scraper
from price_monitor.notifier import TelegramNotifier
from price_monitor.scrapers.oberpfalz_beef import OberpfalzBeefLammScraper
from price_monitor.store import PriceStore

SCRAPERS: list[Scraper] = [
    OberpfalzBeefLammScraper(),
]


def main() -> None:
    data_path = Path(os.environ.get("PRICE_DATA_PATH", "data/prices.json"))
    store = PriceStore(data_path)

    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

    notifier: TelegramNotifier | None = None
    if bot_token and chat_id:
        notifier = TelegramNotifier(bot_token, chat_id)
    else:
        print("Warning: Telegram credentials not set, notifications disabled.")

    for scraper in SCRAPERS:
        print(f"Checking {scraper.name}...")
        try:
            products = scraper.scrape()
        except Exception as e:
            print(f"  Error scraping {scraper.name}: {e}", file=sys.stderr)
            continue

        print(f"  Found {len(products)} products.")

        diff = store.compare(scraper.name, products)

        if diff.changes or diff.new_products or diff.removed_product_ids:
            print("  Changes detected!")
            if notifier:
                try:
                    notifier.notify(diff)
                    print("  Telegram notification sent.")
                except Exception as e:
                    print(
                        f"  Error sending notification: {e}",
                        file=sys.stderr,
                    )
        else:
            print("  No changes.")

        store.update(scraper.name, products)
