import os
from dotenv import load_dotenv
import requests
import pandas as pd

# Load environment variables
load_dotenv()


class MovieAnalyzer:
    def __init__(self, api_key=None):
        """
        Initialize MovieAnalyzer with TMDB API key

        Args:
            api_key (str, optional): TMDB API key.
            If not provided, tries to load from environment variable.
        """
        self.api_key = api_key or os.getenv('TMDB_API_KEY')

        if not self.api_key:
            raise ValueError(
                "TMDB API Key is required. "
                "Set TMDB_API_KEY in .env file or pass directly to constructor."
            )

        self.base_url = 'https://api.themoviedb.org/3'

    def fetch_popular_movies(self, year=2025, limit=100):
        """
        Retrieves popular movies from a specific year using TMDB API

        Args:
            year (int): Production year of movies
            limit (int): Maximum number of movies to fetch

        Returns:
            pandas.DataFrame: DataFrame with movie information
        """
        movies = []
        page = 1

        while len(movies) < limit:
            url = f"{self.base_url}/discover/movie"
            params = {
                'api_key': self.api_key,
                'primary_release_year': year,
                'sort_by': 'popularity.desc',
                'page': page
            }

            response = requests.get(url, params=params).json()
            movies.extend(response['results'])

            if page >= response['total_pages']:
                break
            page += 1

        df_movies = pd.DataFrame(movies)
        return df_movies[['title', 'vote_average', 'popularity', 'original_language']]

    def statistical_analysis(self, df):
        """
        Performs statistical analysis of movies

        Args:
            df (pandas.DataFrame): DataFrame with movies

        Returns:
            dict: Dictionary with key statistics
        """
        statistics = {
            'average_rating': df['vote_average'].mean(),
            'popularity_median': df['popularity'].median(),
            'languages': df['original_language'].value_counts()
        }
        return statistics


if __name__ == "__main__":
    analyzer = MovieAnalyzer()
