# Processor backend

This is the FastAPI backend foundation for GeoInformatik. It currently provides
one endpoint: `GET /health`, which confirms that the application is running.
All application functions use synchronous `def`.

## Structure

```text
processor/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── bootstrap/
│   │   ├── __init__.py
│   │   └── application.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── health.py
│   ├── use_cases/
│   │   └── __init__.py
│   ├── repositories/
│   │   └── __init__.py
│   └── models/
│       └── __init__.py
├── tests/
│   └── test_health.py
├── requirements.txt
└── README.md
```

- `src/main.py` exposes the application that Uvicorn runs.
- `src/bootstrap/` creates the FastAPI application and registers API routers.
- `src/api/` contains HTTP endpoints, request validation, and responses.
- `src/use_cases/` will contain business operations.
- `src/repositories/` will contain data access when storage is needed.
- `src/models/` will contain Pydantic request and response models and other
  simple data models when needed.
- `tests/` contains automated tests.

## Install

Use Python 3.11 or newer. Run these commands from the repository root:

```bash
cd processor
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with
`.venv\Scripts\Activate.ps1` instead of `source .venv/bin/activate`.
If your system uses `python3` instead of `python`, use `python3` to create the
virtual environment. Once activated, use `python` for the remaining commands.

FastAPI handles HTTP requests, Uvicorn runs the server, and Pydantic supports
data validation. Tests use pytest and FastAPI's TestClient, which requires httpx2.

## Start

From `processor/`, with the virtual environment activated:

```bash
python -m uvicorn src.main:app --reload
```

The server runs at `http://127.0.0.1:8000`. The `--reload` option restarts it
when source files change. Press `Ctrl+C` to stop it.

## Check health

Open `http://127.0.0.1:8000/health` in a browser, or run this in another terminal
while the server is running:

```bash
curl -i http://127.0.0.1:8000/health
```

Expect HTTP `200 OK` with this JSON:

```json
{"status": "ok"}
```

## Run tests

From `processor/`, with the virtual environment activated:

```bash
python -m pytest
```

The health test checks the HTTP status and the exact response JSON. It uses
TestClient, so you do not need to start a server to run it.

## Add a feature

Put each concrete business operation in its own class in `src/use_cases/`.
Name the class `<Action>UseCase`, for example `SubmitReportUseCase`, and give it
one primary public method, `def execute(self, ...)`. Use private helper methods
such as `_validate_input` when needed. Keep all methods synchronous.

An API endpoint can directly import and instantiate the required use case, call
`execute`, and return an HTTP response. Register any new API routers in
`src/bootstrap/application.py`.

When a use case needs data access, add an ordinary concrete repository class in
`src/repositories/`. The use case may import that class directly. Pass dependencies
through `__init__` when appropriate and construct them locally at the endpoint.
Add Pydantic models in `src/models/` when requests or responses need them.

Keep this straightforward: no base use cases, repository interfaces, global
use case registry, or dependency injection container are needed.
