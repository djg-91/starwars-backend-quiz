APP_MODULE := api.main:app
PORT ?= 8000
UV := uv run

.PHONY: help
help:
	@echo ""
	@echo "Makefile commands:"
	@echo "  make install             Install dependencies (uv sync)"
	@echo "  make install-cli-alias   Install alias starwars-cli"
	@echo "  make run                 Run FastAPI app (reload)"
	@echo "  make test                Run tests with pytest"
	@echo "  make lint                Run Ruff checks"
	@echo "  make lint-fix            Apply Ruff fixes"
	@echo "  make up                  Docker Compose up (only API)"
	@echo "  make down                Docker Compose down"
	@echo ""

.PHONY: install
install:
	uv sync

.PHONY: install-cli-alias
install-cli-alias:
	bash install-alias.sh

.PHONY: run
run:
	$(UV) uvicorn $(APP_MODULE) --reload --port $(PORT)

.PHONY: test
test:
	$(UV) pytest

.PHONY: lint
lint:
	$(UV) ruff check .

.PHONY: lint-fix
lint-fix:
	$(UV) ruff check --fix .
	$(UV) ruff format .
	$(UV) ruff check .

.PHONY: up
up:
	docker-compose up --build --detach api

.PHONY: down
down:
	docker-compose down
