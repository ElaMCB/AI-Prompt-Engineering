# Quick Start Guide

Get up and running with AI Prompt Engineering tools in minutes.

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [First Steps](#first-steps)
- [Next Steps](#next-steps)

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- API key (OpenAI, Anthropic, or Ollama)

### Step 1: Clone Repository

```bash
git clone https://github.com/ElaMCB/AI-Prompt-Engineering.git
cd AI-Prompt-Engineering
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up API Keys

**Option 1: Environment Variables**

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

**Option 2: .env File**

Create `.env` file in project root:
```
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Option 3: Ollama (Local - No API Key Needed)**

1. Install Ollama: https://ollama.ai
2. Start Ollama service
3. Pull a model: `ollama pull llama2`

---

## Basic Usage

### 1. Prompt Validator

Validate and score prompts instantly:

```python
from notebooks.prompt_validator import PromptValidator

validator = PromptValidator()

prompt = """
You are a conversion copywriter specializing in SaaS email marketing. 
Write a 200-word welcome email for new trial users of a project management tool. 
Target audience: small business owners who just signed up but haven't logged in yet. 
Must include: specific next steps, one key benefit, and a clear call-to-action.
"""

result = validator.score_prompt(prompt)
print(f"Score: {result['overall_score']}%")
print(f"Grade: {result['grade']}")

for feedback in result['feedback']:
    print(f"- {feedback}")
```

### 2. LLM Playground

Test prompts with real LLM providers:

```python
from notebooks.model_providers import UnifiedLLMClient

# Auto-detect provider (uses available API keys)
client = UnifiedLLMClient()

# Generate response
response = client.generate(
    "Write a haiku about AI",
    max_tokens=100,
    temperature=0.8
)

if response.error:
    print(f"Error: {response.error}")
else:
    print(response.content)
    print(f"Latency: {response.latency_ms:.0f}ms")
    print(f"Tokens: {response.tokens_used}")
```

### 3. A/B Testing

Compare different prompt versions:

```python
from notebooks.ab_testing_framework import PromptABTester

tester = PromptABTester()

# Create test
test = tester.create_test(
    test_id="email_subject_test",
    prompt_a="Write a subject line",
    prompt_b="You are an email marketing expert. Write a compelling subject line...",
    metric="click_through_rate",
    description="Testing generic vs specific prompt"
)

# Record results
tester.record_result("email_subject_test", "A", 4.2, "Weekly Newsletter")
tester.record_result("email_subject_test", "B", 8.1, "5 Growth Hacks That Doubled Revenue")

# Analyze
analysis = tester.analyze_test("email_subject_test")
print(f"Winner: {analysis['winner']}")
print(tester.generate_report("email_subject_test"))
```

### 4. Production Validator

Test prompts for production deployment:

```python
from notebooks.production_validator import ProductionValidator, TestCase
from notebooks.model_providers import UnifiedLLMClient

validator = ProductionValidator()
client = UnifiedLLMClient()

# Add test case
test_case = TestCase(
    input_data="Test input",
    expected_output_type="text",
    expected_keywords=["response"],
    min_length=10,
    max_length=500
)
validator.add_test_case("my_prompt", test_case)

# Create prompt function
def run_prompt(input_data: str) -> str:
    prompt = f"You are a helpful assistant. Respond to: {input_data}"
    response = client.generate(prompt)
    return response.content if not response.error else ""

# Run validation
result = validator.validate_in_production("my_prompt", run_prompt)

print(f"Production Ready Score: {result['production_ready_score']}%")
print(f"Production Ready: {result['production_ready']}")

for recommendation in result['recommendations']:
    print(f"- {recommendation}")
```

---

## First Steps

### Step 1: Run the Streamlit Dashboard

```bash
streamlit run streamlit_app.py
```

This opens an interactive dashboard in your browser at `http://localhost:8501`.

**Features:**
- Prompt Validator - Score prompts instantly
- LLM Playground - Test prompts with real models
- Production Validator - Validate for deployment
- A/B Testing - Compare prompt versions
- Progress Tracker - Track your learning

### Step 2: Validate Your First Prompt

1. Open the **Prompt Validator** tab in the dashboard
2. Enter a prompt in the text area
3. Click "Validate Prompt"
4. Review score, feedback, and suggestions

### Step 3: Test with Real LLM

1. Open the **LLM Playground** tab
2. Ensure your API key is configured
3. Enter a prompt
4. Click "Generate Response"
5. Review response and metrics

---

## Next Steps

### 1. Learn the CLEAR Framework

The validator uses the CLEAR framework:
- **C**ontext - Set a clear role
- **L**ength - Specify output length
- **E**xamples - Provide examples
- **A**udience - Define target audience
- **R**equirements - List specific requirements

### 2. Practice with Exercises

- Fix broken prompts in `notebooks/foundations_lab.ipynb`
- Complete challenges in the course roadmap
- Build portfolio projects

### 3. Explore Advanced Features

- Set up A/B testing for production
- Use production validator before deployment
- Track your progress with progress tracker
- Try different LLM providers

### 4. Join the Community

- Star the repository
- Report issues
- Contribute improvements
- Share your success stories

---

## Common Examples

### Example 1: Improving a Bad Prompt

**Before:**
```python
prompt = "Write something about marketing"
result = validator.score_prompt(prompt)
# Score: 25% - D (Poor - Needs Major Revision)
```

**After:**
```python
prompt = """
You are a conversion copywriter specializing in SaaS email marketing. 
Write a 200-word welcome email for new trial users of a project management tool. 
Target audience: small business owners who just signed up but haven't logged in yet. 
Must include: specific next steps, one key benefit, and a clear call-to-action.
Tone should be friendly but professional.
"""
result = validator.score_prompt(prompt)
# Score: 87% - A (Very Good)
```

### Example 2: A/B Testing Email Subject Lines

```python
tester = PromptABTester()

# Create test
tester.create_test(
    test_id="email_subject_ab",
    prompt_a="Write a subject line for our newsletter",
    prompt_b="""You are an email marketing expert. Write a compelling subject line 
    for our weekly newsletter targeting small business owners. Focus on urgency and value. 
    Keep under 50 characters.""",
    metric="click_through_rate",
    description="Testing generic vs specific prompt"
)

# Test both versions multiple times
for _ in range(20):
    version, prompt = tester.get_random_prompt("email_subject_ab")
    # Run prompt, get output, evaluate...
    tester.record_result("email_subject_ab", version, score, output)

# Analyze results
analysis = tester.analyze_test("email_subject_ab")
print(tester.generate_report("email_subject_ab"))
```

### Example 3: Production Validation

```python
# Before deploying a prompt, validate it
result = validator.validate_in_production("customer_support_prompt", run_prompt)

if result['production_ready']:
    print("Safe to deploy!")
    # Deploy to production
else:
    print("Not ready - address issues:")
    for rec in result['recommendations']:
        print(f"  - {rec}")
    # Fix issues and re-validate
```

---

## Troubleshooting

### Issue: API Key Not Found

**Solution:** Set environment variable or create `.env` file
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

### Issue: Import Errors

**Solution:** Ensure you're in the project directory and dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: Dashboard Won't Start

**Solution:** Install Streamlit
```bash
pip install streamlit
streamlit run streamlit_app.py
```

For more troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

---

## Resources

- [API Reference](API_REFERENCE.md) - Complete API documentation
- [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues and solutions
- [Contributing Guide](../CONTRIBUTING.md) - How to contribute
- [Course Roadmap](../COURSE_ROADMAP.md) - Full learning path

---

## Need Help?

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Search [GitHub Issues](https://github.com/ElaMCB/AI-Prompt-Engineering/issues)
- Open a new issue for bugs or questions

**Happy Prompt Engineering!**
