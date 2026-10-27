# Week 8, Day 5 — AI Data Platform: Full Demo and Documentation

## 1. Project Overview

The AI Data Platform project provides an interactive way to upload CSV files, analyze data, ask questions about datasets, and view analytical results through a web application.

## 2. Features

- Upload CSV files for analysis.
- Validate uploaded file types.
- Generate data insights using Python and Pandas.
- Ask questions about uploaded data through the API.
- Access interactive charts and analysis results.
- View API documentation through Swagger UI.
- Check application health through the health endpoint.

## 3. Technology Stack

- **Programming language:** Python
- **Backend framework:** FastAPI
- **Data analysis:** Pandas
- **Frontend:** HTML, CSS, JavaScript
- **Server:** Uvicorn
- **Testing:** Pytest
- **Deployment:** Render

## 4. Project Structure

```text
Week 07/
└── Day 5/
    ├── api.py
    ├── index.html
    ├── script.js
    ├── style.css
    ├── requirements.txt
    └── tests/
        └── test_api.py

Week 08/
├── Day 4/
│   └── README.md
└── Day 5/
    └── README.md

render.yaml
```

## 5. Local Setup

1. Clone the repository.
2. Open the repository folder in VS Code.
3. Activate the Python virtual environment.
4. Install the required dependencies:

```powershell
pip install -r "Week 07\Day 5\requirements.txt"
```

5. Start the application:

```powershell
Set-Location "Week 07\Day 5"
python -m uvicorn api:app --reload
```

6. Open `http://127.0.0.1:8000` in your browser.

## 6. API Endpoints

| Endpoint      | Purpose                                     |
| ------------- | ------------------------------------------- |
| `/`           | Opens the web application                   |
| `/health`     | Checks application health                   |
| `/cia/upload` | Uploads a CSV file                          |
| `/cia/query`  | Processes data-analysis queries             |
| `/docs`       | Opens interactive Swagger API documentation |

## 7. Testing

Run the automated tests from the repository root:

```powershell
python -m pytest "Week 07\Day 5\tests\test_api.py" -v
```

The tests cover application health, CSV uploads, query processing, invalid file uploads, and frontend routes.

## 8. Production Deployment

**Platform:** Render

**Deployment URL:** Pending successful deployment.

After deployment, verify the homepage, health endpoint, CSV upload, query functionality, and API documentation. Check the logs for server errors before considering the deployment complete.

## 9. Demo Video

**Demo link:** To be added after recording and uploading the demonstration.

The three-minute demo will show the application, CSV upload, analysis workflow, API documentation, and deployment verification.

## 10. Known Limitations

- Analysis quality depends on the uploaded dataset and the query.
- Only supported CSV uploads should be used.
- Production deployment is not yet confirmed.
- The live URL and demo link will be added after successful verification.

## 11. Conclusion

This project demonstrates an end-to-end data analysis web application using FastAPI, Pandas, and a browser-based interface, with automated tests and production deployment preparation.
