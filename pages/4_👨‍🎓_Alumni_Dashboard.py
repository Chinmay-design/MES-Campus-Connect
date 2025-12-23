import streamlit as st

def alumni_dashboard_page():
    user = st.session_state.user
    st.markdown(f'<h1 class="main-header">Welcome Back, {user["first_name"]}!</h1>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Connections", "156", "+8")
    with col2:
        st.metric("Mentees", "3", "+1")
    with col3:
        st.metric("Events", "4", "+1")
    with col4:
        st.metric("Contributions", "$2,500", "+$500")
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 🤝 Professional Network")
        
        st.markdown("#### 📨 Connection Requests")
        requests = [
            {"name": "John Carter", "position": "Senior Engineer", "company": "Google", "batch": "2020"},
            {"name": "Priya Sharma", "position": "Product Manager", "company": "Microsoft", "batch": "2021"}
        ]
        
        for req in requests:
            col_a, col_b, col_c = st.columns([3, 1, 1])
            with col_a:
                st.write(f"**{req['name']}**")
                st.caption(f"{req['position']} at {req['company']} | Batch {req['batch']}")
            with col_b:
                if st.button("✅", key=f"acc_{req['name']}"):
                    st.success(f"Connected with {req['name']}")
            with col_c:
                if st.button("❌", key=f"rej_{req['name']}"):
                    st.info(f"Ignored {req['name']}")
        
        st.markdown("#### 💼 Job Opportunities")
        jobs = [
            {"title": "Senior Dev", "company": "Amazon", "location": "Remote"},
            {"title": "Data Scientist", "company": "Meta", "location": "Seattle"}
        ]
        
        for job in jobs:
            with st.expander(f"{job['title']} - {job['company']}"):
                st.write(f"📍 {job['location']}")
                if st.button("Apply", key=f"apply_{job['title']}"):
                    st.info("Application started")
    
    with col2:
        st.markdown("### 🎓 Alumni Reunions")
        reunions = [
            {"batch": "2015", "date": "Apr 15", "location": "Campus"},
            {"batch": "2010", "date": "May 20", "location": "Virtual"}
        ]
        
        for reunion in reunions:
            st.info(f"**{reunion['batch']} Batch**\n📅 {reunion['date']}\n📍 {reunion['location']}")
        
        st.markdown("### 💰 Contribute")
        contribution_type = st.selectbox("Type", ["Scholarship", "Infrastructure", "Mentorship"])
        amount = st.number_input("Amount ($)", min_value=10, value=100)
        if st.button("Donate"):
            st.success(f"Thank you for ${amount} {contribution_type} donation!")
