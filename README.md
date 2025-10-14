# Comoda Backend

Backend services and API for the Comoda platform.

## Overview

This repository contains the backend services, API endpoints, and business logic for the Comoda application. Built with modern Python frameworks to provide scalable and maintainable server-side functionality.

## Tech Stack

- **Framework**: FastAPI / Django / Flask (to be determined)
- **Database**: PostgreSQL / MongoDB (to be determined)
- **Authentication**: JWT / OAuth2
- **API Documentation**: OpenAPI/Swagger
- **Testing**: pytest
- **Containerization**: Docker

## Project Structure

```
backend/
├── app/                    # Main application code
├── tests/                  # Test suite
├── config/                 # Configuration files
├── migrations/             # Database migrations
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Local development setup
└── README.md              # This file
```

## Getting Started

### Prerequisites

- Python 3.9+
- pip or pipenv
- Docker (optional)

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run the application:
   ```bash
   python main.py
   ```

### Docker Setup

1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

## API Documentation

Once running, access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

Key environment variables (see `.env.example`):

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT secret key
- `DEBUG`: Enable debug mode (development only)
- `GCP_SERVICE_ACCOUNT_KEY`: GCP service account credentials
- `CRYPTO_API_KEY`: Cryptocurrency API key

## Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app tests/
```

## Deployment

Deployment instructions will be added as the infrastructure is set up.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run the test suite: `pytest`
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Create a Pull Request

## License

[License information to be added]