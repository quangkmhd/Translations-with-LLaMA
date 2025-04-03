import streamlit as st
from main import Config, stream_response, get_translation_prompt

# Streamlit UI Setup
def setup_page():
    st.set_page_config(
        page_title="Llama 3.1 Translator",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    st.markdown(
        """
        <style>
        .stApp { background-color: #f7f7f7; color: #333; font-family: 'Arial', sans-serif; }
        .stSidebar { background-color: #fff; border-right: 2px solid #ddd; }
        .header-title { font-size: 2rem; color: #333; margin-bottom: 1rem; }
        .stButton>button { background-color: #ff6f61; color: white; border-radius: 5px; font-weight: bold; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    setup_page()
    st.markdown("<div class='header-title'>Llama 3.1 Translator</div>", unsafe_allow_html=True)
    
    # Sidebar settings
    with st.sidebar:
        st.title("Settings")
        model_name = st.selectbox("Choose a model", Config.AVAILABLE_MODELS)
        source_lang = st.selectbox("From", ["English", "Japanese", "Vietnamese", "German", "Chinese", "French"])
        target_lang = st.selectbox("To", ["Vietnamese", "English", "Japanese", "German", "Chinese", "French"])
        cultural_context = st.selectbox("Context", ["Formal", "Casual", "Business", "Youth Slang", "Poetic"])
    
    # Main translation area
    st.header("Enter Text for Translation")
    text = st.text_area("Text to translate", "", height=200)
    st.caption(f"Character count: {len(text)}")

    if st.button("Translate and Analyze", type="primary"):
        if text:
            tab1, tab2 = st.tabs(["Translation", "Cultural References"])
            with tab1:
                st.subheader("Translation Result")
                translation_container = st.empty()
                translation_prompt = get_translation_prompt(text, source_lang, target_lang, cultural_context)
                translation = stream_response([{"role": "user", "content": translation_prompt}], translation_container, model_name)

if __name__ == "__main__":
    main()
