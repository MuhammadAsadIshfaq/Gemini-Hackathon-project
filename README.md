# 🚀 Gemini 3 Hackathon Projects

Two innovative AI-powered applications built with Google's Gemini 3 API, combining advanced reasoning, multimodal vision, and long context capabilities.

## 📋 Projects Overview

### 1. 📚 Diagram Decoder (Education)
**Problem Solved:** Students struggle to understand complex diagrams in textbooks.

**Solution:** An AI agent that converts static diagrams into interactive, step-by-step explanations with quiz questions.

**Features:**
- 🔍 **Vision Identification**: Uses Gemini 3 Flash to identify all components, labels, and relationships in diagrams
- 🧠 **Logic Explanation**: Uses Gemini 3 Pro with Thinking Mode to explain causal relationships and processes
- 📝 **Quiz Generation**: Creates educational quiz questions to test understanding

**Perfect for:** Biology, Physics, Engineering, Chemistry diagrams

---

### 2. 📄 Fine Print Translator (Social Good)
**Problem Solved:** People sign contracts and terms of service without understanding hidden risks.

**Solution:** An AI agent that analyzes legal documents for predatory clauses and provides clear risk assessments.

**Features:**
- 📖 **Text Extraction**: Extracts text from images, PDFs, or direct input
- 🔎 **Risk Audit**: Uses Thinking Mode to identify hidden fees, auto-renewals, privacy risks, and more
- 🚦 **Risk Summary**: Provides Red/Yellow/Green risk ratings with actionable recommendations

**Perfect for:** Terms of Service, Rental Agreements, Medical Forms, Employment Contracts

---

## 🎯 Gemini 3 Features Utilized

### Technical Excellence
- ✅ **Multimodal Vision**: Processing images and extracting information from diagrams
- ✅ **Thinking Mode (High)**: Deep reasoning for causal analysis and risk detection
- ✅ **Long Context Window**: Analyzing entire 50+ page documents without losing context
- ✅ **Fast Processing**: Using Flash model for quick responses where appropriate
- ✅ **LangGraph Orchestration**: Complex multi-node agent workflows

### Innovation Highlights
1. **Causal Reasoning**: Diagram Decoder explains not just what's in a diagram, but WHY and HOW components interact
2. **Cross-Document Analysis**: Fine Print Translator finds contradictions between different sections
3. **Educational Focus**: Both tools solve real-world problems with practical applications

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- Google Gemini 3 API key ([Get it here](https://aistudio.google.com/apikey))

### Step 1: Clone or Download
```bash
cd "D:\Hackathons\Geminie hackthon"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API Key
1. Copy `.env.example` to `.env`
2. Add your Gemini API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 4: Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
.
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration and settings
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── README.md                       # This file
└── agents/
    ├── __init__.py                 # Package initialization
    ├── diagram_decoder.py          # Diagram Decoder LangGraph agent
    └── fine_print_translator.py    # Fine Print Translator LangGraph agent
```

---

## 🎨 How to Use

### Diagram Decoder
1. Select "Diagram Decoder 📚" from the sidebar
2. Upload an image of a diagram (PNG, JPG, JPEG)
3. Click "Analyze Diagram"
4. Review the three-part analysis:
   - Component identification
   - Step-by-step explanation
   - Quiz questions

### Fine Print Translator
1. Select "Fine Print Translator 📄" from the sidebar
2. Choose document type (ToS, Rental Agreement, etc.)
3. Upload image/PDF or paste text
4. Click "Analyze Document"
5. Review the risk assessment:
   - Risk summary with color-coded rating
   - Detailed audit of all risks found
   - Recommendations

---

## 🔧 Technical Architecture

### LangGraph Agent Workflows

#### Diagram Decoder Flow:
```
[Image Upload] 
    ↓
[Node 1: Vision Identification] → Gemini Flash
    ↓
[Node 2: Logic Explanation] → Gemini Pro (Thinking: High)
    ↓
[Node 3: Quiz Generation] → Gemini Flash
    ↓
[Results Display]
```

#### Fine Print Translator Flow:
```
[Document Input] 
    ↓
[Node 1: Text Extraction] → Gemini Flash / PyPDF
    ↓
[Node 2: Risk Audit] → Gemini Pro (Thinking: High)
    ↓
[Node 3: Risk Summary] → Gemini Flash
    ↓
[Results Display]
```

### Key Technologies
- **LangGraph**: Agent orchestration and state management
- **LangChain**: LLM integration and prompt management
- **Streamlit**: Beautiful, interactive web interface
- **Pillow**: Image processing
- **PyPDF**: PDF text extraction

---

## 🎯 Hackathon Submission Details

### Gemini 3 Integration Description

**Diagram Decoder:**
- Uses Gemini 3 Flash for fast multimodal vision processing to identify diagram components
- Leverages Gemini 3 Pro with Thinking Mode (High) for deep causal reasoning about how diagram components interact
- Processes entire diagram images in a single pass, maintaining context across all elements

**Fine Print Translator:**
- Utilizes Gemini 3's long context window to analyze entire documents (50+ pages) without losing track of cross-references
- Employs Thinking Mode (High) to identify subtle contradictions and predatory clauses that require complex reasoning
- Combines vision capabilities (for image-based documents) with text processing for comprehensive analysis

Both agents are central to their respective applications - the entire value proposition depends on Gemini 3's advanced reasoning and multimodal capabilities.

### Demo Video Points
1. Show Diagram Decoder analyzing a biology/physics diagram
2. Demonstrate the step-by-step explanation and quiz generation
3. Show Fine Print Translator analyzing a Terms of Service document
4. Highlight the risk assessment and recommendations
5. Emphasize the real-world impact and use cases

---

## 🏆 Why This Will Win

### Technical Execution (40%)
- ✅ Clean, modular code architecture
- ✅ Proper error handling and user feedback
- ✅ Efficient use of Gemini 3's capabilities
- ✅ Production-ready Streamlit interface

### Potential Impact (20%)
- ✅ **Diagram Decoder**: Helps millions of students understand complex concepts
- ✅ **Fine Print Translator**: Protects consumers from predatory contracts
- ✅ Both solve real, widespread problems

### Innovation / Wow Factor (30%)
- ✅ Novel application of Thinking Mode for educational explanations
- ✅ Creative use of multimodal vision for diagram analysis
- ✅ Long context window for comprehensive document analysis
- ✅ Two distinct, valuable use cases in one app

### Presentation / Demo (10%)
- ✅ Beautiful, intuitive UI
- ✅ Clear documentation
- ✅ Well-structured code
- ✅ Easy to understand and demonstrate

---

## 📝 License

This project is built for the Gemini 3 Hackathon. All code is provided as-is for demonstration purposes.

---

## 🙏 Acknowledgments

- Google DeepMind for the Gemini 3 API
- LangChain team for LangGraph
- Streamlit for the amazing framework

---

## 📧 Support

For issues or questions, please refer to the hackathon submission page or check the code comments for implementation details.

**Good luck with the hackathon! 🚀**

