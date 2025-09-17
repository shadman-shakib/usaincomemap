import pandas as pd
import folium
import streamlit as st

# Set the page layout to wide (full width)
st.set_page_config(layout="wide")
with open("./income_map.html", "r", encoding="utf-8") as f:
    map_html = f.read()

# Add a title for the page
st.title("State Income Map through the US")
st.components.v1.html(map_html, height=600, width=0,scrolling=True)
