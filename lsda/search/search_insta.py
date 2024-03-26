import os
import json
from instaloader import Instaloader, TopSearchResults

def search_instagram(query, top_results=10):
    """Returns Top K search results from Instagram along with results"""

    user = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    if not user or not password:
        raise ValueError("Instagram login credentials not found in environment variables.")

    # Create an Instaloader instance
    L = Instaloader()

    # Login to Instagram
    L.login(user, password)
    print(f"Logged in as {user}")

    # Perform the search
    search_results = TopSearchResults(L.context, query)
    print(f"Search Results for '{query}':")

    # Process and store the search results
    results_data = []
    print(f"Results Data:\n{results_data}\n\n")

    for i, result in enumerate(search_results.get_profiles()):
        if i >= top_results:
            break
        profile_data = {
            "username": result.username,
            "full_name": result.full_name,
            "biography": result.biography,
            "followers": result.followers,
            "following": result.followees,
            "posts": result.mediacount,
            "is_private": result.is_private
        }
        results_data.append(profile_data)

        print(profile_data)

    # Save the search results to a JSON file
    with open(f"search_results_{query}.json", "w", encoding="utf-8") as file:
        json.dump(results_data, file, indent=4)

    return results_data