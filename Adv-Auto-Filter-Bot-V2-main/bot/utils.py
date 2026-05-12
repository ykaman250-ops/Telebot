import os
import hashlib
import time
import aiohttp

def get_hash(user_id, unique_id, timestamp):
    # Using BOT_TOKEN as a salt constraint to ensure users cannot guess hashes
    secret_key = os.environ.get("BOT_TOKEN", "fallback_secret_salt")
    hash_string = f"{user_id}:{unique_id}:{timestamp}:{secret_key}"
    return hashlib.sha256(hash_string.encode()).hexdigest()

async def get_shortlink(url):
    shortener_api = os.environ.get("SHORTLINK_API", "")
    shortener_url = os.environ.get("SHORTLINK_URL", "")
    
    if not shortener_api or not shortener_url:
        return url
        
    api_url = f"https://{shortener_url}/api?api={shortener_api}&url={url}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=10) as response:
                result = await response.json()
                if result.get("status") == "success" or result.get("status") == "success":
                    return result.get("shortenedUrl")
                return url
    except Exception as e:
        print(f"Error fetching shortlink: {e}")
        return url
