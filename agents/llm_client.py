import os
import sys
import json
import urllib.request
import urllib.error
import time

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def log_debug(msg):
    print(f"[DEBUG] [LLMClient] {msg}", file=sys.stderr)

def send_request_with_retry(req, timeout=60, retries=4):
    delay = 3
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code in [429, 500, 502, 503] and attempt < retries - 1:
                log_debug(f"HTTP {e.code} error on attempt {attempt+1}/{retries}. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
            else:
                raise e

def call_llm(prompt, json_mode=False):
    provider = os.environ.get("LLM_PROVIDER")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    
    if not provider:
        if gemini_key:
            provider = "gemini"
        elif anthropic_key:
            provider = "anthropic"
        elif openai_key:
            provider = "openai"
        else:
            log_debug("ERROR: No API key found in environment (GEMINI_API_KEY, ANTHROPIC_API_KEY, or OPENAI_API_KEY).")
            raise ValueError("No LLM provider keys detected in environment.")
            
    provider = provider.lower()
    
    if provider == "gemini":
        if not gemini_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
        log_debug(f"Routing to Google Gemini using model: {model}")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        if json_mode:
            payload["generationConfig"] = {"responseMimeType": "application/json"}
        
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        res_text = send_request_with_retry(req, timeout=60)
        res_data = json.loads(res_text)
        return res_data["candidates"][0]["content"]["parts"][0]["text"]
        
    elif provider == "anthropic":
        if not anthropic_key:
            raise ValueError("ANTHROPIC_API_KEY is not set.")
        model = os.environ.get("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        log_debug(f"Routing to Anthropic using model: {model}")
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": anthropic_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        
        full_prompt = prompt
        if json_mode:
            full_prompt += "\nOutput response strictly as a valid, parsable JSON block. Do not include markdown wraps."
            
        payload = {
            "model": model,
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": full_prompt}]
        }
        
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        res_text = send_request_with_retry(req, timeout=60)
        res_data = json.loads(res_text)
        return res_data["content"][0]["text"]
        
    elif provider == "openai":
        if not openai_key:
            raise ValueError("OPENAI_API_KEY is not set.")
        model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        log_debug(f"Routing to OpenAI using model: {model}")
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {openai_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
            
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        res_text = send_request_with_retry(req, timeout=60)
        res_data = json.loads(res_text)
        return res_data["choices"][0]["message"]["content"]
        
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
