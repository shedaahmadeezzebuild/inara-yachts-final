import streamlit as st
import requests
import json
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Inara Yachts - Charter & Sales Bot",
    page_icon="⛵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional 3D UI
st.markdown("""
<style>
    /* Color Variables */
    :root {
        --primary: #1e3a8a;
        --secondary: #0ea5e9;
        --accent: #f97316;
        --success: #10b981;
        --dark: #0f172a;
        --light: #f0f9ff;
    }
    
    /* Global Styles */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%);
        box-shadow: 4px 0 15px rgba(0, 0, 0, 0.2);
    }
    
    [data-testid="stSidebar"] [data-testid="stRadio"] {
        padding: 12px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.1);
        margin: 8px 0;
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] [data-testid="stRadio"]:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(5px);
    }
    
    /* Metrics Styling */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.9);
        padding: 16px;
        border-radius: 12px;
        border-left: 4px solid #0ea5e9;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 28px rgba(14, 165, 233, 0.6);
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
    }
    
    /* Chat Message Styling */
    [data-testid="chatAvatarIcon"] {
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
        transition: transform 0.3s ease;
    }
    
    [data-testid="chatAvatarIcon"]:hover {
        transform: scale(1.1);
    }
    
    /* Info Box Styling */
    .stInfo, [data-testid="stMarkdownContainer"] > div > div > div > p > .stAlert {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
        border: 1px solid rgba(14, 165, 233, 0.3);
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    /* Text Input */
    [data-testid="stTextInput"] input {
        border-radius: 10px;
        border: 2px solid #e0f2fe !important;
        padding: 12px 16px !important;
        font-size: 14px;
        transition: all 0.3s ease;
        background: white;
    }
    
    [data-testid="stTextInput"] input:focus {
        border: 2px solid #0ea5e9 !important;
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1);
    }
    
    /* Header Typography */
    h1 {
        color: #1e3a8a;
        font-weight: 800;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    h2, h3 {
        color: #1e40af;
        font-weight: 700;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #0ea5e9, transparent);
        margin: 20px 0;
    }
    
    /* Sidebar Text */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: white;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: #e0f2fe;
    }
    
    /* Form Container */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e0f2fe;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    }
    
    /* Custom Icon Animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .icon-float {
        animation: float 3s ease-in-out infinite;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
MISTRAL_API_KEY = "SsDvv0v2AToQqVj1pDOZSUAFyd0VtnXa"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-large-latest"

# Load data from JSON files
@st.cache_resource
def load_knowledge_base():
    """Load all charter and sales data from JSON files"""
    knowledge_data = {
        "charters": [],
        "sales": [],
        "metadata": {},
        "faq_index": {}
    }
    
    try:
        # Load charter batches
        for batch_num in range(1, 5):
            file_path = f"inara_charter_batch_{batch_num}.json"
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    knowledge_data["charters"].extend(data.get("faq_items", []))
                    if batch_num == 1:
                        knowledge_data["metadata"] = data.get("metadata", {})
        
        # Load sales batches
        for batch_num in range(1, 3):
            file_path = f"inara_sales_batch_{batch_num}.json"
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    knowledge_data["sales"].extend(data.get("faq_items", []))
        
        # Create FAQ index for quick lookup
        for item in knowledge_data["charters"] + knowledge_data["sales"]:
            keywords = item.get("trigger_keywords", [])
            for keyword in keywords:
                if keyword not in knowledge_data["faq_index"]:
                    knowledge_data["faq_index"][keyword] = []
                knowledge_data["faq_index"][keyword].append(item)
        
        return knowledge_data
    except Exception as e:
        st.warning(f"Note: Knowledge base files loaded with status: {str(e)}")
        return knowledge_data

# Load knowledge base
knowledge_base = load_knowledge_base()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_mode" not in st.session_state:
    st.session_state.conversation_mode = "General Inquiry"

# Sidebar configuration
with st.sidebar:
    # Professional header
    col_logo, col_text = st.columns([0.3, 0.7])
    with col_logo:
        st.image("logo.jpg", width=70)
    with col_text:
        st.markdown("<h2 style='margin: 15px 0 0 0; font-size: 18px;'>Inara Yachts</h2><p style='margin: 2px 0 0 0; font-size: 11px; opacity: 0.9;'>AI Charter & Sales</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Service Type Section
    st.markdown("<h3 style='color: white; margin-top: 15px;'>Service Type</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #e0f2fe; font-size: 12px; margin-bottom: 10px;'>What can we help you with?</p>", unsafe_allow_html=True)
    
    service_options = {
        "General Inquiry": "General Inquiry",
        "Charter Booking": "Charter Booking",
        "Yacht Sales": "Yacht Sales",
        "Fleet Information": "Fleet Information",
        "Contact & Support": "Contact & Support"
    }
    
    selected_option = st.radio(
        "Select service:",
        list(service_options.keys()),
        key="mode_radio",
        label_visibility="collapsed"
    )
    st.session_state.conversation_mode = service_options[selected_option]
    
    st.markdown("")
    st.markdown("---")
    
    # Fleet Overview Section
    st.markdown("<h3 style='color: white;'>Fleet Overview</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: rgba(255,255,255,0.08); padding: 12px; border-radius: 8px; border-left: 3px solid #0ea5e9;'>
        <p style='color: #e0f2fe; font-size: 13px; margin: 0;'><b>Luxury Yacht Fleet</b></p>
        <p style='color: #e0f2fe; font-size: 11px; margin: 5px 0 0 0;'>
            Cruising Yachts: 30-80ft<br>
            Motor Yachts: 45-120ft<br>
            Sailing Yachts: 35-100ft<br>
            Catamarans: 40-75ft
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("---")
    
    # Knowledge Base Stats
    st.markdown("<h3 style='color: white;'>Knowledge Base</h3>", unsafe_allow_html=True)
    col_kb1, col_kb2 = st.columns(2)
    with col_kb1:
        st.metric("Charter FAQs", len(knowledge_base["charters"]), delta="Live")
    with col_kb2:
        st.metric("Sales FAQs", len(knowledge_base["sales"]), delta="Live")
    
    st.markdown(f"<p style='text-align: center; color: #e0f2fe; font-size: 11px; margin-top: 10px;'>Model: mistral-large</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Action Button
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main content header
main_col1, main_col2 = st.columns([0.15, 0.85], vertical_alignment="center", gap="medium")
with main_col1:
    st.image("header_logo.jpg", width=100)
with main_col2:
    st.markdown("""
    <div>
        <h1 style='margin: 0; color: #1e3a8a; font-size: 36px;'>Welcome to Inara Yachts</h1>
        <p style='margin: 8px 0 0 0; color: #0ea5e9; font-size: 16px; font-weight: 600;'>Your Premier Yacht Charter & Sales Partner</p>
        <p style='margin: 8px 0 0 0; color: #64748b; font-size: 13px;'>Powered by AI • Enterprise-Grade Service</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown("")

# Display mode
st.markdown(f"""
<div style='display: flex; align-items: center; justify-content: space-between; background: linear-gradient(90deg, rgba(14, 165, 233, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%); padding: 15px 20px; border-radius: 12px; border: 1px solid rgba(14, 165, 233, 0.2); margin-bottom: 20px;'>
    <div>
        <p style='margin: 0; color: #1e3a8a; font-weight: 600;'>Current Mode</p>
        <h3 style='margin: 5px 0 0 0; color: #0284c7; font-size: 18px;'>{st.session_state.conversation_mode}</h3>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# System prompt based on mode
system_prompts = {
    "General Inquiry": """You are a professional concierge for Inara Yachts, a luxury yacht charter and sales company. 
You provide information about our services, fleet, and answer general inquiries about yachting experiences. 
Be welcoming, professional, and knowledgeable about luxury yacht services.""",
    
    "Charter Booking": """You are a yacht charter specialist for Inara Yachts. 
Help clients book luxury yacht charters by understanding their dates, location preferences, group size, budget, and specific requirements.
Provide detailed information about available vessels, itineraries, and pricing.
Always confirm booking details and explain the next steps in the reservation process.""",
    
    "Yacht Sales": """You are a yacht sales consultant for Inara Yachts with expertise in luxury yacht brokerage.
Help buyers find the perfect yacht that matches their needs, budget, and lifestyle.
Discuss yacht specifications, features, prices, financing options, and guide them through the purchase process.
Highlight Inara Yachts' unique value proposition and after-sales services.""",
    
    "Fleet Information": """You are a fleet specialist for Inara Yachts.
Provide detailed information about our yacht fleet including specifications, features, capacity, amenities, and availability.
Answer questions about different yacht types, sizes, and their ideal use cases.
Create comprehensive fleet information based on typical luxury yacht offerings.""",
    
    "Contact & Support": """You are a customer support specialist for Inara Yachts.
Help clients with inquiries about contact information, office locations, support services, and general assistance.
Provide information about booking modifications, cancellations, and customer service channels.""",
}

def call_mistral_api(user_message):
    """Call the Mistral AI API with knowledge base integration"""
    try:
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Prepare messages with system prompt
        system_prompt = system_prompts.get(st.session_state.conversation_mode, system_prompts["General Inquiry"])
        
        # Add knowledge base context
        kb_context = ""
        if st.session_state.conversation_mode == "Charter Booking":
            charter_samples = knowledge_base["charters"][:5]
            if charter_samples:
                kb_context = "\n\nRelevant Charter Information:\n"
                for item in charter_samples:
                    kb_context += f"- {item.get('question', '')}\n  {item.get('answer', '')}\n"
        elif st.session_state.conversation_mode == "Yacht Sales":
            sales_samples = knowledge_base["sales"][:5]
            if sales_samples:
                kb_context = "\n\nRelevant Sales Information:\n"
                for item in sales_samples:
                    kb_context += f"- {item.get('question', '')}\n  {item.get('answer', '')}\n"
        
        system_prompt_enhanced = system_prompt + kb_context
        
        messages = [
            {"role": "system", "content": system_prompt_enhanced}
        ]
        
        # Add conversation history
        for msg in st.session_state.messages:
            messages.append(msg)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        payload = {
            "model": MISTRAL_MODEL,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1500
        }
        
        response = requests.post(MISTRAL_API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        assistant_message = result['choices'][0]['message']['content']
        return assistant_message
    
    except requests.exceptions.RequestException as e:
        return f"⚠️ Error connecting to AI service: {str(e)}"
    except Exception as e:
        return f"⚠️ An error occurred: {str(e)}"

# Display chat history
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar="user_avatar.jpg"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant", avatar="logo.jpg"):
                st.markdown(message["content"])

# Chat input
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([0.85, 0.15], gap="medium")
    with col1:
        user_input = st.text_input(
            "Your message:",
            placeholder="Ask about yacht charters, sales, fleet details, or general inquiries...",
            label_visibility="collapsed"
        )
    with col2:
        submit_button = st.form_submit_button("Send", use_container_width=True)

if submit_button and user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with chat_container:
        with st.chat_message("user", avatar="user_avatar.jpg"):
            st.markdown(user_input)
    
    # Get AI response
    with st.spinner("🤔 Thinking..."):
        response = call_mistral_api(user_input)
    
    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display assistant response
    with chat_container:
        with st.chat_message("assistant", avatar="logo.jpg"):
            st.markdown(response)
    
    st.rerun()

# Footer
st.markdown("")
st.markdown(f"""
<div style='text-align: center; background: linear-gradient(180deg, rgba(30, 58, 138, 0.1) 0%, rgba(14, 165, 233, 0.1) 100%); padding: 30px 20px; border-radius: 15px; border-top: 2px solid rgba(14, 165, 233, 0.3); margin-top: 30px;'>
    <h3 style='margin: 0 0 10px 0; color: #1e3a8a;'>Inara Yachts</h3>
    <p style='margin: 5px 0; color: #0284c7; font-weight: 500; font-size: 14px;'>Premium Yacht Charter & Sales Platform</p>
    <hr style='margin: 15px 0; border: 1px solid rgba(14, 165, 233, 0.2);'>
    <div style='display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin: 15px 0; font-size: 12px; color: #64748b;'>
        <span><b>AI:</b> Mistral Large</span>
        <span>•</span>
        <span><b>Knowledge:</b> {len(knowledge_base['charters']) + len(knowledge_base['sales'])} FAQ Items</span>
        <span>•</span>
        <span><b>Live:</b> 2026</span>
    </div>
    <hr style='margin: 15px 0; border: 1px solid rgba(14, 165, 233, 0.2);'>
    <p style='margin: 10px 0; color: #1e3a8a; font-weight: 500;'>Your journey to luxury yachting starts here</p>
    <p style='margin: 5px 0; color: #64748b; font-size: 12px;'>info@inarayachts.com | +1-800-YACHTS-1</p>
</div>
""", unsafe_allow_html=True)
