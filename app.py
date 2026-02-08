"""
Gemini 3 Hackathon - Main Streamlit Application
Combines two innovative projects:
1. Diagram Decoder - Education tool for explaining diagrams
2. Fine Print Translator - Social Good tool for analyzing contracts
"""
import streamlit as st
import base64
from io import BytesIO
from PIL import Image
import time

from config import MAX_IMAGE_SIZE, MAX_PDF_SIZE, GEMINI_FLASH_MODEL, GEMINI_PRO_MODEL
from agents import process_diagram, process_fine_print

# Page configuration
st.set_page_config(
    page_title="Gemini 3 Hackathon Projects",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .project-card {
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3rem;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .success-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def image_to_base64(image: Image.Image) -> str:
    """Convert PIL Image to base64 string"""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def initialize_session_state():
    """Initialize session state variables"""
    if 'diagram_results' not in st.session_state:
        st.session_state.diagram_results = None
    if 'fine_print_results' not in st.session_state:
        st.session_state.fine_print_results = None
    if 'current_project' not in st.session_state:
        st.session_state.current_project = None
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    if 'api_key_configured' not in st.session_state:
        st.session_state.api_key_configured = False


def render_diagram_decoder():
    """Render the Diagram Decoder project interface"""
    st.markdown("## Diagram Decoder")
    
    uploaded_file = st.file_uploader(
        "Upload a diagram image",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a photo or screenshot of a diagram from your textbook"
    )
    
    if uploaded_file is not None:
        # Check file size
        if uploaded_file.size > MAX_IMAGE_SIZE:
            st.error(f"File too large! Maximum size is {MAX_IMAGE_SIZE / (1024*1024):.1f}MB")
            return
        
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Diagram", use_container_width=True)
        
        # Process button
        if st.button("Analyze Diagram", type="primary", use_container_width=True):
            if not st.session_state.get('api_key') or not st.session_state.api_key_configured:
                st.error("Please configure your Gemini API key first")
                return
            
            with st.spinner("Analyzing diagram... This may take a moment."):
                try:
                    # Convert image to base64
                    image_base64 = image_to_base64(image)
                    
                    # Process through agent
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("Step 1/3: Identifying components...")
                    progress_bar.progress(33)
                    time.sleep(0.5)
                    
                    status_text.text("Step 2/3: Explaining logic and relationships...")
                    progress_bar.progress(66)
                    time.sleep(0.5)
                    
                    status_text.text("Step 3/3: Generating quiz questions...")
                    progress_bar.progress(100)
                    
                    results = process_diagram(image_base64, api_key=st.session_state.api_key)
                    st.session_state.diagram_results = results
                    
                    progress_bar.empty()
                    status_text.empty()
                    
                    st.success("Analysis complete")
                    
                except Exception as e:
                    st.error(f"Error processing diagram: {str(e)}")
                    st.info("Please check your API key and try again.")
        
        # Display results
        if st.session_state.diagram_results:
            results = st.session_state.diagram_results
            
            st.markdown("---")
            st.markdown("### Analysis Results")
            
            # Image Description
            with st.expander("Component Identification", expanded=True):
                st.markdown(results.get('image_description', 'No description available'))
            
            # Logical Explanation
            with st.expander("Step-by-Step Explanation", expanded=True):
                st.markdown(results.get('logical_explanation', 'No explanation available'))
            
            # Quiz Questions
            with st.expander("Quiz Questions", expanded=False):
                st.markdown(results.get('quiz_questions', 'No quiz available'))


def render_fine_print_translator():
    """Render the Fine Print Translator project interface"""
    st.markdown("## Fine Print Translator")
    
    # Document type selector
    doc_type = st.selectbox(
        "Document Type",
        ["Terms of Service", "Rental Agreement", "Medical Form", "Employment Contract", 
         "Service Agreement", "Privacy Policy", "Other Legal Document"],
        help="Select the type of document you're analyzing"
    )
    
    # Input method selector
    input_method = st.radio(
        "Input Method",
        ["Upload Image", "Upload PDF", "Paste Text"],
        horizontal=True
    )
    
    document_text = None
    image_base64 = None
    pdf_bytes = None
    
    if input_method == "Upload Image":
        uploaded_file = st.file_uploader(
            "Upload document image",
            type=['png', 'jpg', 'jpeg'],
            help="Take a photo or screenshot of the document"
        )
        if uploaded_file is not None:
            if uploaded_file.size > MAX_IMAGE_SIZE:
                st.error(f"File too large! Maximum size is {MAX_IMAGE_SIZE / (1024*1024):.1f}MB")
                return
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Document", use_container_width=True)
            image_base64 = image_to_base64(image)
    
    elif input_method == "Upload PDF":
        uploaded_file = st.file_uploader(
            "Upload PDF document",
            type=['pdf'],
            help="Upload a PDF file of the document"
        )
        if uploaded_file is not None:
            if uploaded_file.size > MAX_PDF_SIZE:
                st.error(f"File too large! Maximum size is {MAX_PDF_SIZE / (1024*1024):.1f}MB")
                return
            pdf_bytes = uploaded_file.read()
            st.success(f"PDF uploaded ({uploaded_file.size / 1024:.1f} KB)")
    
    elif input_method == "Paste Text":
        document_text = st.text_area(
            "Paste document text",
            height=200,
            help="Copy and paste the text from your document"
        )
    
    # Process button
    if st.button("Analyze Document", type="primary", use_container_width=True):
        if not st.session_state.get('api_key') or not st.session_state.api_key_configured:
            st.error("Please configure your Gemini API key first")
            return
        
        if not document_text and not image_base64 and not pdf_bytes:
            st.warning("Please provide a document to analyze")
            return
        
        with st.spinner("Analyzing document... This may take a moment for long documents."):
            try:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("Step 1/3: Extracting text from document...")
                progress_bar.progress(33)
                time.sleep(0.5)
                
                status_text.text("Step 2/3: Auditing for risks and predatory clauses...")
                progress_bar.progress(66)
                time.sleep(0.5)
                
                status_text.text("Step 3/3: Generating risk summary...")
                progress_bar.progress(100)
                
                results = process_fine_print(
                    document_text=document_text,
                    image_base64=image_base64,
                    pdf_bytes=pdf_bytes,
                    document_type=doc_type,
                    api_key=st.session_state.api_key
                )
                
                if 'error' in results:
                    st.error(f"{results['error']}")
                else:
                    st.session_state.fine_print_results = results
                    progress_bar.empty()
                    status_text.empty()
                    st.success("Analysis complete")
                    
            except Exception as e:
                st.error(f"Error processing document: {str(e)}")
                st.info("Please check your API key and try again.")
    
    # Display results
    if st.session_state.fine_print_results:
        results = st.session_state.fine_print_results
        
        st.markdown("---")
        st.markdown("### Risk Analysis Results")
        
        # Risk Summary (most important - show first)
        with st.expander("Risk Summary & Recommendations", expanded=True):
            st.markdown(results.get('risk_summary', 'No summary available'))
        
        # Detailed Audit
        with st.expander("Detailed Risk Audit", expanded=False):
            st.markdown(results.get('risk_audit', 'No audit available'))
        
        # Document Preview
        if results.get('document_text'):
            with st.expander("Document Text Preview", expanded=False):
                st.text(results['document_text'])


def main():
    """Main application function"""
    initialize_session_state()
    
    # Check if API key is configured
    if not st.session_state.get('api_key') or not st.session_state.api_key_configured:
        # Show simple API key input screen
        st.markdown('<h1 class="main-header">Gemini 3 Hackathon Projects</h1>', unsafe_allow_html=True)
        
        # Simple API key input form
        with st.form("api_key_form", clear_on_submit=False):
            api_key_input = st.text_input(
                "Enter your Gemini API Key",
                type="password",
                placeholder="Paste your API key here...",
                label_visibility="visible"
            )
            submit_button = st.form_submit_button("Submit", type="primary", use_container_width=True)
            
            if submit_button:
                if api_key_input and len(api_key_input) > 20:
                    st.session_state.api_key = api_key_input
                    st.session_state.api_key_configured = True
                    st.rerun()
                else:
                    st.error("Please enter a valid API key")
        return
    
    # Header
    st.markdown('<h1 class="main-header">Gemini 3 Hackathon Projects</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## Select Project")
        st.markdown("---")
        
        project_choice = st.radio(
            "Choose a project:",
            ["Diagram Decoder", "Fine Print Translator"],
            index=0 if st.session_state.current_project is None else 
                  (0 if st.session_state.current_project == "diagram" else 1)
        )
    
    # Main content area
    if "Diagram Decoder" in project_choice:
        st.session_state.current_project = "diagram"
        render_diagram_decoder()
    else:
        st.session_state.current_project = "fine_print"
        render_fine_print_translator()
    


if __name__ == "__main__":
    main()

