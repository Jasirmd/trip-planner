import streamlit as st
import logging
import pandas as pd
import requests
from io import BytesIO
from PIL import Image
import os

logger = logging.getLogger(__name__)

class TripResults:
    def __init__(self, response_data):
        self.data = response_data
        self.trip_plan = response_data.get("tripPlan", {})
        self.flights = response_data.get("flightsInfo", {})
        self.hotels = response_data.get("accommodations", {})
        self.map_data = response_data.get("map_data", {})
        self.photos = response_data.get("photos", [])

    def render(self):
        # Render tabs for Overview, Itinerary, Practical Info, Travel Details
        tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Itinerary", "Practical Info", "Travel Details"])
        with tab1:
            self._render_overview_tab()
        with tab2:
            self._render_itinerary_tab()
        with tab3:
            self._render_practical_info_tab()
        with tab4:
            self._render_travel_details_tab()

        st.divider()

        # Single column at the bottom left: "Generate Another Trip" button
        col = st.columns([1])[0]
        with col:
            if st.button("Generate Another Trip", key="generate_another_trip"):
                # Clear the trip-related session state
                for key in ["form_data", "pdf_bytes"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.experimental_rerun()

    def _render_overview_tab(self):
        st.markdown("<div class='section-header'>Overview</div>", unsafe_allow_html=True)
        overview = self.trip_plan.get("overview", "")
        if overview:
            st.markdown(overview, unsafe_allow_html=True)
        else:
            st.info("No overview available.")
        self._render_gallery()
        if self.map_data:
            try:
                lat = self.map_data.get("latitude", [])[0]
                lng = self.map_data.get("longitude", [])[0]
                if lat and lng:
                    map_df = pd.DataFrame({"lat": [lat], "lon": [lng]})
                    st.markdown("##### Map")
                    st.map(map_df)
            except Exception as e:
                st.warning(f"Could not display map: {str(e)}")

    def _render_itinerary_tab(self):
        st.markdown("<div class='section-header'>Itinerary</div>", unsafe_allow_html=True)
        itinerary_text = self.trip_plan.get("itinerary", "")
        if not itinerary_text:
            st.info("No itinerary available.")
            return
        days = itinerary_text.split("Day ")
        for i, day_content in enumerate(days):
            if i == 0 or not day_content.strip():
                continue
            day_number = day_content.split(":")[0]
            with st.expander(f"Day {day_number.strip()}", expanded=False):
                st.markdown(f"**Day {day_number.strip()}:** " + day_content[len(day_number):], unsafe_allow_html=True)

    def _render_practical_info_tab(self):
        st.markdown("<div class='section-header'>Practical Info</div>", unsafe_allow_html=True)
        practical_info = self.trip_plan.get("practicalInfo", "")
        if practical_info:
            st.markdown(practical_info, unsafe_allow_html=True)
        else:
            st.info("No practical info available.")

    def _render_travel_details_tab(self):
        st.markdown("<div class='section-header'>Flight Options</div>", unsafe_allow_html=True)
        flight_list = self.flights.get("available_flights", [])
        if flight_list:
            for flight in flight_list:
                st.markdown(
                    f"**{flight.get('airline', '')}** - {flight.get('flight_number', '')}  |  {flight.get('price', '')}"
                )
                st.write(
                    f"**Departure:** {flight.get('departure', 'N/A')}  ➡️  **Arrival:** {flight.get('arrival', 'N/A')}"
                )
                st.write(f"**Duration:** {flight.get('duration', 'N/A')}")
                st.write("---")
        else:
            st.info("No flight information available.")

        st.markdown("<div class='section-header'>Accommodation Options</div>", unsafe_allow_html=True)
        hotel_list = self.hotels.get("hotels", [])
        if hotel_list:
            for hotel in hotel_list:
                st.markdown(
                    f"**{hotel.get('name', 'Unknown')}**  ({'⭐' * int(float(hotel.get('rating', 0)))})"
                )
                st.write(f"**Address:** {hotel.get('address', 'N/A')}")
                st.write(f"**Price Level:** {hotel.get('price_level', 'N/A')}")
                if hotel.get('phone'):
                    st.write(f"**Phone:** {hotel['phone']}")
                if hotel.get('website'):
                    st.write(f"**Website:** [{hotel['website']}]({hotel['website']})")
                st.write("---")
        else:
            st.info("No hotel information available.")

    def _render_gallery(self):
        if not self.photos:
            return
        st.markdown("##### Destination Gallery")
        cols = st.columns(3)
        for i, photo_url in enumerate(self.photos):
            with cols[i % 3]:
                self._display_photo(photo_url)

    def _display_photo(self, url: str):
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                img = Image.open(BytesIO(resp.content))
                st.image(img, use_column_width=True)
            else:
                self._show_fallback()
        except Exception:
            self._show_fallback()

    def _show_fallback(self):
        fallback_path = "./assets/images/fallback-image.jpg"
        if os.path.exists(fallback_path):
            st.image(fallback_path, use_column_width=True, caption="Photo Unavailable")
        else:
            st.warning("Photo unavailable (no fallback image found).")
