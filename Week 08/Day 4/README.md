# Week 8 Day 4 — Production Deployment and API Documentation

## 1. Objective

Prepare the CIA Data Analyst Mode application for production deployment, document its API endpoints, verify functionality, and prepare a demonstration video.

## 2. Project Overview

**Project Name:** CIA Data Analyst Mode

A web application that allows users to upload CSV datasets and perform data analysis through a simple web interface.

## 3. Technology Stack

- Python 3.11
- FastAPI
- Uvicorn
- Pandas
- HTML, CSS, and JavaScript
- Chart.js
- Pytest
- Render (planned deployment platform)

## 4. Features

- CSV upload and validation
- Dataset preview
- Row counting and statistical calculations
- Grouped data analysis
- Chart generation
- REST API endpoints
- API health check
- Interactive Swagger documentation

## 5. API Documentation

| Method | Endpoint        | Description                      |
| ------ | --------------- | -------------------------------- |
| GET    | `/`             | Opens the web application        |
| GET    | `/health`       | Checks API health                |
| POST   | `/cia/upload`   | Uploads and validates a CSV file |
| POST   | `/cia/query`    | Processes a data analysis query  |
| GET    | `/docs`         | Opens Swagger API documentation  |
| GET    | `/openapi.json` | Returns the OpenAPI schema       |

## 6. Local Setup

Run the following commands from the repository root.

Install dependencies:

```powershell
pip install -r "Week 07/Day 5/requirements.txt"
```

Start the application:

```powershell
python -m uvicorn api:app --app-dir "Week 07/Day 5" --reload
```

Open the application at `http://127.0.0.1:8000/`.

API documentation: `http://127.0.0.1:8000/docs`

Health check: `http://127.0.0.1:8000/health`

## 7. Deployment Configuration

- **Platform:** Render
- **Configuration file:** `render.yaml`
- **Application directory:** `Week 07/Day 5`
- **Build command:** `pip install -r requirements.txt`
- **Start command:** `uvicorn api:app --host 0.0.0.0 --port $PORT`
- **Health check path:** `/health`
- **Production URL:** Pending deployment

## 8. Testing

Run the API tests:

```powershell
python -m pytest "Week 07/Day 5/tests/test_api.py" -v
```

**Local test result:** 3 tests passed.

Local checks also confirmed successful responses from the application page, CSS, JavaScript, health endpoint, and Swagger documentation.

Production testing is pending.

## 9. Known Limitations

- Uploaded datasets are stored in memory and may be lost when the server restarts.
- CSV uploads have configured size and dataset limits.
- Only supported analysis questions can be processed.
- In-memory sessions are not shared across multiple application instances.

## 10. Demo and Submission

- **Production URL:** Pending deployment
- **Demo video:** Pending recording
- **Git branch:** `feat/w8d4-3m-Hema`
- **Pull request:** Pending submission

## 11. Current Status

Local application integration and API tests are complete. Production deployment, live endpoint verification, demonstration recording, and pull request submission remain to be completed.
