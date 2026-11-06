# Deploy OpenSTEM Telegram Bot on Railway

This repository runs a **long-polling Python Telegram bot**. It requires an always-running service; static hosting and ordinary serverless functions are not suitable without a webhook rewrite.

## Before deploying (mandatory security)

1. Open [BotFather](https://t.me/BotFather), select `@Openstem_bot`, and use the token-revocation option under the bot's API token settings to generate a **new** token.
2. The original token was accidentally committed to this public repository's history. **Deleting it from the current code does not invalidate it**. Rotation in BotFather is essential.
3. Keep the new token only in the hosting provider's **secret environment variable**, named `BOT_TOKEN`. Do not paste it into GitHub, README files, or chat.

## Deployment

1. Sign in to [Railway](https://railway.com/) and select **New Project** → **Deploy from GitHub repo**.
2. Connect the `karim8siam/openstemtg` repository, branch `main`.
3. Under the new service's **Variables** tab add one variable:
   - **Name**: `BOT_TOKEN`
   - **Value**: the **new**, private BotFather token.
4. Deploy. Railway will detect the root `Dockerfile`, install the Python dependencies and run `python3 bot/main.py`.
5. Keep **one replica only**. Do not run the bot on your laptop or another server at the same time; concurrent polling instances can conflict.
6. For a paid Railway plan, set **Restart Policy → Always** for resilience. Free-plan restart options are limited.
7. No public domain is required for a long-polling bot. The bundled minimal HTTP server is used for service diagnostics, **not** Telegram update delivery.

## Verify operation

1. Under **Deployments → Logs**, look for `Bot is ... active and polling`, with the expected bot username.
2. Open [@Openstem_bot](https://t.me/Openstem_bot) in Telegram and send `/start`.
3. Test each inline-menu area, especially scholarship listings, professor directory, and waiting-university directory.
4. If you see a conflict about `getUpdates`, stop any other running copy and clear any old Telegram webhook. Telegram allows **either** long polling **or** webhook delivery, not both.
5. Monitor logs and billing usage. The committed database is packaged into the Docker image; changes made inside the running container are **not** durable across redeployments.

## Known limitations / follow-up improvements

- The application holds user menu selections in memory, so it loses these on restart. For basic navigation this is usually acceptable; persistent user tracking or broadcasting requires separate database/storage design.
- The SQLite dataset is bundled as a read-mostly file and is not automatically refreshed from OpenSTEM Field. Review listings and deadlines before presenting them as current.
- The GitHub root README currently describes a related outreach workspace. This file describes the Telegram bot's actual deployment.
- This runbook prepares the deployment, but it **does not deploy automatically** and cannot validate Telegram authentication without a new token set securely in Railway.
