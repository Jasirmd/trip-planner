# AI Travel Planner

**AI Travel Planner** is a web application that helps you plan your trips with the help of artificial intelligence. It takes in your travel details like your departure city, destination, travel date, number of travelers, and interests. Then, it creates a detailed trip plan with an itinerary, hotel options, flight suggestions, and a map showing the destination.

---

## How It Works

1. **User Input**  
   - On the website, you fill out a form with your travel details (where you're leaving from, where you want to go, travel date, how many people are traveling, and your interests such as food, culture, adventure, etc.).

2. **Backend Processing**  
   - The frontend sends your travel information to a backend server built using FastAPI.
   - The backend uses the Gemini API (an AI service) to generate a trip plan.
   - It also calls the Google Maps API to fetch extra details like hotel information, flight data, and map coordinates.

3. **Trip Plan Display**  
   - The backend sends a structured response back to the frontend.
   - The frontend, built with Streamlit, displays the trip plan in three parts:
     - **Overview:** With a map and photos of the destination.
     - **Itinerary:** A day-by-day breakdown of activities.
     - **Travel Details:** Information about flights and accommodations.
   - There is also an option to "Generate Another Trip" if you want to plan a new trip.

---

## Technologies Used

- **Python 3** – The programming language used for both backend and frontend.
- **FastAPI** – A web framework used to build the backend API.
- **Uvicorn** – An ASGI server used to run the FastAPI application.
- **Streamlit** – A framework used to build the interactive frontend of the web app.
- **Google Maps API** – Used to fetch maps, hotel details, and other location-based data.
- **Gemini API** – An AI service that generates the trip plan based on your input.

---

## How to Run the Project Locally

### 1. Clone the Repository

Clone the project from GitHub:

```
git clone https://github.com/Jasirmd/trip-planner.git
cd trip-planner
```

### 2. Create a Virtual Environment and Install Dependencies

For the Backend:

```
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
pip install -r requirements.txt
```

For the Frontend:
Open a new terminal window, then:

```
cd frontend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

```
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```
Make sure these keys are valid so that the backend can call the external APIs.

### 4. Run the Backend Server

From the backend folder, start the FastAPI server using Uvicorn:

```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Your server should start and be available at http://localhost:8000.

### 5. Run the Frontend

In another terminal (from the frontend folder), start the Streamlit app:

```
streamlit run app.py
```
This will open a new browser window or tab with your AI Travel Planner interface.

### Troubleshooting

## CORS Issues:

If your frontend cannot access the backend, check the CORS settings in your FastAPI app. The code includes CORS middleware that allows all origins:

```
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 502/405 Errors:
These errors usually mean the backend is not reachable or you are using the wrong HTTP method. Make sure your frontend is sending a POST request to the /api/plan-trip endpoint.

## Environment Variables:
Ensure that your API keys are correctly set in your environment so that the APIs (Gemini and Google Maps) work as expected.

## Summary

AI Travel Planner helps you plan trips by generating a detailed itinerary and showing additional travel information like hotels and flights. The backend uses FastAPI to process data and call external APIs, while the frontend uses Streamlit to create a user-friendly interface. You can run this project locally by setting up virtual environments, installing dependencies, setting environment variables, and starting both the backend and frontend.

Happy planning and safe travels!
