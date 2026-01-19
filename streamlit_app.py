"""
Streamlit Dashboard for Prompt Engineering
Interactive tool for testing and validating prompts
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add notebooks directory to path
sys.path.append(str(Path(__file__).parent / "notebooks"))

from prompt_validator import PromptValidator
from production_validator import ProductionValidator, TestCase
from model_providers import UnifiedLLMClient, ModelProviderFactory
from ab_testing_framework import PromptABTester
from progress_tracker import ProgressTracker

# Page configuration
st.set_page_config(
    page_title="AI Prompt Engineering Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
    }
    .warning-message {
        color: #ffc107;
        font-weight: bold;
    }
    .error-message {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'validator' not in st.session_state:
        st.session_state.validator = PromptValidator()
    if 'prod_validator' not in st.session_state:
        st.session_state.prod_validator = ProductionValidator()
    if 'ab_tester' not in st.session_state:
        st.session_state.ab_tester = PromptABTester()
    if 'llm_client' not in st.session_state:
        try:
            st.session_state.llm_client = UnifiedLLMClient()
        except:
            st.session_state.llm_client = None
    if 'progress_tracker' not in st.session_state:
        st.session_state.progress_tracker = ProgressTracker()


def main():
    """Main application"""
    initialize_session_state()
    
    # Sidebar navigation
    st.sidebar.title("🤖 Prompt Engineering Tools")
    page = st.sidebar.radio(
        "Navigate",
        ["🏠 Home", "✅ Prompt Validator", "🚀 Production Validator", 
         "⚖️ A/B Testing", "📊 Progress Tracker", "🤖 LLM Playground", "📚 About"]
    )
    
    if page == "🏠 Home":
        show_home()
    elif page == "✅ Prompt Validator":
        show_prompt_validator()
    elif page == "🚀 Production Validator":
        show_production_validator()
    elif page == "⚖️ A/B Testing":
        show_ab_testing()
    elif page == "📊 Progress Tracker":
        show_progress_tracker()
    elif page == "🤖 LLM Playground":
        show_llm_playground()
    elif page == "📚 About":
        show_about()


def show_home():
    """Home page"""
    st.markdown('<div class="main-header">AI Prompt Engineering Dashboard</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>✅ Prompt Validator</h3>
            <p>Score prompts 0-100% using best practices. Get instant feedback on clarity, specificity, context, structure, and examples.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🚀 Production Validator</h3>
            <p>Test prompts for production deployment. Validate consistency, robustness, edge cases, and performance.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>⚖️ A/B Testing</h3>
            <p>Compare different prompt versions scientifically. Optimize prompts with data-driven insights.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.header("Quick Start")
    st.markdown("""
    1. **Validate a Prompt**: Use the Prompt Validator to score your prompts and get improvement suggestions
    2. **Test with LLM**: Use the LLM Playground to test prompts with real models
    3. **Production Ready**: Use Production Validator before deploying prompts
    4. **Compare Versions**: Use A/B Testing to optimize your best prompts
    5. **Track Progress**: Monitor your learning progress with the Progress Tracker
    """)


def show_prompt_validator():
    """Prompt Validator page"""
    st.header("✅ Prompt Validator")
    st.markdown("Score your prompts and get instant feedback on quality and best practices.")
    
    prompt = st.text_area(
        "Enter your prompt:",
        height=200,
        placeholder="You are a conversion copywriter specializing in SaaS email marketing. Write a 200-word welcome email..."
    )
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        validate_button = st.button("🔍 Validate Prompt", type="primary", use_container_width=True)
    
    if validate_button and prompt:
        with st.spinner("Analyzing prompt..."):
            result = st.session_state.validator.score_prompt(prompt)
        
        # Overall score
        score = result['overall_score']
        st.metric("Overall Score", f"{score:.1f}%", delta=f"{score - 70:.1f}% vs threshold")
        
        # Grade badge
        grade = result['grade']
        if score >= 90:
            st.success(f"**Grade: {grade}** 🎉")
        elif score >= 70:
            st.info(f"**Grade: {grade}** 👍")
        else:
            st.warning(f"**Grade: {grade}** ⚠️")
        
        # Score breakdown
        st.subheader("📊 Score Breakdown")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        breakdown = result['breakdown']
        with col1:
            st.metric("Clarity", f"{breakdown['clarity_score']*100:.0f}%")
        with col2:
            st.metric("Specificity", f"{breakdown['specificity_score']*100:.0f}%")
        with col3:
            st.metric("Context", f"{breakdown['context_score']*100:.0f}%")
        with col4:
            st.metric("Structure", f"{breakdown.get('structure_score', 0)*100:.0f}%")
        with col5:
            st.metric("Examples", f"{breakdown['examples_score']*100:.0f}%")
        
        # Feedback
        st.subheader("💡 Feedback & Suggestions")
        feedback = result.get('feedback', [])
        for item in feedback:
            st.markdown(f"- {item}")
        
        suggestions = result.get('suggestions', [])
        if suggestions:
            st.subheader("🚀 Quick Wins")
            for suggestion in suggestions:
                st.markdown(f"- {suggestion}")
    
    elif validate_button:
        st.warning("Please enter a prompt to validate.")


def show_production_validator():
    """Production Validator page"""
    st.header("🚀 Production Validator")
    st.markdown("Test prompts for production deployment with consistency, robustness, and performance tests.")
    
    prompt_id = st.text_input("Prompt ID:", value="my_prompt")
    prompt_text = st.text_area("Prompt Text:", height=150)
    
    st.subheader("Test Configuration")
    col1, col2, col3 = st.columns(3)
    with col1:
        include_edge = st.checkbox("Include Edge Cases", value=True)
    with col2:
        include_perf = st.checkbox("Include Performance", value=True)
    with col3:
        num_runs = st.number_input("Consistency Runs", min_value=3, max_value=10, value=5)
    
    if st.button("🚀 Run Production Validation", type="primary"):
        if not prompt_text:
            st.error("Please enter prompt text.")
        elif not st.session_state.llm_client:
            st.error("LLM client not configured. Please check your API keys.")
        else:
            with st.spinner("Running production validation tests..."):
                # Add test case
                test_case = TestCase(
                    input_data="Test input",
                    expected_output_type="text",
                    expected_keywords=["response"],
                    min_length=10
                )
                st.session_state.prod_validator.add_test_case(prompt_id, test_case)
                
                # Create prompt function
                def run_prompt(input_data: str) -> str:
                    full_prompt = f"{prompt_text}\n\nInput: {input_data}"
                    response = st.session_state.llm_client.generate(full_prompt)
                    return response.content if not response.error else ""
                
                # Run validation
                result = st.session_state.prod_validator.validate_in_production(
                    prompt_id, run_prompt,
                    include_edge_cases=include_edge,
                    include_performance=include_perf
                )
            
            # Display results
            score = result['production_ready_score']
            st.metric("Production Readiness Score", f"{score:.1f}%")
            
            if result['production_ready']:
                st.success("✅ **Production Ready!** All tests passed.")
            else:
                st.warning("⚠️ **Not Production Ready** - Address issues before deployment.")
            
            # Test results
            st.subheader("📊 Test Results")
            for test_name, test_result in result['test_results'].items():
                with st.expander(f"{test_name.replace('_', ' ').title()}", expanded=True):
                    st.json(test_result)
            
            # Recommendations
            if result['recommendations']:
                st.subheader("💡 Recommendations")
                for rec in result['recommendations']:
                    st.markdown(f"- {rec}")


def show_ab_testing():
    """A/B Testing page"""
    st.header("⚖️ A/B Testing Framework")
    st.markdown("Compare different prompt versions and track performance scientifically.")
    
    tab1, tab2, tab3 = st.tabs(["Create Test", "View Results", "Analyze Test"])
    
    with tab1:
        st.subheader("Create New A/B Test")
        test_id = st.text_input("Test ID:", value="prompt_comparison_1")
        prompt_a = st.text_area("Prompt A (Version 1):", height=150)
        prompt_b = st.text_area("Prompt B (Version 2):", height=150)
        metric = st.selectbox("Metric to measure:", ["quality", "relevance", "completeness", "clarity"])
        description = st.text_input("Description:")
        
        if st.button("Create Test", type="primary"):
            test = st.session_state.ab_tester.create_test(
                test_id, prompt_a, prompt_b, metric, description
            )
            st.success(f"Test '{test_id}' created successfully!")
    
    with tab2:
        st.subheader("Record Test Results")
        tests = st.session_state.ab_tester.list_tests()
        if tests:
            test_options = {t['test_id']: f"{t['test_id']} - {t['description']}" for t in tests}
            selected_test = st.selectbox("Select Test:", list(test_options.keys()), format_func=lambda x: test_options[x])
            
            col1, col2 = st.columns(2)
            with col1:
                version = st.radio("Version:", ["A", "B"])
                score = st.slider("Score (1-10):", 1, 10, 5)
            with col2:
                response_text = st.text_area("Response Text:", height=100)
                notes = st.text_input("Notes (optional):")
            
            if st.button("Record Result", type="primary"):
                st.session_state.ab_tester.record_result(
                    selected_test, version, float(score), response_text, notes
                )
                st.success("Result recorded!")
        else:
            st.info("No tests created yet. Create one in the 'Create Test' tab.")
    
    with tab3:
        st.subheader("Analyze Test Results")
        tests = st.session_state.ab_tester.list_tests()
        if tests:
            test_options = {t['test_id']: f"{t['test_id']} - {t['description']}" for t in tests}
            selected_test = st.selectbox("Select Test to Analyze:", list(test_options.keys()), format_func=lambda x: test_options[x], key="analyze_test")
            
            if st.button("Analyze", type="primary"):
                analysis = st.session_state.ab_tester.analyze_test(selected_test)
                if "error" not in analysis:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Prompt A Avg Score", f"{analysis['prompt_a']['mean_score']:.2f}/10")
                    with col2:
                        st.metric("Prompt B Avg Score", f"{analysis['prompt_b']['mean_score']:.2f}/10")
                    
                    st.info(f"🏆 **Winner: {analysis['winner']}** (Confidence: {analysis['confidence']})")
                    
                    report = st.session_state.ab_tester.generate_report(selected_test)
                    st.text(report)
                else:
                    st.warning(analysis['error'])
        else:
            st.info("No tests available for analysis.")


def show_progress_tracker():
    """Progress Tracker page"""
    st.header("📊 Progress Tracker")
    st.markdown("Track your learning progress and skill mastery.")
    
    student_name = st.text_input("Your Name:", value=st.session_state.progress_tracker.student_name)
    st.session_state.progress_tracker.student_name = student_name
    
    progress = st.session_state.progress_tracker.get_overall_progress()
    
    st.metric("Overall Progress", f"{progress['overall_progress']:.1f}%")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Skills Mastered", progress['skills_mastered'])
    with col2:
        st.metric("Assessments", progress['assessments_completed'])
    with col3:
        st.metric("Projects", progress['projects_completed'])
    
    st.info(f"💡 **Next Milestone:** {progress['next_milestone']}")
    
    if st.button("Generate Skill Report"):
        report = st.session_state.progress_tracker.generate_skill_report()
        st.text(report)


def show_llm_playground():
    """LLM Playground page"""
    st.header("🤖 LLM Playground")
    st.markdown("Test prompts with real LLM providers (OpenAI, Anthropic, Ollama).")
    
    # Provider selection
    if st.session_state.llm_client:
        current_provider = st.session_state.llm_client.get_provider_name()
        st.info(f"Current Provider: **{current_provider.upper()}**")
    else:
        st.warning("⚠️ No LLM provider configured. Please set API keys in your environment.")
        provider_type = st.selectbox("Select Provider:", ["openai", "anthropic", "ollama"])
        if st.button("Initialize Provider"):
            try:
                st.session_state.llm_client = ModelProviderFactory.create_provider(provider_type)
                st.success(f"Provider '{provider_type}' initialized!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error: {e}")
        return
    
    # Model selection
    models = st.session_state.llm_client.get_available_models()
    selected_model = st.selectbox("Select Model:", models)
    
    # Prompt input
    prompt = st.text_area("Enter Prompt:", height=200)
    
    # Parameters
    col1, col2, col3 = st.columns(3)
    with col1:
        max_tokens = st.number_input("Max Tokens:", min_value=1, max_value=4000, value=1000)
    with col2:
        temperature = st.slider("Temperature:", 0.0, 2.0, 0.7, 0.1)
    with col3:
        st.write("")  # Spacer
    
    if st.button("🚀 Generate Response", type="primary"):
        if prompt:
            with st.spinner("Generating response..."):
                response = st.session_state.llm_client.generate(
                    prompt,
                    model=selected_model,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
            
            if response.error:
                st.error(f"❌ Error: {response.error}")
            else:
                st.subheader("Response:")
                st.write(response.content)
                
                # Stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Latency", f"{response.latency_ms:.0f}ms" if response.latency_ms else "N/A")
                with col2:
                    st.metric("Tokens", response.tokens_used or "N/A")
                with col3:
                    st.metric("Provider", response.provider.upper())
        else:
            st.warning("Please enter a prompt.")


def show_about():
    """About page"""
    st.header("📚 About This Dashboard")
    st.markdown("""
    ### AI Prompt Engineering Dashboard
    
    This interactive dashboard provides professional-grade tools for prompt engineering:
    
    - **Prompt Validator**: Score prompts 0-100% with detailed feedback
    - **Production Validator**: Test prompts for production deployment
    - **A/B Testing**: Compare prompt versions scientifically
    - **Progress Tracker**: Monitor learning progress
    - **LLM Playground**: Test prompts with real LLM providers
    
    ### Features
    
    - ✅ Multi-factor weighted scoring system
    - ✅ Production-ready validation framework
    - ✅ Model-agnostic LLM support (OpenAI, Anthropic, Ollama)
    - ✅ Statistical A/B testing
    - ✅ Real-time feedback and suggestions
    
    ### Getting Started
    
    1. Set up your API keys in environment variables:
       - `OPENAI_API_KEY` for OpenAI
       - `ANTHROPIC_API_KEY` for Anthropic
       - Or run Ollama locally for free
    
    2. Start using the tools from the sidebar navigation
    
    ### License
    
    MIT License - See LICENSE file for details
    """)


if __name__ == "__main__":
    main()
