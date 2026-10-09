"""
Mini Database — RDS-backed Web App
====================================
Web UI for the Mini Database project, but every operation now reads/writes to your
Amazon RDS MySQL instance via db.py, instead of session_state.
Data persists across restarts, browser sessions, and even different
users hitting the app at once.

Setup: see the docstring at the top of db.py first.

Run:
    pip install streamlit pandas pymysql
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import db

st.set_page_config(page_title="Mini Database (RDS)", page_icon="🗂️")
st.title("🗂️ Mini Database — RDS backend")
st.caption("CRUD app backed by a real Amazon RDS MySQL instance.")

tab_create, tab_view, tab_update, tab_delete, tab_search = st.tabs(
    ["➕ Create", "📋 View All", "✏️ Update", "🗑️ Delete", "🔍 Search"]
)

# CREATE
with tab_create:
    st.subheader("Add a new record")
    with st.form("create_form", clear_on_submit=True):
        name = st.text_input("Name")
        role = st.text_input("Role")
        city = st.text_input("City")
        if st.form_submit_button("Create") and name:
            new_id = db.create_record(name, role, city)
            st.success(f"Created record #{new_id}")

# VIEW ALL
with tab_view:
    st.subheader("All records")
    rows = db.read_all()
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
    else:
        st.info("No records yet. Add one in the Create tab.")

# UPDATE
with tab_update:
    st.subheader("Update a record")
    rows = db.read_all()
    ids = [r["id"] for r in rows]
    if ids:
        rid = st.selectbox("Choose record id", ids, key="update_id")
        record = db.read_by_id(rid)
        with st.form("update_form"):
            name = st.text_input("Name", value=record["name"])
            role = st.text_input("Role", value=record["role"])
            city = st.text_input("City", value=record["city"])
            if st.form_submit_button("Save changes"):
                db.update_record(rid, name, role, city)
                st.success(f"Updated record #{rid}")
    else:
        st.info("No records yet.")

# DELETE
with tab_delete:
    st.subheader("Delete a record")
    rows = db.read_all()
    ids = [r["id"] for r in rows]
    if ids:
        rid = st.selectbox("Choose record id", ids, key="delete_id")
        if st.button("Delete", type="primary"):
            db.delete_record(rid)
            st.success(f"Deleted record #{rid}")
            st.rerun()
    else:
        st.info("No records yet.")

# SEARCH
with tab_search:
    st.subheader("Search records")
    col1, col2, col3 = st.columns(3)
    name_q = col1.text_input("Name contains")
    role_q = col2.text_input("Role equals")
    city_q = col3.text_input("City equals")
    if st.button("Search"):
        results = db.search(name=name_q, role=role_q, city=city_q)
        if results:
            st.dataframe(pd.DataFrame(results), use_container_width=True)
        else:
            st.warning("No matching records.")
