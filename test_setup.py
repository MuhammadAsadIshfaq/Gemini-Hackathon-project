"""
Simple test script to verify setup and API connection
Run this to check if everything is configured correctly
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    try:
        import streamlit
        print("✅ Streamlit installed")
    except ImportError:
        print("❌ Streamlit not installed")
        return False
    
    try:
        import langgraph
        print("✅ LangGraph installed")
    except ImportError:
        print("❌ LangGraph not installed")
        return False
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ LangChain Google GenAI installed")
    except ImportError:
        print("❌ LangChain Google GenAI not installed")
        return False
    
    try:
        import pypdf
        print("✅ PyPDF installed")
    except ImportError:
        print("❌ PyPDF not installed")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow installed")
    except ImportError:
        print("❌ Pillow not installed")
        return False
    
    return True


def test_api_key():
    """Test if API key is configured"""
    print("\nTesting API key...")
    api_key = os.getenv("GEMINI_API_KEY", "")
    if api_key:
        if len(api_key) > 20:  # Basic validation
            print(f"✅ API key found (length: {len(api_key)})")
            return True
        else:
            print("⚠️ API key seems too short, might be invalid")
            return False
    else:
        print("❌ API key not found in environment")
        print("   Create a .env file with: GEMINI_API_KEY=your_key_here")
        return False


def test_config():
    """Test if config file loads correctly"""
    print("\nTesting configuration...")
    try:
        from config import GEMINI_API_KEY, GEMINI_FLASH_MODEL, GEMINI_PRO_MODEL
        print(f"✅ Config loaded")
        print(f"   Flash Model: {GEMINI_FLASH_MODEL}")
        print(f"   Pro Model: {GEMINI_PRO_MODEL}")
        return True
    except Exception as e:
        print(f"❌ Config error: {str(e)}")
        return False


def test_agents():
    """Test if agents can be imported"""
    print("\nTesting agents...")
    try:
        from agents import process_diagram, process_fine_print
        print("✅ Agents imported successfully")
        return True
    except Exception as e:
        print(f"❌ Agent import error: {str(e)}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("Gemini 3 Hackathon - Setup Test")
    print("=" * 50)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("API Key", test_api_key()))
    results.append(("Config", test_config()))
    results.append(("Agents", test_agents()))
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 All tests passed! You're ready to run the app.")
        print("   Run: streamlit run app.py")
    else:
        print("⚠️ Some tests failed. Please fix the issues above.")
    print("=" * 50)

