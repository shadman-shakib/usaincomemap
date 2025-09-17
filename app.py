import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium

# Set the page layout to wide (full width)
st.set_page_config(layout="wide")
with open("./income_map.html", "r", encoding="utf-8") as f:
    map_html = f.read()

# Add a title for the page
st.title("State Income Map through the US")

# Load income data
income = pd.read_csv(
    "https://raw.githubusercontent.com/pri-data/50-states/master/data/income-counties-states-national.csv",
    dtype={"fips": str},
)
# errors="coerce" handles non-numeric values by replacing them with NaN
income["income-2015"] = pd.to_numeric(income["income-2015"], errors="coerce")

# Define state_medians
state_medians = income.groupby("state").agg(
    state_med_2015=("income-2015", "median"),
    state_med_1989=("income-1989b", "median"), # Use income-1989b for inflation-adjusted median
).reset_index()

# Display the map and the state income data side by side
col1, col2 = st.columns(2)

with col1:
    st.subheader("US State Income Map (2015 Median)")
    st.components.v1.html(map_html, height=600, width=0,scrolling=True)


with col2:
    st.subheader("State Income Statistics")
    all_states = sorted(state_medians["state"].unique())
    pick = st.selectbox("Choose a state", all_states, index=all_states.index("NE") if "NE" in all_states else 0)

    # Filter data for chosen state
    sub = income[income["state"] == pick].copy()
    sub = sub.rename(columns={
        "county": "County",
        "income-2015": "Income 2015 (USD)",
        "income-1989a": "Income 1989 (USD)" # Using 1989a for raw 1989 income
    })[["County", "Income 2015 (USD)", "Income 1989 (USD)"]].sort_values("County")

    # Get medians for the selected state
    state_median_2015_value = state_medians[state_medians["state"] == pick]['state_med_2015'].iloc[0]
    state_median_1989_value = state_medians[state_medians["state"] == pick]['state_med_1989'].iloc[0]

    st.metric("State Median Income (2015)", f"${state_median_2015_value:,.0f}")
    st.metric("State Median Income (1989, inflation-adjusted)", f"${state_median_1989_value:,.0f}")

    st.dataframe(sub, use_container_width=True, height=420)
