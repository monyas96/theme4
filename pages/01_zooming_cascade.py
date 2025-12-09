"""
Design 1: The Zooming Cascade
Animated scrollytelling experience with three sequential sections.
"""
import streamlit as st
import sys
from pathlib import Path

# set_page_config MUST be the first Streamlit command
st.set_page_config(
    page_title="DRM Framework - Zooming Cascade",
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

# Import config
try:
    from app_core.config.pillars_config import PILLARS, TOPICS
except ImportError:
    PILLARS = {}
    TOPICS = {}

# === Custom Styling ===
st.markdown("""
<style>
    .section-container {
        min-height: 100vh;
        padding: 3rem 2rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .nexus-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #002B7F;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .nexus-title::before {
        content: "→";
        color: #666;
        font-size: 1.2rem;
    }
    
    /* Section 1: Non-clickable concept diagram */
    .pillar-card {
        pointer-events: none;
        cursor: default;
    }
    
    /* Section 2: Faded/dimmed pillars */
    .pillar-faded {
        opacity: 0.25;
        filter: grayscale(70%);
        transform: scale(0.85);
        transition: all 0.5s ease;
    }
    
    .pillar-focused {
        opacity: 1;
        transform: scale(1.1);
        z-index: 10;
        position: relative;
    }
    
    .pillar-focus-card {
        background: linear-gradient(135deg, rgba(0, 114, 188, 0.15) 0%, rgba(0, 114, 188, 0.05) 100%);
        border-radius: 20px;
        padding: 3rem 2rem;
        border: 4px solid #0072BC;
        box-shadow: 0 8px 32px rgba(0, 114, 188, 0.2);
        text-align: center;
        margin: 2rem 0;
    }
    
    .theme-4-only {
        background: linear-gradient(135deg, rgba(0, 127, 255, 0.1) 0%, rgba(0, 127, 255, 0.05) 100%);
        border: 3px solid #007FFF;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 6px 24px rgba(0, 127, 255, 0.15);
    }
    
    /* Section 3: Topic card container */
    .topic-card-wrapper {
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    
    .topic-card {
        flex: 1;
        display: flex;
        flex-direction: column;
        min-height: 180px;
    }
    
    .topic-card p {
        flex-grow: 1;
    }
    
    .topic-card-buttons {
        margin-top: 1rem;
        display: flex;
        gap: 0.5rem;
    }
    
    /* Style for primary Explore buttons - ensure orange accent */
    button[data-testid*="topic_4"] {
        background: linear-gradient(135deg, #F26C2B 0%, #E85A1F 100%) !important;
        background-color: #F26C2B !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }
    
    button[data-testid*="topic_4"]:hover {
        background: linear-gradient(135deg, #E85A1F 0%, #D1490F 100%) !important;
        background-color: #E85A1F !important;
    }
    
    /* Style for secondary CTA buttons - distinct orange gradient */
    button[data-testid*="linkage"] {
        background: linear-gradient(135deg, #E87722 0%, #F26C2B 100%) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        padding: 0.5rem 0.8rem !important;
        white-space: normal !important;
        line-height: 1.3 !important;
    }
    
    button[data-testid*="linkage"]:hover {
        background: linear-gradient(135deg, #F26C2B 0%, #E85A1F 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 3px 10px rgba(232, 119, 34, 0.25) !important;
    }
    
    
    .theme-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .theme-card.highlight {
        border-color: #007FFF;
        box-shadow: 0 4px 12px rgba(0, 127, 255, 0.3);
        transform: scale(1.05);
    }
    
    .theme-card.ghost {
        opacity: 0.3;
        filter: grayscale(80%);
    }
    
    .topic-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border-left: 5px solid #0072BC;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .topic-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }
    
    .narrative-text {
        font-size: 1.1rem;
        line-height: 1.8;
        color: #333;
        margin: 2rem 0;
        padding: 1.5rem;
        background: rgba(0, 43, 127, 0.03);
        border-radius: 10px;
        border-left: 4px solid #E87722;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to render topic card with buttons
def render_topic_card(topic_num, title, description, topic_route, has_linkage=False):
    """Render a topic card with buttons, ensuring proper alignment."""
    with st.container():
        st.markdown(f"""
        <div class="topic-card-wrapper">
            <div class="topic-card">
                <h3>Topic {topic_num}: {title}</h3>
                <p>{description}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # No buttons displayed

# === PAGE TITLE ===
st.markdown("""
<div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
    <h1 style="color: #002B7F; font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem;">
        Evidence Policy Making in Practice
    </h1>
    <h2 style="color: #0072BC; font-size: 1.8rem; font-weight: 400;">
        The case of DRM
    </h2>
</div>
""", unsafe_allow_html=True)

# === SECTION 1: Four Pillars Constellation ===
# Paragraph 1 at the top
PARAGRAPH_1 = """
Lasting peace is unattainable without addressing the structural drivers of instability—economic vulnerability, social exclusion, and weak governance. This is why Africa's development rests on four interdependent pillars: durable peace requires sustainable development; sustainable development requires sustainable financing; sustainable financing requires control over economic flows; and that control requires strong institutions. These pillars form a virtuous cycle of transformation—not sequential steps, but a dynamic system where each reinforces the others. Any strategy that treats them separately will fail Therefore, the most urgent leverage point in this cycle is securing the financial resources necessary to power the entire system.
"""

st.markdown(f"""
<div class="narrative-text">
{PARAGRAPH_1}
</div>
""", unsafe_allow_html=True)

# Simple single row of four pillars
st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <h3 style="color: #002B7F; font-size: 1.5rem; font-weight: 700; margin-bottom: 2rem;">The Four Pillars of the Development Nexus</h3>
</div>
""", unsafe_allow_html=True)

pillars_data = [
    {"num": 1, "title": "Durable Peace", "color": "#1B75BB", "desc": "Requires Sustainable Development"},
    {"num": 2, "title": "Sustainable Financing", "color": "#0072BC", "desc": "Requires Sustainable Development"},
    {"num": 3, "title": "Control Over Flows", "color": "#3B9C9C", "desc": "Requires Sustainable Financing"},
    {"num": 4, "title": "Strong Institutions", "color": "#264653", "desc": "Requires Control Over Flows"}
]

# Single row with 4 columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    p = pillars_data[0]
    st.markdown(f"""
    <div class="pillar-card" style="pointer-events: none; cursor: default;">
        <div class="pillar-icon" style="background-color: {p['color']};">{p['num']}</div>
        <h3>{p['title']}</h3>
        <p>{p['desc']}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    p = pillars_data[1]
    st.markdown(f"""
    <div class="pillar-card" style="pointer-events: none; cursor: default;">
        <div class="pillar-icon" style="background-color: {p['color']};">{p['num']}</div>
        <h3>{p['title']}</h3>
        <p>{p['desc']}</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    p = pillars_data[2]
    st.markdown(f"""
    <div class="pillar-card" style="pointer-events: none; cursor: default;">
        <div class="pillar-icon" style="background-color: {p['color']};">{p['num']}</div>
        <h3>{p['title']}</h3>
        <p>{p['desc']}</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    p = pillars_data[3]
    st.markdown(f"""
    <div class="pillar-card" style="pointer-events: none; cursor: default;">
        <div class="pillar-icon" style="background-color: {p['color']};">{p['num']}</div>
        <h3>{p['title']}</h3>
        <p>{p['desc']}</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# === SECTION 2: Pillar 2 Focus ===
# Paragraph 2 at the top
PARAGRAPH_2 = """
Since sustainable development requires sustainable financing. Countries cannot invest in infrastructure, education, or institutions without funding that is not only substantial but also enduring and resilient. Dependence on volatile external flows—aid, debt, commodity exports—leaves nations unable to align resources with local priorities or plan for long-term growth. Without nationally owned financing, transformation remains theoretical. Overcoming this dependency requires a decisive shift toward national control of capital flows and internal investment capabilities.
"""

st.markdown(f"""
<div class="narrative-text">
{PARAGRAPH_2}
</div>
""", unsafe_allow_html=True)

# Visual zoom: Faded pillars in a line with focused Pillar 2 in center
pillar_col1, pillar_col2, pillar_col3, pillar_col4 = st.columns([1, 2, 1, 1])

with pillar_col1:
    # Faded Pillar 1
    st.markdown("""
    <div class="pillar-faded" style="opacity: 0.3; filter: grayscale(80%);">
        <div style="background: #f0f0f0; border-radius: 12px; padding: 1rem; text-align: center; border: 1px solid rgba(0,0,0,0.1);">
            <div style="width: 40px; height: 40px; border-radius: 50%; background: #9e9e9e; margin: 0 auto 0.5rem; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 1.2rem;">1</div>
            <div style="font-size: 0.8rem; color: #999;">Durable Peace</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with pillar_col2:
    # Focused Pillar 2 - slightly smaller
    st.markdown("""
    <div class="pillar-focus-card" style="background: linear-gradient(135deg, rgba(0, 114, 188, 0.15) 0%, rgba(0, 114, 188, 0.08) 100%); border: 4px solid #0072BC; border-radius: 20px; padding: 2rem 1.5rem; box-shadow: 0 8px 32px rgba(0, 114, 188, 0.2); text-align: center; margin: 2rem 0;">
        <div class="pillar-icon" style="background-color: #0072BC; width: 60px; height: 60px; border-radius: 50%; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: 800; color: white; box-shadow: 0 4px 16px rgba(0, 114, 188, 0.3);">2</div>
        <h3 style="color: #002B7F; margin-bottom: 0; font-size: 1.2rem; font-weight: 700; line-height: 1.4;">Sustainable Development Requires Sustainable Financing</h3>
    </div>
    """, unsafe_allow_html=True)
    
with pillar_col3:
    # Faded Pillar 3
    st.markdown("""
    <div class="pillar-faded" style="opacity: 0.3; filter: grayscale(80%);">
        <div style="background: #f0f0f0; border-radius: 12px; padding: 1rem; text-align: center; border: 1px solid rgba(0,0,0,0.1);">
            <div style="width: 40px; height: 40px; border-radius: 50%; background: #9e9e9e; margin: 0 auto 0.5rem; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 1.2rem;">3</div>
            <div style="font-size: 0.8rem; color: #999;">Control Over Flows</div>
        </div>
            </div>
            """, unsafe_allow_html=True)

with pillar_col4:
    # Faded Pillar 4
    st.markdown("""
    <div class="pillar-faded" style="opacity: 0.3; filter: grayscale(80%);">
        <div style="background: #f0f0f0; border-radius: 12px; padding: 1rem; text-align: center; border: 1px solid rgba(0,0,0,0.1);">
            <div style="width: 40px; height: 40px; border-radius: 50%; background: #9e9e9e; margin: 0 auto 0.5rem; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 1.2rem;">4</div>
            <div style="font-size: 0.8rem; color: #999;">Strong Institutions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Theme 4 card below the divider
st.markdown("""
<div class="theme-4-only" style="background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1); border: 2px solid #007FFF; max-width: 800px; margin: 2rem auto; text-align: center;">
    <h3 style="color: #007FFF; margin-bottom: 1rem; font-size: 1.3rem; font-weight: 700;">Theme 4: DRM Institutions</h3>
    <p style="color: #555; line-height: 1.6; font-size: 1rem; margin: 0;">Building robust tax, budgeting, and capital-market systems while incentivizing private investment.</p>
</div>
""", unsafe_allow_html=True)

# === SECTION 3: Theme 4 Deep Dive ===
# Paragraph 3 at the top
PARAGRAPH_3 = """
Domestic Resource Mobilization (DRM) is how countries create the fiscal space to guide their own policy processes. Strengthening tax systems, improving public expenditure efficiency, developing capital markets, and curbing illicit flows—these are not technical exercises. They are the mechanisms that allow African states to mobilize and manage domestic resources sustainably. This tool translates the DRM framework into measurable indicators and actionable evidence, so you can identify leverage points, track performance, and inform policy decisions.
"""

st.markdown(f"""
<div class="narrative-text">
{PARAGRAPH_3}
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Topic cards in 2x2 grid
topic_col1, topic_col2 = st.columns(2)

with topic_col1:
    # Topic 4.1 with secondary CTA
    render_topic_card(
        "4.1",
        "Public Expenditures",
        "Efficient management of public funds ensures allocation toward priority sectors and responsible spending.",
        "pages/3_topic_4_1.py",
        has_linkage=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Topic 4.3
    render_topic_card(
        "4.3",
        "Capital Markets",
        "Well-developed capital markets channel savings into productive investments, promoting economic growth.",
        "pages/5_topic_4_3.py",
        has_linkage=False
    )

with topic_col2:
    # Topic 4.2 with secondary CTA
    render_topic_card(
        "4.2",
        "Budget and Tax Revenues",
        "Strengthening tax administration and expanding the taxpayer base for mobilizing domestic resources.",
        "pages/4_topic_4_2.py",
        has_linkage=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Topic 4.4
    render_topic_card(
        "4.4",
        "Illicit Financial Flows",
        "Addressing IFFs helps retain domestic resources by curbing trade mispricing, tax evasion, and corruption.",
        "pages/6_topic_4_4.py",
        has_linkage=False
    )

# Add spacing before CTA button
st.markdown("<br><br><br>", unsafe_allow_html=True)

# CTA Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("→ Explore DRM Framework", type="primary", use_container_width=True):
        st.switch_page("pages/2_theme_4.py")

