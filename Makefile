# Define the image and service names
IMAGE_NAME=drug-info-assistant-app
SERVICE_NAME=app

# Build the Docker image
build:
	docker-compose build

# Start the containers in detached mode
up:
	docker-compose up -d

# View logs from the containers
logs:
	docker-compose logs -f

# Stop the containers
down:
	docker-compose down

# Run tests (you can customize this to run your tests in a container)
test:
	docker-compose exec $(SERVICE_NAME) pytest

# Clean up unused Docker images and volumes
prune:
	docker system prune -f
	docker volume prune -f

# Rebuild and restart the containers
restart:
	docker-compose down
	docker-compose up -d

# Build the Docker image and run containers with one command
build_and_up: build up

# Access the running app's shell in the container (useful for debugging)
shell:
	docker-compose exec $(SERVICE_NAME) /bin/bash
