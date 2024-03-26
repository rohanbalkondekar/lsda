import os
import json
import logging
from itertools import islice
from instaloader import Instaloader, Profile, ConnectionException, InvalidArgumentException

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def scrape_instagram(username, top_x_posts_recent=10, top_x_comments=100):
    """
    Scrape Instagram data for the given user.
    Args:
        username (str): The Instagram username to scrape.
        top_x_posts_recent (int, optional): The number of most recent posts to fetch. Defaults to 10.
        top_x_comments (int, optional): The number of top comments to fetch for each post. Defaults to 100.
    Returns:
        list: A list containing the account information (first element) and the post data.
    """
    # Fetch login credentials from environment variables
    user = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    if not user or not password:
        raise ValueError("Instagram login credentials not found in environment variables.")

    l = Instaloader()
    try:
        l.login(user, password)
        logging.info("Logged In")

        # Create a directory to save the data
        data_dir = f"{username}_top_{top_x_posts_recent}_recent_posts"
        os.makedirs(data_dir, exist_ok=True)

        profile = Profile.from_username(l.context, username)

        # Extract account information
        account_data = {
            "username": profile.username,
            "followers": profile.followers,
            "followees": profile.followees,
            "biography": profile.biography,
            "is_private": profile.is_private,
            "total_posts": profile.mediacount,
        }

        # Save account information to a JSON file
        account_file = os.path.join(data_dir, f"{username}_account.json")
        with open(account_file, "w", encoding="utf-8") as f:
            json.dump(account_data, f, indent=4)

        # Get the most recent posts
        recent_posts = list(profile.get_posts())[:top_x_posts_recent]
        logging.info(f"Found {len(recent_posts)} recent posts")

        # Process and save the posts
        post_data = []
        for post_count, post in enumerate(recent_posts):
            logging.info(f"Processing post {post_count + 1} of {len(recent_posts)}")

            # Create a JSON file for the post
            post_file = os.path.join(data_dir, f"post_{post_count + 1}.json")
            post_info = {
                "caption": post.caption,
                "timestamp": post.date_utc.isoformat(),
                "location": post.location.name if post.location else None,
                "likes": post.likes,
                "comments": post.comments,
                "comments_top": [],
            }

            # Get the top comments
            try:
                comments = list(post.get_comments())
            except Exception as e:
                logging.warning(f"Error retrieving comments for post {post_count + 1}: {e}")
                comments = []

            if comments:
                # comments = sorted(comments, key=lambda x: x.likes_count, reverse=True)
                for comment in islice(comments, top_x_comments):
                    if comment.text.strip():
                        post_info["comments_top"].append(comment.text.strip())

            with open(post_file, "w", encoding="utf-8") as f:
                json.dump(post_info, f, indent=4)

            logging.info(f"Post {post_count + 1} data saved to {post_file}")
            post_data.append(post_info)

        logging.info(f"Processed a total of {len(recent_posts)} posts.")
        logging.info(f"Data saved in the '{data_dir}' directory.")
        return [account_data] + post_data

    except InvalidArgumentException as e:
        logging.error(f"Error: {e}")
        raise e
    except ConnectionException as e:
        logging.error(f"Connection error: {e}")
        raise e
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise e