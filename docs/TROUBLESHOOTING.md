# Troubleshooting Guide

Common issues and solutions for AI Prompt Engineering tools.

## Table of Contents

- [Installation Issues](#installation-issues)
- [API Key Configuration](#api-key-configuration)
- [LLM Provider Issues](#llm-provider-issues)
- [Prompt Validator Issues](#prompt-validator-issues)
- [Streamlit Dashboard Issues](#streamlit-dashboard-issues)
- [Performance Issues](#performance-issues)
- [Common Errors](#common-errors)

---

## Installation Issues

### Issue: Package Installation Fails

**Error:**
```
ERROR: Could not find a version that satisfies the requirement...
```

**Solution:**
1. Update pip: `python -m pip install --upgrade pip`
2. Use Python 3.8 or higher
3. Check requirements.txt for correct package names
4. Install packages individually to identify problematic ones

**Example:**
```bash
pip install openai
pip install anthropic
pip install streamlit
```

---

### Issue: Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'openai'
```

**Solution:**
1. Ensure virtual environment is activated
2. Reinstall requirements: `pip install -r requirements.txt`
3. Check Python path: `python -c "import sys; print(sys.path)"`
4. Use full path to modules: `from notebooks.prompt_validator import PromptValidator`

---

## API Key Configuration

### Issue: API Key Not Found

**Error:**
```
ValueError: OPENAI_API_KEY not found in environment
```

**Solution:**

#### Option 1: Environment Variables (Recommended)

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
```

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=sk-your-key-here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

**Permanent (Linux/Mac):**
Add to `~/.bashrc` or `~/.zshrc`:
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

#### Option 2: .env File

Create `.env` file in project root:
```
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Install python-dotenv:
```bash
pip install python-dotenv
```

Load in code:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

### Issue: Invalid API Key

**Error:**
```
401 Authentication failed
```

**Solution:**
1. Verify API key is correct
2. Check for extra spaces or quotes
3. Ensure key hasn't expired
4. Verify account has sufficient credits
5. Check API key permissions

---

## LLM Provider Issues

### Issue: Ollama Not Available

**Error:**
```
Connection refused to http://localhost:11434
```

**Solution:**
1. Install Ollama: https://ollama.ai
2. Start Ollama service
3. Pull a model: `ollama pull llama2`
4. Verify connection:
```bash
curl http://localhost:11434/api/tags
```

**Alternative:**
Use different provider (OpenAI or Anthropic)

---

### Issue: Rate Limits Exceeded

**Error:**
```
429 Too Many Requests
```

**Solution:**
1. Add rate limiting:
```python
import time

def rate_limited_generate(client, prompt, delay=1):
    time.sleep(delay)
    return client.generate(prompt)
```

2. Use exponential backoff
3. Upgrade API tier for higher limits
4. Reduce request frequency

---

### Issue: Model Not Available

**Error:**
```
Model not found: gpt-5
```

**Solution:**
1. Check available models:
```python
client.get_available_models()
```

2. Use correct model name
3. Ensure model is available in your region/tier
4. Check model status on provider's website

---

## Prompt Validator Issues

### Issue: Low Scores for Good Prompts

**Problem:**
Prompt works well but validator gives low score.

**Solution:**
1. Check breakdown to see which criteria failed
2. Validator emphasizes structure - add clear sections
3. Add examples if score is low
4. Be more specific with requirements

**Example:**
```python
result = validator.score_prompt(prompt)
print(result['breakdown'])  # See detailed scores
print(result['feedback'])   # Get improvement suggestions
```

---

### Issue: Validator Too Strict

**Problem:**
All prompts get low scores.

**Solution:**
1. Review scoring criteria in code
2. Adjust weights if needed:
```python
validator.criteria_weights['clarity'] = 0.30  # Increase weight
validator.criteria_weights['examples'] = 0.10  # Decrease weight
```

3. Use as guideline, not absolute truth
4. Consider prompt effectiveness in practice

---

## Streamlit Dashboard Issues

### Issue: Dashboard Won't Start

**Error:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
```bash
pip install streamlit
streamlit run streamlit_app.py
```

---

### Issue: Import Errors in Dashboard

**Error:**
```
ImportError: cannot import name 'PromptValidator' from 'notebooks.prompt_validator'
```

**Solution:**
1. Check file structure:
```
project/
├── notebooks/
│   └── prompt_validator.py
└── streamlit_app.py
```

2. Add notebooks to path:
```python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "notebooks"))
```

3. Use relative imports if needed

---

### Issue: Dashboard Freezes

**Problem:**
Dashboard becomes unresponsive.

**Solution:**
1. Check for infinite loops
2. Add timeout to LLM calls:
```python
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Request timed out")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)  # 30 second timeout
```

3. Reduce number of concurrent requests
4. Restart Streamlit server

---

## Performance Issues

### Issue: Slow Response Times

**Problem:**
LLM responses take too long.

**Solutions:**

1. **Reduce max_tokens:**
```python
response = client.generate(prompt, max_tokens=500)  # Instead of 2000
```

2. **Use faster model:**
```python
client = UnifiedLLMClient(provider=OpenAIProvider(model="gpt-3.5-turbo"))  # Faster than gpt-4
```

3. **Enable caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_generate(prompt):
    return client.generate(prompt)
```

4. **Use streaming for long outputs**

---

### Issue: High Token Usage

**Problem:**
Using too many tokens, high costs.

**Solutions:**

1. **Reduce prompt length:**
   - Remove unnecessary context
   - Use concise language

2. **Limit output:**
```python
response = client.generate(prompt, max_tokens=200)
```

3. **Use cheaper models:**
   - gpt-3.5-turbo instead of gpt-4
   - Claude Haiku instead of Opus

4. **Monitor usage:**
```python
print(f"Tokens used: {response.tokens_used}")
```

---

## Common Errors

### Error: "No LLM provider available"

**Cause:** No API keys configured.

**Solution:**
```bash
# Set at least one API key
export OPENAI_API_KEY="sk-..."
# OR
export ANTHROPIC_API_KEY="sk-ant-..."
# OR
# Start Ollama service
```

---

### Error: "Production validation failed"

**Cause:** Edge cases not handled.

**Solution:**
1. Review test results:
```python
result = validator.validate_in_production(prompt_id, run_fn)
print(result['recommendations'])
```

2. Add error handling:
```python
def safe_run_prompt(input_data: str) -> str:
    try:
        return run_prompt(input_data)
    except Exception as e:
        return f"Error: {str(e)}"
```

3. Handle empty/invalid inputs

---

### Error: "A/B test has insufficient data"

**Cause:** Not enough test results.

**Solution:**
```python
# Need at least 10 results per version
for _ in range(10):
    version, prompt = tester.get_random_prompt(test_id)
    output = run_prompt(prompt)
    score = evaluate_output(output)
    tester.record_result(test_id, version, score, output)
```

---

## Getting Help

If you're still experiencing issues:

1. **Check Issues:**
   - Search existing GitHub issues
   - Check closed issues for solutions

2. **Create New Issue:**
   - Include error messages
   - Provide environment details
   - Include minimal reproduction code

3. **Community:**
   - Join discussions
   - Ask questions
   - Share solutions

---

## Tips for Smooth Operation

1. **Use Virtual Environments:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Keep Dependencies Updated:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Monitor API Usage:**
   - Set usage limits
   - Track costs
   - Use monitoring tools

4. **Test Incrementally:**
   - Test simple prompts first
   - Gradually increase complexity
   - Validate results

5. **Use Logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)
   logger.info("Starting prompt validation")
   ```

---

## Additional Resources

- [API Reference](API_REFERENCE.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [GitHub Issues](https://github.com/ElaMCB/AI-Prompt-Engineering/issues)

---

**Still stuck?** Open an issue with:
- Error message
- Steps to reproduce
- Environment details
- Code example (if applicable)
