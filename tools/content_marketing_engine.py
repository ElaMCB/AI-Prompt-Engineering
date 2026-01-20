"""
Content Marketing Engine
Automates blog post generation, case study collection, and content scheduling
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from notebooks.model_providers import UnifiedLLMClient, ModelProviderFactory
except ImportError:
    print("Warning: Model providers not available. Install required dependencies.")


@dataclass
class BlogPost:
    """Blog post structure"""
    title: str
    topic: str
    target_audience: str
    publish_date: str
    status: str  # draft, scheduled, published
    content: Optional[str] = None
    tags: List[str] = None
    seo_keywords: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.seo_keywords is None:
            self.seo_keywords = []


@dataclass
class CaseStudy:
    """Case study structure"""
    student_name: str
    role: str
    outcome: str
    before_situation: str
    after_situation: str
    key_prompts_used: List[str]
    results_metrics: Dict[str, str]
    publish_date: str
    status: str  # draft, scheduled, published
    content: Optional[str] = None


class BlogPostGenerator:
    """Generate weekly blog posts about prompt engineering"""
    
    def __init__(self, llm_client: Optional[UnifiedLLMClient] = None):
        self.llm_client = llm_client
        self.blog_dir = Path(__file__).parent.parent / "content" / "blog"
        self.blog_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_blog_post(self, topic: str, target_audience: str, 
                          publish_date: Optional[str] = None) -> BlogPost:
        """Generate a blog post on a given topic"""
        if publish_date is None:
            publish_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        
        if self.llm_client:
            title = self._generate_title(topic, target_audience)
            content = self._generate_content(title, topic, target_audience)
        else:
            title = f"Mastering {topic}: A Guide for {target_audience}"
            content = None
        
        blog_post = BlogPost(
            title=title,
            topic=topic,
            target_audience=target_audience,
            publish_date=publish_date,
            status="draft",
            content=content,
            tags=self._generate_tags(topic),
            seo_keywords=self._generate_seo_keywords(topic)
        )
        
        self._save_blog_post(blog_post)
        return blog_post
    
    def _generate_title(self, topic: str, audience: str) -> str:
        """Generate SEO-optimized blog post title"""
        prompt = f"""Generate a compelling, SEO-friendly blog post title about "{topic}" 
for the target audience: {audience}.

Requirements:
- 50-60 characters
- Include power words
- Focus on value/outcome
- Include "prompt engineering" naturally

Return only the title, no quotes."""
        
        if self.llm_client:
            return self.llm_client.generate(prompt, max_tokens=100).strip()
        return f"How to Master {topic} with Prompt Engineering"
    
    def _generate_content(self, title: str, topic: str, audience: str) -> str:
        """Generate full blog post content"""
        prompt = f"""Write a comprehensive 1500-2000 word blog post with the title: "{title}"

Topic: {topic}
Target Audience: {audience}

Structure:
1. Engaging hook (problem-focused)
2. Clear explanation of the concept
3. Step-by-step guide with examples
4. Real-world use cases
5. Common mistakes to avoid
6. Actionable takeaways

