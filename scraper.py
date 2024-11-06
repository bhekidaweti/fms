import praw, os
from dotenv import load_dotenv
from models import db, Meme


load_dotenv()

def get_memes():
    reddit = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent=os.getenv("USER_AGENT")
    )

    try:
        # This will return the authenticated user's Reddit username
        print("Authenticated user:", reddit.user.me())
    except Exception as e:
        print("Error:", e)


    subreddits = ["memes", "ProgrammerDadJokes", "dankmemes", "programmerhumor"]
    memes = []


#Iterating throgh subreddits and fetch top memes
    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit).hot(limit=10):
            if not submission.stickied:
                if submission.url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4')) or \
                   submission.url.startswith("https://v.redd.it/"):  # Include Reddit video URLs
                    # Create a new Meme object and add to the database
                    new_meme = Meme(title=submission.title, url=submission.url, permalink=submission.permalink)
                    db.session.add(new_meme)
                    memes.append(new_meme)
    db.session.commit()  # Commit the changes to the database
    return memes

