from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.trip import TripRequest
from app.services.gemini_service import GeminiService
from app.services.google_maps_service import GoogleMapsService
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Trip Planner API",
    description="AI-powered trip planning API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
gemini_service = GeminiService()
google_maps_service = GoogleMapsService()
logger.info("Services initialized successfully")


@app.get("/")
def read_root():
    return {"message": "Trip Planner API is running"}


@app.post("/api/plan-trip")
async def plan_trip(trip_request: TripRequest):
    """
    Generate a trip plan using the Gemini LLM, fetch hotels, flights,
    and photos from Google Maps, then return all data in a structured response.
    """
    logger.info(f"Received trip request: {trip_request}")
    try:
        # 1) Generate trip plan text via Gemini
        logger.info("Generating trip plan with Gemini")
        response_text = await gemini_service.generate_trip_plan(trip_request)
        logger.info(f"Received AI response: {response_text[:200]}...")

        # 2) Parse AI response into sections
        sections = response_text.split("#")
        overview = next((s for s in sections if "OVERVIEW" in s), "").replace("OVERVIEW", "").strip()
        itinerary = next((s for s in sections if "ITINERARY" in s), "").replace("ITINERARY", "").strip()
        practical_info = next((s for s in sections if "PRACTICAL_INFO" in s), "").replace("PRACTICAL_INFO", "").strip()

        # 3) Fetch additional details
        logger.info("Fetching additional trip details")
        coordinates = await google_maps_service.get_coordinates(trip_request.destination)
        flights_info = google_maps_service.get_realistic_flights(trip_request.fromLocation, trip_request.destination)
        hotels_info = await google_maps_service.get_hotels(trip_request.destination)
        photos = await google_maps_service.get_places_photos(trip_request.destination)

        # Provide a fallback if no photos found
        if not photos:
            logger.warning("No photos retrieved from Google Maps API")
            photos = ["default_photo_url"]  # Temporary fallback

        # 4) Construct final response
        result = {
            "tripPlan": {
                "overview": overview,
                "itinerary": itinerary,
                "practicalInfo": practical_info
            },
            "flightsInfo": flights_info,
            "accommodations": hotels_info,
            "map_data": {
                "latitude": [float(coordinates["lat"])],
                "longitude": [float(coordinates["lng"])]
            },
            "photos": photos
        }
        logger.info(f"Final trip response: {result}")
        return result

    except Exception as e:
        logger.error(f"Error generating trip plan: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """
    Simple health check endpoint to verify connectivity with external services.
    """
    try:
        services_status = {
            "gemini_service": bool(gemini_service),
            "google_maps_service": bool(google_maps_service)
        }
        test_coordinates = await google_maps_service.get_coordinates("London")
        api_status = bool(test_coordinates.get("lat"))

        return {
            "status": "healthy" if all(services_status.values()) and api_status else "degraded",
            "services": services_status,
            "api_status": "operational" if api_status else "error",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )


@app.get("/api/supported-locations")
async def get_supported_locations():
    """
    Return a list of popular destinations and their coordinates.
    """
    try:
        popular_destinations = ["London", "Paris", "New York", "Tokyo", "Dubai"]
        locations = {}
        for city in popular_destinations:
            coords = await google_maps_service.get_coordinates(city)
            locations[city] = coords
        return {"supported_locations": locations, "total_count": len(locations)}
    except Exception as e:
        logger.error(f"Error getting supported locations: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch supported locations")
