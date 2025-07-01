import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def display_berth_map(rows=3, berths_per_row=4, taken_berths=None, key_prefix="train_berth"):
    taken_berths = taken_berths or []
    berth_labels = ["LB", "UB", "MB", "SL"][:berths_per_row]

    if key_prefix not in st.session_state:
        st.session_state[key_prefix] = []

    st.markdown("### Select Your Berths")

    cols = st.columns(berths_per_row)
    for row in range(1, rows + 1):
        for i, col in enumerate(cols):
            berth_id = f"{row}{berth_labels[i]}"
            disabled = berth_id in taken_berths
            selected = berth_id in st.session_state[key_prefix]

            if disabled:
                col.button(f"{berth_id} ❌", disabled=True)
            else:
                clicked = col.button(
                    f"{'✅ ' if selected else ''}{berth_id}",
                    key=f"{key_prefix}_{berth_id}"
                )
                if clicked:
                    if selected:
                        st.session_state[key_prefix].remove(berth_id)
                    else:
                        st.session_state[key_prefix].append(berth_id)

    return st.session_state[key_prefix]

# Page config – only once, at the top
st.set_page_config(page_title="Travel Planner & Flight Booking", page_icon="🌍", layout="centered")

# ---------- Load model ---
@st.cache_resource
def load_model():
    tok = AutoTokenizer.from_pretrained("google/flan-t5-base")
    mdl = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
    return tok, mdl

tokenizer, model = load_model()

# ---------- Tabs ----------
tab1, tab2 = st.tabs(["🗺 Travel Planner", "✈ Flight Booking"])

# ===== 1. TRAVEL PLANNER =====
with tab1:
    st.header("AI Travel Planner")
    st.markdown("Enter your trip preferences and get a perfect travel plan powered by AI!")

    with st.form("travel_form"):
        destination = st.text_input("Destination", placeholder="e.g., Paris")
        days = st.number_input("Trip Duration (days)", 1, 60, 5)
        month = st.text_input("Travel Month / Season", placeholder="e.g., April or Summer")
        budget = st.text_input("Total Budget", placeholder="e.g., $1000 or ₹50 000")
        travel_type = st.selectbox("Travel Type", ["Solo", "Couple", "Family", "Group", "Business"])
        accommodation = st.selectbox("Accommodation", ["Hostel", "Budget Hotel", "Airbnb", "Luxury Hotel"])
        interests = st.text_input("Your Interests", placeholder="e.g., food, history, beaches")
        pace = st.selectbox("Preferred Pace", ["Relaxed", "Balanced", "Packed"])
        special_requests = st.text_area("Special Requests (optional)", height=80)
        submit = st.form_submit_button("Generate Plan")

    if submit:
        if not destination or not month or not interests:
            st.warning("Please fill in Destination, Month/Season, and Interests.")
        else:
            with st.spinner("Generating your travel plan..."):
                prompt = (
                    f"Plan a {days}-day {travel_type.lower()} trip to {destination} in {month}. "
                    f"Budget: {budget or 'not specified'}. "
                    f"The traveler prefers a {pace.lower()} itinerary and will stay in a {accommodation}. "
                    f"Interests include {interests}. "
                )
                if special_requests.strip():
                    prompt += f"Special requests: {special_requests.strip()}. "
                prompt += (
                    "Provide a detailed, day‑by‑day itinerary with morning, afternoon, and evening plans. "
                    "Include food recommendations, accommodations, transport tips, and safety advice."
                )

                inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=500,
                    temperature=0.9,
                    top_p=0.95,
                    repetition_penalty=1.5,
                    no_repeat_ngram_size=3,
                )
                plan = tokenizer.decode(outputs[0], skip_special_tokens=True)

            st.subheader("Your AI‑Generated Travel Plan")
            st.markdown(plan.replace("\n", "\n\n"))

