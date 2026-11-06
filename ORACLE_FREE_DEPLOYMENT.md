# OpenSTEM Telegram Bot - Oracle Cloud Always Free VM

This deployment keeps the existing `python-telegram-bot` long-polling code and bundled read/write SQLite database. It does not rely on Railway, Render, an HTTP webhook, a public website, or paid hosting.

## Cloud VM setup (user action)

1. Sign up or sign in at https://www.oracle.com/cloud/free/ . Oracle typically requires an identity check and a supported bank card. Only one Free account per person is permitted.
2. Select **Compute > Instances > Create instance** in your **home region**.
3. Name the VM `openstem-telegram-bot`.
4. Select Ubuntu 24.04 LTS or Ubuntu 22.04 LTS as the image, and an **Always Free eligible** shape:
   - Preferred: `VM.Standard.A1.Flex`, **1 OCPU + 1-2 GB RAM** (ARM64), inside the Always Free limit.
   - Fallback: `VM.Standard.E2.1.Micro` (AMD64), if A1 has no capacity. Its 1 GB RAM is tight; use A1 when available.
5. Select a VCN/subnet with outbound internet connectivity. For easiest SSH setup assign a public IPv4 address. Allow SSH 22 only from your trusted IP when possible. **Do not open port 8080**; Telegram polling requires only outbound HTTPS (TCP 443).
6. Generate/download the SSH private key to your computer. **Never upload that key or bot token into GitHub or a chat**.
7. Confirm the exact VM shape and boot storage say **Always Free eligible**; do not choose paid add-ons.

Oracle Always Free compute resources are only eligible in your home region. A1 has a limited free allocation and can be unavailable due to host capacity. Oracle may reclaim VMs its policies deem idle.

Oracle references:
- https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/launchinginstance.htm

## Install on your VM (Ubuntu)

From your Mac terminal (change key path and IP address):

```bash
chmod 600 ~/Downloads/your-oci-private-key.key
ssh -i ~/Downloads/your-oci-private-key.key ubuntu@YOUR_VM_PUBLIC_IP
```

On the remote Ubuntu VM:

```bash
sudo apt-get update
sudo apt-get install -y git
git clone --depth 1 https://github.com/karim8siam/openstemtg.git ~/openstemtg-install
sudo bash ~/openstemtg-install/deploy/oracle-ubuntu-setup.sh
```

The installer creates a dedicated non-login Linux user, clones the GitHub code to `/opt/openstem-telegram-bot`, installs requirements into a Python virtual environment, and configures a systemd service that automatically restarts the bot. It intentionally **does not start the service** until you add a new Telegram bot token.

## Activate bot securely

First revoke the old exposed token with Telegram [@BotFather](https://t.me/BotFather), and create a fresh token. Do not post tokens into chat, repositories, screenshots, or shell commands recorded in history.

```bash
sudo nano /etc/openstem-bot.env
```

Enter exactly one line, replacing the placeholder with the new token:

```text
BOT_TOKEN=PASTE_THE_NEW_TOKEN_HERE
```

Then save the file and run:

```bash
sudo chmod 600 /etc/openstem-bot.env
sudo systemctl start openstem-bot
sudo systemctl status openstem-bot --no-pager
sudo journalctl -u openstem-bot -n 80 --no-pager
```

Open https://t.me/Openstem_bot, send `/start`, and test the main menu. In logs, look for `Bot is 100% active and polling`. This logging phrase reflects app startup, not a real uptime guarantee.

## Useful operations

```bash
sudo systemctl restart openstem-bot
sudo systemctl stop openstem-bot
sudo systemctl status openstem-bot --no-pager
sudo journalctl -u openstem-bot -f
```

**Preserve the SQLite database** at `/opt/openstem-telegram-bot/data/openstem.db` before any reinstall or future code update. The installer refuses to overwrite an existing deployment directory. Avoid running two copies of the same Telegram bot token with long polling. The HTTP health server in `bot/main.py` is not needed for public traffic on a VM; leave its port closed.

## What cannot be completed without your Oracle VM

There is no connected Oracle Cloud infrastructure management access in ChatGPT. An Oracle account and an actual VM must be created/authorized by you. The Linux installation and service activation must then run on that VM. This repository preparation by itself **does not make the bot live**.
