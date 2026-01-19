# API Reference

Complete API documentation for all prompt engineering tools in this repository.

## Table of Contents

- [PromptValidator](#promptvalidator)
- [ProductionValidator](#productionvalidator)
- [Model Providers](#model-providers)
- [A/B Testing Framework](#ab-testing-framework)
- [Progress Tracker](#progress-tracker)

---

## PromptValidator

Enhanced prompt validation system with multi-factor weighted scoring.

### Class: `PromptValidator`

```python
from notebooks.prompt_validator import PromptValidator

validator = PromptValidator()
```

#### Methods

##### `score_prompt(prompt: str) -> Dict`

Scores a prompt using weighted criteria and returns detailed feedback.

**Parameters:**
- `prompt` (str): The prompt text to validate

**Returns:**
- `Dict` with keys:
  - `overall_score` (float): 0-100 score
  - `breakdown` (Dict): Individual component scores
  - `weighted_scores` (Dict): Weighted component scores
  - `feedback` (List[str]): Improvement suggestions
  - `suggestions` (List[str]): Quick-win recommendations
  - `grade` (str): Letter grade (A+ to F)

**Example:**
```python
validator = PromptValidator()
result = validator.score_prompt(
    "You are a copywriter. Write a 200-word blog post about AI."
)
print(f"Score: {result['overall_score']}%")
print(f"Grade: {result['grade']}")
for feedback in result['feedback']:
    print(f"- {feedback}")
```

#### Scoring Criteria (Weighted)

| Criteria | Weight | Description |
|----------|--------|-------------|
| Clarity | 25% | Clear, actionable language |
| Specificity | 25% | Specific vs vague language |
| Context | 20% | Role and context setting |
| Structure | 15% | Well-structured prompt |
| Examples | 15% | Examples and format guidance |

---

## ProductionValidator

Production validation framework for real-world deployment scenarios.

### Class: `ProductionValidator`

```python
from notebooks.production_validator import ProductionValidator, TestCase

validator = ProductionValidator()
```

#### Methods

##### `add_test_case(prompt_id: str, test_case: TestCase)`

Add a test case for validation.

**Parameters:**
- `prompt_id` (str): Unique identifier for the prompt
- `test_case` (TestCase): Test case configuration

**Example:**
```python
test_case = TestCase(
    input_data="Test input",
    expected_output_type="text",
    expected_keywords=["response", "answer"],
    min_length=10,
    max_length=500
)
validator.add_test_case("my_prompt", test_case)
```

##### `test_consistency(prompt_id: str, run_prompt_fn, num_runs: int = 5) -> Dict`

Test prompt consistency across multiple runs.

**Parameters:**
- `prompt_id` (str): Prompt identifier
- `run_prompt_fn` (callable): Function that takes input and returns output
- `num_runs` (int): Number of runs to test (default: 5)

**Returns:**
- `Dict` with consistency metrics

**Example:**
```python
def run_prompt(input_data: str) -> str:
    # Your LLM call here
    return llm_response

result = validator.test_consistency("my_prompt", run_prompt, num_runs=5)
print(f"Consistency Score: {result['consistency_score']}")
```

##### `test_robustness(prompt_id: str, run_prompt_fn) -> Dict`

Test prompt robustness with edge cases.

**Parameters:**
- `prompt_id` (str): Prompt identifier
- `run_prompt_fn` (callable): Function that takes input and returns output

**Returns:**
- `Dict` with robustness metrics

##### `test_performance(prompt_id: str, run_prompt_fn, num_iterations: int = 10) -> Dict`

Test prompt performance (execution time).

**Parameters:**
- `prompt_id` (str): Prompt identifier
- `run_prompt_fn` (callable): Function to test
- `num_iterations` (int): Number of iterations (default: 10)

**Returns:**
- `Dict` with performance metrics

##### `validate_in_production(prompt_id: str, run_prompt_fn, include_edge_cases: bool = True, include_performance: bool = True) -> Dict`

Complete production validation suite.

**Returns:**
- `Dict` with:
  - `production_ready_score` (float): 0-100 score
  - `production_ready` (bool): Ready for deployment
  - `test_results` (Dict): All test results
  - `recommendations` (List[str]): Improvement recommendations

---

## Model Providers

Model-agnostic LLM provider support for OpenAI, Anthropic, and Ollama.

### Class: `UnifiedLLMClient`

```python
from notebooks.model_providers import UnifiedLLMClient, ModelProviderFactory

# Auto-detect provider
client = UnifiedLLMClient()

# Or specify provider
provider = ModelProviderFactory.create_provider("openai", model="gpt-4")
client = UnifiedLLMClient(provider=provider)
```

#### Methods

##### `generate(prompt: str, **kwargs) -> LLMResponse`

Generate a response from the LLM.

**Parameters:**
- `prompt` (str): Input prompt
- `model` (str, optional): Override default model
- `max_tokens` (int, optional): Maximum tokens (default: 1000)
- `temperature` (float, optional): Temperature 0-2 (default: 0.7)

**Returns:**
- `LLMResponse` with:
  - `content` (str): Generated text
  - `model` (str): Model used
  - `provider` (str): Provider name
  - `tokens_used` (int, optional): Tokens consumed
  - `latency_ms` (float, optional): Response time in milliseconds
  - `error` (str, optional): Error message if failed

**Example:**
```python
response = client.generate(
    "Write a haiku about AI",
    model="gpt-4",
    max_tokens=100,
    temperature=0.8
)
if response.error:
    print(f"Error: {response.error}")
else:
    print(response.content)
    print(f"Latency: {response.latency_ms:.0f}ms")
```

##### `get_provider_name() -> str`

Get the current provider name.

##### `get_available_models() -> List[str]`

Get list of available models for current provider.

##### `switch_provider(provider_type: str, **kwargs)`

Switch to a different provider.

**Example:**
```python
client.switch_provider("anthropic", model="claude-3-opus-20240229")
```

### Factory: `ModelProviderFactory`

#### `create_provider(provider_type: str, **kwargs) -> LLMProvider`

Create a provider instance.

**Supported providers:**
- `"openai"`: OpenAI GPT models
- `"anthropic"`: Anthropic Claude models
- `"ollama"`: Local Ollama models

**Example:**
```python
# OpenAI
provider = ModelProviderFactory.create_provider(
    "openai",
    api_key="sk-...",  # Optional if set in env
    model="gpt-4"
)

# Anthropic
provider = ModelProviderFactory.create_provider(
    "anthropic",
    api_key="sk-ant-...",  # Optional if set in env
    model="claude-3-sonnet-20240229"
)

# Ollama (local)
provider = ModelProviderFactory.create_provider(
    "ollama",
    base_url="http://localhost:11434",
    model="llama2"
)
```

---

## A/B Testing Framework

### Class: `PromptABTester`

```python
from notebooks.ab_testing_framework import PromptABTester

tester = PromptABTester()
```

#### Methods

##### `create_test(test_id: str, prompt_a: str, prompt_b: str, metric: str, description: str) -> PromptTest`

Create a new A/B test.

**Example:**
```python
test = tester.create_test(
    test_id="email_subject_test",
    prompt_a="Write a subject line",
    prompt_b="You are an email marketing expert. Write a compelling subject line...",
    metric="click_through_rate",
    description="Testing generic vs specific prompt"
)
```

##### `record_result(test_id: str, prompt_version: str, score: float, response_text: str, notes: str = None)`

Record a test result.

**Example:**
```python
tester.record_result(
    "email_subject_test",
    "A",
    4.2,
    "Weekly Newsletter #47",
    notes="Low engagement"
)
```

##### `analyze_test(test_id: str) -> Dict`

Analyze test results.

**Returns:**
- `Dict` with statistical analysis

##### `generate_report(test_id: str) -> str`

Generate formatted report.

---

## Progress Tracker

### Class: `ProgressTracker`

```python
from notebooks.progress_tracker import ProgressTracker

tracker = ProgressTracker(student_name="Your Name")
```

#### Methods

##### `update_skill(week: str, skill: str, score: float)`

Update a skill score (0-1).

**Example:**
```python
tracker.update_skill("week1_foundations", "prompt_debugging", 0.8)
```

##### `record_assessment(week: str, assessment_type: str, score: float, details: Dict = None)`

Record assessment results.

##### `complete_project(project_name: str, description: str, github_link: str = None)`

Mark a project as completed.

##### `get_overall_progress() -> Dict`

Get overall progress statistics.

##### `generate_skill_report() -> str`

Generate detailed skill progress report.

##### `generate_certificate(week: str) -> str`

Generate completion certificate.

---

## Error Handling

All classes handle errors gracefully:

- **API Errors**: Return error message in response object
- **Missing Keys**: Provide helpful error messages
- **Validation Errors**: Return detailed feedback

---

## Best Practices

1. **Prompt Validation**: Always validate prompts before production
2. **A/B Testing**: Test with multiple runs for statistical significance
3. **Production Validation**: Run full validation suite before deployment
4. **Model Selection**: Choose appropriate model based on task and budget
5. **Error Handling**: Always check for errors in responses

---

## Examples

See the `examples/` directory for complete working examples of all tools.
