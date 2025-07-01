import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import string
import re
import json

# Page Configuration
st.set_page_config(
    page_title="Enhanced Travel Planner & Booking", 
    page_icon="🌍", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.booking-card {
    border: 1px solid #e0e0e0;
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.success-card {
    border: 2px solid #4CAF50;
    border-radius: 15px;
    padding: 20px;
    background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
    margin: 15px 0;
}
.price-highlight {
    font-size: 24px;
    font-weight: bold;
    color: #2E8B57;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    padding-left: 20px;
    padding-right: 20px;
}
</style>
""", unsafe_allow_html=True)

# Validation Functions
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    pattern = r'^[+]?[\d\s\-\(\)]{10,15}$'
    return re.match(pattern, phone) is not None

def validate_iata_code(code):
    return len(code) == 3 and code.isalpha()

# Enhanced Data
@st.cache_data
def load_enhanced_food_recommendations():
    return {
        "delhi": [
            ("Chole Bhature", "Spicy chickpeas with fluffy fried bread", "₹150-200"),
            ("Butter Chicken", "Creamy, rich chicken curry", "₹300-400"),
            ("Paranthas", "Stuffed flatbreads from Chandni Chowk", "₹100-150"),
            ("Kebabs", "Grilled meat skewers from Old Delhi", "₹200-300")
        ],
        "mumbai": [
            ("Vada Pav", "Mumbai's iconic spicy potato burger", "₹15-25"),
            ("Pav Bhaji", "Mashed spicy vegetables with buns", "₹80-120"),
            ("Bhel Puri", "Crunchy street snack mix", "₹40-60"),
            ("Misal Pav", "Spicy sprouted lentil curry", "₹60-100")
        ],
        "chennai": [
            ("Dosa", "Crispy fermented crepe with chutneys", "₹50-100"),
            ("Chettinad Chicken", "Spicy and aromatic chicken curry", "₹250-350"),
            ("Idli Sambar", "Steamed rice cakes with lentil soup", "₹40-80"),
            ("Filter Coffee", "Traditional South Indian coffee", "₹20-40")
        ],
        "hyderabad": [
            ("Hyderabadi Biryani", "Fragrant rice with tender meat", "₹300-500"),
            ("Haleem", "Slow-cooked lentils and meat stew", "₹200-300"),
            ("Nihari", "Rich meat curry traditionally eaten for breakfast", "₹250-400"),
            ("Double Ka Meetha", "Bread pudding dessert", "₹100-150")
        ],
        "goa": [
            ("Fish Curry Rice", "Coconut-based spicy fish curry", "₹200-300"),
            ("Bebinca", "Traditional layered dessert", "₹150-200"),
            ("Pork Vindaloo", "Spicy Portuguese-influenced curry", "₹300-400"),
            ("Feni", "Local cashew or palm spirit", "₹100-200")
        ],
        "kerala": [
            ("Appam & Stew", "Fermented pancakes with vegetable curry", "₹120-180"),
            ("Puttu", "Steamed rice cake with coconut", "₹80-120"),
            ("Fish Molee", "Mild coconut fish curry", "₹250-350"),
            ("Payasam", "Sweet rice pudding dessert", "₹80-120")
        ]
    }

@st.cache_data
def load_enhanced_cuisine_recommendations():
    return {
        "Mediterranean": [
            ("Greek Moussaka", "Layered eggplant, potatoes, and meat", "₹400-600"),
            ("Italian Risotto", "Creamy rice with mushrooms or seafood", "₹350-500"),
            ("Spanish Paella", "Saffron rice with seafood and meat", "₹500-700"),
            ("Turkish Kebab", "Grilled meat with yogurt sauce", "₹300-450")
        ],
        "East Asian": [
            ("Pad Thai", "Stir-fried noodles with tamarind sauce", "₹250-350"),
            ("Sushi Platter", "Fresh raw fish with seasoned rice", "₹800-1200"),
            ("Dim Sum", "Steamed dumplings and small plates", "₹400-600"),
            ("Ramen", "Japanese noodle soup", "₹300-500")
        ],
        "Latin American": [
            ("Tacos al Pastor", "Pork tacos with pineapple", "₹200-300"),
            ("Feijoada", "Brazilian black bean stew", "₹350-500"),
            ("Ceviche", "Raw fish marinated in citrus", "₹400-600"),
            ("Empanadas", "Stuffed pastries", "₹150-250")
        ],
        "Middle Eastern": [
            ("Hummus & Pita", "Chickpea dip with flatbread", "₹200-300"),
            ("Shawarma", "Grilled meat wrap", "₹250-350"),
            ("Falafel", "Fried chickpea balls", "₹180-280"),
            ("Baklava", "Sweet pastry with nuts and honey", "₹150-250")
        ]
    }

# Load enhanced data
FOOD_RECS = load_enhanced_food_recommendations()
CUISINE_RECS = load_enhanced_cuisine_recommendations()

# Initialize session state
if 'booking_history' not in st.session_state:
    st.session_state.booking_history = []
if 'saved_preferences' not in st.session_state:
    st.session_state.saved_preferences = {}

def generate_booking_id(length=8):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def save_booking(booking_details):
    """Save booking to history"""
    st.session_state.booking_history.append({
        'id': booking_details['id'],
        'type': booking_details['type'],
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'details': booking_details
    })

def get_weather_placeholder(destination):
    """Placeholder weather function"""
    weather_options = [
        {"temp": "25°C", "condition": "☀️ Sunny", "humidity": "60%"},
        {"temp": "22°C", "condition": "⛅ Partly Cloudy", "humidity": "65%"},
        {"temp": "28°C", "condition": "🌧️ Light Rain", "humidity": "80%"},
        {"temp": "30°C", "condition": "🌤️ Clear", "humidity": "55%"}
    ]
    return random.choice(weather_options)

def display_enhanced_berth_map(rows=3, berths_per_row=4, taken_berths=None, key_prefix="train_berth"):
    taken_berths = taken_berths or []
    berth_labels = ["LB", "UB", "MB", "SL"][:berths_per_row]
    if key_prefix not in st.session_state:
        st.session_state[key_prefix] = []

    st.markdown("### 🚂 Select Your Berths")
    st.markdown("**Legend:** LB=Lower Berth, UB=Upper Berth, MB=Middle Berth, SL=Side Lower")
    
    for row in range(1, rows + 1):
        cols = st.columns(berths_per_row)
        for i, col in enumerate(cols):
            berth_id = f"{row}{berth_labels[i]}"
            selected = berth_id in st.session_state[key_prefix]
            disabled = (
                berth_id in taken_berths or
                (not selected and len(st.session_state[key_prefix]) >= st.session_state.get("train_passengers", 6))
            )
            
            if berth_id in taken_berths:
                col.button(f"{berth_id} 🚫", disabled=True, help="Already booked")
            elif selected:
                if col.button(f"✅ {berth_id}", key=f"{key_prefix}_{berth_id}", help="Click to deselect"):
                    st.session_state[key_prefix].remove(berth_id)
            else:
                if not disabled:
                    if col.button(f"🪑 {berth_id}", key=f"{key_prefix}_{berth_id}", help="Click to select"):
                        st.session_state[key_prefix].append(berth_id)
                else:
                    col.button(f"{berth_id} ⚠️", disabled=True, help="Selection limit reached")
    
    return st.session_state[key_prefix]

def display_enhanced_flight_seat_map(rows=6, seats_per_row=6, taken_seats=None, key_prefix="flight_seat"):
    taken_seats = taken_seats or []
    seat_labels = ["A", "B", "C", "D", "E", "F"][:seats_per_row]
    if key_prefix not in st.session_state:
        st.session_state[key_prefix] = []

    st.markdown("### ✈️ Select Your Seats")
    st.markdown("**Legend:** A,F=Window | B,E=Middle | C,D=Aisle")
    
    for row in range(1, rows + 1):
        cols = st.columns(seats_per_row)
        for i, col in enumerate(cols):
            seat_id = f"{row}{seat_labels[i]}"
            selected = seat_id in st.session_state[key_prefix]
            disabled = (
                seat_id in taken_seats or
                (not selected and len(st.session_state[key_prefix]) >= st.session_state.get("passengers", 9))
            )
            
            # Determine seat type for icon
            if seat_labels[i] in ['A', 'F']:
                seat_icon = "🪟"  # Window
            elif seat_labels[i] in ['C', 'D']:
                seat_icon = "🚶"  # Aisle
            else:
                seat_icon = "💺"  # Middle
            
            if seat_id in taken_seats:
                col.button(f"{seat_id} 🚫", disabled=True, help="Seat taken")
            elif selected:
                if col.button(f"✅ {seat_id}", key=f"{key_prefix}_{seat_id}", help="Click to deselect"):
                    st.session_state[key_prefix].remove(seat_id)
            else:
                if not disabled:
                    if col.button(f"{seat_icon} {seat_id}", key=f"{key_prefix}_{seat_id}", help="Click to select"):
                        st.session_state[key_prefix].append(seat_id)
                else:
                    col.button(f"{seat_id} ⚠️", disabled=True, help="Selection limit reached")
    
    return st.session_state[key_prefix]

def generate_enhanced_plan(destination, days, month, budget, travel_type, accommodation, interests, pace, special_requests):
    weather = get_weather_placeholder(destination)
    
    plan = f"""
# 🌍 {days}-Day {travel_type} Adventure to {destination.title()}

## 📋 Trip Overview
- **📅 When:** {month}
- **💰 Budget:** {budget}
- **🏨 Accommodation:** {accommodation}
- **⏱️ Pace:** {pace}
- **🌤️ Expected Weather:** {weather['condition']} {weather['temp']} (Humidity: {weather['humidity']})

## 📍 Detailed Itinerary

### Day 1: Grand Arrival 🛬
- **Morning:** Airport pickup and check-in to {accommodation.lower()}
- **Afternoon:** Welcome lunch and neighborhood orientation walk
- **Evening:** Local market visit and traditional dinner
- **💡 Tip:** Keep first day light to adjust to new environment

### Days 2-{days-1}: Core Adventures 🗺️
"""
    
    if "food" in interests.lower() or "culinary" in interests.lower():
        plan += """
#### 🍽️ Culinary Experiences
- Food walking tours and cooking classes
- Local market visits with chef guides
- Traditional restaurant hopping
- Street food adventures (with safety tips)
"""
    
    if "history" in interests.lower() or "culture" in interests.lower():
        plan += """
#### 🏛️ Cultural & Historical Sites
- Guided museum tours with audio guides
- Historical monument visits
- Cultural performances and local art galleries
- Heritage walks through old quarters
"""
    
    if "beach" in interests.lower() or "water" in interests.lower():
        plan += """
#### 🏖️ Beach & Water Activities
- Beach relaxation with water sports
- Sunset boat rides or ferry trips
- Snorkeling or diving excursions
- Beachside cafes and seafood dining
"""
    
    if "nature" in interests.lower() or "adventure" in interests.lower():
        plan += """
#### 🌿 Nature & Adventure
- National parks and wildlife sanctuaries
- Hiking trails with scenic viewpoints
- Photography tours for landscapes
- Adventure sports (based on location)
"""
    
    plan += f"""
### Day {days}: Farewell & Departure 👋
- **Morning:** Final shopping and souvenir hunting
- **Afternoon:** Packing and checkout
- **Evening:** Airport transfer and departure
- **💡 Tip:** Keep 3-4 hours buffer for international flights

## 🎯 Special Recommendations
- **Best Photo Spots:** Research Instagram-worthy locations
- **Local Transportation:** Download local transport apps
- **Emergency Contacts:** Save local emergency numbers
- **Currency:** Keep some local cash for small vendors

## 📱 Useful Apps to Download
- Local maps (offline capability)
- Translation apps
- Local ride-sharing apps
- Weather forecasting apps
"""
    
    if special_requests:
        plan += f"""
## 🌟 Your Special Requests
{special_requests}

*We'll ensure these preferences are incorporated into your itinerary!*
"""
    
    return plan

# ========================
# MAIN APPLICATION TABS
# ========================

# Sidebar for saved preferences and booking history
with st.sidebar:
    st.header("🔖 Quick Access")
    
    # Saved Preferences
    if st.session_state.saved_preferences:
        st.subheader("💾 Saved Preferences")
        for pref_type, prefs in st.session_state.saved_preferences.items():
            with st.expander(f"{pref_type.title()} Preferences"):
                st.json(prefs)
    
    # Booking History
    if st.session_state.booking_history:
        st.subheader("📚 Booking History")
        for booking in st.session_state.booking_history[-3:]:  # Show last 3
            with st.expander(f"{booking['type']} - {booking['id']}"):
                st.write(f"**Date:** {booking['date']}")
                st.write(f"**Type:** {booking['type']}")
                if 'total_cost' in booking['details']:
                    st.write(f"**Cost:** ₹{booking['details']['total_cost']:,}")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Travel Planner", "✈️ Flight Booking", "🚆 Train Booking", "📊 Dashboard"])

# ========================
# TAB 1: ENHANCED TRAVEL PLANNER
# ========================
with tab1:
    st.header("🌍 AI-Powered Travel Planner")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("enhanced_travel_form"):
            st.subheader("📝 Tell Us About Your Dream Trip")
            
            # Basic trip details
            destination = st.text_input("🎯 Destination", placeholder="e.g., Paris, Delhi, Tokyo")
            
            col_days, col_month = st.columns(2)
            with col_days:
                days = st.number_input("📅 Trip Duration (days)", 1, 60, 5)
            with col_month:
                month = st.text_input("🗓️ Travel Month/Season", placeholder="e.g., April 2024")
            
            # Budget and preferences
            col_budget, col_type = st.columns(2)
            with col_budget:
                budget = st.selectbox("💰 Budget Range", 
                    ["₹20,000 - ₹50,000", "₹50,000 - ₹1,00,000", "₹1,00,000 - ₹2,00,000", "₹2,00,000+"])
            with col_type:
                travel_type = st.selectbox("👥 Travel Type", ["Solo", "Couple", "Family", "Group", "Business"])
            
            accommodation = st.selectbox("🏨 Accommodation Preference", 
                ["Budget Hostel", "Mid-range Hotel", "Luxury Hotel", "Airbnb/Apartment", "Resort", "Boutique Hotel"])
            
            # Interests with multiselect
            interests = st.multiselect("🎨 Your Interests", 
                ["Food & Culinary", "History & Culture", "Beach & Water Sports", "Nature & Adventure", 
                 "Shopping", "Nightlife", "Photography", "Wellness & Spa", "Art & Museums", "Sports"])
            
            pace = st.selectbox("⏱️ Travel Pace", 
                ["Relaxed (2-3 activities/day)", "Balanced (3-4 activities/day)", "Packed (5+ activities/day)"])
            
            special_requests = st.text_area("🌟 Special Requests", 
                placeholder="Any specific requirements, dietary restrictions, accessibility needs, etc.", 
                height=100)
            
            # Submit button
            submit = st.form_submit_button("🚀 Generate My Perfect Plan", use_container_width=True)
    
    with col2:
        st.subheader("💡 Planning Tips")
        st.info("""
        **Pro Tips for Better Planning:**
        
        ✅ Be specific about your destination
        
        ✅ Consider seasonal weather patterns
        
        ✅ Mix must-see attractions with local experiences
        
        ✅ Budget 20% extra for unexpected discoveries
        
        ✅ Check visa requirements early
        
        ✅ Book accommodations in advance for peak seasons
        """)
    
    # Process form submission
    if submit:
        if not destination or not month or not interests:
            st.error("⚠️ Please fill in Destination, Travel Month, and at least one Interest.")
        else:
            with st.spinner("🔮 Creating your personalized travel plan..."):
                # Generate enhanced plan
                interests_str = ", ".join(interests)
                plan = generate_enhanced_plan(destination, days, month, budget, travel_type, 
                                            accommodation, interests_str, pace, special_requests)
                
                # Display plan in an attractive format
                st.markdown('<div class="booking-card">', unsafe_allow_html=True)
                st.markdown(plan)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Food recommendations section
                dest_key = destination.strip().lower().replace(" ", "")
                if dest_key in FOOD_RECS:
                    st.subheader(f"🍽️ Must-Try Local Cuisine in {destination.title()}")
                    
                    food_cols = st.columns(2)
                    for i, (dish, desc, price) in enumerate(FOOD_RECS[dest_key]):
                        with food_cols[i % 2]:
                            st.markdown(f"""
                            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin: 10px 0;">
                                <h4 style="margin: 0 0 10px 0;">🍽️ {dish}</h4>
                                <p style="margin: 0 0 5px 0;">{desc}</p>
                                <p style="color: #2E8B57; font-weight: bold; margin: 0;">💰 {price}</p>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Cuisine exploration
                with st.expander("🌮 Explore Different Cuisines"):
                    for cuisine, items in CUISINE_RECS.items():
                        st.markdown(f"### {cuisine}")
                        cuisine_cols = st.columns(2)
                        for i, (dish, desc, price) in enumerate(items):
                            with cuisine_cols[i % 2]:
                                st.markdown(f"**{dish}** - {desc} | *{price}*")

# ========================
# TAB 2: ENHANCED FLIGHT BOOKING
# ========================
with tab2:
    st.header("✈️ Smart Flight Booking")
    
    # Enhanced sidebar filters
    with st.sidebar:
        st.header("🔍 Flight Search")
        
        # Load saved preferences
        if st.button("📂 Load Flight Preferences"):
            if 'flight' in st.session_state.saved_preferences:
                st.success("✅ Preferences loaded!")
        
        # Origin and destination with validation
        origin = st.text_input("🛫 Origin (IATA Code)", "DEL", help="3-letter airport code")
        dest = st.text_input("🛬 Destination (IATA Code)", "BOM", help="3-letter airport code")
        
        # Validate IATA codes
        if origin and not validate_iata_code(origin.upper()):
            st.error("❌ Invalid origin airport code")
        if dest and not validate_iata_code(dest.upper()):
            st.error("❌ Invalid destination airport code")
        
        # Trip type
        trip_type = st.radio("🔄 Trip Type", ["One Way", "Round Trip"])
        
        # Dates
        travel_date = st.date_input(
            "📅 Departure Date",
            min_value=datetime.today().date(),
            value=datetime.today().date() + timedelta(days=7)
        )
        
        if trip_type == "Round Trip":
            return_date = st.date_input(
                "🔙 Return Date",
                min_value=travel_date + timedelta(days=1),
                value=travel_date + timedelta(days=7)
            )
        
        passengers = st.number_input("👥 Passengers", 1, 9, 1)
        travel_class = st.selectbox("💺 Class", ["Economy", "Premium Economy", "Business", "First"])
        
        # Enhanced filters
        st.markdown("---")
        st.subheader("🎛️ Advanced Filters")
        
        # Price range
        price_col1, price_col2 = st.columns(2)
        with price_col1:
            min_price = st.number_input("💰 Min Price", value=2000, step=500)
        with price_col2:
            max_price = st.number_input("💰 Max Price", value=25000, step=500)
        
        # Time preferences
        dep_time_range = st.select_slider(
            "🕒 Departure Time", 
            options=[f"{i:02d}:00" for i in range(24)], 
            value=("06:00", "22:00")
        )
        
        # Airline preferences
        preferred_airlines = st.multiselect(
            "✈️ Preferred Airlines",
            ["IndiGo", "Air India", "SpiceJet", "Vistara", "Go First", "Akasa Air"]
        )
        
        # Additional options
        direct_only = st.checkbox("🎯 Direct flights only")
        refundable = st.checkbox("💵 Refundable tickets only")
        
        # Save preferences
        if st.button("💾 Save Search Preferences"):
            st.session_state.saved_preferences['flight'] = {
                'origin': origin, 'dest': dest, 'class': travel_class,
                'passengers': passengers, 'airlines': preferred_airlines
            }
            st.success("✅ Preferences saved!")
    
    # Search button and results
    if st.button("🔍 Search Flights", use_container_width=True):
        if not validate_iata_code(origin.upper()) or not validate_iata_code(dest.upper()):
            st.error("❌ Please enter valid IATA airport codes")
        else:
            with st.spinner("🔍 Searching for the best flights..."):
                # Enhanced flight generation
                airlines = ["IndiGo", "Air India", "SpiceJet", "Vistara", "Go First", "Akasa Air"]
                aircraft_types = ["A320", "B737", "A321", "B777", "A350", "B787"]
                
                # Filter airlines if preferences set
                if preferred_airlines:
                    airlines = [a for a in airlines if a in preferred_airlines]
                
                base_prices = {"Economy": 3000, "Premium Economy": 6000, "Business": 12000, "First": 20000}
                tax_rates = {"Economy": 0.05, "Premium Economy": 0.08, "Business": 0.12, "First": 0.18}
                
                flights = []
                for i in range(8):  # More flight options
                    airline = random.choice(airlines)
                    aircraft = random.choice(aircraft_types)
                    flight_num = f"{airline[:2].upper()}{random.randint(100, 999)}"
                    
                    # Generate times
                    dep_hour = random.randint(int(dep_time_range[0][:2]), int(dep_time_range[1][:2]))
                    dep_time = datetime.combine(travel_date, datetime.min.time()) + timedelta(hours=dep_hour, minutes=random.randint(0, 59))
                    duration_hours = random.randint(2, 6)
                    arr_time = dep_time + timedelta(hours=duration_hours, minutes=random.randint(0, 59))
                    
                    # Pricing
                    base_price = base_prices[travel_class] + random.randint(-1000, 2000)
                    if base_price < min_price or base_price > max_price:
                        continue
                    
                    tax = base_price * tax_rates[travel_class]
                    service_fee = base_price * 0.025
                    total = base_price + tax + service_fee
                    
                    flights.append({
                        "Select": False,
                        "✈️ Flight": f"{airline} {flight_num}",
                        "🛫 Departure": dep_time.strftime("%H:%M"),
                        "🛬 Arrival": arr_time.strftime("%H:%M"),
                        "⏱️ Duration": f"{duration_hours}h {random.randint(0, 59)}m",
                        "🛩️ Aircraft": aircraft,
                        "🎯 Stops": "Non-stop" if direct_only or random.choice([True, False]) else f"{random.randint(1, 2)} stop(s)",
                        "💰 Base Price": f"₹{base_price:,}",
                        "📊 Tax": f"₹{int(tax):,}",
                        "🔧 Service": f"₹{int(service_fee):,}",
                        "💳 Total": f"₹{int(total):,}",
                        "_total_numeric": int(total)
                    })
                
                if flights:
                    # Sort options
                    sort_by = st.selectbox("📊 Sort by", ["Price (Low to High)", "Price (High to Low)", "Duration", "Departure Time"])
                    
                    if sort_by == "Price (Low to High)":
                        flights.sort(key=lambda x: x["_total_numeric"])
                    elif sort_by == "Price (High to Low)":
                        flights.sort(key=lambda x: x["_total_numeric"], reverse=True)
                    
                    # Display results
                    st.subheader(f"🎯 Available Flights: {origin.upper()} → {dest.upper()} ({travel_date})")
                    st.info(f"Found {len(flights)} flights matching your criteria")
                    
                    # Create a more attractive display
                    df = pd.DataFrame(flights)
                    selected_df = st.data_editor(
                        df.drop('_total_numeric', axis=1), 
                        use_container_width=True,
                        key="flight_booking_table",
                        column_config={
                            "Select": st.column_config.CheckboxColumn("Select", default=False),
                            "💳 Total": st.column_config.TextColumn("💳 Total", width="small")
                        }
                    )
                    
                    # Process selections
                    selected_flights = selected_df[selected_df["Select"]]
                    
                    if not selected_flights.empty:
                        st.success(f"✅ {len(selected_flights)} flight(s) selected!")
                        
                        # Booking form
                        with st.form("enhanced_flight_booking"):
                            st.subheader("👤 Passenger Information")
                            
                            passenger_data = []
                            for i in range(passengers):
                                st.markdown(f"**Passenger {i+1}**")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    name = st.text_input(f"Full Name", key=f"flight_name_{i}")
                                with col2:
                                    age = st.number_input(f"Age", 1, 100, 30, key=f"flight_age_{i}")
                                with col3:
                                    gender = st.selectbox(f"Gender", ["Male", "Female", "Other"], key=f"flight_gender_{i}")
                                
                                passenger_data.append({"name": name, "age": age, "gender": gender})
                            
                            # Contact information
                            st.markdown("**📞 Contact Information**")
                            col1, col2 = st.columns(2)
                            with col1:
                                email = st.text_input("📧 Email Address")
                            with col2:
                                phone = st.text_input("📱 Phone Number")
                            
                            # Additional services
                            st.markdown("**🎯 Additional Services**")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                meal_pref = st.selectbox("🍽️ Meal Preference", 
                                    ["Regular", "Vegetarian", "Vegan", "Halal", "Kosher", "Diabetic"])
                            with col2:
                                baggage = st.selectbox("🧳 Extra Baggage", ["None", "15kg (+₹1,500)", "20kg (+₹2,500)", "30kg (+₹4,000)"])
                            with col3:
                                insurance = st.checkbox("🛡️ Travel Insurance (+₹800)")
                            
                            # Seat selection
                            st.markdown("---")
                            taken_seats = random.sample([f"{i}{c}" for i in range(1, 7) for c in "ABCDEF"], 
                                                      random.randint(5, 15))
                            selected_seats = display_enhanced_flight_seat_map(
                                rows=6, seats_per_row=6, taken_seats=taken_seats, key_prefix="flight_seat"
                            )
                            
                            # Confirmation
                            confirm_flight = st.form_submit_button("✈️ Confirm Flight Booking", use_container_width=True)
                            
                            if confirm_flight:
                                # Validation
                                errors = []
                                if any(p["name"].strip() == "" for p in passenger_data):
                                    errors.append("All passenger names are required")
                                if not validate_email(email):
                                    errors.append("Valid email address is required")
                                if not validate_phone(phone):
                                    errors.append("Valid phone number is required")
                                if len(selected_seats) < passengers:
                                    errors.append(f"Please select {passengers} seat(s)")
                                
                                if errors:
                                    for error in errors:
                                        st.error(f"❌ {error}")
                                else:
                                    # Calculate total cost
                                    base_total = sum(int(row["💳 Total"].replace("₹", "").replace(",", "")) 
                                                   for _, row in selected_flights.iterrows()) * passengers
                                    
                                    baggage_cost = 0
                                    if baggage != "None":
                                        baggage_cost = int(baggage.split('+₹')[1].split(')')[0].replace(',', ''))
                                    
                                    insurance_cost = 800 if insurance else 0
                                    grand_total = base_total + baggage_cost + insurance_cost
                                    
                                    # Generate booking
                                    booking_id = generate_booking_id()
                                    
                                    # Save booking
                                    booking_details = {
                                        'id': booking_id,
                                        'type': 'Flight',
                                        'route': f"{origin.upper()} → {dest.upper()}",
                                        'passengers': passengers,
                                        'total_cost': grand_total,
                                        'travel_date': travel_date.strftime("%Y-%m-%d")
                                    }
                                    save_booking(booking_details)
                                    
                                    # Success display
                                    st.markdown('<div class="success-card">', unsafe_allow_html=True)
                                    st.success("🎉 Flight Booking Confirmed Successfully!")
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.markdown(f"""
                                        ### 📋 Booking Summary
                                        **Booking ID:** `{booking_id}`  
                                        **Route:** {origin.upper()} → {dest.upper()}  
                                        **Date:** {travel_date}  
                                        **Passengers:** {passengers}  
                                        **Class:** {travel_class}  
                                        **Contact:** {email}
                                        """)
                                    
                                    with col2:
                                        st.markdown(f"""
                                        ### 💰 Cost Breakdown
                                        **Flight Cost:** ₹{base_total:,}  
                                        **Baggage:** ₹{baggage_cost:,}  
                                        **Insurance:** ₹{insurance_cost:,}  
                                        **Grand Total:** <span class="price-highlight">₹{grand_total:,}</span>
                                        """, unsafe_allow_html=True)
                                    
                                    # Passenger and seat details
                                    st.markdown("### 👥 Passenger Details")
                                    for i, (passenger, seat) in enumerate(zip(passenger_data, selected_seats)):
                                        st.markdown(f"**{i+1}.** {passenger['name']} ({passenger['age']}, {passenger['gender']}) — Seat: **{seat}**")
                                    
                                    st.markdown('</div>', unsafe_allow_html=True)
                                    st.info("📧 E-tickets and booking confirmation sent to your email!")
                else:
                    st.warning("⚠️ No flights found matching your criteria. Please adjust your filters.")

# ========================
# TAB 3: ENHANCED TRAIN BOOKING
# ========================
with tab3:
    st.header("🚆 Smart Train Booking")
    
    with st.sidebar:
        st.header("🔍 Train Search")
        
        # Load saved preferences
        if st.button("📂 Load Train Preferences"):
            if 'train' in st.session_state.saved_preferences:
                st.success("✅ Preferences loaded!")
        
        train_origin = st.text_input("🚉 Origin Station", "NDLS", help="Station code (e.g., NDLS)")
        train_dest = st.text_input("🎯 Destination Station", "BCT", help="Station code (e.g., BCT)")
        
        train_date = st.date_input(
            "📅 Travel Date",
            min_value=datetime.today().date(),
            value=datetime.today().date() + timedelta(days=7),
            key="train_travel_date"
        )
        
        train_passengers = st.number_input("👥 Passengers", 1, 6, 1, key="train_passengers_input")
        train_class = st.selectbox("🎫 Class", ["Sleeper (SL)", "AC 3 Tier (3A)", "AC 2 Tier (2A)", "AC 1st Class (1A)"])
        
        # Enhanced filters
        st.markdown("---")
        st.subheader("🎛️ Train Filters")
        
        price_range = st.slider("💰 Price Range (₹)", 200, 5000, (500, 3000))
        max_duration = st.slider("⏱️ Max Journey Time (hours)", 4, 24, 18)
        max_stops = st.slider("🛑 Maximum Stops", 0, 10, 5)
        
        departure_time = st.selectbox("🕐 Preferred Departure", 
            ["Any Time", "Early Morning (04:00-08:00)", "Morning (08:00-12:00)", 
             "Afternoon (12:00-16:00)", "Evening (16:00-20:00)", "Night (20:00-04:00)"])
        
        train_type_pref = st.multiselect("🚄 Train Types",
            ["Rajdhani", "Shatabdi", "Duronto", "Express", "Mail", "Passenger"])
        
        # Save preferences
        if st.button("💾 Save Train Preferences"):
            st.session_state.saved_preferences['train'] = {
                'origin': train_origin, 'dest': train_dest, 'class': train_class,
                'passengers': train_passengers
            }
            st.success("✅ Preferences saved!")
    
    # Search trains
    if st.button("🔍 Search Trains", use_container_width=True, key="search_trains_btn"):
        with st.spinner("🔍 Finding the best trains for your journey..."):
            # Generate enhanced train data
            train_types = ["Rajdhani Express", "Shatabdi Express", "Duronto Express", 
                          "Garib Rath", "Superfast Express", "Mail Express", "Passenger"]
            
            if train_type_pref:
                train_types = [t for t in train_types if any(pref in t for pref in train_type_pref)]
            
            base_prices = {"Sleeper (SL)": 400, "AC 3 Tier (3A)": 1200, "AC 2 Tier (2A)": 1800, "AC 1st Class (1A)": 3000}
            
            trains = []
            for i in range(6):
                train_name = random.choice(train_types)
                train_number = f"{random.randint(12000, 19999)}"
                
                # Generate realistic times
                dep_hour = random.randint(4, 23)
                dep_minute = random.choice([0, 15, 30, 45])
                departure = f"{dep_hour:02d}:{dep_minute:02d}"
                
                # Duration and arrival
                duration_hours = random.randint(6, 20)
                duration_minutes = random.randint(0, 59)
                duration = f"{duration_hours}h{duration_minutes:02d}m"
                
                arr_hour = (dep_hour + duration_hours + (dep_minute + duration_minutes) // 60) % 24
                arr_minute = (dep_minute + duration_minutes) % 60
                arrival = f"{arr_hour:02d}:{arr_minute:02d}"
                if duration_hours >= 12:
                    arrival += " +1"
                
                # Other details
                stops = random.randint(0, 8)
                base_price = base_prices[train_class] + random.randint(-200, 500)
                
                # Apply filters
                if not (price_range[0] <= base_price <= price_range[1]):
                    continue
                if stops > max_stops:
                    continue
                if duration_hours > max_duration:
                    continue
                
                # Check departure time filter
                if departure_time != "Any Time":
                    time_ranges = {
                        "Early Morning (04:00-08:00)": (4, 8),
                        "Morning (08:00-12:00)": (8, 12),
                        "Afternoon (12:00-16:00)": (12, 16),
                        "Evening (16:00-20:00)": (16, 20),
                        "Night (20:00-04:00)": (20, 24)
                    }
                    if departure_time in time_ranges:
                        start, end = time_ranges[departure_time]
                        if not (start <= dep_hour < end or (departure_time == "Night (20:00-04:00)" and dep_hour < 4)):
                            continue
                
                trains.append({
                    "Select": False,
                    "🚆 Train": f"{train_name} ({train_number})",
                    "🚉 Departure": departure,
                    "🎯 Arrival": arrival,
                    "⏱️ Duration": duration,
                    "🛑 Stops": stops,
                    "💰 Price": f"₹{base_price}",
                    "🎫 Class": train_class,
                    "_price_numeric": base_price
                })
            
            if trains:
                # Sort options
                sort_option = st.selectbox("📊 Sort by", ["Price (Low to High)", "Duration", "Departure Time", "Fewest Stops"])
                
                if sort_option == "Price (Low to High)":
                    trains.sort(key=lambda x: x["_price_numeric"])
                elif sort_option == "Duration":
                    trains.sort(key=lambda x: int(x["⏱️ Duration"].split('h')[0]))
                elif sort_option == "Fewest Stops":
                    trains.sort(key=lambda x: x["🛑 Stops"])
                
                st.subheader(f"🎯 Available Trains: {train_origin} → {train_dest} ({train_date})")
                st.info(f"Found {len(trains)} trains matching your preferences")
                
                # Display train options
                df_trains = pd.DataFrame(trains)
                selected_trains = st.data_editor(
                    df_trains.drop('_price_numeric', axis=1),
                    use_container_width=True,
                    key="train_selection_table",
                    column_config={
                        "Select": st.column_config.CheckboxColumn("Select", default=False)
                    }
                )
                
                selected_train_data = selected_trains[selected_trains["Select"]]
                
                if not selected_train_data.empty:
                    selected_train_name = selected_train_data.iloc[0]["🚆 Train"]
                    st.success(f"✅ Selected: {selected_train_name}")
                    
                    # Berth selection
                    st.markdown("---")
                    berth_ids = [f"{i}{b}" for i in range(1, 4) for b in ["LB", "UB", "MB", "SL"]]
                    taken_berths = random.sample(berth_ids, k=random.randint(3, 8))
                    selected_berths = display_enhanced_berth_map(
                        rows=3, berths_per_row=4, taken_berths=taken_berths, key_prefix="train_berth"
                    )
                    
                    if len(selected_berths) >= train_passengers:
                        # Booking form
                        with st.form("enhanced_train_booking"):
                            st.subheader("👤 Passenger Information")
                            
                            train_passenger_data = []
                            for i in range(train_passengers):
                                st.markdown(f"**Passenger {i+1}**")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    name = st.text_input(f"Full Name", key=f"train_name_{i}")
                                with col2:
                                    age = st.number_input(f"Age", 1, 100, 30, key=f"train_age_{i}")
                                with col3:
                                    gender = st.selectbox(f"Gender", ["Male", "Female", "Transgender"], key=f"train_gender_{i}")
                                
                                train_passenger_data.append({"name": name, "age": age, "gender": gender})
                            
                            # Contact information
                            st.markdown("**📞 Contact Information**")
                            col1, col2 = st.columns(2)
                            with col1:
                                train_email = st.text_input("📧 Email Address", key="train_email")
                            with col2:
                                train_phone = st.text_input("📱 Phone Number", key="train_phone")
                            
                            # Additional preferences
                            st.markdown("**🍽️ Food & Other Preferences**")
                            col1, col2 = st.columns(2)
                            with col1:
                                food_pref = st.selectbox("Meal Preference", ["Veg", "Non-Veg", "Jain", "No Food"])
                            with col2:
                                bedding = st.checkbox("🛏️ Bedding & Linen (+₹60 per passenger)")
                            
                            confirm_train = st.form_submit_button("🚆 Confirm Train Booking", use_container_width=True)
                            
                            if confirm_train:
                                # Validation
                                errors = []
                                if any(p["name"].strip() == "" for p in train_passenger_data):
                                    errors.append("All passenger names are required")
                                if not validate_email(train_email):
                                    errors.append("Valid email address is required")
                                if not validate_phone(train_phone):
                                    errors.append("Valid phone number is required")
                                
                                if errors:
                                    for error in errors:
                                        st.error(f"❌ {error}")
                                else:
                                    # Calculate costs
                                    base_cost = selected_train_data.iloc[0]["_price_numeric"] * train_passengers
                                    bedding_cost = 60 * train_passengers if bedding else 0
                                    convenience_fee = base_cost * 0.02  # 2% convenience fee
                                    total_cost = base_cost + bedding_cost + convenience_fee
                                    
                                    # Generate booking
                                    booking_id = generate_booking_id()
                                    
                                    # Save booking
                                    booking_details = {
                                        'id': booking_id,
                                        'type': 'Train',
                                        'route': f"{train_origin} → {train_dest}",
                                        'passengers': train_passengers,
                                        'total_cost': int(total_cost),
                                        'travel_date': train_date.strftime("%Y-%m-%d")
                                    }
                                    save_booking(booking_details)
                                    
                                    # Success display
                                    st.markdown('<div class="success-card">', unsafe_allow_html=True)
                                    st.success("🎉 Train Booking Confirmed Successfully!")
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.markdown(f"""
                                        ### 📋 Booking Summary
                                        **PNR Number:** `{booking_id}`  
                                        **Train:** {selected_train_name}  
                                        **Route:** {train_origin} → {train_dest}  
                                        **Date:** {train_date}  
                                        **Class:** {train_class}  
                                        **Status:** Confirmed ✅
                                        """)
                                    
                                    with col2:
                                        st.markdown(f"""
                                        ### 💰 Payment Summary
                                        **Ticket Cost:** ₹{base_cost:,}  
                                        **Bedding:** ₹{bedding_cost:,}  
                                        **Convenience Fee:** ₹{int(convenience_fee):,}  
                                        **Total Paid:** <span class="price-highlight">₹{int(total_cost):,}</span>
                                        """, unsafe_allow_html=True)
                                    
                                    # Passenger details with berths
                                    st.markdown("### 👥 Passenger & Berth Details")
                                    for i, (passenger, berth) in enumerate(zip(train_passenger_data, selected_berths[:train_passengers])):
                                        st.markdown(f"**{i+1}.** {passenger['name']} ({passenger['age']}/{passenger['gender']}) — Berth: **{berth}**")
                                    
                                    st.markdown('</div>', unsafe_allow_html=True)
                                    st.info("📱 SMS and email confirmation sent! Download the app for real-time updates.")
                    else:
                        st.warning(f"⚠️ Please select at least {train_passengers} berth(s) to proceed.")
            else:
                st.warning("⚠️ No trains found matching your criteria. Please adjust your filters.")

# ========================
# TAB 4: DASHBOARD
# ========================
with tab4:
    st.header("📊 Travel Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Booking Statistics")
        if st.session_state.booking_history:
            total_bookings = len(st.session_state.booking_history)
            total_spent = sum(booking['details'].get('total_cost', 0) for booking in st.session_state.booking_history)
            
            # Metrics
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Total Bookings", total_bookings)
            with col_b:
                st.metric("Total Spent", f"₹{total_spent:,}")
            
            # Booking types chart
            booking_types = {}
            for booking in st.session_state.booking_history:
                booking_type = booking['type']
                booking_types[booking_type] = booking_types.get(booking_type, 0) + 1
            
            if booking_types:
                st.bar_chart(booking_types)
        else:
            st.info("📝 No bookings yet. Start planning your next adventure!")
    
    with col2:
        st.subheader("🎯 Quick Actions")
        
        if st.button("🗑️ Clear Booking History", use_container_width=True):
            st.session_state.booking_history = []
            st.success("✅ Booking history cleared!")
        
        if st.button("💾 Export Booking Data", use_container_width=True):
            if st.session_state.booking_history:
                booking_df = pd.DataFrame([
                    {
                        'Booking ID': b['id'],
                        'Type': b['type'],
                        'Date': b['date'],
                        'Cost': b['details'].get('total_cost', 'N/A')
                    } for b in st.session_state.booking_history
                ])
                st.dataframe(booking_df, use_container_width=True)
                st.success("📊 Booking data ready for export!")
            else:
                st.info("No booking data to export")
        
        if st.button("🎲 Random Travel Suggestion", use_container_width=True):
            destinations = ["Goa", "Kerala", "Rajasthan", "Himachal Pradesh", "Tamil Nadu", 
                          "Karnataka", "Uttarakhand", "Andhra Pradesh", "West Bengal", "Assam"]
            random_dest = random.choice(destinations)
            random_days = random.randint(3, 10)
            
            st.info(f"🌟 How about a {random_days}-day trip to {random_dest}? Perfect for your next adventure!")
    
    # Recent bookings
    if st.session_state.booking_history:
        st.subheader("📚 Recent Bookings")
        for booking in st.session_state.booking_history[-5:]:  # Show last 5
            with st.expander(f"{booking['type']} Booking - {booking['id']}", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Type:** {booking['type']}")
                    st.write(f"**Date:** {booking['date']}")
                with col2:
                    if 'route' in booking['details']:
                        st.write(f"**Route:** {booking['details']['route']}")
                    if 'passengers' in booking['details']:
                        st.write(f"**Passengers:** {booking['details']['passengers']}")
                with col3:
                    if 'total_cost' in booking['details']:
                        st.write(f"**Cost:** ₹{booking['details']['total_cost']:,}")
                    if 'travel_date' in booking['details']:
                        st.write(f"**Travel Date:** {booking['details']['travel_date']}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666;">
    <p>🌍 <strong>Enhanced Travel Planner</strong> - Your AI-powered travel companion</p>
    <p>✈️ Safe travels and happy adventures! 🚆</p>
</div>
""", unsafe_allow_html=True)import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import string
import re
import json

# Page Configuration
st.set_page_config(
    page_title="Enhanced Travel Planner & Booking", 
    page_icon="🌍", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.booking-card {
    border: 1px solid #e0e0e0;
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.success-card {
    border: 2px solid #4CAF50;
    border-radius: 15px;
    padding: 20px;
    background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
    margin: 15px 0;
}
.price-highlight {
    font-size: 24px;
    font-weight: bold;
    color: #2E8B57;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    padding-left: 20px;
    padding-right: 20px;
}
</style>
""", unsafe_allow_html=True)

# Validation Functions
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    pattern = r'^[+]?[\d\s\-\(\)]{10,15}$'
    return re.match(pattern, phone) is not None

def validate_iata_code(code):
    return len(code) == 3 and code.isalpha()

# Enhanced Data
@st.cache_data
def load_enhanced_food_recommendations():
    return {
        "delhi": [
            ("Chole Bhature", "Spicy chickpeas with fluffy fried bread", "₹150-200"),
            ("Butter Chicken", "Creamy, rich chicken curry", "₹300-400"),
            ("Paranthas", "Stuffed flatbreads from Chandni Chowk", "₹100-150"),
            ("Kebabs", "Grilled meat skewers from Old Delhi", "₹200-300")
        ],
        "mumbai": [
            ("Vada Pav", "Mumbai's iconic spicy potato burger", "₹15-25"),
            ("Pav Bhaji", "Mashed spicy vegetables with buns", "₹80-120"),
            ("Bhel Puri", "Crunchy street snack mix", "₹40-60"),
            ("Misal Pav", "Spicy sprouted lentil curry", "₹60-100")
        ],
        "chennai": [
            ("Dosa", "Crispy fermented crepe with chutneys", "₹50-100"),
            ("Chettinad Chicken", "Spicy and aromatic chicken curry", "₹250-350"),
            ("Idli Sambar", "Steamed rice cakes with lentil soup", "₹40-80"),
            ("Filter Coffee", "Traditional South Indian coffee", "₹20-40")
        ],
        "hyderabad": [
            ("Hyderabadi Biryani", "Fragrant rice with tender meat", "₹300-500"),
            ("Haleem", "Slow-cooked lentils and meat stew", "₹200-300"),
            ("Nihari", "Rich meat curry traditionally eaten for breakfast", "₹250-400"),
            ("Double Ka Meetha", "Bread pudding dessert", "₹100-150")
        ],
        "goa": [
            ("Fish Curry Rice", "Coconut-based spicy fish curry", "₹200-300"),
            ("Bebinca", "Traditional layered dessert", "₹150-200"),
            ("Pork Vindaloo", "Spicy Portuguese-influenced curry", "₹300-400"),
            ("Feni", "Local cashew or palm spirit", "₹100-200")
        ],
        "kerala": [
            ("Appam & Stew", "Fermented pancakes with vegetable curry", "₹120-180"),
            ("Puttu", "Steamed rice cake with coconut", "₹80-120"),
            ("Fish Molee", "Mild coconut fish curry", "₹250-350"),
            ("Payasam", "Sweet rice pudding dessert", "₹80-120")
        ]
    }

@st.cache_data
def load_enhanced_cuisine_recommendations():
    return {
        "Mediterranean": [
            ("Greek Moussaka", "Layered eggplant, potatoes, and meat", "₹400-600"),
            ("Italian Risotto", "Creamy rice with mushrooms or seafood", "₹350-500"),
            ("Spanish Paella", "Saffron rice with seafood and meat", "₹500-700"),
            ("Turkish Kebab", "Grilled meat with yogurt sauce", "₹300-450")
        ],
        "East Asian": [
            ("Pad Thai", "Stir-fried noodles with tamarind sauce", "₹250-350"),
            ("Sushi Platter", "Fresh raw fish with seasoned rice", "₹800-1200"),
            ("Dim Sum", "Steamed dumplings and small plates", "₹400-600"),
            ("Ramen", "Japanese noodle soup", "₹300-500")
        ],
        "Latin American": [
            ("Tacos al Pastor", "Pork tacos with pineapple", "₹200-300"),
            ("Feijoada", "Brazilian black bean stew", "₹350-500"),
            ("Ceviche", "Raw fish marinated in citrus", "₹400-600"),
            ("Empanadas", "Stuffed pastries", "₹150-250")
        ],
        "Middle Eastern": [
            ("Hummus & Pita", "Chickpea dip with flatbread", "₹200-300"),
            ("Shawarma", "Grilled meat wrap", "₹250-350"),
            ("Falafel", "Fried chickpea balls", "₹180-280"),
            ("Baklava", "Sweet pastry with nuts and honey", "₹150-250")
        ]
    }

# Load enhanced data
FOOD_RECS = load_enhanced_food_recommendations()
CUISINE_RECS = load_enhanced_cuisine_recommendations()

# Initialize session state
if 'booking_history' not in st.session_state:
    st.session_state.booking_history = []
if 'saved_preferences' not in st.session_state:
    st.session_state.saved_preferences = {}

def generate_booking_id(length=8):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def save_booking(booking_details):
    """Save booking to history"""
    st.session_state.booking_history.append({
        'id': booking_details['id'],
        'type': booking_details['type'],
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'details': booking_details
    })

def get_weather_placeholder(destination):
    """Placeholder weather function"""
    weather_options = [
        {"temp": "25°C", "condition": "☀️ Sunny", "humidity": "60%"},
        {"temp": "22°C", "condition": "⛅ Partly Cloudy", "humidity": "65%"},
        {"temp": "28°C", "condition": "🌧️ Light Rain", "humidity": "80%"},
        {"temp": "30°C", "condition": "🌤️ Clear", "humidity": "55%"}
    ]
    return random.choice(weather_options)

def display_enhanced_berth_map(rows=3, berths_per_row=4, taken_berths=None, key_prefix="train_berth"):
    taken_berths = taken_berths or []
    berth_labels = ["LB", "UB", "MB", "SL"][:berths_per_row]
    if key_prefix not in st.session_state:
        st.session_state[key_prefix] = []

    st.markdown("### 🚂 Select Your Berths")
    st.markdown("**Legend:** LB=Lower Berth, UB=Upper Berth, MB=Middle Berth, SL=Side Lower")
    
    for row in range(1, rows + 1):
        cols = st.columns(berths_per_row)
        for i, col in enumerate(cols):
            berth_id = f"{row}{berth_labels[i]}"
            selected = berth_id in st.session_state[key_prefix]
            disabled = (
                berth_id in taken_berths or
                (not selected and len(st.session_state[key_prefix]) >= st.session_state.get("train_passengers", 6))
            )
            
            if berth_id in taken_berths:
                col.button(f"{berth_id} 🚫", disabled=True, help="Already booked")
            elif selected:
                if col.button(f"✅ {berth_id}", key=f"{key_prefix}_{berth_id}", help="Click to deselect"):
                    st.session_state[key_prefix].remove(berth_id)
            else:
                if not disabled:
                    if col.button(f"🪑 {berth_id}", key=f"{key_prefix}_{berth_id}", help="Click to select"):
                        st.session_state[key_prefix].append(berth_id)
                else:
                    col.button(f"{berth_id} ⚠️", disabled=True, help="Selection limit reached")
    
    return st.session_state[key_prefix]

def display_enhanced_flight_seat_map(rows=6, seats_per_row=6, taken_seats=None, key_prefix="flight_seat"):
    taken_seats = taken_seats or []
    seat_labels = ["A", "B", "C", "D", "E", "F"][:seats_per_row]
    if key_prefix not in st.session_state:
        st.session_state[key_prefix] = []

    st.markdown("### ✈️ Select Your Seats")
    st.markdown("**Legend:** A,F=Window | B,E=Middle | C,D=Aisle")
    
    for row in range(1, rows + 1):
        cols = st.columns(seats_per_row)
        for i, col in enumerate(cols):
            seat_id = f"{row}{seat_labels[i]}"
            selected = seat_id in st.session_state[key_prefix]
            disabled = (
                seat_id in taken_seats or
                (not selected and len(st.session_state[key_prefix]) >= st.session_state.get("passengers", 9))
            )
            
            # Determine seat type for icon
            if seat_labels[i] in ['A', 'F']:
                seat_icon = "🪟"  # Window
            elif seat_labels[i] in ['C', 'D']:
                seat_icon = "🚶"  # Aisle
            else:
                seat_icon = "💺"  # Middle
            
            if seat_id in taken_seats:
                col.button(f"{seat_id} 🚫", disabled=True, help="Seat taken")
            elif selected:
                if col.button(f"✅ {seat_id}", key=f"{key_prefix}_{seat_id}", help="Click to deselect"):
                    st.session_state[key_prefix].remove(seat_id)
            else:
                if not disabled:
                    if col.button(f"{seat_icon} {seat_id}", key=f"{key_prefix}_{seat_id}", help="Click to select"):
                        st.session_state[key_prefix].append(seat_id)
                else:
                    col.button(f"{seat_id} ⚠️", disabled=True, help="Selection limit reached")
    
    return st.session_state[key_prefix]

def generate_enhanced_plan(destination, days, month, budget, travel_type, accommodation, interests, pace, special_requests):
    weather = get_weather_placeholder(destination)
    
    plan = f"""
# 🌍 {days}-Day {travel_type} Adventure to {destination.title()}

## 📋 Trip Overview
- **📅 When:** {month}
- **💰 Budget:** {budget}
- **🏨 Accommodation:** {accommodation}
- **⏱️ Pace:** {pace}
- **🌤️ Expected Weather:** {weather['condition']} {weather['temp']} (Humidity: {weather['humidity']})

## 📍 Detailed Itinerary

### Day 1: Grand Arrival 🛬
- **Morning:** Airport pickup and check-in to {accommodation.lower()}
- **Afternoon:** Welcome lunch and neighborhood orientation walk
- **Evening:** Local market visit and traditional dinner
- **💡 Tip:** Keep first day light to adjust to new environment

### Days 2-{days-1}: Core Adventures 🗺️
"""
    
    if "food" in interests.lower() or "culinary" in interests.lower():
        plan += """
#### 🍽️ Culinary Experiences
- Food walking tours and cooking classes
- Local market visits with chef guides
- Traditional restaurant hopping
- Street food adventures (with safety tips)
"""
    
    if "history" in interests.lower() or "culture" in interests.lower():
        plan += """
#### 🏛️ Cultural & Historical Sites
- Guided museum tours with audio guides
- Historical monument visits
- Cultural performances and local art galleries
- Heritage walks through old quarters
"""
    
    if "beach" in interests.lower() or "water" in interests.lower():
        plan += """
#### 🏖️ Beach & Water Activities
- Beach relaxation with water sports
- Sunset boat rides or ferry trips
- Snorkeling or diving excursions
- Beachside cafes and seafood dining
"""
    
    if "nature" in interests.lower() or "adventure" in interests.lower():
        plan += """
#### 🌿 Nature & Adventure
- National parks and wildlife sanctuaries
- Hiking trails with scenic viewpoints
- Photography tours for landscapes
- Adventure sports (based on location)
"""
    
    plan += f"""
### Day {days}: Farewell & Departure 👋
- **Morning:** Final shopping and souvenir hunting
- **Afternoon:** Packing and checkout
- **Evening:** Airport transfer and departure
- **💡 Tip:** Keep 3-4 hours buffer for international flights

## 🎯 Special Recommendations
- **Best Photo Spots:** Research Instagram-worthy locations
- **Local Transportation:** Download local transport apps
- **Emergency Contacts:** Save local emergency numbers
- **Currency:** Keep some local cash for small vendors

## 📱 Useful Apps to Download
- Local maps (offline capability)
- Translation apps
- Local ride-sharing apps
- Weather forecasting apps
"""
    
    if special_requests:
        plan += f"""
## 🌟 Your Special Requests
{special_requests}

*We'll ensure these preferences are incorporated into your itinerary!*
"""
    
    return plan

# ========================
# MAIN APPLICATION TABS
# ========================

# Sidebar for saved preferences and booking history
with st.sidebar:
    st.header("🔖 Quick Access")
    
    # Saved Preferences
    if st.session_state.saved_preferences:
        st.subheader("💾 Saved Preferences")
        for pref_type, prefs in st.session_state.saved_preferences.items():
            with st.expander(f"{pref_type.title()} Preferences"):
                st.json(prefs)
    
    # Booking History
    if st.session_state.booking_history:
        st.subheader("📚 Booking History")
        for booking in st.session_state.booking_history[-3:]:  # Show last 3
            with st.expander(f"{booking['type']} - {booking['id']}"):
                st.write(f"**Date:** {booking['date']}")
                st.write(f"**Type:** {booking['type']}")
                if 'total_cost' in booking['details']:
                    st.write(f"**Cost:** ₹{booking['details']['total_cost']:,}")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Travel Planner", "✈️ Flight Booking", "🚆 Train Booking", "📊 Dashboard"])

# ========================
# TAB 1: ENHANCED TRAVEL PLANNER
# ========================
with tab1:
    st.header("🌍 AI-Powered Travel Planner")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("enhanced_travel_form"):
            st.subheader("📝 Tell Us About Your Dream Trip")
            
            # Basic trip details
            destination = st.text_input("🎯 Destination", placeholder="e.g., Paris, Delhi, Tokyo")
            
            col_days, col_month = st.columns(2)
            with col_days:
                days = st.number_input("📅 Trip Duration (days)", 1, 60, 5)
            with col_month:
                month = st.text_input("🗓️ Travel Month/Season", placeholder="e.g., April 2024")
            
            # Budget and preferences
            col_budget, col_type = st.columns(2)
            with col_budget:
                budget = st.selectbox("💰 Budget Range", 
                    ["₹20,000 - ₹50,000", "₹50,000 - ₹1,00,000", "₹1,00,000 - ₹2,00,000", "₹2,00,000+"])
            with col_type:
                travel_type = st.selectbox("👥 Travel Type", ["Solo", "Couple", "Family", "Group", "Business"])
            
            accommodation = st.selectbox("🏨 Accommodation Preference", 
                ["Budget Hostel", "Mid-range Hotel", "Luxury Hotel", "Airbnb/Apartment", "Resort", "Boutique Hotel"])
            
            # Interests with multiselect
            interests = st.multiselect("🎨 Your Interests", 
                ["Food & Culinary", "History & Culture", "Beach & Water Sports", "Nature & Adventure", 
                 "Shopping", "Nightlife", "Photography", "Wellness & Spa", "Art & Museums", "Sports"])
            
            pace = st.selectbox("⏱️ Travel Pace", 
                ["Relaxed (2-3 activities/day)", "Balanced (3-4 activities/day)", "Packed (5+ activities/day)"])
            
            special_requests = st.text_area("🌟 Special Requests", 
                placeholder="Any specific requirements, dietary restrictions, accessibility needs, etc.", 
                height=100)
            
            # Submit button
            submit = st.form_submit_button("🚀 Generate My Perfect Plan", use_container_width=True)
    
    with col2:
        st.subheader("💡 Planning Tips")
        st.info("""
        **Pro Tips for Better Planning:**
        
        ✅ Be specific about your destination
        
        ✅ Consider seasonal weather patterns
        
        ✅ Mix must-see attractions with local experiences
        
        ✅ Budget 20% extra for unexpected discoveries
        
        ✅ Check visa requirements early
        
        ✅ Book accommodations in advance for peak seasons
        """)
    
    # Process form submission
    if submit:
        if not destination or not month or not interests:
            st.error("⚠️ Please fill in Destination, Travel Month, and at least one Interest.")
        else:
            with st.spinner("🔮 Creating your personalized travel plan..."):
                # Generate enhanced plan
                interests_str = ", ".join(interests)
                plan = generate_enhanced_plan(destination, days, month, budget, travel_type, 
                                            accommodation, interests_str, pace, special_requests)
                
                # Display plan in an attractive format
                st.markdown('<div class="booking-card">', unsafe_allow_html=True)
                st.markdown(plan)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Food recommendations section
                dest_key = destination.strip().lower().replace(" ", "")
                if dest_key in FOOD_RECS:
                    st.subheader(f"🍽️ Must-Try Local Cuisine in {destination.title()}")
                    
                    food_cols = st.columns(2)
                    for i, (dish, desc, price) in enumerate(FOOD_RECS[dest_key]):
                        with food_cols[i % 2]:
                            st.markdown(f"""
                            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin: 10px 0;">
                                <h4 style="margin: 0 0 10px 0;">🍽️ {dish}</h4>
                                <p style="margin: 0 0 5px 0;">{desc}</p>
                                <p style="color: #2E8B57; font-weight: bold; margin: 0;">💰 {price}</p>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Cuisine exploration
                with st.expander("🌮 Explore Different Cuisines"):
                    for cuisine, items in CUISINE_RECS.items():
                        st.markdown(f"### {cuisine}")
                        cuisine_cols = st.columns(2)
                        for i, (dish, desc, price) in enumerate(items):
                            with cuisine_cols[i % 2]:
                                st.markdown(f"**{dish}** - {desc} | *{price}*")

# ========================
# TAB 2: ENHANCED FLIGHT BOOKING
# ========================
with tab2:
    st.header("✈️ Smart Flight Booking")
    
    # Enhanced sidebar filters
    with st.sidebar:
        st.header("🔍 Flight Search")
        
        # Load saved preferences
        if st.button("📂 Load Flight Preferences"):
            if 'flight' in st.session_state.saved_preferences:
                st.success("✅ Preferences loaded!")
        
        # Origin and destination with validation
        origin = st.text_input("🛫 Origin (IATA Code)", "DEL", help="3-letter airport code")
        dest = st.text_input("🛬 Destination (IATA Code)", "BOM", help="3-letter airport code")
        
        # Validate IATA codes
        if origin and not validate_iata_code(origin.upper()):
            st.error("❌ Invalid origin airport code")
        if dest and not validate_iata_code(dest.upper()):
            st.error("❌ Invalid destination airport code")
        
        # Trip type
        trip_type = st.radio("🔄 Trip Type", ["One Way", "Round Trip"])
        
        # Dates
        travel_date = st.date_input(
            "📅 Departure Date",
            min_value=datetime.today().date(),
            value=datetime.today().date() + timedelta(days=7)
        )
        
        if trip_type == "Round Trip":
            return_date = st.date_input(
                "🔙 Return Date",
                min_value=travel_date + timedelta(days=1),
                value=travel_date + timedelta(days=7)
            )
        
        passengers = st.number_input("👥 Passengers", 1, 9, 1)
        travel_class = st.selectbox("💺 Class", ["Economy", "Premium Economy", "Business", "First"])
        
        # Enhanced filters
        st.markdown("---")
        st.subheader("🎛️ Advanced Filters")
        
        # Price range
        price_col1, price_col2 = st.columns(2)
        with price_col1:
            min_price = st.number_input("💰 Min Price", value=2000, step=500)
        with price_col2:
            max_price = st.number_input("💰 Max Price", value=25000, step=500)
        
        # Time preferences
        dep_time_range = st.select_slider(
            "🕒 Departure Time", 
            options=[f"{i:02d}:00" for i in range(24)], 
            value=("06:00", "22:00")
        )
        
        # Airline preferences
        preferred_airlines = st.multiselect(
            "✈️ Preferred Airlines",
            ["IndiGo", "Air India", "SpiceJet", "Vistara", "Go First", "Akasa Air"]
        )
        
        # Additional options
        direct_only = st.checkbox("🎯 Direct flights only")
        refundable = st.checkbox("💵 Refundable tickets only")
        
        # Save preferences
        if st.button("💾 Save Search Preferences"):
            st.session_state.saved_preferences['flight'] = {
                'origin': origin, 'dest': dest, 'class': travel_class,
                'passengers': passengers, 'airlines': preferred_airlines
            }
            st.success("✅ Preferences saved!")
    
    # Search button and results
    if st.button("🔍 Search Flights", use_container_width=True):
        if not validate_iata_code(origin.upper()) or not validate_iata_code(dest.upper()):
            st.error("❌ Please enter valid IATA airport codes")
        else:
            with st.spinner("🔍 Searching for the best flights..."):
                # Enhanced flight generation
                airlines = ["IndiGo", "Air India", "SpiceJet", "Vistara", "Go First", "Akasa Air"]
                aircraft_types = ["A320", "B737", "A321", "B777", "A350", "B787"]
                
                # Filter airlines if preferences set
                if preferred_airlines:
                    airlines = [a for a in airlines if a in preferred_airlines]
                
                base_prices = {"Economy": 3000, "Premium Economy": 6000, "Business": 12000, "First": 20000}
                tax_rates = {"Economy": 0.05, "Premium Economy": 0.08, "Business": 0.12, "First": 0.18}
                
                flights = []
                for i in range(8):  # More flight options
                    airline = random.choice(airlines)
                    aircraft = random.choice(aircraft_types)
                    flight_num = f"{airline[:2].upper()}{random.randint(100, 999)}"
                    
                    # Generate times
                    dep_hour = random.randint(int(dep_time_range[0][:2]), int(dep_time_range[1][:2]))
                    dep_time = datetime.combine(travel_date, datetime.min.time()) + timedelta(hours=dep_hour, minutes=random.randint(0, 59))
                    duration_hours = random.randint(2, 6)
                    arr_time = dep_time + timedelta(hours=duration_hours, minutes=random.randint(0, 59))
                    
                    # Pricing
                    base_price = base_prices[travel_class] + random.randint(-1000, 2000)
                    if base_price < min_price or base_price > max_price:
                        continue
                    
                    tax = base_price * tax_rates[travel_class]
                    service_fee = base_price * 0.025
                    total = base_price + tax + service_fee
                    
                    flights.append({
                        "Select": False,
                        "✈️ Flight": f"{airline} {flight_num}",
                        "🛫 Departure": dep_time.strftime("%H:%M"),
                        "🛬 Arrival": arr_time.strftime("%H:%M"),
                        "⏱️ Duration": f"{duration_hours}h {random.randint(0, 59)}m",
                        "🛩️ Aircraft": aircraft,
                        "🎯 Stops": "Non-stop" if direct_only or random.choice([True, False]) else f"{random.randint(1, 2)} stop(s)",
                        "💰 Base Price": f"₹{base_price:,}",
                        "📊 Tax": f"₹{int(tax):,}",
                        "🔧 Service": f"₹{int(service_fee):,}",
                        "💳 Total": f"₹{int(total):,}",
                        "_total_numeric": int(total)
                    })
                
                if flights:
                    # Sort options
                    sort_by = st.selectbox("📊 Sort by", ["Price (Low to High)", "Price (High to Low)", "Duration", "Departure Time"])
                    
                    if sort_by == "Price (Low to High)":
                        flights.sort(key=lambda x: x["_total_numeric"])
                    elif sort_by == "Price (High to Low)":
                        flights.sort(key=lambda x: x["_total_numeric"], reverse=True)
                    
                    # Display results
                    st.subheader(f"🎯 Available Flights: {origin.upper()} → {dest.upper()} ({travel_date})")
                    st.info(f"Found {len(flights)} flights matching your criteria")
                    
                    # Create a more attractive display
                    df = pd.DataFrame(flights)
                    selected_df = st.data_editor(
                        df.drop('_total_numeric', axis=1), 
                        use_container_width=True,
                        key="flight_booking_table",
                        column_config={
                            "Select": st.column_config.CheckboxColumn("Select", default=False),
                            "💳 Total": st.column_config.TextColumn("💳 Total", width="small")
                        }
                    )
                    
                    # Process selections
                    selected_flights = selected_df[selected_df["Select"]]
                    
                    if not selected_flights.empty:
                        st.success(f"✅ {len(selected_flights)} flight(s) selected!")
                        
                        # Booking form
                        with st.form("enhanced_flight_booking"):
                            st.subheader("👤 Passenger Information")
                            
                            passenger_data = []
                            for i in range(passengers):
                                st.markdown(f"**Passenger {i+1}**")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    name = st.text_input(f"Full Name", key=f"flight_name_{i}")
                                with col2:
                                    age = st.number_input(f"Age", 1, 100, 30, key=f"flight_age_{i}")
                                with col3:
                                    gender = st.selectbox(f"Gender", ["Male", "Female", "Other"], key=f"flight_gender_{i}")
                                
                                passenger_data.append({"name": name, "age": age, "gender": gender})
                            
                            # Contact information
                            st.markdown("**📞 Contact Information**")
                            col1, col2 = st.columns(2)
                            with col1:
                                email = st.text_input("📧 Email Address")
                            with col2:
                                phone = st.text_input("📱 Phone Number")
                            
                            # Additional services
                            st.markdown("**🎯 Additional Services**")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                meal_pref = st.selectbox("🍽️ Meal Preference", 
                                    ["Regular", "Vegetarian", "Vegan", "Halal", "Kosher", "Diabetic"])
                            with col2:
                                baggage = st.selectbox("🧳 Extra Baggage", ["None", "15kg (+₹1,500)", "20kg (+₹2,500)", "30kg (+₹4,000)"])
                            with col3:
                                insurance = st.checkbox("🛡️ Travel Insurance (+₹800)")
                            
                            # Seat selection
                            st.markdown("---")
                            taken_seats = random.sample([f"{i}{c}" for i in range(1, 7) for c in "ABCDEF"], 
                                                      random.randint(5, 15))
                            selected_seats = display_enhanced_flight_seat_map(
                                rows=6, seats_per_row=6, taken_seats=taken_seats, key_prefix="flight_seat"
                            )
                            
                            # Confirmation
                            confirm_flight = st.form_submit_button("✈️ Confirm Flight Booking", use_container_width=True)
                            
                            if confirm_flight:
                                # Validation
                                errors = []
                                if any(p["name"].strip() == "" for p in passenger_data):
                                    errors.append("All passenger names are required")
                                if not validate_email(email):
                                    errors.append("Valid email address is required")
                                if not validate_phone(phone):
                                    errors.append("Valid phone number is required")
                                if len(selected_seats) < passengers:
                                    errors.append(f"Please select {passengers} seat(s)")
                                
                                if errors:
                                    for error in errors:
                                        st.error(f"❌ {error}")
                                else:
                                    # Calculate total cost
                                    base_total = sum(int(row["💳 Total"].replace("₹", "").replace(",", "")) 
                                                   for _, row in selected_flights.iterrows()) * passengers
                                    
                                    baggage_cost = 0
                                    if baggage != "None":
                                        baggage_cost = int(baggage.split('+₹')[1].split(')')[0].replace(',', ''))
                                    
                                    insurance_cost = 800 if insurance else 0
                                    grand_total = base_total + baggage_cost + insurance_cost
                                    
                                    # Generate booking
                                    booking_id = generate_booking_id()
                                    
                                    # Save booking
                                    booking_details = {
                                        'id': booking_id,
                                        'type': 'Flight',
                                        'route': f"{origin.upper()} → {dest.upper()}",
                                        'passengers': passengers,
                                        'total_cost': grand_total,
                                        'travel_date': travel_date.strftime("%Y-%m-%d")
                                    }
                                    save_booking(booking_details)
                                    
                                    # Success display
                                    st.markdown('<div class="success-card">', unsafe_allow_html=True)
                                    st.success("🎉 Flight Booking Confirmed Successfully!")
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.markdown(f"""
                                        ### 📋 Booking Summary
                                        **Booking ID:** `{booking_id}`  
                                        **Route:** {origin.upper()} → {dest.upper()}  
                                        **Date:** {travel_date}  
                                        **Passengers:** {passengers}  
                                        **Class:** {travel_class}  
                                        **Contact:** {email}
                                        """)
                                    
                                    with col2:
                                        st.markdown(f"""
                                        ### 💰 Cost Breakdown
                                        **Flight Cost:** ₹{base_total:,}  
                                        **Baggage:** ₹{baggage_cost:,}  
                                        **Insurance:** ₹{insurance_cost:,}  
                                        **Grand Total:** <span class="price-highlight">₹{grand_total:,}</span>
                                        """, unsafe_allow_html=True)
                                    
                                    # Passenger and seat details
                                    st.markdown("### 👥 Passenger Details")
                                    for i, (passenger, seat) in enumerate(zip(passenger_data, selected_seats)):
                                        st.markdown(f"**{i+1}.** {passenger['name']} ({passenger['age']}, {passenger['gender']}) — Seat: **{seat}**")
                                    
                                    st.markdown('</div>', unsafe_allow_html=True)
                                    st.info("📧 E-tickets and booking confirmation sent to your email!")
                else:
                    st.warning("⚠️ No flights found matching your criteria. Please adjust your filters.")

# ========================
# TAB 3: ENHANCED TRAIN BOOKING
# ========================
with tab3:
    st.header("🚆 Smart Train Booking")
    
    with st.sidebar:
        st.header("🔍 Train Search")
        
        # Load saved preferences
        if st.button("📂 Load Train Preferences"):
            if 'train' in st.session_state.saved_preferences:
                st.success("✅ Preferences loaded!")
        
        train_origin = st.text_input("🚉 Origin Station", "NDLS", help="Station code (e.g., NDLS)")
        train_dest = st.text_input("🎯 Destination Station", "BCT", help="Station code (e.g., BCT)")
        
        train_date = st.date_input(
            "📅 Travel Date",
            min_value=datetime.today().date(),
            value=datetime.today().date() + timedelta(days=7),
            key="train_travel_date"
        )
        
        train_passengers = st.number_input("👥 Passengers", 1, 6, 1, key="train_passengers_input")
        train_class = st.selectbox("🎫 Class", ["Sleeper (SL)", "AC 3 Tier (3A)", "AC 2 Tier (2A)", "AC 1st Class (1A)"])
        
        # Enhanced filters
        st.markdown("---")
        st.subheader("🎛️ Train Filters")
        
        price_range = st.slider("💰 Price Range (₹)", 200, 5000, (500, 3000))
        max_duration = st.slider("⏱️ Max Journey Time (hours)", 4, 24, 18)
        max_stops = st.slider("🛑 Maximum Stops", 0, 10, 5)
        
        departure_time = st.selectbox("🕐 Preferred Departure", 
            ["Any Time", "Early Morning (04:00-08:00)", "Morning (08:00-12:00)", 
             "Afternoon (12:00-16:00)", "Evening (16:00-20:00)", "Night (20:00-04:00)"])
        
        train_type_pref = st.multiselect("🚄 Train Types",
            ["Rajdhani", "Shatabdi", "Duronto", "Express", "Mail", "Passenger"])
        
        # Save preferences
        if st.button("💾 Save Train Preferences"):
            st.session_state.saved_preferences['train'] = {
                'origin': train_origin, 'dest': train_dest, 'class': train_class,
                'passengers': train_passengers
            }
            st.success("✅ Preferences saved!")
    
    # Search trains
    if st.button("🔍 Search Trains", use_container_width=True, key="search_trains_btn"):
        with st.spinner("🔍 Finding the best trains for your journey..."):
            # Generate enhanced train data
            train_types = ["Rajdhani Express", "Shatabdi Express", "Duronto Express", 
                          "Garib Rath", "Superfast Express", "Mail Express", "Passenger"]
            
            if train_type_pref:
                train_types = [t for t in train_types if any(pref in t for pref in train_type_pref)]
            
            base_prices = {"Sleeper (SL)": 400, "AC 3 Tier (3A)": 1200, "AC 2 Tier (2A)": 1800, "AC 1st Class (1A)": 3000}
            
            trains = []
            for i in range(6):
                train_name = random.choice(train_types)
                train_number = f"{random.randint(12000, 19999)}"
                
                # Generate realistic times
                dep_hour = random.randint(4, 23)
                dep_minute = random.choice([0, 15, 30, 45])
                departure = f"{dep_hour:02d}:{dep_minute:02d}"
                
                # Duration and arrival
                duration_hours = random.randint(6, 20)
                duration_minutes = random.randint(0, 59)
                duration = f"{duration_hours}h{duration_minutes:02d}m"
                
                arr_hour = (dep_hour + duration_hours + (dep_minute + duration_minutes) // 60) % 24
                arr_minute = (dep_minute + duration_minutes) % 60
                arrival = f"{arr_hour:02d}:{arr_minute:02d}"
                if duration_hours >= 12:
                    arrival += " +1"
                
                # Other details
                stops = random.randint(0, 8)
                base_price = base_prices[train_class] + random.randint(-200, 500)
                
                # Apply filters
                if not (price_range[0] <= base_price <= price_range[1]):
                    continue
                if stops > max_stops:
                    continue
                if duration_hours > max_duration:
                    continue
                
                # Check departure time filter
                if departure_time != "Any Time":
                    time_ranges = {
                        "Early Morning (04:00-08:00)": (4, 8),
                        "Morning (08:00-12:00)": (8, 12),
                        "Afternoon (12:00-16:00)": (12, 16),
                        "Evening (16:00-20:00)": (16, 20),
                        "Night (20:00-04:00)": (20, 24)
                    }
                    if departure_time in time_ranges:
                        start, end = time_ranges[departure_time]
                        if not (start <= dep_hour < end or (departure_time == "Night (20:00-04:00)" and dep_hour < 4)):
                            continue
                
                trains.append({
                    "Select": False,
                    "🚆 Train": f"{train_name} ({train_number})",
                    "🚉 Departure": departure,
                    "🎯 Arrival": arrival,
                    "⏱️ Duration": duration,
                    "🛑 Stops": stops,
                    "💰 Price": f"₹{base_price}",
                    "🎫 Class": train_class,
                    "_price_numeric": base_price
                })
            
            if trains:
                # Sort options
                sort_option = st.selectbox("📊 Sort by", ["Price (Low to High)", "Duration", "Departure Time", "Fewest Stops"])
                
                if sort_option == "Price (Low to High)":
                    trains.sort(key=lambda x: x["_price_numeric"])
                elif sort_option == "Duration":
                    trains.sort(key=lambda x: int(x["⏱️ Duration"].split('h')[0]))
                elif sort_option == "Fewest Stops":
                    trains.sort(key=lambda x: x["🛑 Stops"])
                
                st.subheader(f"🎯 Available Trains: {train_origin} → {train_dest} ({train_date})")
                st.info(f"Found {len(trains)} trains matching your preferences")
                
                # Display train options
                df_trains = pd.DataFrame(trains)
                selected_trains = st.data_editor(
                    df_trains.drop('_price_numeric', axis=1),
                    use_container_width=True,
                    key="train_selection_table",
                    column_config={
                        "Select": st.column_config.CheckboxColumn("Select", default=False)
                    }
                )
                
                selected_train_data = selected_trains[selected_trains["Select"]]
                
                if not selected_train_data.empty:
                    selected_train_name = selected_train_data.iloc[0]["🚆 Train"]
                    st.success(f"✅ Selected: {selected_train_name}")
                    
                    # Berth selection
                    st.markdown("---")
                    berth_ids = [f"{i}{b}" for i in range(1, 4) for b in ["LB", "UB", "MB", "SL"]]
                    taken_berths = random.sample(berth_ids, k=random.randint(3, 8))
                    selected_berths = display_enhanced_berth_map(
                        rows=3, berths_per_row=4, taken_berths=taken_berths, key_prefix="train_berth"
                    )
                    
                    if len(selected_berths) >= train_passengers:
                        # Booking form
                        with st.form("enhanced_train_booking"):
                            st.subheader("👤 Passenger Information")
                            
                            train_passenger_data = []
                            for i in range(train_passengers):
                                st.markdown(f"**Passenger {i+1}**")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    name = st.text_input(f"Full Name", key=f"train_name_{i}")
                                with col2:
                                    age = st.number_input(f"Age", 1, 100, 30, key=f"train_age_{i}")
                                with col3:
                                    gender = st.selectbox(f"Gender", ["Male", "Female", "Transgender"], key=f"train_gender_{i}")
                                
                                train_passenger_data.append({"name": name, "age": age, "gender": gender})
                            
                            # Contact information
                            st.markdown("**📞 Contact Information**")
                            col1, col2 = st.columns(2)
                            with col1:
                                train_email = st.text_input("📧 Email Address", key="train_email")
                            with col2:
                                train_phone = st.text_input("📱 Phone Number", key="train_phone")
                            
                            # Additional preferences
                            st.markdown("**🍽️ Food & Other Preferences**")
                            col1, col2 = st.columns(2)
                            with col1:
                                food_pref = st.selectbox("Meal Preference", ["Veg", "Non-Veg", "Jain", "No Food"])
                            with col2:
                                bedding = st.checkbox("🛏️ Bedding & Linen (+₹60 per passenger)")
                            
                            confirm_train = st.form_submit_button("🚆 Confirm Train Booking", use_container_width=True)
                            
                            if confirm_train:
                                # Validation
                                errors = []
                                if any(p["name"].strip() == "" for p in train_passenger_data):
                                    errors.append("All passenger names are required")
                                if not validate_email(train_email):
                                    errors.append("Valid email address is required")
                                if not validate_phone(train_phone):
                                    errors.append("Valid phone number is required")
                                
                                if errors:
                                    for error in errors:
                                        st.error(f"❌ {error}")
                                else:
                                    # Calculate costs
                                    base_cost = selected_train_data.iloc[0]["_price_numeric"] * train_passengers
                                    bedding_cost = 60 * train_passengers if bedding else 0
                                    convenience_fee = base_cost * 0.02  # 2% convenience fee
                                    total_cost = base_cost + bedding_cost + convenience_fee
                                    
                                    # Generate booking
                                    booking_id = generate_booking_id()
                                    
                                    # Save booking
                                    booking_details = {
                                        'id': booking_id,
                                        'type': 'Train',
                                        'route': f"{train_origin} → {train_dest}",
                                        'passengers': train_passengers,
                                        'total_cost': int(total_cost),
                                        'travel_date': train_date.strftime("%Y-%m-%d")
                                    }
                                    save_booking(booking_details)
                                    
                                    # Success display
                                    st.markdown('<div class="success-card">', unsafe_allow_html=True)
                                    st.success("🎉 Train Booking Confirmed Successfully!")
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.markdown(f"""
                                        ### 📋 Booking Summary
                                        **PNR Number:** `{booking_id}`  
                                        **Train:** {selected_train_name}  
                                        **Route:** {train_origin} → {train_dest}  
                                        **Date:** {train_date}  
                                        **Class:** {train_class}  
                                        **Status:** Confirmed ✅
                                        """)
                                    
                                    with col2:
                                        st.markdown(f"""
                                        ### 💰 Payment Summary
                                        **Ticket Cost:** ₹{base_cost:,}  
                                        **Bedding:** ₹{bedding_cost:,}  
                                        **Convenience Fee:** ₹{int(convenience_fee):,}  
                                        **Total Paid:** <span class="price-highlight">₹{int(total_cost):,}</span>
                                        """, unsafe_allow_html=True)
                                    
                                    # Passenger details with berths
                                    st.markdown("### 👥 Passenger & Berth Details")
                                    for i, (passenger, berth) in enumerate(zip(train_passenger_data, selected_berths[:train_passengers])):
                                        st.markdown(f"**{i+1}.** {passenger['name']} ({passenger['age']}/{passenger['gender']}) — Berth: **{berth}**")
                                    
                                    st.markdown('</div>', unsafe_allow_html=True)
                                    st.info("📱 SMS and email confirmation sent! Download the app for real-time updates.")
                    else:
                        st.warning(f"⚠️ Please select at least {train_passengers} berth(s) to proceed.")
            else:
                st.warning("⚠️ No trains found matching your criteria. Please adjust your filters.")

# ========================
# TAB 4: DASHBOARD
# ========================
with tab4:
    st.header("📊 Travel Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Booking Statistics")
        if st.session_state.booking_history:
            total_bookings = len(st.session_state.booking_history)
            total_spent = sum(booking['details'].get('total_cost', 0) for booking in st.session_state.booking_history)
            
            # Metrics
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Total Bookings", total_bookings)
            with col_b:
                st.metric("Total Spent", f"₹{total_spent:,}")
            
            # Booking types chart
            booking_types = {}
            for booking in st.session_state.booking_history:
                booking_type = booking['type']
                booking_types[booking_type] = booking_types.get(booking_type, 0) + 1
            
            if booking_types:
                st.bar_chart(booking_types)
        else:
            st.info("📝 No bookings yet. Start planning your next adventure!")
    
    with col2:
        st.subheader("🎯 Quick Actions")
        
        if st.button("🗑️ Clear Booking History", use_container_width=True):
            st.session_state.booking_history = []
            st.success("✅ Booking history cleared!")
        
        if st.button("💾 Export Booking Data", use_container_width=True):
            if st.session_state.booking_history:
                booking_df = pd.DataFrame([
                    {
                        'Booking ID': b['id'],
                        'Type': b['type'],
                        'Date': b['date'],
                        'Cost': b['details'].get('total_cost', 'N/A')
                    } for b in st.session_state.booking_history
                ])
                st.dataframe(booking_df, use_container_width=True)
                st.success("📊 Booking data ready for export!")
            else:
                st.info("No booking data to export")
        
        if st.button("🎲 Random Travel Suggestion", use_container_width=True):
            destinations = ["Goa", "Kerala", "Rajasthan", "Himachal Pradesh", "Tamil Nadu", 
                          "Karnataka", "Uttarakhand", "Andhra Pradesh", "West Bengal", "Assam"]
            random_dest = random.choice(destinations)
            random_days = random.randint(3, 10)
            
            st.info(f"🌟 How about a {random_days}-day trip to {random_dest}? Perfect for your next adventure!")
    
    # Recent bookings
    if st.session_state.booking_history:
        st.subheader("📚 Recent Bookings")
        for booking in st.session_state.booking_history[-5:]:  # Show last 5
            with st.expander(f"{booking['type']} Booking - {booking['id']}", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Type:** {booking['type']}")
                    st.write(f"**Date:** {booking['date']}")
                with col2:
                    if 'route' in booking['details']:
                        st.write(f"**Route:** {booking['details']['route']}")
                    if 'passengers' in booking['details']:
                        st.write(f"**Passengers:** {booking['details']['passengers']}")
                with col3:
                    if 'total_cost' in booking['details']:
                        st.write(f"**Cost:** ₹{booking['details']['total_cost']:,}")
                    if 'travel_date' in booking['details']:
                        st.write(f"**Travel Date:** {booking['details']['travel_date']}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666;">
    <p>🌍 <strong>Enhanced Travel Planner</strong> - Your AI-powered travel companion</p>
    <p>✈️ Safe travels and happy adventures! 🚆</p>
</div>
""", unsafe_allow_html=True)
