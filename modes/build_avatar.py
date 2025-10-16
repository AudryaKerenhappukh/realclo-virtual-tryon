import streamlit as st
from PIL import Image
from io import BytesIO
import requests
from utils.api import AVATAR_URL, create_task, poll_task
from utils.ui_helpers import (
    categorize_measurements, render_garment_uploader, render_tryon_section
)

def run():
    """Build Avatar page — generate a realistic avatar and try on clothes."""
    st.markdown("### 🧍 Build Avatar")
    col1, col2, col3 = st.columns(3, gap="large")

    # --- Step 1: Measurements & Avatar Generation ---
    with col1:
        st.markdown("#### 1. Enter Your Measurements")
        avatar_placeholder = st.empty()

        # Skin tones
        skin_tones = {
            "Fair": "#f2d3c2",
            "Light": "#d8a98f",
            "Medium": "#a97b64",
            "Tan": "#7a4f3a",
            "Dark": "#4a3223",
        }
        choice = st.radio("Skin Tone", list(skin_tones.keys()), horizontal=True, label_visibility="collapsed")

        cols = st.columns(len(skin_tones))
        for idx, (label, color) in enumerate(skin_tones.items()):
            border = "#000" if choice == label else "#ccc"
            with cols[idx]:
                st.markdown(
                    f"""<div style="text-align:center">
                          <div style="background-color:{color};
                                      width:45px;height:45px;border-radius:50%;
                                      margin:auto;border:3px solid {border};"></div>
                          <div style="margin-top:4px;font-size:12px;">{label}</div>
                        </div>""",
                    unsafe_allow_html=True,
                )

        selected_color = skin_tones[choice]

        # Basic measurements
        height = st.number_input("Height (cm)", min_value=140, max_value=220)
        weight = st.number_input("Weight (kg)", min_value=40, max_value=150)
        body_type = st.selectbox("Body Shape", ["Slim", "Athletic", "Curvy", "Average"])
        gender = st.selectbox("Gender", ["Female", "Male"])

        # Optional details
        with st.expander("Add more detailed measurements (optional)"):
            bust = st.number_input("Bust (cm)", min_value=70, max_value=150, value=None, placeholder="Optional")
            waist = st.number_input("Waist (cm)", min_value=50, max_value=140, value=None, placeholder="Optional")
            hips = st.number_input("Hips (cm)", min_value=70, max_value=160, value=None, placeholder="Optional")
            shoulder = st.number_input("Shoulder Width (cm)", min_value=30, max_value=60, value=None, placeholder="Optional")
            st.session_state["body_description"] = categorize_measurements(height, weight, bust, waist, hips, shoulder)

        # Avatar generation prompt
        avatar_prompt = (
            "Full-body fashion model photo, plain studio background, standing upright, "
            f"Gender: {gender}. Skin color: {selected_color}. "
            f"Height: {height}cm, Weight: {weight}kg, Body type: {body_type}. "
            f"Body description: {st.session_state.get('body_description', 'proportional build')}."
        )

        if st.button("Generate Avatar", type="primary", use_container_width=True):
            payload = {"model_name": "kling-v2-1", "prompt": avatar_prompt, "aspect_ratio": "3:4"}
            with st.spinner("Generating avatar..."):
                task = create_task(AVATAR_URL, payload)
                task_id = task["data"]["task_id"]
                result = poll_task(AVATAR_URL, task_id)
            if result and "task_result" in result["data"]:
                url = result["data"]["task_result"]["images"][0]["url"]
                img = Image.open(BytesIO(requests.get(url).content)).convert("RGB")
                st.session_state["human_preview"] = img
                st.session_state["avatar_url"] = url
                avatar_placeholder.image(url, caption="Generated Avatar", use_container_width=True)
                st.success("Avatar generation completed!")

        # Placeholder
        if "avatar_url" not in st.session_state:
            avatar_placeholder.markdown(
                """<div style="width:100%;height:150px;border:2px dashed #94a3b8;
                            border-radius:10px;display:flex;align-items:center;
                            justify-content:center;color:#94a3b8;font-size:14px;">
                        No Avatar Generated</div>""",
                unsafe_allow_html=True,
            )

    # --- Step 2: Garment Upload ---
    with col2:
        cloth_preview = render_garment_uploader()

    # --- Step 3: Try-On ---
    with col3:
        render_tryon_section(st.session_state.get("human_preview"), cloth_preview, key_suffix="avatar")
