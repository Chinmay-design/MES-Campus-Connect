import streamlit as st
import pandas as pd

# Page config
st.set_page_config(
    page_title="MES Connect",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = "Login"

# Import page functions
from utils.database import db

def main():
    # Sidebar navigation
    if st.session_state.authenticated and st.session_state.user:
        user = st.session_state.user
        
        with st.sidebar:
            st.image("https://via.placeholder.com/150x50/3B82F6/FFFFFF?text=MES+Connect", use_column_width=True)
            st.markdown(f"### 👤 {user['first_name']} {user['last_name']}")
            st.markdown(f"**Role:** {user['role'].title()}")
            
            if user['role'] == 'student':
                pages = ["Dashboard", "Profile", "Friends", "Chat", "Groups", "Confessions", "Events", "Settings"]
            elif user['role'] == 'alumni':
                pages = ["Dashboard", "Profile", "Networking", "Chat", "Groups", "Events", "Contributions", "Settings"]
            else:  # admin
                pages = ["Dashboard", "Student Management", "Alumni Management", "Announcements", "Confession Moderation", "Analytics"]
            
            selected = st.selectbox("Navigation", pages)
            st.session_state.page = selected.replace(" ", "_").lower()
            
            st.markdown("---")
            if st.button("🚪 Logout"):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.session_state.page = "Login"
                st.rerun()
    
    # Page routing
    if not st.session_state.authenticated:
        if st.session_state.page == "login":
            from pages._1_🏠_Login import login_page
            login_page()
        elif st.session_state.page == "student_signup":
            from pages._2_👤_Student_Signup import student_signup_page
            student_signup_page()
    else:
        user = st.session_state.user
        
        if user['role'] == 'student':
            if st.session_state.page == "dashboard":
                from pages._3_🎓_Student_Dashboard import student_dashboard_page
                student_dashboard_page()
            elif st.session_state.page == "profile":
                from pages.student_profile import student_profile_page
                student_profile_page()
            elif st.session_state.page == "friends":
                from pages.friends import friends_page
                friends_page()
            elif st.session_state.page == "chat":
                from pages.chat import chat_page
                chat_page()
            elif st.session_state.page == "groups":
                from pages.groups import groups_page
                groups_page()
            elif st.session_state.page == "confessions":
                from pages.confessions import confessions_page
                confessions_page()
            elif st.session_state.page == "events":
                from pages.events import events_page
                events_page()
            elif st.session_state.page == "settings":
                from pages.settings import settings_page
                settings_page()
        
        elif user['role'] == 'alumni':
            if st.session_state.page == "dashboard":
                from pages._4_👨‍🎓_Alumni_Dashboard import alumni_dashboard_page
                alumni_dashboard_page()
            elif st.session_state.page == "profile":
                from pages.alumni_profile import alumni_profile_page
                alumni_profile_page()
            elif st.session_state.page == "networking":
                from pages.networking import networking_page
                networking_page()
            elif st.session_state.page == "chat":
                from pages.chat import chat_page
                chat_page()
            elif st.session_state.page == "groups":
                from pages.alumni_groups import alumni_groups_page
                alumni_groups_page()
            elif st.session_state.page == "events":
                from pages.alumni_events import alumni_events_page
                alumni_events_page()
            elif st.session_state.page == "contributions":
                from pages.contributions import contributions_page
                contributions_page()
            elif st.session_state.page == "settings":
                from pages.settings import settings_page
                settings_page()
        
        elif user['role'] == 'admin':
            if st.session_state.page == "dashboard":
                from pages._5_🛠️_Admin_Dashboard import admin_dashboard_page
                admin_dashboard_page()
            elif st.session_state.page == "student_management":
                from pages.student_management import student_management_page
                student_management_page()
            elif st.session_state.page == "alumni_management":
                from pages.alumni_management import alumni_management_page
                alumni_management_page()
            elif st.session_state.page == "announcements":
                from pages.admin_announcements import admin_announcements_page
                admin_announcements_page()
            elif st.session_state.page == "confession_moderation":
                from pages.confession_moderation import confession_moderation_page
                confession_moderation_page()

if __name__ == "__main__":
    main()
