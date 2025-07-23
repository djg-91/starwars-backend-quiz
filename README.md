# Star Wars Backend Quiz

A FastAPI + Typer CLI backend project to explore Star Wars data from [SWAPI](https://swapi.info/api). Features include pagination, sorting, filtering, logging, a CLI client, and an endpoint for mock AI insights.

## 🚀 Tech Stack

- Python 3.13
- FastAPI (API backend)
- Uvicorn (ASGI server)
- uv (Python environment manager)
- Pydantic v2 (data validation & docs)
- Docker / Docker Compose (deployment)
- Typer (CLI commands)
- pytest + asyncio (testing)
- Ruff (linting & formatting)

## 🛠 Prerequisites

- **Docker:** Used to run the API in an isolated container  
→ Install: https://docs.docker.com/get-docker/

- **uv:** Fast Python package and environment manager (replacement for pip + virtualenv)  
→ Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`

- **make:** For running predefined development commands via Makefile  
  → On Debian/Ubuntu: `sudo apt install make`

## 📦 Make Commands

| Command                  | Description                                        |
|--------------------------|----------------------------------------------------|
| `make install`           | Install dependencies using `uv sync`               |
| `make install-cli-alias` | Install alias starwars-cli using `docker-compose`  |
| `make run`               | Start FastAPI server with reload (localhost:8000)  |
| `make test`              | Run unit tests using pytest                        |
| `make lint`              | Run Ruff to check code quality                     |
| `make lint-fix`          | Auto-fix and format with Ruff                      |
| `make up`                | Build and run Docker container for the API         |
| `make down`              | Stop Docker container                              |
| `make help`              | Show help information                              |

## 🐳 Docker Setup

```bash
# Copy and configure environment variables
cp .env.example .env

# Start the API container
make up
```

## 💻 CLI Setup

```bash
# Install a convenient CLI alias 
make install-cli-alias
```

You can then use the CLI as:

```bash
starwars-cli planets list --search=tatooine

starwars-cli people list --sort-by=height --order=desc
```

## 📚 API Documentation

Once the API is running, you can explore and test all endpoints interactively via the FastAPI docs:

**Swagger UI:** http://localhost:6969/docs

**ReDoc (alternative view):** http://localhost:6969/redoc

These docs are auto-generated and reflect the available endpoints, query parameters, and example responses.

## 🌍 API Endpoints

FastAPI runs at `http://localhost:6969`

- `/people`: Paginated, filtered list of characters
- `/planets`: Paginated, filtered list of planets
- `/simulate-ai-insight`: Returns mock AI descriptions

## 🧪 Testing

```bash
make test
```

Tests include:

- Pagination
- Filtering
- Sorting
- CLI parsing

---

May the code be with you ✨
