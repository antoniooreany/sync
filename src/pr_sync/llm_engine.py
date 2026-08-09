import json
import os
import time
import urllib.request
import urllib.error
from typing import Optional

def _get_best_gemini_model(api_key: str) -> str:
    """Query the API to find an available flash model."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        req = urllib.request.Request(url, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=15.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            
            available_models = [m.get("name") for m in data.get("models", []) if "generateContent" in m.get("supportedGenerationMethods", [])]
            
            for target in [
                "models/gemini-2.0-flash-lite", 
                "models/gemini-flash-lite-latest", 
                "models/gemma-4-26b-a4b-it",
                "models/gemma-4-31b-it",
                "models/gemini-3.1-flash-lite",
                "models/gemini-3.5-flash-lite",
                "models/gemini-2.0-flash"
            ]:
                if target in available_models:
                    return target
                    
            for name in available_models:
                if "lite" in name and "vision" not in name and "2.5" not in name:
                    return name
                    
    except Exception as e:
        print(f"Failed to list Gemini models: {e}")
        
    return "models/gemini-2.0-flash"

def generate_smart_pr_summary(diff: str, commits: list[str], custom_model: Optional[str] = None) -> Optional[str]:
    """Uses LLM API to generate a smart summary and risk analysis."""
    ollama_model_raw = custom_model if custom_model else os.environ.get("OLLAMA_MODEL")
    ollama_model = ollama_model_raw.strip() if ollama_model_raw else None
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    
    if not ollama_model and not anthropic_key and not gemini_key:
        print("No OLLAMA_MODEL, ANTHROPIC_API_KEY, or GEMINI_API_KEY found.")
        return None

    prompt = f"""You are an expert software engineer reviewing a pull request.
Based on the following commits and git diff, generate a concise and meaningful PR description.
Do NOT just list the commits. Group the changes logically into features, bug fixes, and chores.
Analyze the risks based on the files changed.

Commits:
{chr(10).join(commits)}

Diff:
{diff[:4000]}

Respond with ONLY the markdown content for these two sections:
## Smart Summary
<your logical grouping of changes>

## Risk Analysis
<your assessment of risks>
"""

    if ollama_model:
        print(f" ⚙️  Using local Ollama API (Model: {ollama_model})...")
        url = "http://127.0.0.1:11434/api/generate"
        payload = {
            "model": ollama_model,
            "prompt": prompt,
            "stream": False
        }
        headers = {"Content-Type": "application/json"}
    elif anthropic_key:
        print(" ⚙️  Using Anthropic Claude API...")
        url = "https://api.anthropic.com/v1/messages"
        payload = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        }
        headers = {
            "x-api-key": anthropic_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
    else:
        print(" ⚙️  Using Google Gemini API...")
        model_name = _get_best_gemini_model(gemini_key)
        url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={gemini_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2}
        }
        headers = {"Content-Type": "application/json"}

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers
    )
    
    retries = 3
    delay = 10
    
    start_time = time.time()
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=120.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                elapsed = time.time() - start_time
                print(f" ✨ LLM API call completed in {elapsed:.2f} seconds.")
                if ollama_model:
                    return data["response"]
                elif anthropic_key:
                    return data["content"][0]["text"]
                else:
                    return data["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                print(f" ⚠️  Rate limited (429). Retrying in {delay} seconds (Attempt {attempt+1}/{retries})...")
                time.sleep(delay)
                delay *= 2
                continue
                
            print(f" ❌ API Error: {e}")
            try:
                print(f"    Response body: {e.read().decode('utf-8')}")
            except:
                pass
            return None
        except Exception as e:
            print(f" ❌ API Error: {e}")
            return None
            
    return None



