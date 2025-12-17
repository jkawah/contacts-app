# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 19:12:57 2025

@author: JKawah
"""

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Config
st.set_page_config(page_title="My Contacts Lookup", layout="wide")
st.title("Quick Contacts Manager")
#FILE_PATH = 'C:/Users/JKawah/OneDrive/Documents/aa LRA work/aa LRA My Projects/AI and automation support/contacts.csv'  # UPDATE THIS TO YOUR CSV PATH (or .xlsx)
FILE_PATH = 'contacts.csv'  # UPDATE THIS TO YOUR CSV PATH (or .xlsx)
# Load data
def load_data():
    try:
        return pd.read_csv(FILE_PATH) if FILE_PATH.endswith('.csv') else pd.read_excel(FILE_PATH)
    except FileNotFoundError:
        st.error("File not found! Check the path.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# Search bar
search = st.text_input("Search contacts (name, phone, email, etc.)")
if search:
    df_display = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
else:
    df_display = df.copy()

# Editable grid
gb = GridOptionsBuilder.from_dataframe(df_display)
gb.configure_default_column(editable=True, groupable=True)
gb.configure_selection('single')
grid_options = gb.build()

response = AgGrid(
    df_display,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.SELECTION_CHANGED,
    height=500,
    fit_columns_on_grid_load=True,
    theme='streamlit'
)

edited_df = response['data']

# Save changes button
if st.button("Save Changes to File"):
    edited_df.to_csv(FILE_PATH, index=False) if FILE_PATH.endswith('.csv') else edited_df.to_excel(FILE_PATH, index=False)
    st.success("Changes saved!")
    st.experimental_rerun()

# Add new contact
st.subheader("Add New Contact")
with st.form("add_form"):
    new_row = {}
    for col in df.columns:
        new_row[col] = st.text_input(col)
    if st.form_submit_button("Add Contact"):
        new_df = pd.DataFrame([new_row])
        updated_df = pd.concat([df, new_df], ignore_index=True)
        updated_df.to_csv(FILE_PATH, index=False) if FILE_PATH.endswith('.csv') else updated_df.to_excel(FILE_PATH, index=False)
        st.success("New contact added!")
        st.experimental_rerun()

# Delete selected
if response['selected_rows']:
    sel_row = pd.DataFrame(response['selected_rows'])
    if st.button("Delete Selected Contact"):
        df = df.drop(sel_row.index)
        df.to_csv(FILE_PATH, index=False) if FILE_PATH.endswith('.csv') else df.to_excel(FILE_PATH, index=False)
        st.success("Deleted!")

        st.experimental_rerun()
