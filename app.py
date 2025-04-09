# app.py
import streamlit as st
from agent import run_agent

# Session State Init for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar Configuration
with st.sidebar:
    st.title("✈️ TravelGenie AI")

    with st.container():
        st.markdown("#### Travel Preferences")
        start_city = st.text_input("Start City", placeholder="Enter your starting city")
        destinations = st.text_input(
            "Destinations", placeholder="Enter your destination(s)"
        )
        travel_dates = st.date_input("Travel Dates", [], format="MM/DD/YYYY")
        interests = st.multiselect(
            "Interests",
            [
                "Museums",
                "Food",
                "Culture",
                "Adventure",
                "Relaxation",
                "Business",
                "Nature",
            ],
            default=[],
        )

        st.markdown("#### Travelers & Budget")
        col1, col2 = st.columns(2)
        with col1:
            adult_travelers = st.number_input("Adults", min_value=1, value=2)
        with col2:
            child_travelers = st.number_input("Kids", min_value=0, value=0)

        budget = st.number_input("Budget ($)", min_value=0, value=2000, step=100)
        special_requests = st.text_area(
            "Special Requests",
            height=60,
            placeholder="Vegetarian meals, wheelchair accessible",
        )

        if st.button("Generate Travel Plan"):
            if not start_city or not destinations or not travel_dates:
                st.warning(
                    "Please fill in all required fields to generate a travel plan."
                )
            else:
                pre_filled_prompt = f"""Plan a trip with the following details:
                - Starting from: {start_city}
                - Destinations: {destinations}
                - Travel dates: {" - ".join([date.strftime("%m/%d/%Y") for date in travel_dates])}
                - Interests: {", ".join(interests) if interests else "None"}
                - Budget: ${budget}
                - Number of travelers: {adult_travelers} Adults, {child_travelers} Kids
                - Special requests: {special_requests if special_requests else "None"}

                Please provide a detailed travel plan including:
                1. Recommended itinerary
                2. Transportation options
                3. Accommodation suggestions
                4. Activities and attractions
                5. Estimated costs
                6. Any special considerations based on the provided preferences
                """
                st.session_state.chat_history.append(
                    {
                        "role": "user",
                        "content": f"Generate a travel plan with the following details:\n"
                        f"- Starting city: {start_city}\n"
                        f"- Destination(s): {destinations}\n"
                        f"- Travel dates: {travel_dates[0].strftime('%m/%d/%Y')} to {travel_dates[-1].strftime('%m/%d/%Y')}\n"
                        f"- Travelers: {adult_travelers} adult(s) and {child_travelers} kid(s)\n"
                        f"- Budget: ${budget}\n"
                        f"- Interests: {', '.join(interests) if interests else 'None'}.",
                    }
                )
                with st.spinner("Generating your travel plan..."):
                    try:
                        response = run_agent(pre_filled_prompt)
                        st.session_state.chat_history.append(
                            {"role": "assistant", "content": response}
                        )
                    except Exception as e:
                        st.session_state.chat_history.append(
                            {
                                "role": "assistant",
                                "content": f"❌ Error generating plan: {e}",
                            }
                        )


# Chat Display
st.title("💬 Chat with TravelGenie AI")

for message in st.session_state.chat_history:
    with st.chat_message(
        message["role"], avatar="🧞" if message["role"] == "assistant" else "👤"
    ):
        st.markdown(message["content"])

# User Input Field
prompt = st.chat_input("Where would you like to travel?")

if prompt:
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar="🧞"):
        with st.spinner("TravelGenie is thinking..."):
            try:
                response = run_agent(prompt)
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": response}
                )
                st.markdown(response)
            except Exception as e:
                error_msg = f"❌ Error: {e}"
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": error_msg}
                )
                st.error(error_msg)