Tone: Educational, practical, and accessible
Include specific prompt examples throughout."""
        
        if self.llm_client:
            return self.llm_client.generate(prompt, max_tokens=2000)
        return f"# {title}\n\n[Content for {topic} - Generated content would appear here]"
    
    def _generate_tags(self, topic: str) -> List[str]:
        """Generate relevant tags"""
        base_tags = ["prompt engineering", "AI", "LLM", "productivity"]
        topic_tags = topic.lower().split()
        return base_tags + topic_tags[:3]
    
    def _generate_seo_keywords(self, topic: str) -> List[str]:
        """Generate SEO keywords"""
        return [
            f"{topic} prompt engineering",
            "how to prompt engineering",
            "AI prompt techniques",
            f"prompt engineering for {topic.lower()}"
        ]
    
    def _save_blog_post(self, blog_post: BlogPost):
        """Save blog post to file"""
        filename = blog_post.title.lower().replace(" ", "_").replace(":", "")
        filename = "".join(c for c in filename if c.isalnum() or c in ("_", "-"))
        filepath = self.blog_dir / f"{blog_post.publish_date}_{filename}.json"
        
        with open(filepath, "w") as f:
            json.dump(asdict(blog_post), f, indent=2)
    
    def schedule_weekly_posts(self, weeks: int = 4, topics: List[str] = None):
        """Schedule weekly blog posts for the next N weeks"""
        if topics is None:
            topics = [
                "Context Injection Techniques",
                "Chain-of-Thought Prompting",
                "Few-Shot Learning",
                "Prompt Optimization Strategies",
                "Production Prompt Testing",
                "Multi-Modal Prompts",
                "Prompt Versioning",
                "A/B Testing Prompts"
            ]
        
        scheduled = []
        for i in range(weeks):
            publish_date = (datetime.now() + timedelta(weeks=i+1)).strftime("%Y-%m-%d")
            topic = topics[i % len(topics)]
            
            blog_post = self.generate_blog_post(
                topic=topic,
                target_audience="developers and content creators",
                publish_date=publish_date
            )
            scheduled.append(blog_post)
        
        return scheduled


class CaseStudyCollector:
    """Collect and format student success case studies"""
    
    def __init__(self):
        self.case_studies_dir = Path(__file__).parent.parent / "content" / "case_studies"
        self.case_studies_dir.mkdir(parents=True, exist_ok=True)
    
    def create_case_study(self, student_name: str, role: str, 
                         before_situation: str, after_situation: str,
                         key_prompts: List[str], results: Dict[str, str],
                         publish_date: Optional[str] = None) -> CaseStudy:
        """Create a new case study"""
        if publish_date is None:
            publish_date = datetime.now().strftime("%Y-%m-%d")
        
        case_study = CaseStudy(
            student_name=student_name,
            role=role,
            outcome=self._extract_outcome(after_situation),
            before_situation=before_situation,
            after_situation=after_situation,
            key_prompts_used=key_prompts,
            results_metrics=results,
            publish_date=publish_date,
            status="draft"
        )
        
        self._save_case_study(case_study)
        return case_study
    
    def _extract_outcome(self, after_situation: str) -> str:
        """Extract the key outcome from after situation"""
        # Simple extraction - could be enhanced with LLM
        return after_situation[:200] + "..."
    
    def generate_case_study_content(self, case_study: CaseStudy, 
                                   llm_client: Optional[UnifiedLLMClient] = None) -> str:
        """Generate formatted case study content"""
        prompt = f"""Create a compelling case study based on this information:

Student: {case_study.student_name}
Role: {case_study.role}

Before: {case_study.before_situation}

After: {case_study.after_situation}

Results: {case_study.results_metrics}

Key Prompts Used:
{chr(10).join(f"- {p}" for p in case_study.key_prompts_used)}

Structure:
1. Headline with specific outcome
2. Challenge section
3. Solution approach
4. Key prompts that made the difference
5. Results and metrics
6. Takeaways for readers

Tone: Inspiring, specific, and actionable"""
        
        if llm_client:
            content = llm_client.generate(prompt, max_tokens=1500)
        else:
            content = f"# Case Study: {case_study.student_name}\n\n[Case study content would be generated here]"
        
        case_study.content = content
        self._save_case_study(case_study)
        return content
    
    def _save_case_study(self, case_study: CaseStudy):
        """Save case study to file"""
        filename = case_study.student_name.lower().replace(" ", "_")
        filename = "".join(c for c in filename if c.isalnum() or c == "_")
        filepath = self.case_studies_dir / f"{case_study.publish_date}_{filename}.json"
        
        with open(filepath, "w") as f:
            json.dump(asdict(case_study), f, indent=2)


class ToolReleaseManager:
    """Manage free tool releases to drive traffic"""
    
    def __init__(self):
        self.releases_dir = Path(__file__).parent.parent / "content" / "releases"
        self.releases_dir.mkdir(parents=True, exist_ok=True)
    
    def create_release_announcement(self, tool_name: str, description: str,
                                   features: List[str], use_cases: List[str],
                                   release_date: Optional[str] = None):
        """Create a tool release announcement"""
        if release_date is None:
            release_date = datetime.now().strftime("%Y-%m-%d")
        
        release = {
            "tool_name": tool_name,
            "description": description,
            "features": features,
            "use_cases": use_cases,
            "release_date": release_date,
            "github_url": f"https://github.com/ElaMCB/AI-Prompt-Engineering/tree/main/tools/{tool_name.lower().replace(' ', '_')}",
            "status": "scheduled"
        }
        
        filepath = self.releases_dir / f"{release_date}_{tool_name.lower().replace(' ', '_')}.json"
        with open(filepath, "w") as f:
            json.dump(release, f, indent=2)
        
        return release
    
    def generate_release_content(self, release: dict, 
                                llm_client: Optional[UnifiedLLMClient] = None) -> str:
        """Generate release announcement content"""
        prompt = f"""Create an engaging tool release announcement:

