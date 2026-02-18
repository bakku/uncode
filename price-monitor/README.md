# Price Monitor

Monitors online shop product prices and sends Telegram notifications when prices change.

Runs entirely via GitHub Actions on a daily schedule.

## How It Works

1. **Scrapers** fetch product pages and extract product names + prices
2. **Price store** compares current prices against `data/prices.json`
3. **Telegram notifier** sends a message if prices increased or decreased
4. GitHub Actions commits the updated price data back to the repo

## Setup

### 1. Create a Telegram Bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Create a new bot with `/newbot`
3. Copy the bot token
4. Send a message to your bot, then get your chat ID from `https://api.telegram.org/bot<TOKEN>/getUpdates`

### 2. Configure GitHub Secrets

In your repository settings, add these secrets:

- `TELEGRAM_BOT_TOKEN` — your bot token from BotFather
- `TELEGRAM_CHAT_ID` — your chat ID

### 3. Enable the Workflow

The workflow runs daily at 08:00 UTC. You can also trigger it manually from the Actions tab.

## Local Development

```bash
# Install dependencies
uv sync

# Run the monitor (without Telegram, prints to stdout)
uv run price-monitor

# Run with Telegram notifications
TELEGRAM_BOT_TOKEN=... TELEGRAM_CHAT_ID=... uv run price-monitor

# Run tests
uv run pytest tests/

# Type check
uv run ty check
```

## Adding a New Scraper

1. Create a new file in `src/price_monitor/scrapers/`, e.g. `my_shop.py`
2. Implement a class with a `name` attribute and a `scrape()` method:

```python
from price_monitor.models import Product

class MyShopScraper:
    name = "my-shop"

    def scrape(self) -> list[Product]:
        # Fetch the page, parse products, return them
        ...
```

3. Register it in `src/price_monitor/__init__.py`:

```python
from price_monitor.scrapers.my_shop import MyShopScraper

SCRAPERS: list[Scraper] = [
    OberpfalzBeefLammScraper(),
    MyShopScraper(),
]
```