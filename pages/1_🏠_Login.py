import streamlit as st
from utils.database import db

def login_page():
    st.markdown('<h1 class="main-header">MES Connect</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown("### Login")
            login_id = st.text_input("Login ID or Email")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Login As", ["student", "alumni", "admin"])
            
            col_a, col_b = st.columns(2)
            with col_a:
                login_btn = st.form_submit_button("Login")
            with col_b:
                if st.form_submit_button("Forgot Password?"):
                    st.session_state.page = "forgot_password"
            
            if login_btn:
                if login_id and password:
                    user = db.authenticate_user(login_id, password, role)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user = user
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                else:
                    st.error("Please enter credentials")
        
        st.markdown("---")
        if st.button("Student Sign Up"):
            st.session_state.page = "student_signup"
            st.rerun()
