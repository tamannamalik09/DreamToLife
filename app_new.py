import streamlit as st
from dreamtolife_app.coordinator import CoordinatorAgent

# Page metadata and layout configuration
st.set_page_config(
    page_title="DreamToLife",
    page_icon="🌙",
    layout="wide"
)

# App header and introduction
st.title("🌙 DreamToLife")
st.markdown("#### AI Dream Reflection System")
st.markdown("_Transform your dream impressions into reflective, actionable insights._")

# Dream input form keeps the interface clean and responsive
with st.form(key="dream_form"):
    dream = st.text_area(
        "Describe your dream",
        height=220,
        placeholder="Type your dream in as much detail as you remember..."
    )
    analyze_button = st.form_submit_button("Analyze Dream")

if analyze_button:
    if not dream.strip():
        st.warning("Please enter a dream description before analyzing.")
    else:
        try:
            with st.spinner("Analyzing your dream with DreamToLife..."):
                coordinator = CoordinatorAgent()
                result = coordinator.analyze_dream(dream.strip())

            st.success("Dream analyzed successfully! ✨")
            st.markdown("---")

            # Dream Summary section
            with st.container():
                st.subheader("📝 Dream Summary")
                st.write(result.get("summary", "No summary available."))

            # Emotion Analysis section with progress bars
            emotions = result.get("emotions", {}) or {}
            with st.container():
                st.subheader("🎭 Emotion Analysis")
                if emotions:
                    sorted_emotions = sorted(emotions.items(), key=lambda item: item[1], reverse=True)
                    for emotion, value in sorted_emotions:
                        percentage = int(value) if isinstance(value, (int, float)) else 0
                        st.markdown(f"**{emotion}** — {percentage}%")
                        st.progress(min(max(percentage, 0), 100))
                    dominant_emotion = sorted_emotions[0][0]
                    st.caption(f"Dominant Emotion: **{dominant_emotion}**")
                else:
                    st.info("No strong emotions were detected from this dream.")

            st.markdown("---")

            # Symbols and Themes section using columns
            symbols = result.get("symbols", []) or []
            themes = result.get("themes", []) or []
            with st.container():
                st.subheader("🔍 Symbols & Themes")
                sym_col, theme_col = st.columns([2, 1])
                with sym_col:
                    st.markdown("**Symbols**")
                    if symbols:
                        symbol_tags = "  ".join([f"`{tag}`" for tag in symbols])
                        st.markdown(symbol_tags)
                    else:
                        st.write("No symbols were detected.")
                with theme_col:
                    st.markdown("**Themes**")
                    if themes:
                        for theme in themes:
                            st.markdown(f"- {theme}")
                    else:
                        st.write("No themes were detected.")

            st.markdown("---")

            # Narrative section in a styled information box
            with st.container():
                st.subheader("📖 Dream Narrative")
                narrative = result.get("narrative", "No narrative available.")
                if narrative and narrative.strip():
                    st.info(narrative)
                else:
                    st.write("No narrative was generated for this dream.")

            # Growth Insight section highlighted with a success box
            with st.container():
                st.subheader("🌱 Growth Insight")
                growth_insight = result.get("growth_insight", "No growth insight available.")
                if growth_insight and growth_insight.strip():
                    st.success(growth_insight)
                else:
                    st.write("No growth insight is available for this dream.")

            st.markdown("---")

            # Scorecard section using metrics
            with st.container():
                st.subheader("📊 Dream Scorecard")
                scorecard = result.get("scorecard", {}) or {}
                metric_1 = scorecard.get("Emotional Intensity", 0)
                metric_2 = scorecard.get("Reflection Depth", 0)
                metric_3 = scorecard.get("Growth Opportunity", 0)
                col1, col2, col3 = st.columns(3)
                col1.metric("Emotional Intensity", f"{metric_1}%")
                col2.metric("Reflection Depth", f"{metric_2}%")
                col3.metric("Growth Opportunity", f"{metric_3}%")

            st.markdown("---")

            # AI Image Prompt inside an expandable section
            with st.expander("🔎 AI Image Prompt"):
                st.write(result.get("image_prompt", "No image prompt available."))

        except Exception as exc:
            st.error("Something went wrong while analyzing your dream. Please try again.")
            st.exception(exc)
