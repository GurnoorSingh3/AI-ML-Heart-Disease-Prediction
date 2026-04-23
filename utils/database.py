import sqlite3
from datetime import datetime

# Path to the SQLite database file (created automatically if it doesn't exist)
DB_PATH = "predictions.db"

def init_db():
    """Create the predictions table if it doesn't already exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT,
            age         REAL,
            trestbps    REAL,
            chol        REAL,
            thalch      REAL,
            oldpeak     REAL,
            ca          REAL,
            sex         TEXT,
            cp          TEXT,
            fbs         TEXT,
            restecg     TEXT,
            exang       TEXT,
            slope       TEXT,
            thal        TEXT,
            prediction  TEXT,
            probability REAL,
            timestamp   TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_prediction(name,age, trestbps, chol, thalch, oldpeak, ca,
                    sex, cp, fbs, restecg, exang, slope, thal,
                    prediction, probability):
    """Insert one prediction record into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions
        (name,age, trestbps, chol, thalch, oldpeak, ca,
         sex, cp, fbs, restecg, exang, slope, thal,
         prediction, probability, timestamp)
        VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,age, trestbps, chol, thalch, oldpeak, ca,
        str(sex), str(cp), str(fbs), str(restecg), str(exang), str(slope), str(thal),
        prediction, probability,
        datetime.now().strftime("%Y-%m-%d %H:%M")   # human-readable timestamp
    ))
    conn.commit()
    conn.close()


def get_all_predictions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, age, trestbps, chol, thalch, oldpeak, ca,
               sex, cp, fbs, restecg, exang, slope, thal,
               prediction, probability, timestamp
        FROM predictions
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def clear_all_predictions():
    """Delete every row from the predictions table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions")
    conn.commit()
    conn.close()

