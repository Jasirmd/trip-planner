import googlemaps
import os
from dotenv import load_dotenv
import logging
from typing import Dict, List, Any
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

class GoogleMapsService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY not found in environment variables")
        self.client = googlemaps.Client(key=self.api_key)
        logger.info("Google Maps Service initialized")

    async def get_coordinates(self, location: str) -> Dict[str, float]:
        """
        Get coordinates for a location using Google Maps Geocoding API.
        """
        try:
            logger.info(f"Getting coordinates for {location}")
            geocode_result = self.client.geocode(location)
            if geocode_result and len(geocode_result) > 0:
                loc = geocode_result[0]['geometry']['location']
                return {
                    "lat": loc['lat'],
                    "lng": loc['lng']
                }
            else:
                logger.warning(f"No coordinates found for {location}")
                return {"lat": 0, "lng": 0}
        except Exception as e:
            logger.error(f"Error getting coordinates for {location}: {str(e)}")
            return {"lat": 0, "lng": 0}

    async def get_hotels(self, location: str) -> Dict[str, Any]:
        """
        Get hotel information using Google Places API.
        """
        try:
            logger.info(f"Getting hotels in {location}")
            coordinates = await self.get_coordinates(location)
            places_result = self.client.places_nearby(
                location=coordinates,
                radius=5000,  # 5km radius
                type='lodging',
                keyword='hotel'
            )
            hotels = []
            for place in places_result.get('results', [])[:8]:
                try:
                    details = self.client.place(
                        place['place_id'],
                        fields=[
                            'name', 'rating', 'formatted_address',
                            'price_level', 'website', 'formatted_phone_number',
                            'reviews', 'opening_hours', 'photo'
                        ]
                    )['result']
                    # Collect up to 3 photos
                    photo_refs = place.get('photos', [])
                    photos = []
                    for photo in photo_refs[:3]:
                        if 'photo_reference' in photo:
                            photo_url = (
                                f"https://maps.googleapis.com/maps/api/place/photo"
                                f"?maxwidth=800&photoreference={photo['photo_reference']}"
                                f"&key={self.api_key}"
                            )
                            photos.append(photo_url)

                    hotels.append({
                        "name": details.get('name', 'Unknown Hotel'),
                        "rating": details.get('rating', 'N/A'),
                        "address": details.get('formatted_address', 'Address not available'),
                        "price_level": "€" * (details.get('price_level', 1) if details.get('price_level') else 1),
                        "phone": details.get('formatted_phone_number', 'Phone not available'),
                        "website": details.get('website', ''),
                        "photos": photos,
                        "reviews": details.get('reviews', [])[:3],
                        "opening_hours": details.get('opening_hours', {}).get('weekday_text', [])
                    })
                except Exception as e:
                    logger.error(f"Error processing hotel: {str(e)}")
                    continue
            return {"hotels": hotels}
        except Exception as e:
            logger.error(f"Error getting hotels: {str(e)}")
            return {"hotels": []}

    async def get_places_photos(self, location: str) -> List[str]:
        """
        Get photos of popular places in the destination (tourist attractions).
        """
        try:
            logger.info(f"Fetching photos for popular places in {location}")
            coordinates = await self.get_coordinates(location)
            places_result = self.client.places_nearby(
                location=coordinates,
                radius=5000,
                type='tourist_attraction',
                keyword='landmarks'
            )
            photos = []
            if 'results' in places_result:
                # Go through up to 15 places
                for place in places_result['results'][:15]:
                    # Each place might have a 'photos' key
                    place_photos = place.get('photos', [])
                    if len(place_photos) > 0:
                        photo_ref = place_photos[0].get('photo_reference')
                        if photo_ref:
                            photo_url = (
                                f"https://maps.googleapis.com/maps/api/place/photo?"
                                f"maxwidth=800&photoreference={photo_ref}"
                                f"&key={self.api_key}"
                            )
                            photos.append(photo_url)

            if not photos:
                logger.warning(f"No photos found for {location}")
            else:
                logger.info(f"Fetched {len(photos)} photo(s) for {location}")

            return photos

        except Exception as e:
            logger.error(f"Error getting photos: {str(e)}")
            return []

    def get_realistic_flights(self, from_location: str, to_location: str) -> Dict[str, Any]:
        """
        Generate simplistic flight data for demonstration. In production,
        you'd integrate with a real flight API or database.
        """
        try:
            # Predefined route info
            route_info = {
                ('Bengaluru', 'Delhi'): {
                    'duration': '2h 45m',
                    'airlines': ['Air India', 'IndiGo'],
                    'base_price': 350
                },
                ('Delhi', 'Mumbai'): {
                    'duration': '2h 15m',
                    'airlines': ['IndiGo', 'Vistara'],
                    'base_price': 300
                },
                # Add more routes as needed
            }

            flights = []
            route = (from_location, to_location)
            route_data = route_info.get(route, {
                'duration': '3h 00m',
                'airlines': ['Major Airline', 'Budget Carrier'],
                'base_price': 400
            })

            # Morning flight
            flights.append({
                "airline": route_data['airlines'][0],
                "flight_number": f"{route_data['airlines'][0][:2]}123",
                "departure": "08:30 AM",
                "arrival": "11:15 AM",
                "duration": route_data['duration'],
                "price": f"${route_data['base_price']}",
                "stops": "Non-stop",
                "aircraft": "Airbus A320"
            })

            # Evening flight
            flights.append({
                "airline": route_data['airlines'][1],
                "flight_number": f"{route_data['airlines'][1][:2]}456",
                "departure": "16:45 PM",
                "arrival": "19:30 PM",
                "duration": route_data['duration'],
                "price": f"${route_data['base_price'] - 50}",
                "stops": "Non-stop",
                "aircraft": "Boeing 737"
            })

            return {"available_flights": flights}
        except Exception as e:
            logger.error(f"Error generating flight data: {str(e)}")
            return {"available_flights": []}
