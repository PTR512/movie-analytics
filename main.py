import os
from dotenv import load_dotenv
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

            for movie in response['results']:
                # Fetch additional details for each movie
                movie_id = movie['id']
                details_url = f"{self.base_url}/movie/{movie_id}"
                details_params = {'api_key': self.api_key}
                details = requests.get(details_url, params=details_params).json()

                # Add budget and revenue to the movie data
                movie['budget'] = details.get('budget', 0)
                movie['revenue'] = details.get('revenue', 0)
                movie['runtime'] = details.get('runtime', 0)
            movies.extend(response['results'])

            if page >= response['total_pages'] or len(movies) >= limit:
                break
            page += 1

        df_movies = pd.DataFrame(movies)
        return df_movies[['title', 'vote_average', 'popularity', 'original_language',
                          'budget', 'revenue', 'runtime']]

    def statistical_analysis(self, df):
        """
        Performs statistical analysis of movies

        Args:
            df (pandas.DataFrame): DataFrame with movies

        Returns:
            dict: Dictionary with key statistics
        """
        if not df.empty:
            df['roi'] = (df['revenue'] - df['budget']) / df['budget']

        statistics = {
            'average_rating': df['vote_average'].mean(),
            'popularity_median': df['popularity'].median(),
            'languages': df['original_language'].value_counts(),
            'avg_budget': df['budget'].mean() if not df.empty else 0,
            'avg_revenue': df['revenue'].mean() if not df.empty else 0,
            'avg_roi': df['roi'].mean() if not df.empty else 0,
            'avg_runtime': df['runtime'].mean()
        }
        return statistics

    def correlation_analysis(self, df):
        """
               Analyzes correlations between movie metrics

               Args:
                   df (pandas.DataFrame): DataFrame with movies

               Returns:
                   pandas.DataFrame: Correlation matrix
               """
        # Filter out movies with zero budget for better analysis
        df_valid = df[(df['budget'] > 0) & (df['revenue'] > 0)].copy()

        if df_valid.empty:
            print("Insufficient data for correlation analysis")
            return None

        # Calculate ROI
        df_valid['roi'] = (df_valid['revenue'] - df_valid['budget']) / df_valid['budget']

        # Select relevant columns for correlation
        correlation_data = df_valid[['vote_average', 'popularity', 'budget',
                                     'revenue', 'runtime', 'roi']]

        # Calculate correlation matrix
        correlation_matrix = correlation_data.corr()

        # Create correlation heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm',
                    fmt='.2f', linewidths=0.5)
        plt.title('Correlation Between Movie Metrics')
        plt.tight_layout()
        plt.show()

        return correlation_matrix

    def create_visualizations(self, df):
        """
        Creates data visualizations for movies

        Args:
            df (pandas.DataFrame): DataFrame with movies
        """
        if df.empty:
            print("No movie data available for visualization.")
            return

        plt.figure(figsize=(15, 10))

        # Rating distribution
        plt.subplot(2, 2, 1)
        sns.histplot(df['vote_average'], kde=True)
        plt.title('Rating Distribution')
        plt.xlabel('Rating')
        plt.ylabel('Frequency')

        # Movie popularity
        plt.subplot(2, 2, 2)
        sns.boxplot(x=df['popularity'])
        plt.title('Movie Popularity')
        plt.xlabel('Popularity')

        # Budget vs Rating
        plt.subplot(2, 2, 3)
        valid_data = df[df['budget'] > 0]
        if not valid_data.empty:
            sns.scatterplot(x='budget', y='vote_average', data=valid_data)
            plt.title('Budget vs Rating')
            plt.xlabel('Budget ($)')
            plt.ylabel('Average Rating')
            plt.xscale('log')
        else:
            plt.text(0.5, 0.5, "No valid budget data",
                     horizontalalignment='center', verticalalignment='center')

        # Movie languages
        plt.subplot(2, 2, 4)
        language_counts = df['original_language'].value_counts()
        language_counts.plot(kind='pie', autopct='%1.1f%%')
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
        print(f"Average budget: ${statistics['avg_budget']:,.2f}")
        print(f"Average revenue: ${statistics['avg_revenue']:,.2f}")
        print(f"Average ROI: {statistics['avg_roi']:.2%}")
        print(f"Average runtime: {statistics['avg_runtime']:.1f} minutes")

        print("\n--- Movie Languages ---")
        print(statistics['languages'])

        # Perform correlation analysis
        correlation_matrix = self.correlation_analysis(movies)
        if correlation_matrix is not None:
            print("\n--- Correlation Analysis ---")
            print("Correlation between metrics:")
            print(correlation_matrix.round(2))

        self.create_visualizations(movies)


if __name__ == "__main__":
    analyzer = MovieAnalyzer()
    analyzer.generate_report()
