"""
Fine Print Translator Agent - Social Good Tool
Analyzes contracts, terms of service, and legal documents for hidden risks.
Uses Gemini 3's long context window and thinking capabilities.
"""
from typing import TypedDict, Annotated
import base64
from io import BytesIO
from PIL import Image
import pypdf

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from config import GEMINI_API_KEY, GEMINI_FLASH_MODEL, GEMINI_PRO_MODEL, THINKING_MODE


def extract_text_from_response(response):
    """Helper function to extract text content from LangChain response"""
    if hasattr(response, 'content'):
        if isinstance(response.content, str):
            return response.content
        elif isinstance(response.content, list):
            # Handle list of content blocks
            text_parts = []
            for block in response.content:
                if isinstance(block, dict):
                    # Handle dictionary blocks
                    if 'text' in block:
                        text_parts.append(block['text'])
                    elif 'type' in block and block.get('type') == 'text' and 'text' in block:
                        text_parts.append(block['text'])
                elif isinstance(block, str):
                    text_parts.append(block)
            return '\n'.join(text_parts) if text_parts else str(response.content)
        else:
            return str(response.content)
    else:
        return str(response)


class FinePrintState(TypedDict):
    """State for Fine Print Translator agent"""
    document_text: str  # Extracted text from document
    document_type: str  # Type of document (contract, ToS, medical form, etc.)
    risk_audit: str  # Output from Node 2
    risk_summary: str  # Output from Node 3 (Red/Yellow/Green report)
    api_key: str  # API key for Gemini
    messages: Annotated[list, add_messages]


def create_scanner_model(api_key=None):
    """Create Gemini Flash model for text extraction"""
    api_key = api_key or GEMINI_API_KEY
    return ChatGoogleGenerativeAI(
        model=GEMINI_FLASH_MODEL,
        google_api_key=api_key,
        temperature=0.1,
    )


def create_audit_model(api_key=None):
    """Create Gemini Pro model with thinking mode for risk analysis"""
    api_key = api_key or GEMINI_API_KEY
    # Gemini 3 models support thinking mode natively
    # The model will use thinking capabilities automatically for complex reasoning
    return ChatGoogleGenerativeAI(
        model=GEMINI_PRO_MODEL,
        google_api_key=api_key,
        temperature=0.1,
    )


def extract_text_from_image(image_base64: str, api_key: str = None) -> str:
    """Extract text from an image using Gemini's vision capabilities"""
    api_key = api_key or GEMINI_API_KEY
    vision_model = create_scanner_model(api_key=api_key)
    
    prompt = """Extract ALL text from this document image. Preserve the structure, formatting, and order of the text. Include everything - headers, paragraphs, fine print, footnotes, and any text in the margins. Be thorough and accurate."""

    try:
        # Create message with image using LangChain format
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": f"data:image/png;base64,{image_base64}"
                }
            ]
        )
        
        response = vision_model.invoke([message])
        return extract_text_from_response(response)
    except Exception as e:
        return f"Error extracting text: {str(e)}"


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from a PDF file"""
    try:
        pdf_file = BytesIO(pdf_bytes)
        reader = pypdf.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"


def node_1_scanner(state: FinePrintState) -> FinePrintState:
    """
    Node 1: Scanner - Extracts text from image/PDF
    Uses Gemini 3 Flash for fast text extraction
    """
    # If document_text is already provided, skip extraction
    if state.get("document_text") and state["document_text"]:
        return state
    
    # This node is typically called before state is set up
    # The actual extraction happens in the process_fine_print function
    return state


def node_2_audit(state: FinePrintState) -> FinePrintState:
    """
    Node 2: Audit - Uses Thinking Mode to look for predatory clauses
    Uses Gemini 3 Pro with Thinking: High for deep reasoning
    """
    api_key = state.get("api_key") or GEMINI_API_KEY
    audit_model = create_audit_model(api_key=api_key)
    
    document_text = state.get("document_text", "")
    document_type = state.get("document_type", "legal document")
    
    prompt = f"""You are an expert legal analyst specializing in identifying predatory clauses and hidden risks in {document_type}s.

Document Text:
{document_text}

Your task:
Analyze this document thoroughly and identify ALL potential risks, predatory clauses, and "gotchas" including:

1. **Hidden Fees & Charges**: Any fees that are not clearly disclosed upfront
2. **Auto-Renewal Clauses**: Automatic renewal without clear opt-out
3. **Privacy Risks**: Data sharing, selling, or usage rights that users might not expect
4. **Liability Limitations**: Clauses that limit the company's liability or shift risk to the user
5. **Binding Arbitration**: Forced arbitration clauses that prevent lawsuits
6. **Cancellation Penalties**: Fees or penalties for canceling
7. **Data Retention**: How long data is kept and what happens to it
8. **Jurisdiction Issues**: Unfavorable legal jurisdictions
9. **Modification Rights**: Ability to change terms without notice
10. **Waiver of Rights**: Any rights the user is giving up

