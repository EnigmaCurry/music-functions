.PHONY: help # Show this help screen
help:
	@grep -h '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) # \(.*\)/make \1 \t- \2/' | expand -t20

.PHONY: install # Build and install Docker container on Docker server
install: build start

.PHONY: build # Build Docker containers
build:
	docker compose build

.PHONY: build-clean # Build Docker containers from scratch (no cache)
build-clean:
	docker compose build --no-cache

.PHONY: build-dev # Build development Docker containers
build-dev:
	docker compose --file docker-compose.dev.yaml build

.PHONY: start # Start docker container
start:
	docker compose up -d

.PHONY: start-dev # Start development docker container
start-dev:
	docker compose --file docker-compose.dev.yaml up -d

.PHONY: api-dev # Run API server locally
api-dev:
	cd api && poetry run uvicorn app.main:app --port 8090 --reload

.PHONY: dev # Run dev server with local files mounted to remote docker server
dev: build-dev start-dev

.PHONY: sync # Run continuous synchronization to remote server
sync:
	./_scripts/sync.sh . $$(docker context inspect | jq -r '.[0]["Endpoints"]["docker"]["Host"]' | sed 's|ssh://||'):$$(./_scripts/dotenv.sh -f .env get DEVELOPMENT_MOUNTED_VOLUME)

.PHONY: logs # Get production logs
logs:
	docker logs -f music-functions-api 

.PHONY: logs-dev # Get development logs
logs-dev:
	docker logs -f music-functions-api-dev 

.PHONY: logs-dev-fe # Get development frontend logs
logs-dev-fe:
	docker logs -f music-functions-frontend-dev

.PHONY: test # Run unit tests
test:
	sh -c "cd api; 	poetry run pytest app/test"
