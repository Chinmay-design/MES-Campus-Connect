import streamlit as st
from utils.database import db
import re

def student_signup_page():
    st.markdown('<h1 class="main-header">Student Registration</h1>', unsafe_allow_html=True)
    
    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name *")
            date_of_birth = st.date_input("Date of Birth *")
            email = st.text_input("Email *")
            year = st.selectbox("Year *", ["1st Year PUC", "2nd Year PUC"])
            login_id = st.text_input("Login ID *")
            security_answer = st.text_input("Security Answer *", type="password")
        
        with col2:
            last_name = st.text_input("Last Name *")
            id_card_number = st.text_input("ID Card Number *")
            contact_number = st.text_input("Contact Number *")
            stream = st.selectbox("Stream *", ["Science", "Commerce", "Arts"])
            password = st.text_input("Password *", type="password")
            confirm_password = st.text_input("Confirm Password *", type="password")
        
        security_question = st.selectbox("Security Question *", [
            "What is your mother's maiden name?",
            "What was your first pet's name?"
        ])
        
        hobbies = st.text_area("Hobbies & Interests *")
        section = st.selectbox("Section", ["A", "B", "C", "Not Assigned"])
        
        if st.form_submit_button("Create Account"):
            # Validation
            if password != confirm_password:
                st.error("Passwords don't match")
            elif len(password) < 8:
                st.error("Password must be 8+ characters")
            elif not re.search(r"[A-Z]", password):
                st.error("Password needs uppercase")
            elif not re.search(r"[a-z]", password):
                st.error("Password needs lowercase")
            elif not re.search(r"\d", password):
                st.error("Password needs number")
            elif not re.search(r"[@$!%*?&]", password):
                st.error("Password needs special character")
            else:
                user_data = {
                    'login_id': login_id,
                    'email': email,
                    'password': password,
                    'first_name': first_name,
                    'last_name': last_name,
                    'date_of_birth': date_of_birth.strftime('%Y-%m-%d'),
                    'id_card_number': id_card_number,
                    'year': year,
                    'stream': stream,
                    'section': section,
                    'contact_number': contact_number,
                    'security_question': security_question,
                    'security_answer': security_answer,
                    'hobbies': hobbies,
                    'role': 'student',
                    'status': 'pending'
                }
                
                user_id = db.create_user(user_data)
                if user_id:
                    st.success("Account created! Pending admin approval.")
                    if st.button("Go to Login"):
                        st.session_state.page = "login"
                        st.rerun()
