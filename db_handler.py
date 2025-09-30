import sqlite3
from datetime import datetime
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "life_portfolio.db")

def create_table():
    """Create the life_portfolio table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS life_portfolio (
        `Strategic Life Areas(SLAs)` TEXT,
        `Strategic Life Units (SLUs)` TEXT,
        `Importance Level` INTEGER,
        `Satisfaction Level` INTEGER,
        `Average Hours Spent in Week` INTEGER,
        Email TEXT,
        Created_Date DATETIME
    )
    """)
    conn.commit()
    conn.close()

def save_dataframe(df: pd.DataFrame, email: str):
    """Save the DataFrame to SQLite, adding email and timestamp."""
    if df.empty:
        return False
    
    df_copy = df.copy()
    df_copy["Email"] = email
    df_copy["Created_Date"] = datetime.now()

    conn = sqlite3.connect(DB_PATH)
    df_copy.to_sql("life_portfolio", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()
    return True

def get_latest_portfolio_data(email: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT * FROM life_portfolio WHERE Email = ?
    AND Created_Date = (
        SELECT MAX(Created_Date)
        FROM life_portfolio
        WHERE Email = ?
    )
    """

    df = pd.read_sql_query(query, conn, params = (email, email))
    conn.close()
    return df 

def get_unique_submission_date(email: str):
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT DISTINCT Created_Date
    FROM life_portfolio
    WHERE Email = ?
    ORDER BY Created_Date DESC
    """
    cursor = conn.cursor()
    cursor.execute(query, (email,))
    rows = cursor.fetchall()
    conn.close()

    return [row[0] for row in rows]


def get_specific_portfolio_data(email: str, date):
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT * FROM life_portfolio WHERE Email = ? and Created_Date = ?    
    """
    df = pd.read_sql_query(query, conn, params = (email, date))
    conn.close()
    return df

def delete_specific_portfolio_data(email: str, date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    DELETE FROM life_portfolio WHERE Email = ? and Created_Date = ?    
    """

    cursor.execute(query, (email, date))
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()
    return deleted_rows > 0