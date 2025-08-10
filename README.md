# URL Shortener 

A sleek, high-performance URL shortening service built with FastAPI and SQLite which does:

- Generate short URLs that redirect to original links
- URL expiration after configurable period (default 30 days)
- Click analytics with timestamp, IP, and user-agent logging
- Simple web interface using Jinja2 templates and Bootstrap
- Clean, async database operations via `databases` and SQLAlchemy core

---

## Features

- Shorten URLs with a unique 6-character alphanumeric code
- Redirect short URLs seamlessly to the original URL
- **Expiry:** URLs automatically expire after 30 days (configurable)
- **Click tracking:** Logs every click’s timestamp, IP address, and browser agent
- **Analytics page:** View click history and total clicks per short URL
- Lightweight and easy to extend — perfect for learning or production

---

## Tech Stack

- Python 3.12+
- FastAPI
- Jinja2 Templates
- SQLite (via SQLAlchemy core and databases async lib)
- Bootstrap 5 (for clean UI)
- `python-dateutil` for robust datetime parsing

---

## Installation

1. Clone the repo
2. Install dependencies

---

## Running the App

Start the FastAPI server:
`uvicorn app:app --reload`

Open your browser at: `http://localhost:8000` or at your development environment  to start shortening URLs!

---

Host it in a service to use it across browser and in the internet

---

## Notes & Future Improvements

- User authentication and personal URL dashboards
- Custom URL aliases
- More detailed analytics (geolocation, device types)
- API endpoints for programmatic shortening
- Docker containerization for easy deployment

---

## License

MIT License © 2025 Yashwin
