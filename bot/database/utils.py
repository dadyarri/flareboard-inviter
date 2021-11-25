import os


def get_tg_token():
    return os.getenv("TELEGRAM_TOKEN")


def get_admin_ids():
    return map(int, os.getenv("ADMIN_IDS").split(","))
