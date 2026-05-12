from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import HospitalMetric
from typing import Optional

router = APIRouter()

@router.get("/")
def get_metrics(
    state: Optional[str] = Query(None),
    measure_id: Optional[str] = Query(None),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    query = db.query(HospitalMetric)
    
    if state:
        query = query.filter(HospitalMetric.state == state.upper())
        
    if measure_id:
        query = query.filter(HospitalMetric.measure_id == measure_id)
        
    return query.limit(limit).all()

@router.get("/aggregate")
def get_aggregate(
    measure_id: str = Query(...),
    group_by: str = Query("state"),
    db: Session = Depends(get_db)
):
    query = db.query(
        HospitalMetric.state,
        func.avg(HospitalMetric.score).label("avg_score"),
        func.min(HospitalMetric.score).label("min_score"),
        func.max(HospitalMetric.score).label("max_score"),
        func.count(HospitalMetric.facility_id).label("hospital_count")
    ).filter(
        HospitalMetric.measure_id == measure_id
    ).group_by(
        HospitalMetric.state
    ).order_by(
        func.avg(HospitalMetric.score).desc()
    )
    
    results = query.all()
    
    return [ 
        {
            "state": r.state,
            "avg_score": round(r.avg_score, 2),
            "min_score": r.min_score,
            "max_score": r.max_score,
            "hospital_count": r.hospital_count
        }
        for r in results
    ]
    
    