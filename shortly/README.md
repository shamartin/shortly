# Shortly - URL Shortener Service

A simple URL shortener web service built with Python and Flask. It takes a long URL and returns a shortened link that redirects users to the original URL.

## Features
- Create shortened URLs from long URLs
- Redirect shortened URLs to original destinations
- Base62 encoding of unique IDs for short link generation
- Duplicate URL detection (returns existing short URL if already stored)
- URL validation to prevent invalid inputs
- Basic error handling for missing or invalid URLs
- Unit tests with test fixtures

## Tech Stack
- Python
- Flask
- SQLite
- GitHub Actions (CI for running unit tests)

## Project Structure
- models/ – database models
- resources/ – API routes and endpoints
- utils/ – helper functions (encoding, validation, etc.)
- tests/ – unit tests and test configuration
- shortly.py – main Flask application entry point

## Development Setup

### 1. Clone the repository
git clone https://github.com/shamartin/shortly.git  
cd shortly

### 2. Create virtual environment
python -m venv venv  
source venv/bin/activate  # Mac/Linux  
venv\Scripts\activate     # Windows

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run the application
flask --app shortly.py run

## Testing
Run unit tests using:
python -m pytest

## CI/CD
This project uses GitHub Actions to run unit tests automatically before pull requests can be merged.
