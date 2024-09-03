import httpx
from httpx import Response


async def validate_text(text: str) -> Response:
    api_url = f'https://speller.yandex.net/services/spellservice.json/checkText?text={text}'
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
        return response.json()
