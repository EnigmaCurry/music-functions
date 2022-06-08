.PHONY: help # Show this help screen
help:
	@grep -h '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) # \(.*\)/make \1 \t- \2/' | expand -t20

.PHONY: install # Build and install Docker container on Docker server
install: build start

.PHONY: build # Build Docker containers
build:
	docker compose --env-file=.env build

.PHONY: build-dev # Build development Docker containers
build-dev:
	docker compose --file docker-compose.dev.yaml --env-file=.env-dev build

.PHONY: start # Start docker container
start:
	docker compose --env-file=.env up -d

.PHONY: start-dev # Start development docker container
start-dev:
	docker compose --file docker-compose.dev.yaml --env-file=.env-dev up -d

.PHONY: api-dev # Run API server locally
api-dev:
	cd api && poetry run uvicorn app.main:app --port 8090 --reload

.PHONY: mount-sshfs # Mount local directory to remote docker server via SSHFS
mount-sshfs:
	killall ncat
	ncat -l -p 34567 -e /usr/lib/ssh/sftp-server &
	ssh -t -R 34568:localhost:34567 docker-vm "mkdir -p /mnt/dev; sshfs localhost: /mnt/dev -o directport=34568"

.PHONY: dev # Run dev server with local files mounted to remote docker server
dev: mount-sshfs build-dev start-dev
