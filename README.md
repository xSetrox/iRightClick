# Please note: This project is currently broken.  
I believe they changed things around with their API. If I have time in the future I will fix it. Otherwise feel free to fork and try and fix it yourself.  
  
![iRightClick](https://i.imgur.com/M9nyzWv.png)
# iRightClick
Quickly, simply, and asynchronously download NFT's from an Opensea collection.


### NOTICE
This tool is not developed to encourage or facilitate any piracy. It exists to express a point; that NFT's are nothing more than receipts on the blockchain, and that all assets are simply hosted on Google and can easily be downloaded by anyone. It also exists to allow NFT enthusiasts and owners to easily access their own NFT's as well as other NFT's in the collection.
No warez is included in this release and this release utilizes the official OpenSea API (which they can modify to prevent this) to accomplish tasks.

## Installation
`pip install -r requirements.txt`

## Usage:
`main.py collection_id` (collection is also known as "slug").
Example: `main.py boredapeyachtclub`

### Rate limits
This release uses the official OpenSea API. While it uses a throttler library to prevent it, you may still get temporarily rate limited or blocked from OpenSea API. I am not responsible for this or other disciplinary measures that OpenSea (although they probably wont) may take against you.
That being said, you can edit the throttler declaration at the top of the module to slow down or speed up the downloader if things are too slow or if you are getting 429'd.


### Credits
Resources used for creating logo:  
<a href="https://iconscout.com/icons/mouse" target="_blank">Mouse Icon</a> by <a href="https://iconscout.com/contributors/phoenix-group" target="_blank">Phoenix Dungeon</a>  
<a href="https://iconscout.com/icons/canvas-painting" target="_blank">Canvas Painting Icon</a> on <a href="https://iconscout.com">Iconscout</a>
