"""
Design 2: The Split-Screen Lens
Interactive two-column layout with framework visualization and mission narrative.
"""
import streamlit as st
import sys
from pathlib import Path

# set_page_config MUST be the first Streamlit command
st.set_page_config(
    page_title="DRM Framework - Split Screen",
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
    /* Vertical Rhythm - Normalized spacing */
    .section-spacing {
        margin-bottom: 1.5rem;
    }
    
    .section-spacing-tight {
        margin-bottom: 0.75rem;
    }
    
    /* Column Wrappers - Consolidated styling */
    .left-column-wrapper {
        padding: 2rem;
        margin-right: 0.5rem;
        position: relative;
    }
    
    .right-column-wrapper {
        padding: 2rem;
        margin-left: 0.5rem;
        position: relative;
    }
    
    /* Pillar Items - Consolidated */
    .pillar-item {
        padding: 1rem;
        margin: 0.4rem 0;
        border-radius: 8px;
        border-left: 4px solid;
        background: white;
        transition: all 0.3s ease;
    }
    
    .pillar-item.highlight {
        background: linear-gradient(135deg, rgba(232, 119, 34, 0.15) 0%, rgba(232, 119, 34, 0.08) 100%);
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(232, 119, 34, 0.2);
    }
    
    /* Pillar Map - Consolidated */
    .pillar-map {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 0.75rem;
    }
    
    .pillar-map h4 {
        color: #E87722;
        margin-bottom: 1rem;
        font-size: 1.1rem;
        font-weight: 700;
    }
    
    /* Theme List - Tightened spacing */
    .theme-list {
        margin-left: 1.5rem;
        margin-top: 0.5rem;
    }
    
    .theme-item {
        padding: 0.5rem;
        margin: 0.2rem 0;
        border-radius: 6px;
        font-size: 0.9rem;
    }
    
    .theme-item.highlight {
        background: rgba(232, 119, 34, 0.15);
        font-weight: 700;
    }
    
    /* Topic Grid - Consolidated */
    .topic-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-top: 0.75rem;
    }
    
    .topic-mini-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #E87722;
        text-align: center;
        font-size: 0.85rem;
    }
    
    /* Callout Boxes - Increased padding, consolidated styling */
    .callout-box {
        border-radius: 8px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 114, 188, 0.1);
        border-left: 4px solid #0072BC;
        background: linear-gradient(135deg, rgba(0, 114, 188, 0.1) 0%, rgba(0, 114, 188, 0.05) 100%);
    }
    
    .callout-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #002B7F;
    }
    
    .callout-text {
        font-size: 1rem;
        line-height: 1.7;
        color: #333;
    }
    
    /* Header Bar - Consolidated */
    .header-bar {
        background: #F0F4F8;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        display: flex;
        gap: 0.5rem;
    }
    
    .header-cell {
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 6px;
        text-align: center;
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    .header-cell.orange {
        flex: 1.2;
        background: #E87722;
    }
    
    .header-cell.blue {
        flex: 1;
        background: #0072BC;
    }
    
</style>
""", unsafe_allow_html=True)

# === Page Title ===
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
    
# === Pillar 2 Intro (Conceptual Link) ===
st.markdown("""
<div class="callout-box" style="background: linear-gradient(135deg, rgba(0, 114, 188, 0.08) 0%, rgba(0, 114, 188, 0.04) 100%); border-left-color: #0072BC;">
    <div class="callout-title" style="color: #0072BC;">Theme 4 is part of a Logical Framework</div>
    <div class="callout-text">
        The Nexus Policy Conceptual Framework links OSAA's <strong>Logical Framework</strong> (the Pillars) with its <strong>Measurement Framework</strong> (the Themes and Topics). This translates the causal logic of Africa's development pathways into actionable indicators and data analytics. For this Exploratory Data Product Theme 4: DRM is the crucial translation layer that converts the systemic logic of Sustainable Financing (Pillar 2) into the measurable indicators necessary for policy evaluation.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='section-spacing'></div>", unsafe_allow_html=True)

# === Header Bar with Colored Cells ===
st.markdown("""
<div class="header-bar">
    <div class="header-cell orange">Nexus Pillars: The Structure</div>
    <div class="header-cell blue">The Argument</div>
    </div>
    """, unsafe_allow_html=True)
    
# === Row 1: Four Pillars + The Challenge ===
pillar_col, challenge_col = st.columns([1.2, 1])

with pillar_col:
    st.markdown('<div class="left-column-wrapper">', unsafe_allow_html=True)
    
    pillars = [
        {"num": 1, "title": "Durable Peace", "color": "#1B75BB", "highlight": False},
        {"num": 2, "title": "Sustainable Financing", "color": "#0072BC", "highlight": True},
        {"num": 3, "title": "Control Over Flows", "color": "#3B9C9C", "highlight": False},
        {"num": 4, "title": "Strong Institutions", "color": "#264653", "highlight": False}
    ]
    
    for pillar in pillars:
        highlight_class = "highlight" if pillar["highlight"] else ""
        st.markdown(f"""
        <div class="pillar-item {highlight_class}" style="border-left-color: {pillar['color']};">
            <strong style="color: {pillar['color']};">Pillar {pillar['num']}:</strong> {pillar['title']}
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with challenge_col:
    st.markdown('<div class="right-column-wrapper">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="callout-box challenge">
        <div class="callout-title">The Challenge</div>
        <div class="callout-text">
            Dependence on volatile external flows—aid, debt, commodity exports—leaves nations unable to align resources with local priorities or plan for long-term growth. Without nationally owned financing, transformation remains theoretical.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div class='section-spacing'></div>", unsafe_allow_html=True)
    
# === Row 2: Pillar 2 Themes + The Target ===
theme_col, target_col = st.columns([1.2, 1])

with theme_col:
    st.markdown('<div class="left-column-wrapper">', unsafe_allow_html=True)
    st.markdown("""
    <div class="pillar-map">
        <h4>Pillar 2: Themes</h4>
        <div class="theme-list">
            <div class="theme-item">Theme 1: Debt Management</div>
            <div class="theme-item">Theme 2: Value Chains</div>
            <div class="theme-item">Theme 3: Ownership</div>
            <div class="theme-item highlight">Theme 4: DRM Institutions</div>
            <div class="theme-item">Theme 5: Derisking</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with target_col:
    st.markdown('<div class="right-column-wrapper">', unsafe_allow_html=True)
    st.markdown("""
    <div class="callout-box target">
        <div class="callout-title">The Target (Your Mission)</div>
        <div class="callout-text">
            Our mission is to establish the fiscal space for nationally owned growth through <strong>Domestic Resource Mobilization (DRM)</strong>. This means strengthening tax systems, improving public expenditure efficiency, developing capital markets, and curbing illicit flows—the mechanisms that allow African states to mobilize and manage domestic resources sustainably.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div class='section-spacing-tight'></div>", unsafe_allow_html=True)

# === Row 3: Theme 4 Topics + Call to Action ===
topic_col, action_col = st.columns([1.2, 1])

with topic_col:
    st.markdown('<div class="left-column-wrapper">', unsafe_allow_html=True)
    st.markdown("""
    <div class="pillar-map">
        <h4>Theme 4: Topics</h4>
        <div class="topic-grid">
            <div class="topic-mini-card">4.1 Public Expenditures</div>
            <div class="topic-mini-card">4.2 Budget & Tax</div>
            <div class="topic-mini-card">4.3 Capital Markets</div>
            <div class="topic-mini-card">4.4 Illicit Flows</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
with action_col:
    st.markdown('<div class="right-column-wrapper">', unsafe_allow_html=True)
    st.markdown("""
    <div class="callout-box action">
        <div class="callout-title">Call to Action</div>
        <div class="callout-text">
            Use the <strong>Pillars on the left</strong> to zoom directly into the DRM Topics. Navigate through Pillar 2 → Theme 4 to explore the four core topics: Public Expenditures, Budget & Tax Revenues, Capital Markets, and Illicit Financial Flows.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div class='section-spacing'></div>", unsafe_allow_html=True)
    
# === Row 4: CTA Button ===
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("→ Explore DRM Framework", type="primary", use_container_width=True):
        st.switch_page("pages/2_theme_4.py")
