import streamlit as st
from PIL import Image
from utils.ui_helpers import load_default_images, show_thumbnail_selector, render_garment_uploader, render_tryon_section

HUMAN_DIR = "assets/model"

def run():
    """Photo Fit page — upload or select a human model, then try on a garment."""
    st.markdown("### 👕 Photo Fit")
    col1, col2, col3 = st.columns(3, gap="large")

    # --- Step 1: Human Image ---
    with col1:
        st.markdown("#### 1. Meet Your Model")
        human_placeholder = st.empty()
        human_file = st.file_uploader("", type=["png", "jpg", "jpeg"], key="human_upl")
        st.markdown("###### Or try a sample model 👇")
        human_selected = show_thumbnail_selector(load_default_images(HUMAN_DIR), "model")

        human_preview = None
        if human_file is not None:
            human_preview = Image.open(human_file).convert("RGB")
            human_placeholder.image(human_preview, use_container_width=True)
        elif human_selected:
            human_preview = Image.open(human_selected).convert("RGB")
            human_placeholder.image(human_preview, use_container_width=True)
        else:
            human_placeholder.markdown(
                """<div style="width:100%;height:150px;border:2px dashed #94a3b8;
                            border-radius:10px;display:flex;align-items:center;
                            justify-content:center;color:#94a3b8;font-size:14px;">
                        No Model Selected</div>""",
                unsafe_allow_html=True,
            )

    # --- Step 2: Garment Upload ---
    with col2:
        cloth_preview = render_garment_uploader()

    # --- Step 3: Try-On ---
    with col3:
        render_tryon_section(human_preview, cloth_preview, key_suffix="photo")
