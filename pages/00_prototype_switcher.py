"""
Landing Page Prototype Switcher
Allows users to select and view different DRM landing page prototypes.
"""
import streamlit as st
import sys
from pathlib import Path

# set_page_config MUST be the first Streamlit command
st.set_page_config(
    page_title="DRM Landing Page Prototypes",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add parent directory to path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import navigation component (logo only, no home button since we're on the main page)
try:
    from app_core.components.navigation import render_page_logo
    render_page_logo("top-right")
except ImportError:
    pass

# --- Load OSAA CSS ---
try:
    with open("app_core/styles/style_osaa.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

# Hide sidebar completely
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        display: none !important;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }
    .stApp > header {
        visibility: hidden;
        height: 0;
    }
    .stApp > div:first-child {
        padding-top: 0;
    }
</style>
""", unsafe_allow_html=True)

# === Custom Styling ===
st.markdown("""
<style>
    .prototype-header {
        background: linear-gradient(135deg, #002B7F 0%, #0072BC 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-bottom: 3rem;
        text-align: center;
    }
    
    .prototype-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
    }
    
    .prototype-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin: 0;
    }
    
    .prototype-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border-left: 5px solid #E87722;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .prototype-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }
    
    .prototype-title {
        color: #002B7F;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .prototype-description {
        color: #555;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# === Page Content ===
st.markdown("""
<div class="prototype-header">
    <h1>DRM Landing Page Prototypes</h1>
    <p>Select a prototype to test different user experiences for Theme 4: Domestic Resource Mobilization</p>
</div>
""", unsafe_allow_html=True)

# Prototype descriptions
prototypes = [
    {
        "id": "01_zooming_cascade",
        "title": "Design 1: The Zooming Cascade",
        "description": "Animated scrollytelling experience with three sequential sections: Four Pillars → Pillar 2 Focus → Theme 4 Deep Dive",
        "features": "Sequential storytelling, framework education, visual hierarchy",
        "file": "pages/01_zooming_cascade.py"
    },
    {
        "id": "02_split_screen",
        "title": "Design 2: The Split-Screen Lens",
        "description": "Interactive two-column layout with framework visualization on the left and mission narrative on the right",
        "features": "Interactive exploration, linked scrolling, side-by-side comparison",
        "file": "pages/02_split_screen.py"
    },
    {
        "id": "04_hero_story",
        "title": "Design 3: The Hero Story",
        "description": "Full-screen hero sections with background images and narrative flow",
        "features": "Visual impact, storytelling, marketing-ready",
        "file": "pages/04_hero_story.py"
    }
]

# Show all prototypes as buttons in a grid
st.markdown("### Choose a Prototype to View")

cols = st.columns(2)

for idx, prototype in enumerate(prototypes):
    with cols[idx % 2]:
        st.markdown(f"""
        <div class="prototype-card">
            <div class="prototype-title">{prototype["title"]}</div>
            <div class="prototype-description">{prototype["description"]}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"View {prototype['title']}", key=f"btn_{prototype['id']}", use_container_width=True, type="primary"):
            st.switch_page(prototype["file"])

