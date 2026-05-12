import pandas as pd
import joblib
from sqlalchemy import create_engine #creates database connection
from sklearn.ensemble import IsolationForest

DATABASE_URL = "postgresql+psycopg2://dev:dev@127.0.0.1:5432/healthcare"
engine = create_engine(DATABASE_URL)

def train_model():
    df = pd.read_sql("""
                SELECT facility_id, facility_name, state, measure_id, score
                FROM hospital_metrics
                WHERE measure_id = 'OP_18b'     
                     """, engine)
    X = df[["score"]]
    
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X)
    
    df["anomaly"] = model.predict(X)
    # 1 (normal) and -1 (unusual)
    
    df["anomaly_score"] = model.score_samples(X)
    # more negative = more anomalous
    
    joblib.dump(model, "ml/model.pkl")
    
    print(f"Model trained on {len(df)} hospitals.")
    print(f"Anomalies found: {(df['anomaly'] == -1).sum()}")
    
    return df

if __name__ == "__main__":
    train_model()         