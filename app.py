import streamlit as st
import pandas as pd
import plotly.express as px
import json
from streamlit_plotly_events import plotly_events

st.set_page_config(page_title="Interactive India Map", layout="wide")

st.title("🇮🇳 Interactive India Map - Click a State")

@st.cache_data
def load_geojson():
    with open("india_state.geojson", "r", encoding="utf-8") as f:
        return json.load(f)

geojson = load_geojson()

# Extract state names
state_names = [feature["properties"]["NAME_1"] for feature in geojson["features"]]

# Create dummy data for coloring
df = pd.DataFrame({
    "state": state_names,
    "value": [1] * len(state_names)  # uniform dummy value
})

# Create the choropleth map
fig = px.choropleth(
    df,
    geojson=geojson,
    locations="state",
    featureidkey="properties.NAME_1",
    color="value",
    color_continuous_scale=[[0, "white"], [1, "red"]],
    hover_name="state",
    scope="asia",
)

# Style the map: remove axes, add red borders, hover effect
fig.update_geos(
    fitbounds="locations",
    visible=False,
)

# Red border around states
fig.update_traces(marker_line_width=1, marker_line_color="red")

# Remove colorbar
fig.update_layout(
    margin={"r":0,"t":30,"l":0,"b":0},
    coloraxis_showscale=False,
    title_text="Click a State to Redirect to spoorthyvv.github.io",
)

# Display map and listen for click events
selected_points = plotly_events(fig, click_event=True, hover_event=False)

st.plotly_chart(fig, use_container_width=True)

# Redirect on click
if selected_points:
    clicked_state = selected_points[0].get("location")
    if clicked_state:
        st.success(f"You clicked: {clicked_state}")
        # Redirect to fixed URL on click
        redirect_url = "https://spoorthyvv.github.io/"
        st.markdown(f"Redirecting to [spoorthyvv.github.io]({redirect_url}) ...")

        # Use JS redirect embedded in Streamlit
        st.components.v1.html(f"""
            <script>
            setTimeout(() => {{
                window.location.href = "{redirect_url}";
            }}, 1000);
            </script>
        """, height=0)

