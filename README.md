# Healthcare Analytics API

![CI](https://github.com/DiyanaTial/Healthcare-API/actions/workflows/ci.yml/badge.svg)

This project is a Python REST API that analyzes real U.S. hospital performance data from CMS (Centers for Medicare & Medicaid Services) and it uses machine learning (Isolation Forest) to detect anomalous hospital performance.

## What it does
- Serves real hospital performance data from 4,500+ hospitals in 50 states.
- Allows filtering by state, measure, and performance metric
- Aggregates and compares hospital performance by state
- Uses an Isolation Forest ML model to automatically flag hospitals with unusual performance scores

## Tech stack
- **Python** - core language
- **FastAPI** - REST API framework
- **PostgreSQL** - database
- **SQLAlchemy** - database ORM
- **scikit-learn** - machine learning (Isolation Forest anomaly) 
- **pandas** - data manipulation/processing and ETL
- **Docker** - containerization
- **pytest** - automated testing
- **GitHub** - CI/CD pipeline

## Get started
Make sure you have Docker installed, then run:
```bash
git clone https://github.com/DiyanaTial/Healthcare-API.git
cd Healthcare-API
docker compose up --build
```

The API is available at `http://localhost:8000/docs`

## Project Structure
```
Healthcare-API/
|--app/
|   |--main.py #FastAPI app entry point
|   |--database.py #Database connection
|   |--models.py #SQLAlchemy table definitions
|   |--routes/
|       |--metrics.py #Hospital data endpoints
|       |--insights.py #ML Anomaly detection endpoints
|--ml/
|   |--anomaly.py #Isolation Forest model training
|--data/
|   |--seed.py #ETL script for CMS data
|--tests/
|   |--test_metrics.py #Metrics endpoint tests
|   |--test_insights.py #Insights endpoint tests
|
|--Dockerfile
|--docker-compose.yml
|--requirements.txt

## API endpoints
```
GET `/health` : health check
GET `/metrics/`: Get hospital metrics, filter by state and measure
GET `/metrics/aggregate`: Get average scores grouped by state
GET `/insights/anomalies/`: Get ML-flagged anomalous hospitals

### Example requests
Get all Kansas ER wait times:
GET `/metrics/?state=KS&measure_id=OP_18b`

Get average ER wait time by state:
GET `/metrics/aggregate?measure_id=OP_18b`

Get anomalous hospitals in Kansas:
GET `/insights/anomalies?state=KS`
```

## Data Source
Hospital performance data sourced from the CMS Hospital Care Compare dataset, including 53,749 records covering timely and effective care measures across 4,500+ U.S. hospitals.

## Machine Learning
Isolation Forest Model: trained on ER wait time score (measure id OP_18b) across all hospitals nationwide. The model flags approximately 5% of hospitals as statistical outliers -- both unusally high and unusally low performers.

Exmaple anomalies detected in Kansas:
- **University of Kansas Hospital** — 307 minutes (flagged as unusually high)
- **Sedan City Hospital** — 67 minutes (flagged as unusually low)

## Testing
Run the test suite:

```bash
pytest tests/ -v
```

11 tests that covers endpoint responses, filtering, validation, and ML output. CI runs automatically on every push via GitHub Actions.

## Future Work
- Retrain the model automatically when CMS releases new quarterly data
- Add endpoints for additional measures beyond ER wait times
- Add authentication so only authorized users can access the API
- Deploy to AWS 



