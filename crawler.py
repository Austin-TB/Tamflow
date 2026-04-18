import httpx
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")
API_TOKEN = os.getenv("CF_API_TOKEN")
BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/browser-rendering"

async def fetch_article_markdown(url: str) -> str:
    async with httpx.AsyncClient(timeout=60.0) as client:
        res = await client.post(
            f"{BASE_URL}/markdown",
            headers={
                "Authorization": f"Bearer {API_TOKEN}",
                "Content-Type": "application/json",
            },
            json={"url": url},
        )
        res.raise_for_status()
        return res.json()["result"]


if __name__ == "__main__":
    url="""
    https://cameronrwolfe.substack.com/p/understanding-and-using-supervised
    """

    print(asyncio.run(fetch_article_markdown(url)))