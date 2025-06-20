# app.py
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
    "Arunachal Pradesh": ["Tawang", "West Kameng", "East Kameng", "Papum Pare", "Kurung Kumey", "Kra Daadi", "Lower Subansiri", "Upper Subansiri", "West Siang", "East Siang", "Siang", "Upper Siang", "Lower Siang", "Dibang Valley", "Lower Dibang Valley", "Anjaw", "Lohit", "Namsai", "Changlang", "Tirap", "Longding"],
    "Assam": ["Baksa", "Barpeta", "Biswanath", "Bongaigaon", "Cachar", "Charaideo", "Chirang", "Darrang", "Dhemaji", "Dhubri", "Dibrugarh", "Goalpara", "Golaghat", "Hailakandi", "Hojai", "Jorhat", "Kamrup", "Kamrup Metropolitan", "Karbi Anglong", "Karimganj", "Kokrajhar", "Lakhimpur", "Majuli", "Morigaon", "Nagaon", "Nalbari", "Sivasagar", "Sonitpur", "South Salmara", "Tinsukia", "Udalguri", "West Karbi Anglong"],
    "Bihar": ["Araria", "Arwal", "Aurangabad", "Banka", "Begusarai", "Bhagalpur", "Bhojpur", "Buxar", "Darbhanga", "East Champaran", "Gaya", "Gopalganj", "Jamui", "Jehanabad", "Kaimur", "Katihar", "Khagaria", "Kishanganj", "Lakhisarai", "Madhepura", "Madhubani", "Munger", "Muzaffarpur", "Nalanda", "Nawada", "Patna", "Purnia", "Rohtas", "Saharsa", "Samastipur", "Saran", "Sheikhpura", "Sheohar", "Sitamarhi", "Siwan", "Supaul", "Vaishali", "West Champaran"],
    "Chhattisgarh": ["Balod", "Baloda Bazar", "Balrampur", "Bastar", "Bemetara", "Bijapur", "Bilaspur", "Dantewada", "Dhamtari", "Durg", "Gariaband", "Gaurela Pendra Marwahi", "Janjgir-Champa", "Jashpur", "Kabirdham", "Kanker", "Kondagaon", "Korba", "Korea", "Mahasamund", "Mungeli", "Narayanpur", "Raigarh", "Raipur", "Rajnandgaon", "Sukma", "Surajpur", "Surguja"],
    "Goa": ["North Goa", "South Goa"],
    "Haryana": ["Ambala", "Bhiwani", "Charkhi Dadri", "Faridabad", "Fatehabad", "Gurugram", "Hisar", "Jhajjar", "Jind", "Kaithal", "Karnal", "Kurukshetra", "Mahendragarh", "Nuh", "Palwal", "Panchkula", "Panipat", "Rewari", "Rohtak", "Sirsa", "Sonipat", "Yamunanagar"],
    "Himachal Pradesh": ["Bilaspur", "Chamba", "Hamirpur", "Kangra", "Kinnaur", "Kullu", "Lahaul and Spiti", "Mandi", "Shimla", "Sirmaur", "Solan", "Una"],
    "Jharkhand": ["Bokaro", "Chatra", "Deoghar", "Dhanbad", "Dumka", "East Singhbhum", "Garhwa", "Giridih", "Godda", "Gumla", "Hazaribagh", "Jamtara", "Khunti", "Koderma", "Latehar", "Lohardaga", "Pakur", "Palamu", "Ramgarh", "Ranchi", "Sahibganj", "Seraikela Kharsawan", "Simdega", "West Singhbhum"]
}


if not st.session_state.logged_in:
    st.title("👨‍🌾 AgriPredictor - Farmer Login")
    with st.form("login_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        nationality = st.selectbox("Nationality", ["Indian", "Other"])
        selected_state = st.selectbox("State", list(state_districts.keys()))
        selected_district = st.selectbox("District", state_districts[selected_state])
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

# Sidebar: Logout + Profile
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

# Main Greeting
st.success(f"✅ Welcome {user['name']} from {user['district']}, {user['state']}!")

# ------------------ SECTION ROUTING ------------------ #
selected_section = st.sidebar.radio(
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
