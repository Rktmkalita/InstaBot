import os
import requests
from instagrapi import Client
from dotenv import load_dotenv
import praw

load_dotenv()

# Instagram credentials from .env
INSTA_USERNAME = os.getenv("INSTA_USERNAME")
INSTA_PASSWORD = os.getenv("INSTA_PASSWORD")

# Reddit credentials from .env
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# File to track posted Reddit post IDs
POSTED_FILE = "posted.txt"

# Hashtags to append
hashtags = "#funny #memes #lol #ai"

# Load posted Reddit IDs
def load_posted_ids():
    if not os.path.exists(POSTED_FILE):
        return set()
    with open(POSTED_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_posted_id(post_id):
    with open(POSTED_FILE, "a") as f:
        f.write(post_id + "\n")

# Initialize Reddit client
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
)

def get_new_reddit_post(subreddit="funny", limit=10):
    posted_ids = load_posted_ids()
    for submission in reddit.subreddit(subreddit).hot(limit=limit):
        if submission.id in posted_ids:
            continue
        if submission.url.endswith((".jpg", ".jpeg", ".png")):
            caption = f"{submission.title[:200]}\n\nFollow for more memes! 😂 {hashtags}"
            return submission.id, caption, submission.url
    return None, None, None

def download_image(url, filename="temp.jpg"):
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)
    return filename

def upload_to_instagram(image_path, caption):
    cl = Client()
    cl.login(INSTA_USERNAME, INSTA_PASSWORD)
    cl.photo_upload(image_path, caption)

def main():
    post_id, caption, url = get_new_reddit_post()
    if post_id:
        print("Selected:", caption)
        image_path = download_image(url)
        upload_to_instagram(image_path, caption)
        save_posted_id(post_id)
        print("Successfully posted to Instagram.")
    else:
        print("No new Reddit posts to upload.")

if __name__ == "__main__":
    main()
