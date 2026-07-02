"""
app.py
------
Stress Relief Recommendation System (pure Python, powered by Streamlit).

Run with:
    streamlit run app.py
"""

import streamlit as st
import joblib
import numpy as np
import pandas as pd

from recommendations import get_recommendations, AVAILABLE_MOODS

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Unwind — Stress Relief Recommendations",
    page_icon="🌿",
    layout="centered",
)

CUSTOM_CSS = """
<style>
:root {
    --sage: #7C9885;
    --sand: #E8DFD0;
    --dusk: #445069;
    --coral: #E08E79;
}
.stApp { background: linear-gradient(180deg, #F4F1EA 0%, #EDE8DC 100%); }
h1, h2, h3 { color: var(--dusk); font-family: 'Georgia', serif; }
.subtitle { color: #6b7280; font-size: 1.05rem; margin-top: -0.6rem; }
.stress-badge {
    display: inline-block; padding: 0.4rem 1rem; border-radius: 999px;
    font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem;
}
.badge-low { background: #DCEEDD; color: #2F6B3A; }
.badge-medium { background: #FCEBD5; color: #9C5B12; }
.badge-high { background: #F8D9D6; color: #A62E2E; }
.rec-card {
    background: white; border-radius: 12px; padding: 1rem 1.2rem;
    margin-bottom: 0.6rem; border-left: 4px solid var(--sage);
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.rec-title { font-weight: 600; color: var(--dusk); font-size: 1.02rem; }
.rec-meta { color: #8b8b8b; font-size: 0.85rem; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Load model (cached so it only loads once per session)
# ---------------------------------------------------------------------------
@st.cache_resource
def load_model():
    model = joblib.load("stress_model.pkl")
    scaler = joblib.load("stress_scaler.pkl")
    return model, scaler


try:
    model, scaler = load_model()
    MODEL_READY = True
except FileNotFoundError:
    MODEL_READY = False


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("🌿 Unwind")
st.markdown('<p class="subtitle">Tell us about your day — we\'ll find something to help you relax.</p>', unsafe_allow_html=True)
st.write("")

if not MODEL_READY:
    st.error(
        "Model files not found. Run `python train_model.py` once in this folder "
        "before starting the app."
    )
    st.stop()

# ---------------------------------------------------------------------------
# Input form
# ---------------------------------------------------------------------------
with st.form("stress_form"):
    st.subheader("Your day, in a few numbers")

    col1, col2 = st.columns(2)
    with col1:
        sleep_hours = st.slider("Hours of sleep last night", 0.0, 12.0, 7.0, 0.5)
        work_hours = st.slider("Hours worked/studied today", 0.0, 16.0, 8.0, 0.5)
        screen_time_hours = st.slider("Screen time today (hrs)", 0.0, 16.0, 6.0, 0.5)
        physical_activity_hours = st.slider("Physical activity today (hrs)", 0.0, 3.0, 0.3, 0.1)

    with col2:
        social_interaction_score = st.slider("Social connection today (1=isolated, 10=very social)", 1, 10, 5)
        mood_score = st.slider("Overall mood today (1=low, 10=great)", 1, 10, 5)
        caffeine_cups = st.slider("Caffeinated drinks today", 0, 8, 2)
        meditation_minutes = st.slider("Minutes of meditation/relaxation today", 0, 60, 0)

    mood_pref = st.selectbox(
        "What are you in the mood for right now?",
        AVAILABLE_MOODS,
        format_func=lambda m: "Surprise me" if m == "any" else m.capitalize(),
    )

    submitted = st.form_submit_button("Analyze my stress & get recommendations 🌱")

# ---------------------------------------------------------------------------
# Prediction + recommendations
# ---------------------------------------------------------------------------
if submitted:
    features = pd.DataFrame([{
        "sleep_hours": sleep_hours,
        "work_hours": work_hours,
        "screen_time_hours": screen_time_hours,
        "physical_activity_hours": physical_activity_hours,
        "social_interaction_score": social_interaction_score,
        "mood_score": mood_score,
        "caffeine_cups": caffeine_cups,
        "meditation_minutes": meditation_minutes,
    }])

    scaled = scaler.transform(features)
    prediction = model.predict(scaled)[0]
    proba = dict(zip(model.classes_, model.predict_proba(scaled)[0]))

    st.write("---")
    st.subheader("Your stress snapshot")

    badge_class = {"Low": "badge-low", "Medium": "badge-medium", "High": "badge-high"}[prediction]
    st.markdown(
        f'<span class="stress-badge {badge_class}">Stress level: {prediction}</span>',
        unsafe_allow_html=True,
    )

    # confidence breakdown
    proba_df = pd.DataFrame({
        "Stress Level": list(proba.keys()),
        "Confidence": [round(v * 100, 1) for v in proba.values()],
    }).sort_values("Stress Level")
    st.bar_chart(proba_df.set_index("Stress Level"))

    messages = {
        "Low": "You're doing pretty well today. A light, feel-good pick could round things off nicely.",
        "Medium": "You've got some tension built up. Something calming or comforting should help you reset.",
        "High": "It sounds like today's been a lot. Let's ease things down with something gentle and low-effort.",
    }
    st.info(messages[prediction])

    st.write("")
    st.subheader("Recommended for you")

    recs = get_recommendations(prediction, mood_pref, n_per_category=3)

    tabs = st.tabs(["🎬 Movies", "📺 Videos", "🎮 Games"])
    for tab, category in zip(tabs, ["Movies", "Videos", "Games"]):
        with tab:
            for item in recs[category]:
                st.markdown(
                    f"""
                    <div class="rec-card">
                        <div class="rec-title">{item['title']}</div>
                        <div class="rec-meta">{item['genre']} · {item['mood'].capitalize()} vibe</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.caption(
        "This tool offers general relaxation suggestions and is not a substitute "
        "for professional mental health support. If stress is significantly "
        "affecting your life, consider talking to a doctor or counselor."
    )
else:
    st.write("")
    st.caption("Fill in the sliders above and press the button to get your personalized recommendations.")
