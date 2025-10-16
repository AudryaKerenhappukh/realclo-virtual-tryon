import streamlit as st
from streamlit_option_menu import option_menu
from modes import photo_fit, build_avatar

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="RealClo – Virtual Try-On",
    layout="wide",
    page_icon="👗"
)

# ================== GLOBAL STYLE ==================
st.markdown("""
    <style>
     .block-container { max-width: 1300px; max-height: 800px; padding: 2rem 0rem; }
     section[data-testid="stSidebar"] { background-color: #F5F1E8; }
     .sidebar-logo { display: block; margin:auto; width: 100px; margin-bottom: 15px; }
     .sidebar-subtitle { font-size: 16px; color: #334155; text-align: center; margin: 0 0 30px 0; }
    </style>
""", unsafe_allow_html=True)

# ================== SIDEBAR ==================
st.sidebar.image("assets/logo.png", use_container_width=False, output_format="PNG")

st.sidebar.markdown(
    '<div class="sidebar-subtitle"><b>Shop smarter, feel confident, and find your perfect fit every time.</b></div>',
    unsafe_allow_html=True
)

with st.sidebar:
    selected = option_menu(
        "",
        ["Photo Fit", "Build Avatar"],
        icons=["camera", "person"],
        default_index=0,
        styles={
            "container": {"background-color": "#F5F1E8"},
            "nav-link": {
                "font-size": "20px",
                "text-align": "left",
                "margin": "5px",
                "color": "#334155"
            },
            "nav-link-selected": {"background-color": "#e0ddd2"},
        }
    )

# ================== MAIN CONTENT ==================
if selected == "Photo Fit":
    photo_fit.run()
elif selected == "Build Avatar":
    build_avatar.run()
