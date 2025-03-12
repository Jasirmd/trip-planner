import streamlit as st
from datetime import datetime, timedelta

def render_trip_form():
    """
    Render the trip planning form and return:
      - (bool) submitted: whether user submitted
      - (dict) form_data: user input data
    """
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}

    with st.form("trip_planner_form"):
        st.markdown("#### Plan Your Adventure", unsafe_allow_html=True)

        # First row: From, To, Travel Date
        col1, col2, col3 = st.columns(3)
        with col1:
            from_location = st.text_input(
                "From",
                value=st.session_state.form_data.get("fromLocation", ""),
                key="from_input"
            )
        with col2:
            destination = st.text_input(
                "To",
                value=st.session_state.form_data.get("destination", ""),
                key="destination_input"
            )
        with col3:
            min_date = datetime.now().date()
            max_date = min_date + timedelta(days=365)
            # Check if there's a stored travel date, and convert it if needed
            default_travel_date = st.session_state.form_data.get("travelDate")
            if default_travel_date:
                try:
                    default_travel_date = datetime.strptime(default_travel_date, "%Y-%m").date()
                except Exception:
                    default_travel_date = min_date + timedelta(days=30)
            else:
                default_travel_date = min_date + timedelta(days=30)
            travel_date = st.date_input(
                "Travel Date",
                min_value=min_date,
                max_value=max_date,
                value=default_travel_date,
                key="date_input"
            )

        # Second row: Travelers, Duration
        col4, col5 = st.columns(2)
        with col4:
            travelers = st.number_input(
                "Travelers",
                min_value=1,
                max_value=10,
                value=st.session_state.form_data.get("travelers", 2),
                key="travelers_input"
            )
        with col5:
            trip_duration = st.slider(
                "Duration (days)",
                1, 30,
                value=st.session_state.form_data.get("duration", 7),
                key="duration_slider"
            )

        # Interests
        st.markdown("#### What interests you?")
        interests_col = st.columns(3)
        with interests_col[0]:
            historical = st.checkbox(
                "Historical",
                value=st.session_state.form_data.get("interests", {}).get("historical", False),
                key="historical_checkbox"
            )
            nature = st.checkbox(
                "Nature & Parks",
                value=st.session_state.form_data.get("interests", {}).get("nature", False),
                key="nature_checkbox"
            )
        with interests_col[1]:
            cultural = st.checkbox(
                "Cultural",
                value=st.session_state.form_data.get("interests", {}).get("cultural", False),
                key="cultural_checkbox"
            )
            shopping = st.checkbox(
                "Shopping",
                value=st.session_state.form_data.get("interests", {}).get("shopping", False),
                key="shopping_checkbox"
            )
        with interests_col[2]:
            food = st.checkbox(
                "Food & Cuisine",
                value=st.session_state.form_data.get("interests", {}).get("food", False),
                key="food_checkbox"
            )
            adventure = st.checkbox(
                "Adventure",
                value=st.session_state.form_data.get("interests", {}).get("adventure", False),
                key="adventure_checkbox"
            )

        submitted = st.form_submit_button("Plan My Trip")

        if submitted:
            st.session_state.form_data = {
                "fromLocation": from_location,
                "destination": destination,
                "travelers": travelers,
                "travelDate": travel_date.strftime("%Y-%m"),
                "duration": trip_duration,
                "interests": {
                    "historical": historical,
                    "nature": nature,
                    "cultural": cultural,
                    "shopping": shopping,
                    "food": food,
                    "adventure": adventure
                }
            }
            return True, st.session_state.form_data

    return False, None
