import streamlit as st
import requests

API_URL = "https://newsforall-k1ck.onrender.com/api/summary"

st.title("NewsForAll")
st.write("Enter keywords to get a neutral AI summary of the topic across news sources.")

keywords_input = st.text_input("Keywords (comma-separated)", placeholder="e.g. finance, AI, climate")

if st.button("Get Summary"):
    if not keywords_input.strip():
        st.warning("Please enter at least one keyword.")
    else:
        with st.spinner("Connecting to AI Pipeline... (Note: First search may take up to 60 seconds as the server wakes up)"):
            try:
                response = requests.get(API_URL, params={"keywords": keywords_input}, timeout=120)
                data = response.json()
            except Exception as e:
                st.error(f"Failed to reach the API: {e}")
                data = None

        if data:
            # AI Summary
            st.subheader("AI Summary")
            if data.get("ai_summary"):
                st.write(data["ai_summary"])
            else:
                st.write("No summary generated.")

            # Articles
            st.subheader("Articles")
            articles = data.get("articles", [])
            if articles:
                for article in articles:
                    with st.expander(article.get("title", "Untitled")):
                        st.write("**Publisher:**", article.get("publisher") or "N/A")
                        st.write("**Reliability:**", article.get("reliability") or "N/A")
                        st.write("**Bias Label:**", article.get("bias_label") or "N/A")
                        st.write("**Keyword:**", article.get("keyword", "N/A"))
                        st.write("**URL:**", article.get("url", "N/A"))
            else:
                st.write("No articles found.")
