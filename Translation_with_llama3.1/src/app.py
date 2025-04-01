import streamlit as st
from src.api.model_integration import stream_response
from src.utils.prompt_templates import get_translation_prompt
from config.config import Config


def setup_page():
    """
    Sets up the page with custom styles and page configuration.
    """
    st.set_page_config(
        page_title="Llama 3.1 Translator",
        layout="centered",  # Use centered layout for more compact view
        initial_sidebar_state="collapsed",  # Collapsed sidebar by default
    )

    st.markdown(
        """
        <style>
        :root {
            --primary-color: #ff6f61;  /* A warm red color */
            --background-color: #f7f7f7;  /* Light grey background */
            --text-color: #333;  /* Dark text for contrast */
            --header-color: #333;  /* Dark color for header */
            --border-color: #ddd;  /* Light grey border for separation */
        }
        .stApp {
            margin: auto;
            background-color: var(--background-color);
            color: var(--text-color);
            font-family: 'Arial', sans-serif;
        }
        .stSidebar {
            background-color: #fff;  /* White sidebar */
            border-right: 2px solid var(--border-color);
        }
        .header-title {
            font-size: 2rem;
            color: var(--header-color);
            margin-bottom: 1rem;
        }
        .header-subtitle {
            font-size: 1rem;
            color: #666;
        }
        .logo-container img {
            width: 120px;
            display: block;
            margin: 0 auto;
        }
        .content-container {
            padding: 2rem;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .tab-container {
            padding: 1.5rem;
            margin-top: 2rem;
        }
        .stButton>button {
            background-color: var(--primary-color);
            color: white;
            border-radius: 5px;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    setup_page()

    # Header section with title and subtitle
    st.markdown(
        """
        <div class="header-title">Llama 3.1 Translator</div>
        """,
        unsafe_allow_html=True,
    )



    # Sidebar for settings
    with st.sidebar:
        st.title("Settings")
        model_name = st.selectbox("Choose a model", Config.AVAILABLE_MODELS)

        # Cập nhật các ngôn ngữ
        source_lang = st.selectbox(
            "From", ["English", "Japanese", "Vietnamese", "German", "Chinese", "French"]
        )
        target_lang = st.selectbox(
            "To", ["Vietnamese","English", "Japanese",  "German", "Chinese", "French"]
        )
        cultural_context = st.selectbox(
            "Context", ["Formal", "Casual", "Business", "Youth Slang", "Poetic"]
        )

    # Main content area with a background and some padding
    main_container = st.container()

    with main_container:
        
        st.header("Enter Text for Translation and Meaning")

        text = st.text_area(
            "Text to translate",
            "",
            height=200,
        )
        st.caption(f"Character count: {len(text)}")

        if st.button("Translate and Analyze", type="primary"):
            if text:
                # Only Translation and Cultural Context
                tab1, tab2 = st.tabs(["Translation", "Cultural References"])

                # Tab 1: Translation
                with tab1:
                    st.subheader("Translation Result")
                    translation_container = st.empty()
                    translation_prompt = get_translation_prompt(
                        text, source_lang, target_lang, cultural_context
                    )
                    translation = stream_response(
                        [{"role": "user", "content": translation_prompt}],
                        translation_container,
                        model_name,
                    )


        st.markdown('</div>', unsafe_allow_html=True)




if __name__ == "__main__":
    main()
