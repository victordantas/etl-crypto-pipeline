import os
from dotenv import load_dotenv

load_dotenv()

DB = {
    "host": os.gentenv("DB_HOST", "localhost"),
    "port": int(os.gentenv("DB_PORT", "5432")),
    "name": os.gentenv("DB_NAME", "crypto"),
    "user": os.gentenv("DB_USER", "etluser") ,
    "password": os.gentenv("DB_PASSWORD", "etlpass"),
}

COINS = [c.strip() for c in os.gentenv("COINS", "bitcoin,ethereum").split(",") if c.strip()]
VS_CURRENCY = os.gentenv("VS_CURRENCY", "usd")