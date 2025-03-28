# 🎬 Movie Analytics Project

## 📝 Project Description

This Python project provides a comprehensive analysis of movie data using the TMDB (The Movie Database) API, demonstrating advanced data processing, visualization, and API interaction skills.

## ✨ Key Features

- 🔍 Fetch popular movies from TMDB API
- 📊 Perform statistical analysis on movie data
- 📈 Generate insightful visualizations
- 🔒 Secure API key management with environment variables
- 🌐 Support for movies from different years and languages

## 🛠️ Technologies Used

- Python
- Pandas
- Matplotlib
- Seaborn
- python-dotenv
- Requests Library
- TMDB API

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- TMDB API Key (free to obtain)

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/movie-analytics.git
cd movie-analytics
```

2. Install required dependencies
```bash
pip install -r requirements.txt
```

3. Set up Environment Variables
Create a `.env` file in the project root and add your TMDB API key:
```
TMDB_API_KEY=your_tmdb_api_key_here
```

### Usage

```python
from movie_analyzer import MovieAnalyzer

# Automatically loads API key from .env
analyzer = MovieAnalyzer()
analyzer.generate_report(year=2023)
```

## 🔒 Security Note

The project uses `python-dotenv` to manage the API key securely. Never commit your `.env` file to version control.

## 📦 Dependencies

Create a `requirements.txt` file:
```
requests
pandas
matplotlib
seaborn
python-dotenv
```

## 📜 License

[MIT License](LICENSE)
