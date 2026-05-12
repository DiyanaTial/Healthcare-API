from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import HospitalMetric
import pandas as pd
import joblib
from typing import Optional

router = APIRouter()

@router.get("/anomalies")
def get_anomalies(
    state: Optional[str] = Query(None),
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db)
):
    model = joblib.load("ml/model.pkl")
    
    query = db.query(HospitalMetric).filter(
        HospitalMetric.measure_id == "OP_18b"
    )
    
    if state:
        query = query.filter(HospitalMetric.state == state.upper())
    
    records = query.all()
    
    df = pd.DataFrame([{
        "id": r.id,
        "facility_name": r.facility_name,
        "state": r.state,
        "measure_id": r.measure_id,
        "score": r.score
    } for r in records])
    
    df["anomaly"] = model.predict(df[["score"]])
    df["anomaly_score"] = model.score_samples(df[["score"]])
    
    anomalies = df[df["anomaly"] == -1]\
        .sort_values("anomaly_score")\
        .head(limit)
    
    return anomalies.to_dict(orient="records")
       
