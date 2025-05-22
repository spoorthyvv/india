import streamlit as st
import pandas as pd
import plotly.express as px
import json
from streamlit_plotly_events import plotly_events

st.set_page_config(page_title="Interactive India Map", layout="wide")
st.title("🇮🇳 Interactive India Map (Click a State)")

@st.cache_data
def load_geojson():
    with open("india_state.geojson", "r", encoding="utf-8") as f:
        return json.load(f)

geojson = load_geojson()

# Extract state names
state_names = [feature["properties"]["NAME_1"] for feature in geojson["features"]]

# Dummy values for coloring
df = pd.DataFrame({
    "state": state_names,
    "value": [1] * len(state_names),
})

# Create choropleth figure
fig = px.choropleth(
    df,
    geojson=geojson,
    locations="state",
    featureidkey="properties.NAME_1",
    color="value",
    color_continuous_scale=[[0, "white"], [1, "red"]],
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0, "t":30, "l":0, "b":0}, coloraxis_showscale=False, title_text="Click on a state to redirect")

# Show the interactive map and get click events
selected_points = plotly_events(fig, click_event=True)

if selected_points:
    clicked_state = selected_points[0].get("location")
    if clicked_state:
        st.success(f"You clicked on: {clicked_state}")
        target_url = f"https://spoorthyvv.github.io/"
        st.markdown(f"Redirecting to: [{target_url}]({target_url})")

        # HTML to redirect after 1 second
        redirect_html = f"""
            <meta http-equiv="refresh" content="1; URL={target_url}">
            <script>
                setTimeout(function() {{
                    window.location.href = "{target_url}";
                }}, 1000);
            </script>
        """
        st.components.v1.html(redirect_html, height=0)

