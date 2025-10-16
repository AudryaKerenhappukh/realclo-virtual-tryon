import os, base64, streamlit as st
from PIL import Image
from io import BytesIO
from .api import create_task, poll_task, TRYON_URL, download_image

# ========== IMAGE HELPERS ==========

def crop_center_square(img: Image.Image, size=100):
    """Crop an image to a centered square and resize."""
    w, h = img.size
    m = min(w, h)
    left, top = (w - m) // 2, (h - m) // 2
    return img.crop((left, top, left + m, top + m)).resize((size, size))

def img_to_api_b64(img: Image.Image) -> str:
    """Convert an image to base64 for API upload."""
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def load_default_images(folder):
    """Load default images from folder for selection."""
    if not os.path.isdir(folder): 
        return []
    return [os.path.join(folder, f)
            for f in sorted(os.listdir(folder))
            if f.lower().endswith((".png", ".jpg", ".jpeg"))][:9]

# ========== MEASUREMENT HELPERS ==========

def fmt(label, val, unit=""):
    return f"{label}: {val}{unit}," if val not in (None, "", "Unknown") else ""

def categorize_measurements(height=None, bust=None, waist=None, hips=None, shoulder=None):
    """Return descriptive body type text from numerical measurements."""
    descriptors = []
    if height:
        descriptors.append("petite" if height < 160 else "average height" if height <= 175 else "tall")
    if bust and waist and hips:
        if bust - waist > 20 and hips - waist > 20:
            descriptors.append("hourglass")
        elif hips > bust:
            descriptors.append("pear-shaped")
        elif bust > hips:
            descriptors.append("inverted triangle")
        else:
            descriptors.append("rectangle/athletic")
    if shoulder:
        descriptors.append("narrow shoulders" if shoulder < 40 else "medium shoulders" if shoulder <= 45 else "broad shoulders")
    return ", ".join(descriptors) if descriptors else "proportional build"

# ========== UI COMPONENTS ==========

def show_thumbnail_selector(images, key_prefix, size=100, cols_per_row=3):
    """Display selectable image thumbnails centered in their container."""
    sel_key = f"{key_prefix}_selected"
    if sel_key not in st.session_state:
        st.session_state[sel_key] = None
    selected = st.session_state[sel_key]

    # Center the entire grid block
    st.markdown('<div style="display:flex;justify-content:center;">', unsafe_allow_html=True)

    # Build the grid
    cols = st.columns(cols_per_row, gap="medium")

    for i, img_path in enumerate(images):
        img = Image.open(img_path).convert("RGB")
        thumb = crop_center_square(img, size)
        buf = BytesIO(); thumb.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        border = "3px solid #22c55e" if selected == img_path else "1px solid #ccc"

        with cols[i % cols_per_row]:
            st.markdown(
                f"""<div style="width:{size}px;height:{size}px;
                        border:{border};border-radius:8px;
                        overflow:hidden;margin:auto;">
                        <img src="data:image/png;base64,{b64}"
                             style="width:100%;height:100%;object-fit:cover;" />
                    </div>""",
                unsafe_allow_html=True
            )
            if st.button(f"{key_prefix} {i+1}", key=f"{key_prefix}_{i}",
                         use_container_width=True, type="tertiary"):
                st.session_state[sel_key] = img_path
                selected = img_path
            if st.session_state.get(f"{key_prefix}_{i}"):
                st.session_state[sel_key] = img_path
                selected = img_path

    # Close centering div
    st.markdown('</div>', unsafe_allow_html=True)
    return selected


def render_garment_uploader():
    """Upload garment image and show preview."""
    st.markdown("#### 2. Add Your Look")
    placeholder = st.empty()
    file = st.file_uploader("", type=["png", "jpg", "jpeg"], key="garment_upl")
    if file:
        preview = Image.open(file).convert("RGB")
        placeholder.image(preview, use_container_width=True)
        return preview
    placeholder.markdown(
        """<div style="width:100%;height:150px;border:2px dashed #94a3b8;
                        border-radius:10px;display:flex;align-items:center;
                        justify-content:center;color:#94a3b8;font-size:14px;">
                    No Garment Selected</div>""",
        unsafe_allow_html=True)
    return None

def render_tryon_section(human_preview, cloth_preview, key_suffix=""):
    """Run the virtual try-on task and show result."""
    st.markdown("#### 3. Try Your Look")
    result_placeholder = st.empty()
    run = st.button("🚀 Start Try-On", key=f"start_tryon_{key_suffix}",
                    use_container_width=True, type="primary")

    if run:
        if human_preview is None or cloth_preview is None:
            st.error("Please provide both a model and a garment image.")
            st.stop()

        payload = {
            "model_name": "kolors-virtual-try-on-v1-5",
            "human_image": img_to_api_b64(human_preview),
            "cloth_image": img_to_api_b64(cloth_preview),
        }
        with st.spinner("Submitting your try-on request..."):
            task = create_task(TRYON_URL, payload)
        task_id = task["data"]["task_id"]
        result = poll_task(TRYON_URL, task_id)

        if result and "task_result" in result["data"]:
            url = result["data"]["task_result"]["images"][0]["url"]
            output_img = download_image(url)
            st.session_state["tryon_img"] = output_img

        if "tryon_img" in st.session_state:
            result_placeholder.image(st.session_state["tryon_img"],
                                     caption="✨ Your Try-On Result",
                                     use_container_width=True)
            buf = BytesIO()
            st.session_state["tryon_img"].save(buf, format="PNG")
            st.download_button("Download Result", data=buf.getvalue(),
                               file_name="tryon_result.png", mime="image/png",
                               use_container_width=True)
