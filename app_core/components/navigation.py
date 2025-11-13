"""
Reusable navigation component for pages.
Provides Home button with orange styling and home icon.
"""
import streamlit as st
import base64
from pathlib import Path


def render_page_logo(position="top-right"):
    """
    Render the OSAA logo on any page.
    
    Args:
        position: Where to position the logo ("top-right", "top-left", "top-center")
    """
    # Load and encode the logo image
    logo_path = Path("logos/OSAA additional graphic (1).png")
    
    if not logo_path.exists():
        return
    
    try:
        with open(logo_path, "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode()
            
            # Position CSS
            position_css = {
                "top-right": "top: 4rem; right: 1rem;",  # Moved down to avoid Home button
                "top-left": "top: 1rem; left: 1rem;",
                "top-center": "top: 1rem; left: 50%; transform: translateX(-50%);",
                "header-right": "top: 0.5rem; right: 1rem;",  # Near top but not fixed
                "content-top-right": "position: absolute; top: 0; right: 0; margin: 1rem;"
            }
            
            css_position = position_css.get(position, position_css["top-right"])
            
            # Use absolute positioning within relative container for better control
            use_fixed = position != "content-top-right"
            position_type = "fixed" if use_fixed else "absolute"
            
            logo_html = f"""
            <style>
                .page-logo-container {{
                    position: {position_type};
                    {css_position}
                    z-index: 999;
                    max-height: 70px;
                    max-width: 180px;
                }}
                .page-logo-container img {{
                    max-height: 70px;
                    max-width: 180px;
                    height: auto;
                    width: auto;
                    opacity: 0.9;
                }}
                @media (max-width: 768px) {{
                    .page-logo-container {{
                        max-height: 50px;
                        max-width: 130px;
                        top: 3.5rem !important;
                    }}
                    .page-logo-container img {{
                        max-height: 50px;
                        max-width: 130px;
                    }}
                }}
            </style>
            <div class="page-logo-container">
                <img src="data:image/png;base64,{img_data}" alt="OSAA Logo">
            </div>
            """
            st.markdown(logo_html, unsafe_allow_html=True)
    except Exception as e:
        # Silently fail if logo can't be loaded
        pass


def render_navigation_buttons():
    """
    Render Home navigation button in the upper right corner.
    Uses st.page_link for proper browser history support.
    """
    # Navigation button CSS styling - Load with high priority
    st.markdown("""
    <style>
        /* High priority override for Streamlit page_link styling */
        .nav-buttons-container {
            display: flex;
            gap: 0.5rem;
            justify-content: flex-end;
            margin-bottom: 0.5rem !important;
            margin-top: 0.5rem !important;
        }
        /* Style page_link to look beautiful: elegant orange button with gradient */
        /* Target all possible Streamlit page_link variations */
        a[href*="0_home"],
        a[href*="/pages/0_home"],
        a[href*="pages/0_home"],
        a[data-testid*="nav_home"],
        div[data-testid*="nav_home"] > a,
        div[data-testid="stPageLink"] a[href*="0_home"],
        div[data-testid="stPageLink"] a[href*="/pages/0_home"],
        [data-testid="stPageLink"] a,
        div[data-baseweb="button"] a[href*="0_home"],
        .stPageLink a[href*="0_home"],
        .stPageLink a[href*="/pages/0_home"] {
            background: linear-gradient(135deg, #F26C2B 0%, #E85A1F 100%) !important;
            background-color: #F26C2B !important;
            background-image: linear-gradient(135deg, #F26C2B 0%, #E85A1F 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-width: 0 !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            letter-spacing: 0.5px !important;
            text-decoration: none !important;
            padding: 0.7rem 1.8rem !important;
            border-radius: 30px !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: 100% !important;
            box-shadow: 0 3px 10px rgba(242, 108, 43, 0.25), 
                        0 1px 3px rgba(0, 0, 0, 0.1) !important;
            position: relative !important;
            overflow: hidden !important;
            min-height: 44px !important;
        }
        a[href*="0_home"]::before,
        a[href*="/pages/0_home"]::before,
        a[href*="pages/0_home"]::before,
        a[data-testid*="nav_home"]::before,
        div[data-testid*="nav_home"] > a::before,
        div[data-testid="stPageLink"] a[href*="0_home"]::before,
        [data-testid="stPageLink"] a::before {
            content: '' !important;
            position: absolute !important;
            top: 0 !important;
            left: -100% !important;
            width: 100% !important;
            height: 100% !important;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent) !important;
            transition: left 0.5s ease !important;
            z-index: 1 !important;
        }
        a[href*="0_home"]:hover::before,
        a[href*="/pages/0_home"]:hover::before,
        a[href*="pages/0_home"]:hover::before,
        a[data-testid*="nav_home"]:hover::before,
        div[data-testid*="nav_home"] > a:hover::before,
        div[data-testid="stPageLink"] a[href*="0_home"]:hover::before,
        [data-testid="stPageLink"] a:hover::before {
            left: 100% !important;
        }
        a[href*="0_home"]:hover,
        a[href*="/pages/0_home"]:hover,
        a[href*="pages/0_home"]:hover,
        a[data-testid*="nav_home"]:hover,
        div[data-testid*="nav_home"] > a:hover,
        div[data-testid="stPageLink"] a[href*="0_home"]:hover,
        [data-testid="stPageLink"] a:hover {
            background: linear-gradient(135deg, #E85A1F 0%, #D1490F 100%) !important;
            background-color: #E85A1F !important;
            background-image: linear-gradient(135deg, #E85A1F 0%, #D1490F 100%) !important;
            color: #FFFFFF !important;
            text-decoration: none !important;
            box-shadow: 0 6px 20px rgba(242, 108, 43, 0.35), 
                        0 2px 6px rgba(0, 0, 0, 0.15) !important;
            transform: translateY(-2px) !important;
        }
        a[href*="0_home"]:active,
        a[href*="/pages/0_home"]:active,
        a[href*="pages/0_home"]:active,
        a[data-testid*="nav_home"]:active,
        div[data-testid*="nav_home"] > a:active,
        div[data-testid="stPageLink"] a[href*="0_home"]:active,
        [data-testid="stPageLink"] a:active {
            transform: translateY(0px) !important;
            box-shadow: 0 2px 8px rgba(242, 108, 43, 0.3) !important;
        }
        /* Also style button if it exists (for backward compatibility) */
        button[data-testid*="nav_home"],
        div[data-testid*="nav_home"] > button {
            background: linear-gradient(135deg, #F26C2B 0%, #E85A1F 100%) !important;
            background-color: #F26C2B !important;
            color: #FFFFFF !important;
            border: none !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            letter-spacing: 0.5px !important;
            border-radius: 30px !important;
            padding: 0.7rem 1.8rem !important;
            box-shadow: 0 3px 10px rgba(242, 108, 43, 0.25), 
                        0 1px 3px rgba(0, 0, 0, 0.1) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        button[data-testid*="nav_home"]:hover,
        div[data-testid*="nav_home"] > button:hover {
            background: linear-gradient(135deg, #E85A1F 0%, #D1490F 100%) !important;
            background-color: #E85A1F !important;
            color: #FFFFFF !important;
            box-shadow: 0 6px 20px rgba(242, 108, 43, 0.35), 
                        0 2px 6px rgba(0, 0, 0, 0.15) !important;
            transform: translateY(-2px) !important;
        }
        button[data-testid*="nav_home"]:active,
        div[data-testid*="nav_home"] > button:active {
            transform: translateY(0px) !important;
            box-shadow: 0 2px 8px rgba(242, 108, 43, 0.3) !important;
        }
        .home-icon {
            width: 18px;
            height: 18px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-right: 8px;
            vertical-align: middle;
            transition: transform 0.3s ease;
        }
        a[href*="0_home"]:hover .home-icon,
        a[href*="/pages/0_home"]:hover .home-icon,
        a[data-testid*="nav_home"]:hover .home-icon,
        div[data-testid*="nav_home"] > a:hover .home-icon {
            transform: scale(1.1);
        }
    </style>
    <div class="nav-buttons-container">
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 0.15])
    with col1:
        pass  # Empty space on left
    with col2:
        # Use st.page_link instead of st.button + st.switch_page for browser history support
        # st.page_link creates proper browser history entries (no key parameter supported)
        st.page_link("pages/0_home.py", label="Home")

    # Add home icon styling via JavaScript (st.page_link doesn't support custom icons easily)
    st.markdown("""
    <script>
        function initNavigation() {
            // Find home link - try multiple selectors
            let homeLink = document.querySelector('a[href*="0_home"], a[href*="/pages/0_home"], a[href*="pages/0_home"]');
            if (!homeLink) {
                // Try finding by text content
                const allLinks = document.querySelectorAll('a');
                for (let link of allLinks) {
                    if (link.textContent.trim() === 'Home' && (link.href.includes('0_home') || link.href.includes('home'))) {
                        homeLink = link;
                        break;
                    }
                }
            }
            
            if (homeLink && homeLink.textContent.trim() === 'Home') {
                // Apply beautiful styling directly via JavaScript
                homeLink.style.cssText = `
                    background: linear-gradient(135deg, #F26C2B 0%, #E85A1F 100%) !important;
                    background-color: #F26C2B !important;
                    background-image: linear-gradient(135deg, #F26C2B 0%, #E85A1F 100%) !important;
                    color: #FFFFFF !important;
                    border: none !important;
                    border-width: 0 !important;
                    font-weight: 600 !important;
                    font-size: 0.95rem !important;
                    letter-spacing: 0.5px !important;
                    text-decoration: none !important;
                    padding: 0.7rem 1.8rem !important;
                    border-radius: 30px !important;
                    display: inline-flex !important;
                    align-items: center !important;
                    justify-content: center !important;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                    width: 100% !important;
                    box-shadow: 0 3px 10px rgba(242, 108, 43, 0.25), 0 1px 3px rgba(0, 0, 0, 0.1) !important;
                    position: relative !important;
                    overflow: hidden !important;
                    min-height: 44px !important;
                    gap: 0.5rem !important;
                `;
                
                // Add hover effect
                homeLink.addEventListener('mouseenter', function() {
                    this.style.background = 'linear-gradient(135deg, #E85A1F 0%, #D1490F 100%)';
                    this.style.boxShadow = '0 6px 20px rgba(242, 108, 43, 0.35), 0 2px 6px rgba(0, 0, 0, 0.15)';
                    this.style.transform = 'translateY(-2px)';
                });
                homeLink.addEventListener('mouseleave', function() {
                    this.style.background = 'linear-gradient(135deg, #F26C2B 0%, #E85A1F 100%)';
                    this.style.boxShadow = '0 3px 10px rgba(242, 108, 43, 0.25), 0 1px 3px rgba(0, 0, 0, 0.1)';
                    this.style.transform = 'translateY(0)';
                });
                
                // Add home icon if not already present
                const icon = homeLink.querySelector('.home-icon');
                if (!icon && !homeLink.querySelector('svg')) {
                    const iconSpan = document.createElement('span');
                    iconSpan.className = 'home-icon';
                    iconSpan.innerHTML = '<svg viewBox="0 0 24 24" fill="#FFFFFF" xmlns="http://www.w3.org/2000/svg" style="width: 18px; height: 18px; display: inline-block; vertical-align: middle; filter: drop-shadow(0 1px 1px rgba(0,0,0,0.1));"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>';
                    // Insert before the text content
                    const textNode = Array.from(homeLink.childNodes).find(node => node.nodeType === Node.TEXT_NODE);
                    if (textNode) {
                        homeLink.insertBefore(iconSpan, textNode);
                    } else {
                        homeLink.insertBefore(iconSpan, homeLink.firstChild);
                    }
                }
            }
        }
        
        // Initialize on page load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initNavigation);
        } else {
            initNavigation();
        }
        
        // Also run after delays to catch dynamically added elements
        setTimeout(initNavigation, 100);
        setTimeout(initNavigation, 500);
        setTimeout(initNavigation, 1000);
        
        // Use MutationObserver to catch dynamically added elements
        const observer = new MutationObserver(function(mutations) {
            initNavigation();
        });
        observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """, unsafe_allow_html=True)
    
    # Add CSS styling
    st.markdown("""
    <style>
        /* Target page_link elements by href - ensure flex layout */
        a[href*="0_home"],
        a[href*="/pages/0_home"],
        a[href*="pages/0_home"],
        div[data-testid="stPageLink"] a,
        [data-testid="stPageLink"] a {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 0.5rem !important;
        }
        .home-icon {
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 18px !important;
            height: 18px !important;
            transition: transform 0.3s ease !important;
            flex-shrink: 0 !important;
        }
        a[href*="0_home"]:hover .home-icon,
        a[href*="/pages/0_home"]:hover .home-icon,
        a[href*="pages/0_home"]:hover .home-icon,
        div[data-testid="stPageLink"] a:hover .home-icon,
        [data-testid="stPageLink"] a:hover .home-icon {
            transform: scale(1.1) !important;
        }
        /* Override Streamlit's default link styles */
        div[data-testid="stPageLink"] a,
        [data-testid="stPageLink"] a,
        div[data-testid="stPageLink"] a:visited,
        [data-testid="stPageLink"] a:visited {
            color: #FFFFFF !important;
        }
    </style>
    """, unsafe_allow_html=True)

