import os
import streamlit as st
import requests
from components.header import render_header
from components.form import render_trip_form
from components.results import TripResults

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
css_path = os.path.join(os.path.dirname(__file__), "assets", "styles", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("Custom CSS file not found. Using default Streamlit styles.")

def main():
    # 1) Render the hero header
    render_header()

    # 2) Render the trip form
    submitted, form_data = render_trip_form()

    # 3) If user submitted the form, call the API and show results
    if submitted and form_data:
        if not form_data["fromLocation"] or not form_data["destination"]:
            st.error("Please enter both departure and destination locations.")
            return

        with st.spinner("Planning your trip..."):
            try:
                response = requests.post(
                    "http://localhost:8000/api/plan-trip",
                    json=form_data,
                    headers={"Content-Type": "application/json"}
                )
                if response.status_code == 200:
                    response_data = response.json()
                    trip_results = TripResults(response_data)
                    trip_results.render()
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
