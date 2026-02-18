import httpx

from price_monitor.store import PriceDiff


class TelegramNotifier:
    def __init__(self, bot_token: str, chat_id: str) -> None:
        self.bot_token = bot_token
        self.chat_id = chat_id

    def notify(self, diff: PriceDiff) -> None:
        message = self._format(diff)
        if not message:
            return
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        httpx.post(
            url,
            json={
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML",
            },
            timeout=15,
        ).raise_for_status()

    def _format(self, diff: PriceDiff) -> str:
        lines: list[str] = []

        if diff.changes:
            lines.append(f"<b>💰 Price changes in {diff.shop_name}:</b>")
            for c in diff.changes:
                arrow = "📉" if c.diff < 0 else "📈"
                lines.append(
                    f"  {arrow} {c.product_name}: "
                    f"{c.old_price:.2f}€ → {c.new_price:.2f}€ "
                    f"({c.diff:+.2f}€)"
                )

        if diff.new_products:
            lines.append(f"\n<b>🆕 New products in {diff.shop_name}:</b>")
            for p in diff.new_products:
                lines.append(f"  • {p.name}: {p.price:.2f}€")

        if diff.removed_product_ids:
            lines.append(
                f"\n<b>❌ {len(diff.removed_product_ids)} product(s) "
                f"removed from {diff.shop_name}</b>"
            )

        return "\n".join(lines)
