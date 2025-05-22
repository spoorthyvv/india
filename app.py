import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json
from streamlit_plotly_events import plotly_events

# Configure Streamlit page
st.set_page_config(page_title="Interactive India Map", layout="wide")

# Title and instructions
st.title("🇮🇳 Interactive India Map (Click a State)")
st.markdown("""
This is an interactive map of India.  
Click on any state to:
- Highlight it in **red**
- Automatically **redirect** to a URL (placeholder)

You can replace these URLs with your actual site links.
""")

# Load GeoJSON from GitHub (state boundaries)
@st.cache_data
def load_geojson():
    with open("india_state.geojson", "r", encoding="utf-8") as f:
        return json.load(f)

geojson = load_geojson()

# Get list of states from the GeoJSON
state_names = [feature["properties"]["st_nm"] for feature in geojson["features"]]

# Create DataFrame to match Plotly's expectations
df = pd.DataFrame({
    "state": state_names,
    "value": [1] * len(state_names)  # dummy value for coloring
})

# Mapping from state names to placeholder URLs (you can replace these)
state_links = {
    state: f"https://yourdomain.com/{state.replace(' ', '_').lower()}"
    for state in state_names
}

# Create Plotly choropleth map
fig = px.choropleth(
    df,
    geojson=geojson,
    locations="state",
    featureidkey="properties.st_nm",
    color="value",
    color_continuous_scale=[[0, "white"], [1, "red"]],
    scope="asia",
    title="Click a State to Redirect"
)

# Remove axes and color bar
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
    coloraxis_showscale=False
)

# Display map and listen for clicks
selected_points = plotly_events(fig, click_event=True, hover_event=False)
st.plotly_chart(fig, use_container_width=True)

# Show clicked state and redirect
if selected_points:
    clicked_state = selected_points[0]["location"]
    if clicked_state:
        st.success(f"You clicked on: {clicked_state}")
        target_url = state_links.get(clicked_state)

        if target_url:
            st.markdown(f"Redirecting to: [{target_url}]({target_url})")
            # Trigger JavaScript redirect
            st.components.v1.html(f"""
                <meta http-equiv="refresh" content="1; URL={target_url}">
                <script>window.location.href = "{target_url}";</script>
            """, height=0)
        else:
            st.warning("No URL defined for this state.")
