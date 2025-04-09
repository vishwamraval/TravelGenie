# app.py
import streamlit as st
import random
from agent import run_agent

st.set_page_config(page_title="TravelGenie AI", page_icon="✈️")
st.title("✈️ TravelGenie AI")
st.write("Ask me to plan your trip, find flights, or suggest destinations!")

st.sidebar.title("User Input")
st.sidebar.write("Enter your travel preferences below:")

start_city = st.sidebar.text_input("Start City", placeholder="Enter your starting city")
destinations = st.sidebar.text_input("Destinations", placeholder="Enter your destination(s)")
travel_dates = st.sidebar.date_input("Travel Dates", [])
interests = st.sidebar.multiselect("Interests", ["Museums", "Food", "Culture", "Adventure", "Relaxation", "Business"])
st.sidebar.markdown("Budget and Travelers")
budget = st.sidebar.number_input("Budget ($)", min_value=0, value=2000, step=100)
adult_travelers = st.sidebar.number_input("Number of Adults", min_value=1, value=2, step=1)
child_travelers = st.sidebar.number_input("Number of Kids (Under 12)", min_value=0, value=2, step=1)
special_requests = st.sidebar.text_area("Special Requests", placeholder="Vegetarian meals, wheelchair accessible")

placeholders = [
    "Where should I go for a beach vacation?",
    "What are the best restaurants in Paris?",
    "Can you suggest a family-friendly itinerary for New York?",
    "What are some must-see attractions in Tokyo?",
    "Help me plan a weekend getaway to the mountains.",
    "What are the top things to do in Rome?",
    "What are the best travel tips for solo travelers?",
    "Can you recommend a budget-friendly destination in Europe?",
]

user_query = st.text_input(
    "Ask TravelGenie:", 
    placeholder=random.choice(placeholders), 
    key="bottom_query"
)
if st.button("Send"):
    if user_query:
        st.write("### TravelGenie Response")
        response = run_agent(user_query)
        st.write(f"**Response:** {response}")
    else:
        st.warning("Please enter a query to get a response.")

# if the user chooses to send via the presets, generate a prompt and send it to the agent

pre_defined_prompt = f"""Plan a trip with the following details:
- Starting from: {start_city}
- Destinations: {destinations}
- Travel dates: {travel_dates}
- Interests: {', '.join(interests) if interests else 'None'}
- Budget: ${budget}
- Number of travelers: {adult_travelers} Adults, and {child_travelers} Kids
- Special requests: {special_requests}

Please provide a detailed travel plan including:
1. Recommended itinerary
2. Transportation options
3. Accommodation suggestions
4. Activities and attractions
5. Estimated costs
6. Any special considerations based on the provided preferences"""

if st.sidebar.button("Generate Travel Plan"):
    st.write("### Your Travel Plan Request:")
    st.text_area("Generated Prompt:", pre_defined_prompt, height=300)
    st.write("### TravelGenie Response")
    response = run_agent(pre_defined_prompt)
    st.write(f"**Response:** {response}")