For each risk found:
- Quote the exact clause or section
- Explain why it's problematic
- Rate the severity (High/Medium/Low)
- Note if it contradicts information elsewhere in the document

Be thorough. Check for contradictions between different sections. Use your reasoning capabilities to identify subtle risks that might not be obvious."""

    try:
        response = audit_model.invoke(prompt)
        audit_result = extract_text_from_response(response)
        
        return {
            **state,
            "risk_audit": audit_result
        }
    except Exception as e:
        error_msg = str(e)
        # Check if it's a quota error
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
            return {
                **state,
                "risk_audit": f"⚠️ Quota exceeded for Gemini 3 Pro. Please wait a moment and try again, or check your API quota limits.\n\nError: {error_msg[:200]}"
            }
        return {
            **state,
            "risk_audit": f"Error performing audit: {error_msg}"
        }


def node_3_summary(state: FinePrintState) -> FinePrintState:
    """
    Node 3: Summary - Outputs a Red/Yellow/Green risk report
    Uses Gemini 3 Flash for quick summary generation
    """
    api_key = state.get("api_key") or GEMINI_API_KEY
    summary_model = create_scanner_model(api_key=api_key)
    
    prompt = f"""You are a risk assessment expert. Based on the following audit results, create a clear, actionable risk summary report.

Risk Audit Results:
{state.get('risk_audit', '')}

Your task:
Create a comprehensive risk summary with:

1. **Overall Risk Level**: 
   - 🔴 RED (High Risk) - Multiple serious concerns, proceed with extreme caution
   - 🟡 YELLOW (Medium Risk) - Some concerns, review carefully before signing
   - 🟢 GREEN (Low Risk) - Generally safe, minor concerns only

2. **Executive Summary**: 2-3 sentence overview of the main risks

3. **Critical Issues** (if any): List the most serious problems that could significantly impact the user

4. **Moderate Concerns**: Issues that are worth noting but not deal-breakers

5. **Minor Notes**: Small concerns or things to be aware of

6. **Recommendations**: 
   - Should the user sign this? (Yes/No/With Modifications)
   - What should they do? (e.g., negotiate terms, seek legal advice, avoid)

Format the output clearly with emojis and sections. Make it easy for a non-legal expert to understand."""

    try:
        response = summary_model.invoke(prompt)
        summary = extract_text_from_response(response)
        
        return {
            **state,
            "risk_summary": summary
        }
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
            return {
                **state,
                "risk_summary": f"⚠️ Quota exceeded. Please wait a moment and try again.\n\nError: {error_msg[:200]}"
            }
        return {
            **state,
            "risk_summary": f"Error generating summary: {error_msg}"
        }


def create_fine_print_agent():
    """Create and return the Fine Print Translator LangGraph agent"""
    workflow = StateGraph(FinePrintState)
    
    # Add nodes
    workflow.add_node("scanner", node_1_scanner)
    workflow.add_node("audit", node_2_audit)
    workflow.add_node("summary", node_3_summary)
    
    # Define the flow
    workflow.set_entry_point("scanner")
    workflow.add_edge("scanner", "audit")
    workflow.add_edge("audit", "summary")
    workflow.add_edge("summary", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app


def process_fine_print(document_text: str = None, image_base64: str = None, 
                      pdf_bytes: bytes = None, document_type: str = "legal document",
                      api_key: str = None) -> dict:
    """
    Main function to process a document through the agent
    
    Args:
        document_text: Direct text input (optional)
        image_base64: Base64 encoded image of document (optional)
        pdf_bytes: PDF file bytes (optional)
        document_type: Type of document (e.g., "Terms of Service", "Rental Agreement")
        api_key: Gemini API key (optional, falls back to env var)
        
    Returns:
        Dictionary with risk_audit and risk_summary
    """
    api_key = api_key or GEMINI_API_KEY
    
    # Extract text if not provided
    if not document_text:
        if image_base64:
            document_text = extract_text_from_image(image_base64, api_key=api_key)
        elif pdf_bytes:
            document_text = extract_text_from_pdf(pdf_bytes)
        else:
            return {
                "error": "No document input provided. Please provide text, image, or PDF."
            }
    
    agent = create_fine_print_agent()
    
    initial_state = {
        "document_text": document_text,
        "document_type": document_type,
        "risk_audit": "",
        "risk_summary": "",
        "api_key": api_key,
        "messages": []
    }
    
    # Run the agent
    final_state = agent.invoke(initial_state)
    
    return {
        "document_text": final_state.get("document_text", "")[:500] + "..." if len(final_state.get("document_text", "")) > 500 else final_state.get("document_text", ""),  # Preview
        "risk_audit": final_state.get("risk_audit", ""),
        "risk_summary": final_state.get("risk_summary", "")
    }

