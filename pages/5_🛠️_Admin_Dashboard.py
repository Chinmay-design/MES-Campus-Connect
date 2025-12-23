import streamlit as st
import pandas as pd
import plotly.express as px

def admin_dashboard_page():
    st.markdown('<h1 class="main-header">Admin Dashboard</h1>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Users", "1,245", "+23")
    with col2:
        st.metric("Active Today", "342", "-12")
    with col3:
        st.metric("Pending Approvals", "15", "+3")
    with col4:
        st.metric("Groups", "48", "+2")
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "👨‍🎓 Student Management", "👨‍🎓 Alumni Management"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### User Distribution")
            user_data = pd.DataFrame({
                'Role': ['Students', 'Alumni', 'Admins'],
                'Count': [800, 400, 45]
            })
            fig = px.pie(user_data, values='Count', names='Role')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Daily Activity")
            activity_data = pd.DataFrame({
                'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'Users': [300, 320, 350, 380, 400, 250, 200]
            })
            fig = px.line(activity_data, x='Day', y='Users')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        from pages.student_management import student_management_section
        student_management_section()
    
    with tab3:
        from pages.alumni_management import alumni
