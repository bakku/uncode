# SQLAlchemy Daily Tips Telegram Bot

This project is a tiny Telegram bot that delivers one SQLAlchemy micro-lesson per day. GitHub Actions runs the script on a schedule, sends the tip to your chat, and commits the updated progress back to the repository.

## Setup

1. Create a Telegram bot with @BotFather and copy the bot token.
2. Get your chat ID using a bot like @userinfobot or @RawDataBot.
3. Add the secrets in GitHub → Settings → Secrets → Actions:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
4. Ensure GitHub Actions are enabled for the repository.
5. Trigger the workflow manually from the Actions tab to test it.

## Resetting the Schedule

Edit `progress.json` and set `current_day` back to `0` to restart the tips from the beginning.

## Customize Tips

Edit `tips.json` to add or update lessons. Each entry includes a title, explanation, and a short Python snippet.

## Local Testing

Install dependencies and run the script with environment variables set:

```bash
cd sqlalchemy-daily-tips
python -m pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN=your-token
export TELEGRAM_CHAT_ID=your-chat-id
python send_tip.py
```

The script will send the next tip and update `progress.json` after a successful send.
