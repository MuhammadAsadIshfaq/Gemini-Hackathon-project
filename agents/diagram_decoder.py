"""
Diagram Decoder Agent - Education Tool
Converts static diagrams into interactive step-by-step explanations with quizzes.
Uses Gemini 3's multimodal vision and thinking capabilities.
"""
from typing import TypedDict, Annotated
import base64
from io import BytesIO
from PIL import Image

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


class DiagramDecoderState(TypedDict):
    """State for Diagram Decoder agent"""
    image: str  # Base64 encoded image
    image_description: str  # Output from Node 1
    logical_explanation: str  # Output from Node 2
    quiz_questions: str  # Output from Node 3
    api_key: str  # API key for Gemini
    messages: Annotated[list, add_messages]


def create_vision_model(api_key=None):
    """Create Gemini Flash model for vision tasks"""
    api_key = api_key or GEMINI_API_KEY
    return ChatGoogleGenerativeAI(
        model=GEMINI_FLASH_MODEL,
        google_api_key=api_key,
        temperature=0.3,
    )


def create_thinking_model(api_key=None):
    """Create Gemini Pro model with thinking mode for reasoning"""
    api_key = api_key or GEMINI_API_KEY
    # Gemini 3 models support thinking mode natively
    # Try to enable thinking mode if supported by the model
    model_kwargs = {}
    if "thinking" in GEMINI_PRO_MODEL.lower() or "3" in GEMINI_PRO_MODEL:
        # For Gemini 3 models, thinking is built-in and can be enhanced via prompts
        # The model will use thinking capabilities automatically for complex reasoning
        pass
    
    return ChatGoogleGenerativeAI(
        model=GEMINI_PRO_MODEL,
        google_api_key=api_key,
        temperature=0.2,
        **model_kwargs
    )


def node_1_vision_identification(state: DiagramDecoderState) -> DiagramDecoderState:
    """
    Node 1: The Eye - Identifies all labels and components in the diagram
    Uses Gemini 3 Flash for fast multimodal vision processing
    """
    api_key = state.get("api_key") or GEMINI_API_KEY
    vision_model = create_vision_model(api_key=api_key)
    
    prompt = """You are an expert diagram analyzer. Analyze this educational diagram image carefully.

Your task:
1. Identify ALL visible labels, components, parts, and elements in the diagram
2. Describe what each part is and its purpose
3. Note any arrows, connections, or relationships between parts
4. Identify the subject matter (biology, physics, engineering, chemistry, etc.)
5. Describe the overall structure and layout

Be thorough and detailed. List everything you can see, as this will be used to explain the diagram to a student."""

    try:
        # Convert base64 to image for the model
        image_data = base64.b64decode(state["image"])
        image = Image.open(BytesIO(image_data))
        
        # Create message with image using LangChain format
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": f"data:image/png;base64,{state['image']}"
                }
            ]
        )
        
        response = vision_model.invoke([message])
        description = extract_text_from_response(response)
        
        return {
            **state,
            "image_description": description
        }
    except Exception as e:
        return {
            **state,
            "image_description": f"Error analyzing image: {str(e)}"
        }


