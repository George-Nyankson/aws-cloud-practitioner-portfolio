"""
db.py — RDS MySQL backend for the Mini Database app
=====================================================
Replaces the in-memory session_state storage with real persistence
in an Amazon RDS MySQL instance.

SETUP (one-time):
------------------
1. Connect to your RDS instance (you've already done this in the RDS
   SQL operations project) and create the table:

    CREATE DATABASE IF NOT EXISTS mini_database;
    USE mini_database;

    CREATE TABLE IF NOT EXISTS records (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        role VARCHAR(100),
        city VARCHAR(100)
    );

2. In your project folder, create a folder ".streamlit" and inside it
   a file called "secrets.toml" (NEVER commit this file to GitHub —
   add ".streamlit/secrets.toml" to your .gitignore):

    [rds]
    host = "your-instance.xxxxxxxxxx.us-east-1.rds.amazonaws.com"
    port = 3306
    user = "admin"
    password = "your-master-password"
    database = "mini_database"

3. On the RDS security group, make sure inbound rules allow MySQL/Aurora
   (port 3306) from the IP address the app runs on:
     - Running locally on your machine: your current public IP
     - Deployed on Streamlit Community Cloud: 0.0.0.0/0 is required,
       since Streamlit Cloud's IPs aren't fixed (fine for a portfolio
       demo, but for a real app prefer a VPN/bastion or IAM auth instead)
"""

import pymysql
import streamlit as st


def get_connection():
    """Open a connection to RDS using credentials from secrets.toml."""
    cfg = st.secrets["rds"]
    return pymysql.connect(
        host=cfg["host"],
        port=int(cfg.get("port", 3306)),
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def create_record(name, role, city):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO records (name, role, city) VALUES (%s, %s, %s)",
                (name, role, city),
            )
            return cur.lastrowid
    finally:
        conn.close()


def read_all():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM records ORDER BY id")
            return cur.fetchall()
    finally:
        conn.close()


def read_by_id(record_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM records WHERE id = %s", (record_id,))
            return cur.fetchone()
    finally:
        conn.close()


def update_record(record_id, name, role, city):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE records SET name=%s, role=%s, city=%s WHERE id=%s",
                (name, role, city, record_id),
            )
            return cur.rowcount > 0
    finally:
        conn.close()


def delete_record(record_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM records WHERE id = %s", (record_id,))
            return cur.rowcount > 0
    finally:
        conn.close()


def search(name=None, role=None, city=None):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            query = "SELECT * FROM records WHERE 1=1"
            params = []
            if name:
                query += " AND name LIKE %s"
                params.append(f"%{name}%")
            if role:
                query += " AND role = %s"
                params.append(role)
            if city:
                query += " AND city = %s"
                params.append(city)
            cur.execute(query, params)
            return cur.fetchall()
    finally:
        conn.close()
