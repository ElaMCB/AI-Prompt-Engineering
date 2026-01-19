"""
Prompt Engineering Validation System
Provides immediate feedback on prompt quality
"""

import re
from typing import Dict, List, Tuple

class PromptValidator:
    def __init__(self):
        """Enhanced Prompt Validator with multi-factor weighted scoring"""
        # CLEAR framework indicators
        self.clear_framework = {
            'context': ['you are', 'act as', 'imagine you', 'role', 'you are a', 'you are an'],
            'length': ['words', 'sentences', 'paragraphs', 'pages', 'characters', 'lines'],
            'examples': ['example', 'like this', 'format', 'style', 'similar to', 'for instance'],
            'audience': ['audience', 'target', 'for people who', 'readers who', 'users who', 'customers'],
            'requirements': ['must include', 'requirements', 'should contain', 'needs to', 'must have']
        }
        
        # Weighted criteria for multi-factor scoring (must sum to 1.0)
        self.criteria_weights = {
            'clarity': 0.25,      # Clear, actionable language
            'specificity': 0.25,  # Specific vs vague language
            'context': 0.20,      # Role and context setting
            'structure': 0.15,    # Well-structured prompt
            'examples': 0.15      # Examples and format guidance
        }
    
    def score_prompt(self, prompt: str) -> Dict:
        """Score a prompt based on multi-factor weighted system and CLEAR framework"""
        prompt_lower = prompt.lower()
        
        # Calculate individual component scores
        clarity_score = self._check_clarity(prompt)
        specificity_score = self._check_specificity(prompt)
        context_score = self._check_context(prompt_lower)
        structure_score = self._check_structure(prompt, prompt_lower)
        examples_score = self._check_examples(prompt_lower)
        
        # Weighted overall score calculation
        weighted_scores = {
            'clarity': clarity_score * self.criteria_weights['clarity'],
            'specificity': specificity_score * self.criteria_weights['specificity'],
            'context': context_score * self.criteria_weights['context'],
            'structure': structure_score * self.criteria_weights['structure'],
            'examples': examples_score * self.criteria_weights['examples']
        }
        
        overall_score = sum(weighted_scores.values())
        
        # Detailed breakdown for feedback
        breakdown = {
            'clarity_score': round(clarity_score, 2),
            'specificity_score': round(specificity_score, 2),
            'context_score': round(context_score, 2),
            'structure_score': round(structure_score, 2),
            'examples_score': round(examples_score, 2),
            'audience_score': self._check_audience(prompt_lower),
            'requirements_score': self._check_requirements(prompt_lower),
            'length_score': self._check_length_specification(prompt_lower)
        }
        
        return {
            'overall_score': round(overall_score * 100, 2),  # Convert to 0-100 scale
            'breakdown': breakdown,
            'weighted_scores': {k: round(v * 100, 2) for k, v in weighted_scores.items()},
            'feedback': self._generate_feedback(breakdown, prompt),
            'suggestions': self._generate_suggestions(breakdown, prompt),
            'grade': self._get_grade(overall_score)
        }
    
    def _check_structure(self, prompt: str, prompt_lower: str) -> float:
        """Check if prompt is well-structured (has clear sections, logical flow)"""
        score = 0.0
        
        # Check for clear sections (paragraphs or line breaks)
        paragraphs = [p.strip() for p in prompt.split('\n\n') if p.strip()]
        if len(paragraphs) > 1:
            score += 0.3  # Multiple paragraphs suggest structure
        
        # Check for numbered lists or bullet points (structure indicators)
        if re.search(r'\d+\.|[-*•]', prompt):
            score += 0.2
        
        # Check for question words (structured thinking)
        question_words = ['what', 'how', 'why', 'when', 'where', 'who']
        if any(qw in prompt_lower for qw in question_words):
            score += 0.2
        
        # Check for action verbs (clear directives)
        action_verbs = ['write', 'create', 'generate', 'analyze', 'explain', 'describe', 'list']
        action_count = sum(1 for verb in action_verbs if verb in prompt_lower)
        score += min(action_count * 0.1, 0.3)
        
        return min(score, 1.0)
    
    def _check_context(self, prompt: str) -> float:
        """Check if prompt sets proper context/role"""
        context_indicators = self.clear_framework['context']
        found = sum(1 for indicator in context_indicators if indicator in prompt)
        return min(found * 0.5, 1.0)
    
    def _check_length_specification(self, prompt: str) -> float:
        """Check if prompt specifies output length"""
        length_indicators = self.clear_framework['length']
        found = sum(1 for indicator in length_indicators if indicator in prompt)
        return min(found * 0.5, 1.0)
    
    def _check_examples(self, prompt: str) -> float:
        """Check if prompt provides examples or format guidance"""
        example_indicators = self.clear_framework['examples']
        found = sum(1 for indicator in example_indicators if indicator in prompt)
        return min(found * 0.3, 1.0)
    
    def _check_audience(self, prompt: str) -> float:
        """Check if prompt defines target audience"""
        audience_indicators = self.clear_framework['audience']
        found = sum(1 for indicator in audience_indicators if indicator in prompt)
        return min(found * 0.4, 1.0)
    
    def _check_requirements(self, prompt: str) -> float:
        """Check if prompt lists specific requirements"""
        req_indicators = self.clear_framework['requirements']
        found = sum(1 for indicator in req_indicators if indicator in prompt)
        return min(found * 0.3, 1.0)
    
    def _check_specificity(self, prompt: str) -> float:
        """Check for specific vs vague language"""
        vague_words = ['good', 'nice', 'great', 'awesome', 'help', 'some', 'thing']
        specific_words = ['exactly', 'specifically', 'must', 'should', 'include', 'format']
        
        vague_count = sum(1 for word in vague_words if word in prompt.lower())
        specific_count = sum(1 for word in specific_words if word in prompt.lower())
        
        if len(prompt.split()) == 0:
            return 0
        
        specificity_ratio = specific_count / max(len(prompt.split()) * 0.1, 1)
        vague_penalty = vague_count / max(len(prompt.split()) * 0.1, 1)
        
        return max(0, min(1, specificity_ratio - vague_penalty))
    
    def _check_clarity(self, prompt: str) -> float:
        """Check for clear, actionable language"""
        sentences = prompt.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        # Optimal sentence length is 15-25 words
        if 15 <= avg_sentence_length <= 25:
            return 1.0
        elif 10 <= avg_sentence_length <= 30:
            return 0.8
        else:
            return 0.5
    
    def _generate_feedback(self, scores: Dict, prompt: str) -> List[str]:
        """Generate specific feedback for improvement"""
        feedback = []
        
        if scores.get('clarity_score', 0) < 0.7:
            feedback.append("💡 **Clarity**: Use shorter, clearer sentences (optimal: 15-25 words per sentence)")
        
        if scores.get('specificity_score', 0) < 0.7:
            feedback.append("🎯 **Specificity**: Replace vague words ('good', 'nice') with concrete details")
        
        if scores.get('context_score', 0) < 0.5:
            feedback.append("🎭 **Context**: Add a clear role: 'You are a [specific role]...'")
        
        if scores.get('structure_score', 0) < 0.6:
            feedback.append("📐 **Structure**: Organize your prompt with clear sections or numbered points")
        
        if scores.get('examples_score', 0) < 0.5:
            feedback.append("📝 **Examples**: Include examples or format guidance: 'Like this: [example]'")
        
        if scores.get('audience_score', 0) < 0.5:
            feedback.append("👥 **Audience**: Define your audience: 'for [specific group] who [specific situation]'")
        
        if scores.get('length_score', 0) < 0.5:
            feedback.append("📏 **Length**: Specify output length: '200 words', '3 paragraphs', etc.")
        
        if scores.get('requirements_score', 0) < 0.5:
            feedback.append("✅ **Requirements**: List specific requirements: 'Must include...', 'Should contain...'")
        
        if not feedback:
            feedback.append("🎉 **Excellent!** Your prompt follows best practices across all criteria.")
        
        return feedback
    
    def _generate_suggestions(self, scores: Dict, prompt: str) -> List[str]:
        """Generate actionable improvement suggestions"""
        suggestions = []
        
        # Priority-based suggestions
        if scores.get('overall_score', 0) < 70:
            suggestions.append("🚨 **Priority**: Focus on clarity and specificity - these are the most important factors")
        
        if scores.get('context_score', 0) < 0.5:
            suggestions.append("💡 **Quick win**: Start with 'You are a [role]' to immediately improve context")
        
        if scores.get('specificity_score', 0) < 0.6:
            suggestions.append("💡 **Quick win**: Add specific numbers, names, or concrete details")
        
        if all(s < 0.7 for s in [scores.get('clarity_score', 0), scores.get('structure_score', 0)]):
            suggestions.append("📋 **Structure tip**: Break long sentences into shorter ones, use bullet points")
        
        return suggestions
    
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade (score is 0-1, needs to be converted for 0-100 scale)"""
        # Score is 0-1, convert to percentage for grading
        percentage = score * 100
        
        if percentage >= 90:
            return "A+ (Excellent)"
        elif percentage >= 80:
            return "A (Very Good)"
        elif percentage >= 70:
            return "B (Good)"
        elif percentage >= 60:
            return "C (Needs Improvement)"
        elif percentage >= 50:
            return "D (Poor - Needs Major Revision)"
        else:
            return "F (Failed - Complete Revision Required)"

# Example usage and testing
if __name__ == "__main__":
    validator = PromptValidator()
    
    # Test with a bad prompt
    bad_prompt = "Write me something good about marketing"
    result = validator.score_prompt(bad_prompt)
    print(f"Bad Prompt Score: {result['overall_score']} - {result['grade']}")
    print("Feedback:", result['feedback'])
    
    # Test with a good prompt
    good_prompt = """You are a conversion copywriter specializing in SaaS email marketing. 
    Write a 200-word welcome email for new trial users of a project management tool. 
    Target audience: small business owners who just signed up but haven't logged in yet. 
    Must include: specific next steps, one key benefit, and a clear call-to-action. 
    Tone should be friendly but professional."""
    
    result = validator.score_prompt(good_prompt)
    print(f"\nGood Prompt Score: {result['overall_score']} - {result['grade']}")
    print("Feedback:", result['feedback'])