Tool: {release['tool_name']}
Description: {release['description']}

Features:
{chr(10).join(f"- {f}" for f in release['features'])}

Use Cases:
{chr(10).join(f"- {uc}" for uc in release['use_cases'])}

Structure:
1. Hook: Problem this tool solves
2. What it is and why it matters
3. Key features walkthrough
4. Real use cases
5. How to get started (free)
6. Call to action

Tone: Exciting, helpful, and community-focused"""
        
        if llm_client:
            return llm_client.generate(prompt, max_tokens=1200)
        return f"# Introducing {release['tool_name']}\n\n[Release announcement would be generated here]"


class WebinarScheduler:
    """Schedule and manage webinar series"""
    
    def __init__(self):
        self.webinars_dir = Path(__file__).parent.parent / "content" / "webinars"
        self.webinars_dir.mkdir(parents=True, exist_ok=True)
    
    def schedule_webinar(self, topic: str, date: str, duration: int = 60,
                        description: str = None, registration_url: str = None):
        """Schedule a new webinar"""
        webinar = {
            "topic": topic,
            "date": date,
            "duration_minutes": duration,
            "description": description or f"Deep dive into {topic}",
            "registration_url": registration_url,
            "status": "scheduled",
            "created_at": datetime.now().isoformat()
        }
        
        # Clean filename
        safe_topic = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in topic.lower())
        safe_topic = safe_topic.replace(" ", "_")
        filepath = self.webinars_dir / f"{date}_{safe_topic}.json"
        
        # Ensure directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, "w") as f:
            json.dump(webinar, f, indent=2)
        
        return webinar
    
    def schedule_series(self, topics: List[str], start_date: str, 
                       frequency_weeks: int = 2):
        """Schedule a webinar series"""
        start = datetime.strptime(start_date, "%Y-%m-%d")
        scheduled = []
        
        for i, topic in enumerate(topics):
            webinar_date = (start + timedelta(weeks=i * frequency_weeks)).strftime("%Y-%m-%d")
            webinar = self.schedule_webinar(
                topic=topic,
                date=webinar_date,
                description=f"Deep dive into {topic}",
                duration=60
            )
            scheduled.append(webinar)
        
        return scheduled


def main():
    """Example usage"""
    print("Content Marketing Engine - Growth Strategy Tools")
    print("=" * 50)
    
    # Initialize generators
    blog_gen = BlogPostGenerator()
    case_study_collector = CaseStudyCollector()
    release_manager = ToolReleaseManager()
    webinar_scheduler = WebinarScheduler()
    
    # Schedule weekly blog posts
    print("\n1. Scheduling weekly blog posts...")
    blog_posts = blog_gen.schedule_weekly_posts(weeks=4)
    print(f"   Scheduled {len(blog_posts)} blog posts")
    
    # Create example case study
    print("\n2. Creating case study template...")
    case_study = case_study_collector.create_case_study(
        student_name="Sarah M.",
        role="Marketing Manager",
        before_situation="Spent 4 hours writing one blog post, generic results",
        after_situation="Generates 10 high-quality articles in 30 minutes, got promoted",
        key_prompts=["CLEAR framework for content", "Audience-specific prompts"],
        results={"time_saved": "90%", "content_quality": "Increased significantly"}
    )
    print(f"   Created case study: {case_study.student_name}")
    
    # Schedule tool releases
    print("\n3. Scheduling tool releases...")
    release = release_manager.create_release_announcement(
        tool_name="Prompt Validator v2.0",
        description="Advanced prompt scoring with multi-factor analysis",
        features=["Weighted scoring", "Production readiness", "A/B testing"],
        use_cases=["Content creation", "Code generation", "Business automation"]
    )
    print(f"   Scheduled release: {release['tool_name']}")
    
    # Schedule webinar series
    print("\n4. Scheduling webinar series...")
    webinars = webinar_scheduler.schedule_series(
        topics=[
            "Advanced Prompt Engineering Techniques",
            "Production Prompt Deployment",
            "A/B Testing Prompts at Scale",
            "Building AI Agents with Prompts"
        ],
        start_date=(datetime.now() + timedelta(weeks=1)).strftime("%Y-%m-%d"),
        frequency_weeks=2
    )
    print(f"   Scheduled {len(webinars)} webinars")
    
    print("\n" + "=" * 50)
    print("Content Marketing Engine initialized successfully!")
    print(f"Check content/ directory for generated files.")


if __name__ == "__main__":
    main()