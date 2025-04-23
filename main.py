import asyncio
import requests
import urllib.parse
import json
from twikit import Client
import os

# Twitter login credentials
USERNAME = 'twitter_username'
EMAIL = 'twitter_email'
PASSWORD = 'twitter_password'

# Pollinations prompt
PROMPT = (
    "You are a degen meme prophet writing Twitter ads for crypto tokens and NFT projects. "
    "The crypto token and NFT project you are promoting is Degen Rug Rats or DRR. "
    "Keep the post under 280 characters. Use emojis, slang, dramatic lines, and include the CA: 5WtLbfEkVZC8KTDVutTzSPBKwUsvG4jbKQywTUg8hinq. "
    "Inject FOMO, hype, chaos, and red flags. Use spacing and newlines."
)

POLLINATIONS_PARAMS = {
    "model": "openai",
    "seed": 42
}

def get_pollinations_text(prompt, params):
    encoded_prompt = urllib.parse.quote(prompt)
    model = params.get("model", "openai")
    seed = params.get("seed", 42)

    url = f"https://text.pollinations.ai/{encoded_prompt}?model={model}&seed={seed}"

    try:
        response = requests.get(url)
        print("🔄 Pollinations response received.")
        response.raise_for_status()
        print("✅ Pollinations response status:", response.status_code)
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching text: {e}")
        return None

def generate_pollinations_image(prompt="A group of realistic rats gathered in a dark alley at night, illuminated by a moody overhead light, standing in front of a jagged red chart showing a steep crypto market crash — gritty urban environment, dramatic lighting, cinematic shot"):
    params = {
        "width": 1280,
        "height": 720,
        "seed": 42,
        "model": "flux",
        "enhance": "true",
        "nologo": "true"
    }
    encoded_prompt = urllib.parse.quote(prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    print("🖼 Generating image from:", image_url)

    try:
        response = requests.get(image_url)
        response.raise_for_status()

        image_path = "generated_image.jpg"
        with open(image_path, "wb") as f:
            f.write(response.content)
        print("✅ Image saved:", image_path)
        return image_path
    except requests.exceptions.RequestException as e:
        print(f"❌ Error generating image: {e}")
        return None

async def post_tweet(tweet_text, image_path):
    client = Client("en-US")

    try:
        if os.path.exists("cookies.json"):
            client.load_cookies("cookies.json")
            print("✅ Loaded cookies.")
        else:
            print("🔐 Logging in to Twitter...")
            await client.login(
                auth_info_1=USERNAME,
                auth_info_2=EMAIL,
                password=PASSWORD,
                cookies_file="cookies.json"
            )
            print("✅ Logged in and cookies saved.")

        # Upload image and post tweet
        media_id = await client.upload_media(image_path)
        await client.create_tweet(text=tweet_text, media_ids=[media_id])
        print("✅ Tweet with image posted.")
    except Exception as e:
        print(f"❌ Error posting tweet: {e}")

async def main():
    attempt = 1
    while True:
        print(f"\n🔁 Attempt #{attempt}: Generating tweet...")
        tweet_text = get_pollinations_text(PROMPT, POLLINATIONS_PARAMS)

        if not tweet_text:
            print("❌ No text returned. Exiting.")
            break

        tweet_length = len(tweet_text)
        print(f"📏 Tweet length: {tweet_length}")

        if tweet_length <= 280:
            print("\n✅ Valid Tweet:\n", tweet_text)
            image_path = generate_pollinations_image(tweet_text)

            if image_path:
                await post_tweet(tweet_text, image_path)
            else:
                print("⚠️ Image generation failed. Posting text only.")
                await post_tweet(tweet_text, None)
            break
        else:
            print("⚠️ Tweet too long. Retrying...")
            attempt += 1

if __name__ == "__main__":
    print("🚀 Starting Twitter Bot...")
    asyncio.run(main())
