import os
from dotenv import load_dotenv
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

    def create_visualizations(self, df):
        """
        Creates data visualizations for movies

        Args:
            df (pandas.DataFrame): DataFrame with movies
        """
        plt.figure(figsize=(12, 4))

        # Rating distribution
        plt.subplot(131)
        sns.histplot(df['vote_average'], kde=True)
        plt.title('Rating Distribution')

        # Movie popularity
        plt.subplot(132)
        sns.boxplot(x=df['popularity'])
        plt.title('Movie Popularity')

        # Movie languages
        plt.subplot(133)
        df['original_language'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Movie Languages')

        plt.tight_layout()
        plt.show()

    def generate_report(self, year=2023):
        """
        Generates a comprehensive report about movies

        Args:
            year (int): Production year of movies
        """
        print(f"Movie Analytics Report ({year})")
        movies = self.fetch_popular_movies(year)
        statistics = self.statistical_analysis(movies)

        print("\n--- General Statistics ---")
        print(f"Average movie rating: {statistics['average_rating']:.2f}")
        print(f"Popularity median: {statistics['popularity_median']:.2f}")

        print("\n--- Movie Languages ---")
        print(statistics['languages'])

        self.create_visualizations(movies)


if __name__ == "__main__":
    analyzer = MovieAnalyzer()
    analyzer.generate_report()
