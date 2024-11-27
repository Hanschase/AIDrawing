import httpx

async def download_image(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        content = response.content
        import aiofiles
        async with aiofiles.open("drawertemp.png", 'wb') as f:
            await f.write(content)