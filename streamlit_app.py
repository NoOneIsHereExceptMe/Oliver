import streamlit as st
import google.generativeai as genai
import os
from gtts import gTTS
import uuid
import time

# Default SVG logo
DEFAULT_SVG = """
<svg width="90" height="98" viewBox="0 0 358 366" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="179" cy="187" r="176" fill="url(#paint0_linear_1_4)" stroke="url(#paint1_linear_1_4)" stroke-width="6"/>
<path d="M163.655 102.496C163.655 104.117 163.1 105.483 161.991 106.592C160.882 107.701 159.474 108.256 157.767 108.256H155.591C154.482 108.256 153.927 108.811 153.927 109.92V166.112C153.927 167.733 153.372 169.141 152.263 170.336C151.154 171.445 149.788 172 148.167 172H144.583C142.962 172 141.596 171.445 140.487 170.336C139.378 169.141 138.823 167.733 138.823 166.112V109.92C138.823 108.811 138.268 108.256 137.159 108.256H135.367C134.258 108.256 133.703 108.811 133.703 109.92V139.104C133.703 143.2 132.978 147.168 131.527 151.008C130.076 154.763 127.943 158.133 125.127 161.12L116.935 170.08C115.826 171.36 114.375 172 112.583 172C111.9 172 111.218 171.872 110.535 171.616C108.06 170.677 106.823 168.843 106.823 166.112V160.992C106.823 159.371 107.335 158.048 108.359 157.024L113.991 150.88C117.063 147.552 118.599 143.627 118.599 139.104V109.92C118.599 108.811 118.044 108.256 116.935 108.256H112.583C110.962 108.256 109.596 107.701 108.487 106.592C107.378 105.483 106.823 104.117 106.823 102.496V98.912C106.823 97.2907 107.378 95.9253 108.487 94.816C109.596 93.7067 110.962 93.152 112.583 93.152H137.159C137.586 93.152 137.97 92.9813 138.311 92.64C138.652 92.2133 138.823 91.7867 138.823 91.36C138.823 89.7387 139.378 88.3733 140.487 87.264C141.596 86.0693 142.962 85.472 144.583 85.472H148.167C149.788 85.472 151.154 86.0693 152.263 87.264C153.372 88.3733 153.927 89.7387 153.927 91.36C153.927 91.7867 154.098 92.2133 154.439 92.64C154.78 92.9813 155.164 93.152 155.591 93.152H157.767C159.474 93.152 160.882 93.7067 161.991 94.816C163.1 95.9253 163.655 97.2907 163.655 98.912V102.496ZM251.254 131.552C251.254 137.611 249.675 143.285 246.518 148.576L233.846 169.184C232.651 171.061 230.987 172 228.854 172H224.758C222.454 172 220.747 171.019 219.638 169.056C218.529 167.008 218.571 165.045 219.766 163.168L233.59 140.64C235.297 137.739 236.15 134.709 236.15 131.552V94.816C236.15 93.1947 236.705 91.8293 237.814 90.72C238.923 89.6107 240.289 89.056 241.91 89.056H245.494C247.115 89.056 248.481 89.6107 249.59 90.72C250.699 91.8293 251.254 93.1947 251.254 94.816V131.552ZM214.774 138.848C214.774 140.469 214.219 141.877 213.11 143.072C212.001 144.181 210.635 144.736 209.014 144.736H205.43C203.809 144.736 202.443 144.181 201.334 143.072C200.225 141.877 199.67 140.469 199.67 138.848V94.816C199.67 93.1947 200.225 91.8293 201.334 90.72C202.443 89.6107 203.809 89.056 205.43 89.056H209.014C210.635 89.056 212.001 89.6107 213.11 90.72C214.219 91.8293 214.774 93.1947 214.774 94.816V138.848ZM172.489 213.552C172.489 214.405 172.19 215.131 171.592 215.728C171.081 216.24 170.441 216.496 169.673 216.496H166.089C165.321 216.496 164.638 216.24 164.04 215.728C163.443 215.131 163.145 214.405 163.145 213.552V202.416C163.145 201.563 163.443 200.88 164.04 200.368C164.638 199.771 165.321 199.472 166.089 199.472H169.673C170.441 199.472 171.081 199.771 171.592 200.368C172.19 200.88 172.489 201.563 172.489 202.416V213.552ZM160.84 213.552C160.84 214.405 160.542 215.131 159.945 215.728C159.433 216.24 158.75 216.496 157.896 216.496H154.44C153.587 216.496 152.862 216.24 152.264 215.728C151.752 215.131 151.496 214.405 151.496 213.552V202.416C151.496 201.563 151.752 200.88 152.264 200.368C152.862 199.771 153.587 199.472 154.44 199.472H157.896C158.75 199.472 159.433 199.771 159.945 200.368C160.542 200.88 160.84 201.563 160.84 202.416V213.552ZM160.585 279.216C160.84 280.837 160.414 282.416 159.304 283.952C158.11 285.317 156.616 286 154.825 286H151.241C149.875 286 148.638 285.531 147.528 284.592C146.419 283.653 145.736 282.501 145.48 281.136L132.296 206.384C131.87 204.592 132.296 203.013 133.576 201.648C134.6 200.197 136.094 199.472 138.056 199.472H141.64C143.091 199.472 144.328 199.941 145.353 200.88C146.462 201.733 147.144 202.885 147.401 204.336L160.585 279.216ZM127.176 206.384L113.992 281.136C113.736 282.501 113.054 283.653 111.944 284.592C110.92 285.531 109.683 286 108.232 286H104.648C102.856 286 101.363 285.317 100.168 283.952C99.0592 282.416 98.6325 280.837 98.8885 279.216L112.072 204.336C112.328 202.885 113.011 201.733 114.12 200.88C115.23 199.941 116.467 199.472 117.832 199.472H121.416C123.208 199.472 124.702 200.197 125.896 201.648C127.176 203.013 127.603 204.592 127.176 206.384ZM257.231 243.888C257.231 245.509 256.677 246.875 255.567 247.984C254.458 249.093 253.05 249.648 251.343 249.648H206.671C205.05 249.648 203.642 249.093 202.447 247.984C201.338 246.875 200.783 245.509 200.783 243.888V240.304C200.783 238.683 201.338 237.317 202.447 236.208C203.642 235.099 205.05 234.544 206.671 234.544H251.343C253.05 234.544 254.458 235.099 255.567 236.208C256.677 237.317 257.231 238.683 257.231 240.304V243.888Z" fill="url(#paint2_linear_1_4)"/>
<defs>
<linearGradient id="paint0_linear_1_4" x1="179" y1="14" x2="179" y2="360" gradientUnits="userSpaceOnUse">
<stop stop-color="#FF9148"/>
<stop offset="1" stop-color="#1E1E1E" stop-opacity="0"/>
</linearGradient>
<linearGradient id="paint1_linear_1_4" x1="179" y1="14" x2="179" y2="360" gradientUnits="userSpaceOnUse">
<stop offset="0.621" stop-color="white"/>
<stop offset="0.905" stop-color="#1E1E1E" stop-opacity="0"/>
</linearGradient>
<linearGradient id="paint2_linear_1_4" x1="179" y1="0" x2="179" y2="346" gradientUnits="userSpaceOnUse">
<stop offset="0.521" stop-color="#3AD4FF"/>
<stop offset="1" stop-color="#1E1E1E" stop-opacity="0"/>
</linearGradient>
</defs>
</svg>
"""

