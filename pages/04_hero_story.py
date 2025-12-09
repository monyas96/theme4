"""
Design 4: The Hero Story
Full-screen hero sections with background images and narrative flow.
"""
import streamlit as st
import sys
from pathlib import Path

# set_page_config MUST be the first Streamlit command
st.set_page_config(
    page_title="DRM Framework - Hero Story",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add parent directory to path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import navigation component
try:
    from app_core.components.navigation import render_navigation_buttons, render_page_logo
    render_page_logo("top-right")
    render_navigation_buttons()
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
</style>
""", unsafe_allow_html=True)

# === Custom Styling ===
st.markdown("""
<style>
    .hero-section {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, rgba(0, 43, 127, 0.85) 0%, rgba(0, 114, 188, 0.85) 100%),
                    url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600"><rect fill="%23002B7F" width="1200" height="600"/><path d="M0,300 Q300,200 600,300 T1200,300" stroke="rgba(255,255,255,0.1)" stroke-width="2" fill="none"/></svg>');
        background-size: cover;
        background-position: center;
        color: white;
        position: relative;
        border-radius: 0;
        margin: -1rem -1rem 0 -1rem;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        color: white;
    }
    
    .hero-subtitle {
        font-size: 1.8rem;
        font-weight: 400;
        margin-bottom: 2rem;
        color: #E87722;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    .scroll-indicator {
        position: absolute;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateX(-50%) translateY(0); }
        50% { transform: translateX(-50%) translateY(-10px); }
    }
    
    .story-section {
        min-height: 80vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 4rem 2rem;
        background: linear-gradient(180deg, #F9FAFB 0%, #FFFFFF 100%);
        margin: 2rem 0;
        border-radius: 16px;
    }
    
    .story-section.alt {
        background: linear-gradient(180deg, #FFFFFF 0%, #F9FAFB 100%);
    }
    
    .story-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #002B7F;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .story-content {
        font-size: 1.2rem;
        line-height: 2;
        color: #333;
        max-width: 900px;
        margin: 0 auto;
        text-align: center;
    }
    
    .pillars-minimal {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin: 2rem auto;
        max-width: 1000px;
    }
    
    .pillar-mini {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        text-align: center;
        border-top: 4px solid;
    }
    
    .cta-section {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #E87722 0%, #F26C2B 100%);
        border-radius: 16px;
        color: white;
        margin: 2rem 0;
    }
    
    .cta-section h2 {
        color: white;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .cta-section p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# === Hero 1: Title ===
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">Evidence Policy Making in Practice</h1>
    <h2 class="hero-subtitle">The Case of DRM</h2>
    <div class="scroll-indicator">Scroll to explore ↓</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# === Hero 2: Context ===
PARAGRAPH_1 = """
Lasting peace is unattainable without addressing the structural drivers of instability—economic vulnerability, social exclusion, and weak governance. This is why Africa's development rests on four interdependent pillars: durable peace requires sustainable development; sustainable development requires sustainable financing; sustainable financing requires control over economic flows; and that control requires strong institutions. These pillars form a virtuous cycle of transformation—not sequential steps, but a dynamic system where each reinforces the others. Any strategy that treats them separately will fail.
"""

st.markdown(f"""
<div class="story-section">
    <h2 class="story-title">Part of a Larger System</h2>
    <div class="story-content">
        <p>{PARAGRAPH_1.strip()}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Four Pillars Minimal Visualization
pillars_data = [
    {"num": 1, "title": "Durable Peace", "color": "#1B75BB"},
    {"num": 2, "title": "Sustainable Financing", "color": "#0072BC"},
    {"num": 3, "title": "Control Over Flows", "color": "#3B9C9C"},
    {"num": 4, "title": "Strong Institutions", "color": "#264653"}
]

pillars_html = '<div class="pillars-minimal">'
for p in pillars_data:
    pillars_html += f'<div class="pillar-mini" style="border-top-color: {p["color"]};"><div style="font-size: 2rem; font-weight: 800; color: {p["color"]}; margin-bottom: 0.5rem;">{p["num"]}</div><div style="color: #002B7F; font-weight: 600;">{p["title"]}</div></div>'
pillars_html += '</div>'

st.markdown(pillars_html, unsafe_allow_html=True)

st.markdown("---")

# === Hero 3: Problem ===
PARAGRAPH_2 = """
But sustainable development requires sustainable financing. Countries cannot invest in infrastructure, education, or institutions without funding that is not only substantial but also enduring and resilient. Dependence on volatile external flows—aid, debt, commodity exports—leaves nations unable to align resources with local priorities or plan for long-term growth. Without nationally owned financing, transformation remains theoretical.
"""

st.markdown(f"""
<div class="story-section alt">
    <h2 class="story-title">The Financing Constraint</h2>
    <div class="story-content">
        <p>{PARAGRAPH_2.strip()}</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# === Hero 4: Solution + CTA ===
PARAGRAPH_3 = """
Domestic Resource Mobilization (DRM) is how countries create the fiscal space to guide their own policy processes. Strengthening tax systems, improving public expenditure efficiency, developing capital markets, and curbing illicit flows—these are not technical exercises. They are the mechanisms that allow African states to mobilize and manage domestic resources sustainably. This tool translates the DRM framework into measurable indicators and actionable evidence, so you can identify leverage points, track performance, and inform policy decisions.
"""

st.markdown(f"""
<div class="story-section">
    <h2 class="story-title">The DRM Solution</h2>
    <div class="story-content">
        <p>{PARAGRAPH_3.strip()}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# CTA Button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("→ Explore the Framework", type="primary", use_container_width=True):
        st.switch_page("pages/2_theme_4.py")