# ===== 2. FLIGHT BOOKING =====
with tab2:
    st.header("Flight Booking")

    st.sidebar.header("Search Flights")
    origin = st.sidebar.text_input("Origin (IATA)", "DEL")
    dest = st.sidebar.text_input("Destination (IATA)", "BOM")
    travel_date = st.sidebar.date_input(
        "Travel Date",
        min_value=datetime.today().date(),
        value=datetime.today().date() + timedelta(days=7),
    )
    passengers = st.sidebar.number_input("Passengers", 1, 9, 1)
    travel_class = st.sidebar.selectbox("Class", ["Economy", "Premium Economy", "Business", "First"])

    if st.sidebar.button("Search Flights"):
        airlines = ["IndiGo", "Air India", "SpiceJet", "Vistara", "Go First", "Akasa Air"]
        base_price_lookup = {"Economy": 3000, "Premium Economy": 6000, "Business": 12000, "First": 20000}
        tax_lookup = {"Economy": 0.05, "Premium Economy": 0.08, "Business": 0.12, "First": 0.18}
        service_charge_rate = 0.025

        base_price = base_price_lookup[travel_class]
        flights = []
        for i in range(6):
            dep = datetime.combine(travel_date, datetime.min.time()) + timedelta(hours=6 + 2 * i)
            arr = dep + timedelta(hours=random.randint(2, 3))
            price = base_price + random.randint(-500, 1500)
            tax = price * tax_lookup[travel_class]
            service = price * service_charge_rate
            total = price + tax + service

            flights.append(
                {
                    "Select": False,
                    "Flight": f"{airlines[i]} {random.randint(100, 999)}",
                    "Departure": dep.strftime("%H:%M"),
                    "Arrival": arr.strftime("%H:%M"),
                    "Duration": f"{(arr - dep).seconds // 3600} h {(arr - dep).seconds % 3600 // 60} m",
                    "Stops": "Non‑stop",
                    "Base Price": price,
                    "Tax": round(tax),
                    "Service": round(service),
                    "Total": round(total),
                }
            )

        df = pd.DataFrame(flights)
        st.subheader(f"Available flights {origin} → {dest} on {travel_date}")
        selected = st.data_editor(df, use_container_width=True, key="flight_table")
        booked = selected[selected["Select"]]

        if not booked.empty:
            st.success(f"{len(booked)} flight(s) selected. Proceed to booking below.")
            with st.form("booking_form"):
                st.header("Passenger Details")
                names = [st.text_input(f"Passenger {i+1} Name", key=f"name_{i}") for i in range(passengers)]
                contact = st.text_input("Contact Email")
                confirm = st.form_submit_button("Confirm Booking")

                if confirm:
                    if "" in names or contact == "":
                        st.error("Please fill all passenger names and contact email.")
                    else:
                        grand_total = booked["Total"].sum() * passengers
                        st.success("Booking confirmed! 🎉")
                        st.write("### Booking Summary")
                        st.write(booked[["Flight", "Departure", "Arrival", "Base Price", "Tax", "Service", "Total"]])
                        st.write(f"**Passengers:** {passengers}")
                        st.write(f"**Grand Total:** ₹{int(grand_total)}")
                        st.info("E‑tickets have been sent to your personal email.")
# ===== 3. TRAIN BOOKING =====
with tab3:
    st.header("Train Ticket Booking")

    st.sidebar.header("Search Trains")
    train_origin = st.sidebar.text_input("Origin Station Code", "NDLS")
    train_dest = st.sidebar.text_input("Destination Station Code", "BCT")
    train_date = st.sidebar.date_input(
        "Travel Date",
        min_value=datetime.today().date(),
        value=datetime.today().date() + timedelta(days=7),
        key="train_date"
    )
    train_passengers = st.sidebar.number_input("Passengers", 1, 6, 1, key="train_passengers")
    train_class = st.sidebar.selectbox("Class", ["Sleeper", "3A", "2A", "1A"], key="train_class")

    if st.sidebar.button("Search Trains"):
        train_names = ["Rajdhani Express", "Shatabdi Express", "Duronto Express", "Garib Rath", "Vande Bharat", "Intercity Express"]
        base_price_lookup = {"Sleeper": 500, "3A": 1000, "2A": 1500, "1A": 2500}
        tax_rate = 0.05
        service_fee = 0.02

        base_fare = base_price_lookup[train_class]
        trains = []

        for i in range(5):
            dep = datetime.combine(train_date, datetime.min.time()) + timedelta(hours=6 + 3 * i)
            arr = dep + timedelta(hours=random.randint(5, 12))
            fare = base_fare + random.randint(-100, 200)
            tax = fare * tax_rate
            service = fare * service_fee
            total = fare + tax + service

            trains.append({
                "Select": False,
                "Train": f"{train_names[i]} {random.randint(1000, 2999)}",
                "Departure": dep.strftime("%H:%M"),
                "Arrival": arr.strftime("%H:%M"),
                "Duration": f"{(arr - dep).seconds // 3600} h {(arr - dep).seconds % 3600 // 60} m",
                "Class": train_class,
                "Base Fare": fare,
                "Tax": round(tax),
                "Service Fee": round(service),
                "Total": round(total),
            })

        df_trains = pd.DataFrame(trains)
        st.subheader(f"Available trains {train_origin} → {train_dest} on {train_date}")
        selected_trains = st.data_editor(df_trains, use_container_width=True, key="train_editor")
        booked_trains = selected_trains[selected_trains["Select"]]

        if not booked_trains.empty:
    st.success(f"{len(booked_trains)} train(s) selected. Enter passenger details below.")
    with st.form("train_booking_form"):
        st.header("Passenger Details")
        names = [st.text_input(f"Passenger {i+1} Name", key=f"train_name_{i}") for i in range(train_passengers)]
        contact = st.text_input("Contact Email", key="train_contact")

        # Display berth selection UI
        selected_berths = display_berth_map(rows=3, berths_per_row=4, key_prefix="train_berth")

        confirm = st.form_submit_button("Confirm Booking")

        if confirm:
            if "" in names or contact == "":
                st.error("Please fill all passenger names and contact email.")
            elif len(selected_berths) < train_passengers:
                st.error(f"Please select at least {train_passengers} berths.")
            else:
                grand_total = booked_trains["Total"].sum() * train_passengers
                st.success("Train booking confirmed! 🚆")
                st.write("### Booking Summary")
                st.write(booked_trains[["Train", "Departure", "Arrival", "Class", "Base Fare", "Tax", "Service Fee", "Total"]])
                st.write(f"**Passengers:** {train_passengers}")
                st.write(f"**Grand Total:** ₹{int(grand_total):,}")
                for i in range(train_passengers):
                    st.write(f"**Passenger {i+1}:** {names[i]} — **Berth:** {selected_berths[i]}")
                st.info("Tickets have been sent to your personal email.")