# Page configuration
st.set_page_config(
    page_title="Oliver: Japanese Translator",
    page_icon="🎌",
    layout="centered"
)

st.session_state.custom_logo = DEFAULT_SVG

# Load environment variables
# os.environ["GOOGLE_API_KEY"] == st.secrets["GOOGLE_API_KEY"]

def setup_gemini():
    """Initialize the Gemini API client."""
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash', 
                                safety_settings={
                                    'HATE': 'BLOCK_NONE',
                                    'HARASSMENT': 'BLOCK_NONE',
                                    'SEXUAL' : 'BLOCK_NONE',
                                    'DANGEROUS' : 'BLOCK_NONE'
                                }
                                )

def create_prompt(user_input):
    """Create the structured prompt for Gemini."""
    system_prompt = """Translate the text that the user gives you to Japanese language and produce two translations. One is the Japanese text, and a Romaji of the Japanese text.
    Your response should follow this exact format:
    Japanese: [Japanese translation]
    Romaji: [Romaji translation]
    
    Provide only the translations in the specified format with no additional text or explanations."""
    
    return f"{system_prompt}\n\nUser Input: {user_input}"

def get_translation(model, text):
    """Get translation from Gemini API."""
    prompt = create_prompt(text)
    response = model.generate_content(prompt)
    return response.text

