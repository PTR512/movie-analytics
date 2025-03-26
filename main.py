import os
from dotenv import load_dotenv

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


if __name__ == "__main__":
    analyzer = MovieAnalyzer()
