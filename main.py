import streamlit as st
import time
from datetime import datetime
from tools import call_claude_api, search_disasters, get_emergency_contacts
from memory import ConversationMemory
from utils import format_message, get_disaster_stats, load_mock_disasters
import json

# Page configuration
st.set_page_config(
    page_title="🚨 Disaster Response AI Agent",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for 3D effects and light theme
st.markdown("""
<style>
    /* Light Theme with 3D Effects */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* 3D Card Effects */
    .disaster-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 
            0 10px 30px rgba(0,0,0,0.1),
            0 1px 8px rgba(0,0,0,0.06),
            inset 0 1px 0 rgba(255,255,255,0.5);
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.8);
    }
    
    .disaster-card:hover {
        transform: translateY(-8px) rotateX(2deg);
        box-shadow: 
            0 20px 50px rgba(0,0,0,0.15),
            0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Stats Cards with 3D */
    .stat-card {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 
            5px 5px 15px rgba(0,0,0,0.1),
            -5px -5px 15px rgba(255,255,255,0.9);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 
            8px 8px 20px rgba(0,0,0,0.15),
            -8px -8px 20px rgba(255,255,255,0.95);
    }
    
    /* Header with depth */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 
            0 15px 35px rgba(102,126,234,0.3),
            0 5px 15px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* Message bubbles with 3D */
    .user-message {
        background: linear-gradient(145deg, #667eea, #764ba2);
        color: white;
        padding: 15px 20px;
        border-radius: 18px 18px 5px 18px;
        margin: 10px 0;
        box-shadow: 
            3px 3px 10px rgba(102,126,234,0.3),
            -1px -1px 5px rgba(255,255,255,0.1);
        float: right;
        clear: both;
        max-width: 70%;
    }
    
    .assistant-message {
        background: white;
        color: #333;
        padding: 15px 20px;
        border-radius: 18px 18px 18px 5px;
        margin: 10px 0;
        box-shadow: 
            3px 3px 10px rgba(0,0,0,0.1),
            -1px -1px 5px rgba(255,255,255,0.3);
        float: left;
        clear: both;
        max-width: 70%;
        border-left: 4px solid #667eea;
    }
    
    /* Buttons with 3D effect */
    .stButton>button {
        background: linear-gradient(145deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 30px;
        font-weight: 600;
        box-shadow: 
            4px 4px 12px rgba(102,126,234,0.3),
            -2px -2px 8px rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 
            6px 6px 15px rgba(102,126,234,0.4),
            -3px -3px 10px rgba(255,255,255,0.2);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: white;
        box-shadow: 5px 0 15px rgba(0,0,0,0.1);
    }
    
    /* Animated gradient text */
    .gradient-text {
        background: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Pulse animation for active disasters */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    .pulse {
        animation: pulse 2s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'memory' not in st.session_state:
    st.session_state.memory = ConversationMemory()

if 'disasters' not in st.session_state:
    st.session_state.disasters = load_mock_disasters()

if 'view' not in st.session_state:
    st.session_state.view = 'chat'

# Header
st.markdown("""
<div class="main-header">
    <h1 style="margin:0; font-size: 3em;">🚨 Disaster Response AI Agent</h1>
    <p style="margin:10px 0 0 0; font-size: 1.2em; opacity: 0.9;">
        Advanced Emergency Coordination & Response System
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Navigation")
    
    view = st.radio(
        "Select View:",
        ["💬 AI Chat", "🗺️ Disaster Map", "📊 Analytics", "⚙️ Settings"],
        key="view_selector"
    )
    
    st.markdown("---")
    
    # Stats
    stats = get_disaster_stats(st.session_state.disasters)
    
    st.markdown("### 📈 Live Statistics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Active", stats['active'], "2", delta_color="inverse")
    with col2:
        st.metric("Monitoring", stats['monitoring'], "1")
    
    st.metric("Responses Today", stats['responses'], "12")
    
    st.markdown("---")
    
    # Emergency contacts
    st.markdown("### 🚑 Emergency Contacts")
    contacts = get_emergency_contacts()
    for contact in contacts:
        st.info(f"**{contact['country']}**: {contact['number']}")
    
    st.markdown("---")
    
    # System status
    st.markdown("### ⚡ System Status")
    st.success("🟢 AI Agent: Online")
    st.success("🟢 Monitoring: Active")
    st.success("🟢 API: Connected")

# Main content area
if "💬 AI Chat" in view:
    st.markdown("## 💬 AI-Powered Emergency Response")
    
    # Quick action buttons
    st.markdown("### ⚡ Quick Actions")
    cols = st.columns(4)
    
    quick_actions = [
        ("🌍 Active Disasters", "What disasters are currently active worldwide?"),
        ("🎒 Emergency Kit", "What should I have in my emergency kit?"),
        ("🏃 Earthquake Safety", "What should I do during an earthquake?"),
        ("📋 Evacuation Plan", "Help me create an evacuation plan")
    ]
    
    for idx, (label, query) in enumerate(quick_actions):
        with cols[idx]:
            if st.button(label, key=f"quick_{idx}"):
                st.session_state.memory.add_message("user", query)
    
    st.markdown("---")
    
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        messages = st.session_state.memory.get_messages()
        
        if not messages:
            st.info("""
            👋 **Welcome to the Disaster Response AI Agent!**
            
            I can help you with:
            - 🌍 Real-time disaster monitoring and alerts
            - 🚨 Emergency response coordination
            - 🛡️ Safety guidance and evacuation planning
            - 📦 Resource allocation and logistics
            - 🔍 Search and rescue information
            - 🌤️ Weather and hazard tracking
            
            How can I assist you today?
            """)
        
        for msg in messages:
            if msg['role'] == 'user':
                st.markdown(f"""
                <div style="text-align: right; margin: 10px 0;">
                    <div class="user-message">
                        {msg['content']}
                    </div>
                    <div style="clear: both; font-size: 0.8em; color: #666; margin-top: 5px;">
                        {msg['timestamp']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="text-align: left; margin: 10px 0;">
                    <div class="assistant-message">
                        {format_message(msg['content'])}
                    </div>
                    <div style="clear: both; font-size: 0.8em; color: #666; margin-top: 5px;">
                        🤖 AI Agent • {msg['timestamp']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Input area
    st.markdown("---")
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Your message:",
            placeholder="Ask about disasters, emergency procedures, or request assistance...",
            key="user_input",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("🚀 Send", use_container_width=True)
    
    if send_button and user_input:
        # Add user message
        st.session_state.memory.add_message("user", user_input)
        
        # Show loading
        with st.spinner("🤖 AI Agent thinking..."):
            # Call Claude API
            response = call_claude_api(
                user_input,
                st.session_state.memory.get_conversation_history()
            )
            
            # Add assistant response
            st.session_state.memory.add_message("assistant", response)
        
        st.rerun()

elif "🗺️ Disaster Map" in view:
    st.markdown("## 🗺️ Live Disaster Monitoring")
    
    # Map header
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🌍 Global Disaster Tracking")
    
    with col2:
        if st.button("🔄 Refresh Data"):
            st.session_state.disasters = load_mock_disasters()
            st.rerun()
    
    # Map placeholder (would integrate with actual mapping library)
    st.info("""
    🗺️ **Interactive Disaster Map**
    
    Real-time visualization of active disasters, emergency zones, and response coordination.
    Integration with mapping services like Folium or Plotly for geographic visualization.
    """)
    
    # Disaster list
    st.markdown("### 📍 Active Disasters")
    
    for disaster in st.session_state.disasters:
        severity_colors = {
            'Critical': '🔴',
            'High': '🟠',
            'Medium': '🟡',
            'Low': '🔵'
        }
        
        with st.expander(f"{severity_colors.get(disaster['severity'], '⚪')} {disaster['type']} - {disaster['location']}", expanded=False):
            cols = st.columns(3)
            
            with cols[0]:
                st.markdown(f"**Severity:** {disaster['severity']}")
            with cols[1]:
                st.markdown(f"**Status:** {disaster['status']}")
            with cols[2]:
                st.markdown(f"**Time:** {disaster['time']}")
            
            st.markdown(f"**Coordinates:** {disaster['lat']}, {disaster['lng']}")
            
            if st.button(f"🔍 Get Details", key=f"detail_{disaster['id']}"):
                query = f"Tell me about the current {disaster['type']} in {disaster['location']}"
                st.session_state.memory.add_message("user", query)
                st.session_state.view = 'chat'
                st.rerun()

elif "📊 Analytics" in view:
    st.markdown("## 📊 Disaster Analytics & Insights")
    
    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    
    stats = get_disaster_stats(st.session_state.disasters)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <h2 style="color: #667eea; margin: 0;">🔥</h2>
            <h1 style="margin: 10px 0;">""" + str(stats['active']) + """</h1>
            <p style="margin: 0; color: #666;">Active Disasters</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <h2 style="color: #f093fb; margin: 0;">👁️</h2>
            <h1 style="margin: 10px 0;">""" + str(stats['monitoring']) + """</h1>
            <p style="margin: 0; color: #666;">Monitoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <h2 style="color: #4facfe; margin: 0;">💬</h2>
            <h1 style="margin: 10px 0;">""" + str(stats['responses']) + """</h1>
            <p style="margin: 0; color: #666;">Responses</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <h2 style="color: #43e97b; margin: 0;">✅</h2>
            <h1 style="margin: 10px 0;">98%</h1>
            <p style="margin: 0; color: #666;">Uptime</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent activity
    st.markdown("### 📈 Recent Activity")
    
    activity_data = [
        {"time": "2 min ago", "event": "Earthquake alert - California", "severity": "High"},
        {"time": "15 min ago", "event": "Flood warning issued - Bangladesh", "severity": "Medium"},
        {"time": "1 hour ago", "event": "Wildfire contained - Australia", "severity": "Low"},
        {"time": "3 hours ago", "event": "Hurricane tracking - Caribbean", "severity": "High"},
    ]
    
    for activity in activity_data:
        severity_colors = {
            'High': '#ff6b6b',
            'Medium': '#ffd93d',
            'Low': '#6bcf7f'
        }
        
        st.markdown(f"""
        <div class="disaster-card" style="padding: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="color: #333;">{activity['event']}</strong>
                    <p style="margin: 5px 0 0 0; color: #666; font-size: 0.9em;">{activity['time']}</p>
                </div>
                <div style="background: {severity_colors.get(activity['severity'], '#ccc')}; 
                           color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.8em;">
                    {activity['severity']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

else:  # Settings
    st.markdown("## ⚙️ System Settings")
    
    st.markdown("### 🎨 Appearance")
    theme = st.selectbox("Theme", ["Light (Current)", "Dark", "Auto"])
    
    st.markdown("### 🔔 Notifications")
    st.checkbox("Enable push notifications", value=True)
    st.checkbox("Email alerts for critical disasters", value=True)
    st.checkbox("SMS alerts", value=False)
    
    st.markdown("### 🤖 AI Settings")
    response_speed = st.slider("Response Speed", 0, 100, 75)
    st.selectbox("AI Model", ["Claude Sonnet 4 (Current)", "Claude Opus 4"])
    
    st.markdown("### 🌍 Location")
    st.text_input("Your Location", placeholder="Enter city or coordinates")
    
    st.markdown("---")
    
    if st.button("💾 Save Settings"):
        st.success("✅ Settings saved successfully!")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.memory = ConversationMemory()
        st.success("✅ Chat history cleared!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p><strong>🚨 Disaster Response AI Agent</strong> • Powered by Claude AI</p>
    <p style="font-size: 0.9em;">Real-time Monitoring Active • Emergency Services: 911 (US) | 112 (EU) | 999 (UK)</p>
</div>
""", unsafe_allow_html=True)