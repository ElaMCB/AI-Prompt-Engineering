"""
Production Validation Framework for Prompt Engineering
Validates prompts for real-world deployment scenarios
"""

import json
import statistics
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib


@dataclass
class TestCase:
    """Single test case for prompt validation"""
    input_data: str
    expected_output_type: str  # 'json', 'text', 'list', etc.
    expected_keywords: Optional[List[str]] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    validation_rules: Optional[Dict] = None


@dataclass
class ValidationResult:
    """Result of a single validation test"""
    test_id: str
    passed: bool
    score: float  # 0-100
    message: str
    actual_output: Optional[str] = None
    error: Optional[str] = None
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class ProductionValidator:
    """
    Production validation framework for prompt engineering.
    Tests consistency, robustness, edge cases, and performance.
    """
    
    def __init__(self):
        self.test_cases: Dict[str, List[TestCase]] = {}
        self.validation_results: List[ValidationResult] = []
        self.edge_cases = self._generate_edge_cases()
    
    def _generate_edge_cases(self) -> List[str]:
        """Generate common edge cases for testing"""
        return [
            "",  # Empty input
            " " * 100,  # Only whitespace
            "a" * 1000,  # Very long single character
            "!@#$%^&*()",  # Special characters only
            "1234567890" * 100,  # Numbers only
            "test\n\n\n\n\n\ntest",  # Many newlines
            "test" + "\t" * 50 + "test",  # Many tabs
            "UPPERCASE ONLY TEXT",
            "lowercase only text",
            "MiXeD cAsE TeXt",
            "test" * 100,  # Repetitive content
        ]
    
    def add_test_case(self, prompt_id: str, test_case: TestCase):
        """Add a test case for a specific prompt"""
        if prompt_id not in self.test_cases:
            self.test_cases[prompt_id] = []
        self.test_cases[prompt_id].append(test_case)
    
    def test_consistency(self, prompt_id: str, run_prompt_fn, num_runs: int = 5) -> Dict:
        """
        Test prompt consistency across multiple runs.
        Measures how similar outputs are when given the same input.
        """
        if prompt_id not in self.test_cases:
            return {"error": f"No test cases found for prompt {prompt_id}"}
        
        test_case = self.test_cases[prompt_id][0]  # Use first test case
        outputs = []
        scores = []
        
        for i in range(num_runs):
            try:
                output = run_prompt_fn(test_case.input_data)
                outputs.append(output)
                
                # Score based on expected criteria
                score = self._score_output(output, test_case)
                scores.append(score)
            except Exception as e:
                return {"error": f"Error running prompt: {str(e)}"}
        
        # Calculate consistency metrics
        consistency_score = self._calculate_consistency(outputs)
        avg_score = statistics.mean(scores)
        std_dev = statistics.stdev(scores) if len(scores) > 1 else 0
        
        result = {
            "test_type": "consistency",
            "prompt_id": prompt_id,
            "num_runs": num_runs,
            "average_score": round(avg_score, 2),
            "std_deviation": round(std_dev, 2),
            "consistency_score": round(consistency_score, 2),
            "passed": consistency_score >= 0.7 and std_dev <= 10,
            "outputs": outputs[:3]  # Sample first 3 outputs
        }
        
        return result
    
    def test_robustness(self, prompt_id: str, run_prompt_fn) -> Dict:
        """
        Test prompt robustness with edge cases.
        Measures how well prompt handles unusual inputs.
        """
        if prompt_id not in self.test_cases:
            return {"error": f"No test cases found for prompt {prompt_id}"}
        
        test_case = self.test_cases[prompt_id][0]
        edge_case_results = []
        passed_count = 0
        
        for edge_case in self.edge_cases:
            try:
                output = run_prompt_fn(edge_case)
                score = self._score_output(output, test_case)
                passed = score >= 50  # Lower threshold for edge cases
                edge_case_results.append({
                    "input_type": self._categorize_edge_case(edge_case),
                    "passed": passed,
                    "score": round(score, 2)
                })
                if passed:
                    passed_count += 1
            except Exception as e:
                edge_case_results.append({
                    "input_type": self._categorize_edge_case(edge_case),
                    "passed": False,
                    "error": str(e)
                })
        
        robustness_score = passed_count / len(self.edge_cases)
        
        result = {
            "test_type": "robustness",
            "prompt_id": prompt_id,
            "robustness_score": round(robustness_score * 100, 2),
            "passed_edge_cases": f"{passed_count}/{len(self.edge_cases)}",
            "passed": robustness_score >= 0.7,
            "edge_case_results": edge_case_results
        }
        
        return result
    
    def test_edge_cases(self, prompt_id: str, run_prompt_fn, custom_cases: Optional[List[str]] = None) -> Dict:
        """Test prompt with specific edge cases"""
        cases = custom_cases or self.edge_cases
        results = []
        
        for case in cases:
            try:
                output = run_prompt_fn(case)
                test_result = ValidationResult(
                    test_id=f"{prompt_id}_edge_{hashlib.md5(case.encode()).hexdigest()[:8]}",
                    passed=True,
                    score=100.0 if output else 0.0,
                    message=f"Edge case handled: {self._categorize_edge_case(case)}",
                    actual_output=output[:100] if output else None  # Truncate for storage
                )
                results.append(test_result)
            except Exception as e:
                test_result = ValidationResult(
                    test_id=f"{prompt_id}_edge_{hashlib.md5(case.encode()).hexdigest()[:8]}",
                    passed=False,
                    score=0.0,
                    message=f"Edge case failed: {self._categorize_edge_case(case)}",
                    error=str(e)
                )
                results.append(test_result)
        
        passed = sum(1 for r in results if r.passed)
        
        return {
            "test_type": "edge_cases",
            "prompt_id": prompt_id,
            "total_cases": len(cases),
            "passed": passed,
            "passed_percentage": round(passed / len(cases) * 100, 2),
            "results": [asdict(r) for r in results]
        }
    
    def test_performance(self, prompt_id: str, run_prompt_fn, num_iterations: int = 10) -> Dict:
        """
        Test prompt performance metrics.
        Measures execution time, token usage (if available), etc.
        """
        import time
        
        if prompt_id not in self.test_cases:
            return {"error": f"No test cases found for prompt {prompt_id}"}
        
        test_case = self.test_cases[prompt_id][0]
        execution_times = []
        
        for _ in range(num_iterations):
            start_time = time.time()
            try:
                output = run_prompt_fn(test_case.input_data)
                execution_time = time.time() - start_time
                execution_times.append(execution_time)
            except Exception as e:
                return {"error": f"Performance test failed: {str(e)}"}
        
        avg_time = statistics.mean(execution_times)
        median_time = statistics.median(execution_times)
        std_dev = statistics.stdev(execution_times) if len(execution_times) > 1 else 0
        
        # Performance score (lower is better, normalized to 0-100)
        # Assuming optimal time is < 2 seconds
        performance_score = max(0, 100 - (avg_time * 10))
        
        return {
            "test_type": "performance",
            "prompt_id": prompt_id,
            "iterations": num_iterations,
            "avg_execution_time": round(avg_time, 3),
            "median_execution_time": round(median_time, 3),
            "std_deviation": round(std_dev, 3),
            "min_time": round(min(execution_times), 3),
            "max_time": round(max(execution_times), 3),
            "performance_score": round(performance_score, 2),
            "passed": avg_time < 5.0  # Pass if average < 5 seconds
        }
    
    def validate_in_production(self, prompt_id: str, run_prompt_fn, 
                              include_edge_cases: bool = True,
                              include_performance: bool = True) -> Dict:
        """
        Complete production validation suite.
        Runs all validation tests and provides overall production readiness score.
        """
        results = {}
        overall_scores = []
        
        # Test consistency
        consistency_result = self.test_consistency(prompt_id, run_prompt_fn)
        if "error" not in consistency_result:
            results["consistency"] = consistency_result
            overall_scores.append(consistency_result.get("consistency_score", 0))
            overall_scores.append(consistency_result.get("average_score", 0))
        
        # Test robustness
        robustness_result = self.test_robustness(prompt_id, run_prompt_fn)
        if "error" not in robustness_result:
            results["robustness"] = robustness_result
            overall_scores.append(robustness_result.get("robustness_score", 0))
        
        # Test edge cases
        if include_edge_cases:
            edge_cases_result = self.test_edge_cases(prompt_id, run_prompt_fn)
            results["edge_cases"] = edge_cases_result
            overall_scores.append(edge_cases_result.get("passed_percentage", 0))
        
        # Test performance
        if include_performance:
            performance_result = self.test_performance(prompt_id, run_prompt_fn)
            if "error" not in performance_result:
                results["performance"] = performance_result
                overall_scores.append(performance_result.get("performance_score", 0))
        
        # Calculate overall production readiness score
        production_ready_score = statistics.mean(overall_scores) if overall_scores else 0
        
        # Determine if production ready
        all_passed = all(
            result.get("passed", False) 
            for result in results.values() 
            if isinstance(result, dict) and "passed" in result
        )
        
        return {
            "prompt_id": prompt_id,
            "production_ready_score": round(production_ready_score, 2),
            "production_ready": all_passed and production_ready_score >= 70,
            "timestamp": datetime.now().isoformat(),
            "test_results": results,
            "recommendations": self._generate_production_recommendations(results, production_ready_score)
        }
    
    def _score_output(self, output: str, test_case: TestCase) -> float:
        """Score output against test case criteria"""
        score = 0.0
        max_score = 100.0
        
        # Check output type
        if test_case.expected_output_type:
            if test_case.expected_output_type == "json" and output.strip().startswith("{"):
                score += 20
            elif test_case.expected_output_type == "list" and ("[" in output or "-" in output):
                score += 20
            elif test_case.expected_output_type == "text":
                score += 20
        
        # Check for expected keywords
        if test_case.expected_keywords:
            found_keywords = sum(1 for keyword in test_case.expected_keywords if keyword.lower() in output.lower())
            keyword_score = (found_keywords / len(test_case.expected_keywords)) * 30
            score += keyword_score
        
        # Check length constraints
        output_length = len(output)
        if test_case.min_length and output_length >= test_case.min_length:
            score += 25
        if test_case.max_length and output_length <= test_case.max_length:
            score += 25
        elif not test_case.min_length and not test_case.max_length:
            score += 25  # No constraint, give full points
        
        return min(score, max_score)
    
    def _calculate_consistency(self, outputs: List[str]) -> float:
        """Calculate consistency score based on output similarity"""
        if len(outputs) < 2:
            return 1.0
        
        # Simple similarity: compare output lengths
        lengths = [len(output) for output in outputs]
        avg_length = statistics.mean(lengths)
        std_dev = statistics.stdev(lengths) if len(lengths) > 1 else 0
        
        # Consistency score: lower std dev = higher consistency
        # Normalize to 0-1 scale (assuming max std dev of 100)
        consistency = max(0, 1 - (std_dev / max(avg_length, 1)))
        
        return consistency
    
    def _categorize_edge_case(self, case: str) -> str:
        """Categorize edge case type"""
        if not case or case.strip() == "":
            return "empty"
        elif case.isspace():
            return "whitespace_only"
        elif len(case) > 500:
            return "very_long"
        elif case.isupper():
            return "uppercase_only"
        elif case.islower():
            return "lowercase_only"
        elif not case.isalnum() and all(not c.isalnum() for c in case):
            return "special_chars_only"
        elif case.isdigit():
            return "numbers_only"
        elif "\n" * 5 in case:
            return "many_newlines"
        else:
            return "other"
    
    def _generate_production_recommendations(self, results: Dict, score: float) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        if score < 70:
            recommendations.append("⚠️ **Production Not Ready**: Score below 70%. Address critical issues before deployment.")
        
        if "consistency" in results:
            consistency = results["consistency"]
            if consistency.get("std_deviation", 0) > 10:
                recommendations.append("📊 **Consistency**: High variance in outputs. Add more specific constraints.")
        
        if "robustness" in results:
            robustness = results["robustness"]
            if robustness.get("robustness_score", 0) < 70:
                recommendations.append("🛡️ **Robustness**: Prompt fails on edge cases. Add error handling and input validation.")
        
        if "performance" in results:
            performance = results["performance"]
            if performance.get("avg_execution_time", 0) > 5:
                recommendations.append("⚡ **Performance**: Slow execution time. Consider optimizing prompt or reducing output length.")
        
        if score >= 70 and all(r.get("passed", False) for r in results.values() if isinstance(r, dict)):
            recommendations.append("✅ **Production Ready**: All tests passed! Safe to deploy with monitoring.")
        
        return recommendations


# Example usage
if __name__ == "__main__":
    # Mock function for testing
    def mock_run_prompt(input_data: str) -> str:
        """Mock prompt function for demonstration"""
        return f"Generated response for: {input_data[:50]}"
    
    validator = ProductionValidator()
    
    # Add test case
    test_case = TestCase(
        input_data="Test input",
        expected_output_type="text",
        expected_keywords=["response"],
        min_length=10,
        max_length=100
    )
    validator.add_test_case("test_prompt", test_case)
    
    # Run production validation
    result = validator.validate_in_production("test_prompt", mock_run_prompt)
    print(json.dumps(result, indent=2))
