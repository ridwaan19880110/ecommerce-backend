import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def fetch_sellers():
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    rows = await conn.fetch("SELECT id, email, created_at FROM public.sellers;")
    await conn.close()

    for row in rows:
        print(dict(row))

asyncio.run(fetch_sellers())
