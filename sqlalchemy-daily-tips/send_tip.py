import asyncio
import json
import os
from html import escape
from pathlib import Path

from telegram import Bot

BASE_DIR = Path(__file__).resolve().parent
TIPS_PATH = BASE_DIR / "tips.json"
PROGRESS_PATH = BASE_DIR / "progress.json"


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Set {name} as a GitHub secret")
    return value


def load_tips() -> list[dict[str, str]]:
    with TIPS_PATH.open("r", encoding="utf-8") as handle:
        tips = json.load(handle)
    if not isinstance(tips, list):
        raise ValueError("tips.json must contain a list of tips")
    return tips


def load_progress() -> int:
    try:
        with PROGRESS_PATH.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        current_day = int(data.get("current_day", 0))
        return max(current_day, 0)
    except (FileNotFoundError, json.JSONDecodeError, ValueError, TypeError):
        return 0


def save_progress(current_day: int) -> None:
    PROGRESS_PATH.write_text(
        json.dumps({"current_day": current_day}, indent=2) + "\n",
        encoding="utf-8",
    )


def format_tip_message(day_number: int, total: int, tip: dict[str, str]) -> str:
    title = escape(tip["title"])
    explanation = escape(tip["explanation"])
    code = escape(tip["code"])
    return (
        f"📅 <b>Day {day_number} of {total}</b>\n\n"
        f"💡 <b>{title}</b>\n\n"
        f"{explanation}\n\n"
        f"<pre><code class=\"language-python\">{code}</code></pre>\n\n"
        "<i>Tip: run this snippet locally to experiment!</i>"
    )


async def send_message(bot: Bot, chat_id: str, text: str) -> None:
    await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")


def main() -> None:
    token = require_env("TELEGRAM_BOT_TOKEN")
    chat_id = require_env("TELEGRAM_CHAT_ID")

    tips = load_tips()
    current_day = load_progress()
    bot = Bot(token=token)

    if current_day >= len(tips):
        asyncio.run(
            send_message(bot, chat_id, "You've completed all tips! 🎉")
        )
        return

    tip = tips[current_day]
    message = format_tip_message(current_day + 1, len(tips), tip)
    asyncio.run(send_message(bot, chat_id, message))
    save_progress(current_day + 1)


if __name__ == "__main__":
    main()
