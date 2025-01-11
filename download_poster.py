import os
from imdb import IMDb
import requests

def download_poster(abs_path, search):
    parent_dir = os.path.dirname(abs_path)
    # Path to save the poster
    poster_path = f'{parent_dir}/poster.jpg'

    # Check if the poster file already exists
    if os.path.exists(poster_path):
        print(f"Poster already exists as {poster_path}. Skipping download.")
        return

    # Initialize IMDb object
    ia = IMDb()

    # Search for the movie by title
    title = search
    movies = ia.search_movie(title)

    # Check if the search returned results
    if not movies:
        print(f"No results found for '{search}'.")
        return

    # Get the first result (assuming it's the correct one)
    movie = movies[0]

    # Get the movie ID and fetch full details
    movie_id = movie.getID()
    movie_details = ia.get_movie(movie_id)

    # Get the poster URL
    poster_url = movie_details.get('full-size cover url')

    # Check if the poster URL is available
    if poster_url:
        # Send a GET request to fetch the image
        response = requests.get(poster_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the image as poster.jpg in the parent directory
            with open(poster_path, 'wb') as f:
                f.write(response.content)
            print(f"Image for '{search}' downloaded successfully!")
        else:
            print(f"Failed to retrieve the image for '{search}'. Status code: {response.status_code}")
    else:
        print(f"Poster for '{search}' not found.")