def node_2_logic_explanation(state: DiagramDecoderState) -> DiagramDecoderState:
    """
    Node 2: The Logic - Explains the physics/logic/process shown in the diagram
    Uses Gemini 3 Pro with Thinking: High for causal reasoning
    """
    api_key = state.get("api_key") or GEMINI_API_KEY
    thinking_model = create_thinking_model(api_key=api_key)
    
    prompt = f"""You are an expert educator. Based on the following diagram analysis, create a step-by-step explanation of the process, mechanism, or concept shown in the diagram.

Diagram Analysis:
{state['image_description']}

Your task:
1. Explain the diagram as an interactive step-by-step story
2. Use causal reasoning: explain how one part affects another (e.g., "When Part A moves, it causes Part B to rotate because...")
3. Break down complex processes into clear, numbered steps
4. Use simple language that a student can understand
5. Highlight the key relationships and cause-effect chains
6. Explain WHY things happen, not just WHAT happens

Format your response as:
- Step 1: [Description]
- Step 2: [Description]
- etc.

Be thorough and educational. Help the student understand not just what they see, but how it all works together."""

    try:
        response = thinking_model.invoke(prompt)
        explanation = extract_text_from_response(response)
        
        return {
            **state,
            "logical_explanation": explanation
        }
    except Exception as e:
        error_msg = str(e)
        # Check if it's a quota error
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
            return {
                **state,
                "logical_explanation": f"⚠️ Quota exceeded for Gemini 3 Pro. Please wait a moment and try again, or check your API quota limits.\n\nError: {error_msg[:200]}"
            }
        return {
            **state,
            "logical_explanation": f"Error generating explanation: {error_msg}"
        }


def node_3_quiz_generation(state: DiagramDecoderState) -> DiagramDecoderState:
    """
    Node 3: The Quiz - Generates questions to test understanding
    Uses Gemini 3 Flash for quick question generation
    """
    api_key = state.get("api_key") or GEMINI_API_KEY
    quiz_model = create_vision_model(api_key=api_key)
    
    prompt = f"""You are an expert educator creating assessment questions. Based on the diagram analysis and explanation below, generate 3 high-quality quiz questions that test the student's understanding.

Diagram Analysis:
{state['image_description']}

Step-by-Step Explanation:
{state['logical_explanation']}

Your task:
Generate exactly 3 quiz questions that:
1. Test understanding of the key concepts shown in the diagram
2. Require the student to apply the causal relationships explained
3. Range from basic recall to application-level thinking
4. Are clear, unambiguous, and educational

Format each question as:
Question 1: [Question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Correct Answer: [Letter] - [Brief explanation]

Question 2: [Question text]
...

Make sure the questions are directly related to the diagram and explanation provided."""

    try:
        response = quiz_model.invoke(prompt)
        quiz = extract_text_from_response(response)
        
        return {
            **state,
            "quiz_questions": quiz
        }
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
            return {
                **state,
                "quiz_questions": f"⚠️ Quota exceeded. Please wait a moment and try again.\n\nError: {error_msg[:200]}"
            }
        return {
            **state,
            "quiz_questions": f"Error generating quiz: {error_msg}"
        }


def create_diagram_decoder_agent():
    """Create and return the Diagram Decoder LangGraph agent"""
    workflow = StateGraph(DiagramDecoderState)
    
    # Add nodes
    workflow.add_node("vision_identification", node_1_vision_identification)
    workflow.add_node("logic_explanation", node_2_logic_explanation)
    workflow.add_node("quiz_generation", node_3_quiz_generation)
    
    # Define the flow
    workflow.set_entry_point("vision_identification")
    workflow.add_edge("vision_identification", "logic_explanation")
    workflow.add_edge("logic_explanation", "quiz_generation")
    workflow.add_edge("quiz_generation", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app


def process_diagram(image_base64: str, api_key: str = None) -> dict:
    """
    Main function to process a diagram image through the agent
    
    Args:
        image_base64: Base64 encoded image string
        api_key: Gemini API key (optional, falls back to env var)
        
    Returns:
        Dictionary with image_description, logical_explanation, and quiz_questions
    """
    agent = create_diagram_decoder_agent()
    
    initial_state = {
        "image": image_base64,
        "image_description": "",
        "logical_explanation": "",
        "quiz_questions": "",
        "api_key": api_key or GEMINI_API_KEY,
        "messages": []
    }
    
    # Run the agent
    final_state = agent.invoke(initial_state)
    
    return {
        "image_description": final_state.get("image_description", ""),
        "logical_explanation": final_state.get("logical_explanation", ""),
        "quiz_questions": final_state.get("quiz_questions", "")
    }

