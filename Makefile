.PHONY: help # Show this help screen
help:
	@grep -h '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) # \(.*\)/make \1 \t- \2/' | expand -t20

.PHONY: install # Build and install Docker container on Docker server
install: build start

.PHONY: build # Build Docker container
build:
	docker compose --env-file=.env build

.PHONY: start # Start docker container
start:
	docker compose --env-file=.env up -d

.PHONY: api-dev # Run API server locally
api-dev:
	cd api && poetry run uvicorn app.main:app --port 8090 --reload
