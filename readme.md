# 👕 **RealClo: AI-Powered Virtual Try-On**

RealClo offers a new and scalable approach to online fashion retail by allowing customers to **see how clothing realistically looks on their own body or an AI-generated avatar** before purchasing.
The platform bridges the gap between physical and digital shopping by improving **fit confidence**, reducing **product returns**, and enhancing **inclusivity** in fashion e-commerce.

---

### 🌐 **Overview**

RealClo provides two main interactive modes:

1. **👕 Photo Fit** – Upload or select a model photo to visualize how a garment fits.
2. **🧍 Build Avatar** – Generate an AI avatar based on your measurements and skin tone, then try clothes virtually.

The app uses an external API (KlingAI) for generating avatars and performing virtual try-ons.

---

### 🧱 **Repository Structure**

```
realclo/
│
├── app.py                    # Main Streamlit app entry point
│
├── pages/                    # Separate logic for each app section
│   ├── photo_fit.py
│   └── build_avatar.py
│
├── utils/                    # Shared utilities
│   ├── api.py                # API logic (requests, polling, download)
│   └── ui_helpers.py         # UI components, image utilities, measurements
│
├── assets/                   # Static assets
│   ├── logo.png
│   ├── model/
│   ├── garment/
│   └── avatar/
│
├── authenticate.py           # Encodes JWT or API key for KlingAI requests
├── requirements.txt
└── README.md
```

---

### ⚙️ **Installation**

#### 1. Clone the repository

```bash
git clone https://github.com/AudryaKerenhappukh/realclo-virtual-tryon
cd realclo
```

#### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate    # On Mac/Linux
venv\Scripts\activate       # On Windows
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```
---

### 🔐 **Authentication Setup**

RealClo requires two environment variables for KlingAI API access:

| Variable     | Description                                    |
| ------------ | ---------------------------------------------- |
| `ACCESS_KEY` | Your KlingAI access key (public identifier)    |
| `SECRET_KEY` | Your KlingAI secret key (used to sign the JWT) |

Create a `.env` file in the project root and add:

```bash
ACCESS_KEY="your_access_key_here"
SECRET_KEY="your_secret_key_here"
```

Or set them directly in your shell:

```bash
export ACCESS_KEY="your_access_key_here"
export SECRET_KEY="your_secret_key_here"
```

---


### 🚀 **Run the App**

Once everything is set up, launch RealClo:

```bash
streamlit run app.py
```

This will start a local server, typically at:
👉 [http://localhost:8501](http://localhost:8501)

---

### 🧭 **Usage**

1. **Photo Fit**

   * Upload your own photo or select a sample model.
   * Upload a garment image.
   * Click **🚀 Start Try-On** to preview the result.

2. **Build Avatar**

   * Enter your height, weight, and other optional measurements.
   * Choose a skin tone and gender.
   * Click **Generate Avatar** to create a custom model.
   * Upload a garment and click **🚀 Start Try-On**.
