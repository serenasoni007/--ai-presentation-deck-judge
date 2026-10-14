import streamlit as st
import os
from dotenv import load_dotenv
from slide_analyzer import extract_slide_text, evaluate_slides_with_ai

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Presentation Judge Pro", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PROFESSIONAL CSS STYLING ---
st.markdown("""
<style>
    /* Main background & font styling */
    .main {
        background-color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Title Styling */
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 700;
    }
    
    /* Custom Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    div[data-testid="stMetric"] label {
        color: #64748b !important;
        font-weight: 600;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #0f172a;
        font-weight: 700;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        color: #ffffff;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        box-shadow: 0 6px 15px rgba(59, 130, 246, 0.4);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.title("📊 AI Presentation Deck Judge")
st.markdown("Upload your PowerPoint presentation to receive instant, professional AI evaluation on visual hierarchy, content flow, and clarity.")

# Sidebar Upload Controls
with st.sidebar:
    st.header("Upload Center")
    st.markdown("Upload your slide deck in PowerPoint format.")
    uploaded_deck = st.file_uploader("Upload Presentation (.pptx)", type=["pptx"])
    
    st.divider()
    run_analysis = st.button("Run AI Evaluation", use_container_width=True)

# Main Execution Flow
if run_analysis:
    if not uploaded_deck:
        st.warning("⚠️ Please upload a PowerPoint presentation (`.pptx`) to run the evaluation.")
    else:
        with st.spinner("Analyzing slides, structure, and visual clarity with Gemini AI..."):
            # Save temporary file locally for processing
            deck_path = "temp_deck.pptx"
            with open(deck_path, "wb") as f:
                f.write(uploaded_deck.getbuffer())
            
            # Run Slide Analyzer
            slide_data = extract_slide_text(deck_path)
            ai_slide_feedback = evaluate_slides_with_ai(slide_data)
            
            # Clean up temporary file
            os.remove(deck_path)

        st.success("✨ Evaluation Complete!")
        
        # Metric Scorecards Banner
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Slides Analyzed", len(slide_data))
        col2.metric("Primary Engine", "Google Gemini 1.5")
        col3.metric("Status", "Optimized")
        
        st.divider()

        # Dashboard Tab / Display Section
        st.subheader("📋 Comprehensive Presentation Audit")
        
        # Displaying the AI feedback in a clean structured container
        with st.container():
            st.markdown(ai_slide_feedback)

else:
    # Landing Placeholder
    st.markdown("""
        <div style="background-color: #ffffff; padding: 40px; border-radius: 12px; border: 1px dashed #cbd5e1; text-align: center; margin-top: 20px;">
            <h3>👋 Welcome to Presentation Judge Pro</h3>
            <p style="color: #64748b;">Get expert-level critique on your pitch decks and presentations instantly.</p>
            <p style="color: #3b82f6; font-weight: 600;">👉 Upload your `.pptx` file in the sidebar and click 'Run AI Evaluation' to get started.</p>
        </div>
    """, unsafe_allow_html=True)