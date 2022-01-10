import asyncio
from aiohttp import ClientSession
import aiofiles
import os
from asyncio_throttle import Throttler
import argparse
# 5 requests/second by default
# raise if you get 429'd
throttler = Throttler(rate_limit=5, period=1)
parser = argparse.ArgumentParser(description='Input collection slug')
parser.add_argument('slugs', type=str, nargs='*',
                    help='Input the collection ID/slug')

# API endpoint
endpoint = 'https://api.opensea.io/api/v1'
async def asset_worker(url: str, session: ClientSession, slug) -> str:
    """Returns image url's from the assets on the page"""
    async with throttler:
        # first get the page's json which contains all asset data
        resp = await session.request(method="GET", url=url)
        resp.raise_for_status()
        json = await resp.json()
        # then iterate over each asset and extract info
        for a in json['assets']:
            i_url = a['image_url']
            dir = slug
            # create dir if it doesn't exist, skip if it does
            try:
                os.mkdir(slug)
            except FileExistsError:
                pass
            # get the image url from the asset, download its contents
            # using another worker for this could speed things up, but we are already throttling
            # so speed difference will not matter
            async with session.get(i_url) as resp:
                content = await resp.read()
                path = f"{dir}/{a['id']}.png"
                if os.path.isfile(path):
                    print(f"File {path} already exists.")
                else:
                    f = await aiofiles.open(path, mode='wb')
                    await f.write(content)
                    print(f"File {path} created.")
    return

async def get_collection_assets(slug) -> None:
    """Fire up workers to work on the URL\'s"""
    # get the amount of supply in the collection so we can accurately set offset's
    async with ClientSession() as session:
        async with session.get(f"https://api.opensea.io/api/v1/collection/{slug}") as resp:
            json = await resp.json()
            try:
                supply = json['collection']['stats']['total_supply']
            except:
                print(f'Slug \"{slug}\" does not appear to be a valid collection.')
                return
        tasks = []
        # the max assets per response is capped to 50, so divide the total supply by that- that is how many requests we need to make to the API
        # before we start, we need to init offset. start at 0, up by 50 each time
        offset = 0
        print(f"Starting download for {slug}. Tasks for", round(supply/50), "pages will be dispatched. Creating tasks...")
        for i in range(round(supply/50)):
            tasks.append(
                asset_worker(endpoint + f'/assets?order_direction=desc&collection={slug}&limit=50&offset={offset}', session, slug)
            )
            offset += 50
        await asyncio.gather(*tasks)
        print(f"Finished downloading slug {slug}")
        await session.close()
        return

if __name__ == "__main__":
    args = parser.parse_args()
    if not args.slugs:
        print("You must enter a collection slug/ID.")
        exit()
    for slug in args.slugs:
        asyncio.run(get_collection_assets(slug))