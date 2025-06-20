import streamlit as st
import pandas as pd
import os
import pages.planting as planting
print(dir(planting))  # This will list all functions and variables in the file

# Set wide layout for Streamlit
st.set_page_config(page_title="AgriPredictor", layout="wide")

# ------------------ SESSION STATE INIT ------------------ #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_info" not in st.session_state:
    st.session_state.user_info = {}

# ------------------ LOGIN FORM ------------------ #
state_districts = {
    "Maharashtra": ["Mumbai City", "Pune", "Nagpur", "Nashik", "Thane", "Aurangabad", "Solapur", "Amravati", "Kolhapur", "Satara"],
    "Karnataka": ["Bagalkot", "Ballari", "Belagavi", "Bengaluru Rural", "Bengaluru Urban", "Bidar", "Chamarajanagar", "Chikkaballapur", "Chikkamagaluru", "Chitradurga", "Dakshina Kannada", "Davanagere", "Dharwad", "Gadag", "Hassan", "Haveri", "Kalaburagi", "Kodagu", "Kolar", "Koppal", "Mandya", "Mysuru", "Raichur", "Ramanagara", "Shivamogga", "Tumakuru", "Udupi", "Uttara Kannada", "Vijayapura", "Yadgir"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem"],
    "Gujarat": ["Ahmedabad", "Amreli", "Anand", "Aravalli", "Banaskantha", "Bharuch", "Bhavnagar", "Botad", "Chhota Udaipur", "Dahod", "Dang", "Devbhoomi Dwarka", "Gandhinagar", "Gir Somnath", "Jamnagar", "Junagadh", "Kheda", "Kutch", "Mahisagar", "Mehsana", "Morbi", "Narmada", "Navsari", "Panchmahal", "Patan", "Porbandar", "Rajkot", "Sabarkantha", "Surat", "Surendranagar", "Tapi", "Vadodara", "Valsad"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra", "Noida", "Prayagraj"],
    "Andhra Pradesh": ["Anantapur", "Chittoor", "East Godavari", "Guntur", "Krishna", "Kurnool", "Nellore", "Prakasam", "Srikakulam", "Visakhapatnam", "Vizianagaram", "West Godavari", "YSR Kadapa"],
    "Arunachal Pradesh": [...],
    "Assam": [...],
    "Bihar": [...],
    "Chhattisgarh": [...],
    "Goa": ["North Goa", "South Goa"],
    "Haryana": [...],
    "Himachal Pradesh": [...],
    "Jharkhand": [...]
}

# ------------------ LOGIN SCREEN ------------------ #
if not st.session_state.logged_in:
    st.title("👨‍🌾 AgriPredictor - Farmer Login")

    if "selected_state" not in st.session_state:
        st.session_state.selected_state = list(state_districts.keys())[0]

    st.session_state.selected_state = st.selectbox(
        "State", list(state_districts.keys()),
        index=list(state_districts.keys()).index(st.session_state.selected_state)
    )

    selected_state = st.session_state.selected_state
    selected_district = st.selectbox("District", state_districts[selected_state])

    with st.form("login_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        nationality = st.selectbox("Nationality", ["Indian", "Other"])
        login_btn = st.form_submit_button("Login")

    if login_btn:
        if name and email and phone:
            st.session_state.logged_in = True
            st.session_state.user_info = {
                "name": name,
                "email": email,
                "phone": phone,
                "nationality": nationality,
                "state": selected_state,
                "district": selected_district
            }
            st.success(f"✅ Welcome {name} from {selected_district}, {selected_state}!")
            st.rerun()
        else:
            st.warning("⚠️ Please fill in all fields to log in.")

    st.stop()

# ------------------ LOGGED IN UI ------------------ #
user = st.session_state.user_info

# Show Sidebar only after login
with st.sidebar:
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_info = {}
        st.success("🔒 You have been logged out.")
        st.rerun()

    with st.expander("👤 Profile"):
        st.markdown(f"**👨‍🌾 Name:** {user['name']}")
        st.markdown(f"**📧 Email:** {user['email']}")
        st.markdown(f"**📱 Phone:** {user['phone']}")
        st.markdown(f"**🌐 Nationality:** {user['nationality']}")
        st.markdown(f"**📍 Location:** {user['district']}, {user['state']}")

    selected_section = st.radio(
        "📂 Navigation",
        [
            "🏠 Dashboard",
            "🧪 Fertilizer Recommendation",
            "🌾 Crop Recommendation",
            "📈 Commodity Price Forecast",
            "📅 Crop Season & Income Guide",
            "🌿 General Planting Procedures",
            "📊 Agmarknet Prices"
        ]
    )

# Main Greeting
st.success(f"✅ Welcome {user['name']} from {user['district']}, {user['state']}!")

# ------------------ LOAD PAGE MODULES ------------------ #
if selected_section == "🏠 Dashboard":
    import pages.dashboard as dashboard
    dashboard.show()

elif selected_section == "🧪 Fertilizer Recommendation":
    import pages.fertilizer as fertilizer
    fertilizer.show()

elif selected_section == "🌾 Crop Recommendation":
    import pages.crop as crop
    crop.show()

elif selected_section == "📈 Commodity Price Forecast":
    import pages.forecast as forecast
    forecast.show()

elif selected_section == "📅 Crop Season & Income Guide":
    import pages.season_income as season_income
    season_income.show()

elif selected_section == "🌿 General Planting Procedures":
    import pages.planting as planting
    planting.show()

elif selected_section == "📊 Agmarknet Prices":
    import pages.agmarknet as agmarknet
    agmarknet.show()
