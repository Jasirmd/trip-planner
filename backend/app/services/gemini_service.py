import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
from typing import Dict, Any
from app.models.trip import TripRequest  # Import the TripRequest model

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=self.api_key)
        # Adjust model name as needed
        self.model = genai.GenerativeModel('gemini-2.0-pro-exp-02-05')

    async def generate_trip_plan(self, trip_request: TripRequest) -> str:
        """
        Generate a detailed trip plan using Gemini.
        """
        try:
            prompt = self._create_prompt(trip_request)
            response = self.model.generate_content(prompt)
            if not response or not response.text:
                raise ValueError("Empty response from Gemini")
            return response.text
        except Exception as e:
            logger.error(f"Error generating trip plan: {str(e)}")
            raise

    def _create_prompt(self, trip_request: TripRequest) -> str:
        """
        Create a structured prompt for the AI to generate the travel plan.
        """
        selected_interests = [k for k, v in trip_request.interests.items() if v]
        duration = trip_request.duration or 7

        return f"""
        Create a detailed travel plan for a {duration}-day trip from {trip_request.fromLocation} 
        to {trip_request.destination}.
        This trip is for {trip_request.travelers} travelers in {trip_request.travelDate}.
        The travelers are interested in: {', '.join(selected_interests)}.

        Please provide the response in the following structured format:

        #OVERVIEW
        (An introduction about {trip_request.destination}, best time to visit, local culture, etc.)

        #ITINERARY
        (A day-by-day breakdown with morning, afternoon, and evening suggestions.)

        #PRACTICAL_INFO
        (Recommendations about where to stay, budget, local tips, etc.)
        """
