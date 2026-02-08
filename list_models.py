"""
Utility script to list available Gemini models
Run this to see what models are available with your API key
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY", "")
if not api_key:
    print("❌ GEMINI_API_KEY not found in environment")
    print("   Set it in .env file or as environment variable")
    exit(1)

try:
    genai.configure(api_key=api_key)
    
    print("=" * 60)
    print("Available Gemini Models")
    print("=" * 60)
    
    models = genai.list_models()
    
    available_models = []
    for model in models:
        # Only show models that support generateContent
        if 'generateContent' in model.supported_generation_methods:
            available_models.append(model.name)
            print(f"✅ {model.name}")
            if hasattr(model, 'display_name'):
                print(f"   Display Name: {model.display_name}")
            print()
    
    print("=" * 60)
    print(f"Total: {len(available_models)} models available")
    print("=" * 60)
    
    # Suggest models for our use case
    print("\n💡 Recommended models for this project:")
    vision_models = [m for m in available_models if 'flash' in m.lower() or 'vision' in m.lower() or 'pro' in m.lower()]
    thinking_models = [m for m in available_models if 'thinking' in m.lower() or 'pro' in m.lower()]
    
    if vision_models:
        print(f"   Vision/Flash: {vision_models[0]}")
    if thinking_models:
        print(f"   Thinking/Pro: {thinking_models[0]}")
    elif vision_models:
        print(f"   Thinking/Pro: {vision_models[0]} (use for reasoning)")
    
except Exception as e:
    print(f"❌ Error listing models: {str(e)}")
    print("\nTrying alternative method...")
    
    # Try with langchain
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Test common model names
        test_models = [
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-2.0-flash",
            "gemini-pro",
            "gemini-pro-vision"
        ]
        
        print("\nTesting common model names:")
        for model_name in test_models:
            try:
                llm = ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=api_key,
                    temperature=0.1
                )
                # Just test if it can be created
                print(f"✅ {model_name} - Available")
            except Exception as e:
                if "404" in str(e) or "NOT_FOUND" in str(e):
                    print(f"❌ {model_name} - Not found")
                else:
                    print(f"⚠️ {model_name} - Error: {str(e)[:50]}")
    except Exception as e2:
        print(f"❌ Alternative method also failed: {str(e2)}")

