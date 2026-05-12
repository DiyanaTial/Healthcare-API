from fastapi import FastAPI
from app.database import engine, Base
from app.routes import metrics, insights

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Healthcare Analytics API",
    decription="Analyze real U.S. hospital performance data from CMS",
    version="1.0.0"
)

app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])
app.include_router(insights.router, prefix="/insights", tags=["Insights"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

