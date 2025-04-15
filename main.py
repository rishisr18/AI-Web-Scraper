import streamlit as st
from scrape import (Scrape_website, split_dom_content, extract_body_content, clean_body_content)
from parse import parse_with_ollama

st.set_page_config(page_title="AI Web Scraper", layout="wide")
st.title("AI-Powered Web Scraper & Parser")

url = st.text_input("🔗 Enter a website URL:")

if st.button("Scrape Site"):
    if url:
        with st.spinner("Scraping the website..."):
            try:
                dom_content = Scrape_website(url)
                body_content = extract_body_content(dom_content)
                cleaned_content = clean_body_content(body_content)
                st.session_state.dom_content = cleaned_content
                st.success("Website scraped successfully!")

                with st.expander("View Extracted DOM Content"):
                    st.text_area("Cleaned Content", cleaned_content, height=300)
            except Exception as e:
                st.error(f"Please enter a valid URL.\nError: {e}")
    else:
        st.warning("Please enter a valid URL.")

if "dom_content" in st.session_state:
    parse_description = st.text_area("What information do you want to extract?", height=100)

    if st.button("Parse Content"):
        if parse_description:
            with st.spinner("Parsing with Ollama..."):
                dom_chunks = split_dom_content(st.session_state.dom_content)
                parsed_result = parse_with_ollama(dom_chunks, parse_description)
                st.subheader("Parsed Result")
                st.text_area("Output", parsed_result,height=300)

                st.download_button("Download Result", parsed_result, file_name="parsed_result.txt")
        else:
            st.warning("Please describe what you want to extract.")
