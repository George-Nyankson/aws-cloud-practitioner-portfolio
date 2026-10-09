"""
Mini Database — Web App Version
=================================
The same CRUD logic from mini_database.py, wrapped in a Streamlit web UI.
Records are stored in Streamlit's session_state, so they persist while
the app is open in your browser (but reset if the server restarts).

To run this app:
    1. pip install streamlit
    2. streamlit run app.py
It will open automatically in your browser at http://localhost:8501
"""

import streamlit as st
import pandas as pd

# ---------- Database logic (same ideas as the CLI version) ----------

if "database" not in st.session_state:
    st.session_state.database = []
if "next_id" not in st.session_state:
    st.session_state.next_id = 1


def create_record(name, role, city):
    record = {
        "id": st.session_state.next_id,
        "name": name,
        "role": role,
        "city": city,
    }
    st.session_state.database.append(record)
    st.session_state.next_id += 1
    return record


def read_by_id(record_id):
    for record in st.session_state.database:
        if record["id"] == record_id:
            return record
    return None


def update_record(record_id, **fields):
    record = read_by_id(record_id)
    if record:
        record.update(fields)
    return record


def delete_record(record_id):
    record = read_by_id(record_id)
    if record:
        st.session_state.database.remove(record)
        return True
    return False


def search(**criteria):
    results = []
    for record in st.session_state.database:
        if all(record.get(k) == v for k, v in criteria.items() if v):
            results.append(record)
    return results


# ---------- Web UI ----------

st.set_page_config(page_title="Mini Database", page_icon="🗂️")
st.title("🗂️ Mini Database")
st.caption("A simple CRUD app built with lists, dictionaries, and Streamlit.")

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
        submitted = st.form_submit_button("Create")
        if submitted and name:
            record = create_record(name, role, city)
            st.success(f"Created record #{record['id']}")

# VIEW ALL
with tab_view:
    st.subheader("All records")
    if st.session_state.database:
        st.dataframe(pd.DataFrame(st.session_state.database), use_container_width=True)
    else:
        st.info("No records yet. Add one in the Create tab.")

# UPDATE
with tab_update:
    st.subheader("Update a record")
    ids = [r["id"] for r in st.session_state.database]
    if ids:
        rid = st.selectbox("Choose record id", ids, key="update_id")
        record = read_by_id(rid)
        with st.form("update_form"):
            name = st.text_input("Name", value=record["name"])
            role = st.text_input("Role", value=record["role"])
            city = st.text_input("City", value=record["city"])
            if st.form_submit_button("Save changes"):
                update_record(rid, name=name, role=role, city=city)
                st.success(f"Updated record #{rid}")
    else:
        st.info("No records yet.")

# DELETE
with tab_delete:
    st.subheader("Delete a record")
    ids = [r["id"] for r in st.session_state.database]
    if ids:
        rid = st.selectbox("Choose record id", ids, key="delete_id")
        if st.button("Delete", type="primary"):
            delete_record(rid)
            st.success(f"Deleted record #{rid}")
            st.rerun()
    else:
        st.info("No records yet.")

# SEARCH
with tab_search:
    st.subheader("Search records")
    col1, col2, col3 = st.columns(3)
    name_q = col1.text_input("Name contains / equals")
    role_q = col2.text_input("Role equals")
    city_q = col3.text_input("City equals")
    if st.button("Search"):
        results = [
            r
            for r in st.session_state.database
            if (not name_q or name_q.lower() in r["name"].lower())
            and (not role_q or r["role"] == role_q)
            and (not city_q or r["city"] == city_q)
        ]
        if results:
            st.dataframe(pd.DataFrame(results), use_container_width=True)
        else:
            st.warning("No matching records.")
