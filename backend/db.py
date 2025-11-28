# db.py
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def get_conn():
    """Return a new connection (caller must close)."""
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        port=DB_CONFIG.get("port", 3306)
    )

def fetchall_dict(query, params=None):
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        return rows
    finally:
        if conn:
            conn.close()

def fetchone_dict(query, params=None):
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        row = cursor.fetchone()
        return row
    finally:
        if conn:
            conn.close()

def execute(query, params=None):
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.lastrowid
    finally:
        if conn:
            conn.close()
