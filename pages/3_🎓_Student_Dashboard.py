import streamlit as st

def student_dashboard_page():
    user = st.session_state.user
    st.markdown(f'<h1 class="main-header">Welcome, {user["first_name"]}!</h1>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Friends", "24", "+3")
    with col2:
        st.metric("Groups", "5", "+1")
    with col3:
        st.metric("Events", "3", "0")
    with col4:
        st.metric("Messages", "12", "+2")
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 📢 Recent Announcements")
        announcements = [
            {"title": "Hackathon 2024", "date": "2h ago", "content": "Registration open"},
            {"title": "Exam Schedule", "date": "1d ago", "content": "Final exams schedule"}
        ]
        for ann in announcements:
            with st.expander(f"{ann['title']} - {ann['date']}"):
                st.write(ann['content'])
        
        st.markdown("### ⚡ Quick Actions")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("Find Friends"):
                st.session_state.page = "friends"
                st.rerun()
        with col_b:
            if st.button("Post Confession"):
                st.session_state.page = "confessions"
                st.rerun()
        with col_c:
            if st.button("Create Group"):
                st.session_state.page = "groups"
                st.rerun()
    
    with col2:
        st.markdown("### 📅 Upcoming Events")
        events = [
            {"name": "Alumni Talk", "date": "Mar 20", "time": "3 PM"},
            {"name": "Coding Contest", "date": "Mar 22", "time": "10 AM"}
        ]
        for event in events:
            st.info(f"**{event['name']}**\n📅 {event['date']} | ⏰ {event['time']}")