def text_to_speech(text, lang='ja'):
    """Convert text to speech and save to a file with a random name."""
    try:
        filename = f"audio_{uuid.uuid4().hex[:8]}.mp3"
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        return None

def cleanup_audio_files():
    """Clean up audio files that are older than 1 minute."""
    current_time = time.time()
    for file in os.listdir():
        if file.startswith("audio_") and file.endswith(".mp3"):
            file_creation_time = os.path.getctime(file)
            if current_time - file_creation_time > 60:
                try:
                    os.remove(file)
                except:
                    pass

# Initialize Gemini model
@st.cache_resource
def init_gemini():
    return setup_gemini()

# Main app
def main():
    # Clean up old audio files at startup
    cleanup_audio_files()
    
    # Create two columns for logo and title
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # Display current logo
        st.markdown(st.session_state.custom_logo, unsafe_allow_html=True)
    
    with col2:
        st.title("Oliver: Japanese Translator")
    
    # Description
    st.markdown("""
    This app translates text to Japanese and provides both Japanese characters and Romaji.
    Enter your text below to get started!
    """)
    
    # Initialize model
    model = init_gemini()
    
    # Input text area
    user_input = st.text_area("Enter text to translate:", height=100)
    
    # Translation button
    if st.button("Translate", type="primary"):
        if user_input:
            try:
                with st.spinner("Translating..."):
                    translation = get_translation(model, user_input)
                
                # Display results in a nice format
                st.success("Translation Complete!")
                
                # Parse the translation response
                japanese_line = ""
                romaji_line = ""
                
                for line in translation.split('\n'):
                    if line.startswith('Japanese:'):
                        japanese_line = line.replace('Japanese:', '').strip()
                    elif line.startswith('Romaji:'):
                        romaji_line = line.replace('Romaji:', '').strip()
                
                # Display results in columns
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Japanese")
                    st.markdown(f"<h3 style='font-family: sans-serif;'>{japanese_line}</h3>", 
                              unsafe_allow_html=True)
                    
                    # Add audio player for Japanese text
                    st.markdown("Listen to pronunciation:")
                    audio_file = text_to_speech(japanese_line)
                    if audio_file:
                        audio_bytes = open(audio_file, 'rb').read()
                        st.audio(audio_bytes, format='audio/mp3')
                        
                        # Schedule file for deletion
                        cleanup_time = time.time() + 60
                        st.session_state[audio_file] = cleanup_time
                    
                with col2:
                    st.subheader("Romaji")
                    st.markdown(f"<h3>{romaji_line}</h3>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter some text to translate.")
    
    # Cleanup old files
    for filename, cleanup_time in dict(st.session_state).items():
        if filename.startswith("audio_") and filename.endswith(".mp3"):
            if time.time() >= cleanup_time:
                try:
                    os.remove(filename)
                    del st.session_state[filename]
                except:
                    pass
    
    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit, Google's Gemini AI, gTTS, A Shark and A Flower Alchemist.")

if __name__ == "__main__":
    main()
