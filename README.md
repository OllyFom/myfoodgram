# Foodgram - Your Recipe Management Platform

## Project Description
Foodgram is a recipe management service where users can share recipes, follow other users, and create shopping lists from recipe ingredients.

## Technology Stack
- Backend: Python/Django
- Frontend: React
- Database: PostgreSQL
- Server: Nginx
- Containerization: Docker

## Project Structure
```
├── backend/          # Django backend application
├── frontend/         # React frontend application
├── infra/            # Infrastructure configuration files
├── data/             # Initial data and fixtures
└── docs/             # API documentation
```

## Features
- User authentication and authorization
- Create, view, edit and delete recipes
- Add recipes to favorites
- Create shopping lists from recipes
- Follow other users
- Filter recipes by tags

## Docker Images
The project's Docker images are available at:
- Backend: `https://hub.docker.com/r/tirabock/foodgram-backend`
- Frontend: `https://hub.docker.com/r/tirabock/foodgram-frontend`

You can pull these images directly instead of building them locally:
```bash
docker pull tirabock/foodgram-backend
docker pull tirabock/foodgram-frontend
```

To use these images in your docker-compose.yml, replace the build contexts with the image URLs:
```yaml
services:
  backend:
    image: <your-backend-image-url>
    ...

  frontend:
    image: <your-frontend-image-url>
    ...
```

## Environment Variables
The project uses environment variables for configuration. Sample configuration files are provided in `.env.sample`:

### Required Environment Variables:
```bash
# Debug mode (0 for production, 1 for development)
DEBUG=0

# Django secret key
SECRET_KEY=django-insecure-token-yo

# Allowed hosts for the application
ALLOWED_HOSTS=127.0.0.1,backend,localhost,foodgram-backend

# Database configuration
DB_NAME=foodgram-db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=foodgram-postgres
DB_PORT=5432
```

To set up your environment:
1. Copy the sample file:
```bash
cp infra/.env.sample infra/.env
```
2. Update the values in `.env` with your actual configuration

## Installation and Setup

### Prerequisites
- Docker
- Docker Compose

### Development Setup
1. Clone the repository
2. Create environment files as described above
3. Build and run the containers:
   ```bash
   cd infra
   docker-compose up -d --build
   ```
4. Apply migrations:
   ```bash
   docker-compose exec backend python manage.py migrate
   ```
5. Load initial data:
   ```bash
   docker-compose exec backend python manage.py load_ingredients
   ```
6. Create superuser:
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

### API Documentation
API documentation is available at `/api/docs/` after starting the project.
You can find the OpenAPI schema in `docs/openapi-schema.yml`.

### Testing
The project includes a Postman collection for API testing located in `postman_collection/foodgram.postman_collection.json`.
