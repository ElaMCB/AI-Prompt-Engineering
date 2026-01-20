"""
Run Growth Strategies Automation
Scheduled task runner for content marketing engine
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

sys.path.append(str(Path(__file__).parent))

from content_marketing_engine import (
    BlogPostGenerator,
    CaseStudyCollector,
    ToolReleaseManager,
    WebinarScheduler
)

def load_config():
    """Load growth strategies configuration"""
    config_path = Path(__file__).parent / "growth_strategies_config.json"
    with open(config_path, "r") as f:
        return json.load(f)

def run_weekly_tasks():
    """Run weekly content marketing tasks"""
    config = load_config()
    
    # Initialize components
    blog_gen = BlogPostGenerator()
    case_study_collector = CaseStudyCollector()
    release_manager = ToolReleaseManager()
    webinar_scheduler = WebinarScheduler()
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "blog_posts_scheduled": [],
        "case_studies_created": [],
        "releases_scheduled": [],
        "webinars_scheduled": []
    }
    
    # Schedule next blog post
    if config["content_marketing"]["blog_schedule"]["frequency"] == "weekly":
        next_week = (datetime.now() + timedelta(weeks=1)).strftime("%Y-%m-%d")
        topics = config["content_marketing"]["blog_schedule"]["topics"]
        
        # Get next topic (simple rotation)
        topic_index = len([f for f in Path(__file__).parent.parent.glob("content/blog/*.json")]) % len(topics)
        topic = topics[topic_index]
        
        blog_post = blog_gen.generate_blog_post(
            topic=topic,
            target_audience=config["content_marketing"]["blog_schedule"]["target_audiences"][topic_index % len(config["content_marketing"]["blog_schedule"]["target_audiences"])],
            publish_date=next_week
        )
        results["blog_posts_scheduled"].append(blog_post.title)
    
    # Check for new case studies to process
    # (This would typically be triggered by user submissions)
    
    # Schedule next tool release if due
    # (This would check release schedule)
    
    # Schedule next webinar if due
    if config["content_marketing"]["webinar_schedule"]["frequency"] == "bi-weekly":
        next_webinar_date = (datetime.now() + timedelta(weeks=2)).strftime("%Y-%m-%d")
        topics = config["content_marketing"]["webinar_schedule"]["topics"]
        
        # Get next webinar topic
        webinar_index = len([f for f in Path(__file__).parent.parent.glob("content/webinars/*.json")]) % len(topics)
        topic = topics[webinar_index]
        
        webinar = webinar_scheduler.schedule_webinar(
            topic=topic,
            date=next_webinar_date,
            duration=config["content_marketing"]["webinar_schedule"]["duration_minutes"]
        )
        results["webinars_scheduled"].append(webinar["topic"])
    
    return results

if __name__ == "__main__":
    print("Running Growth Strategies Automation...")
    results = run_weekly_tasks()
    
    print("\nResults:")
    print(json.dumps(results, indent=2))
    
    # Save results log
    log_path = Path(__file__).parent.parent / "content" / "automation_log.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    if log_path.exists():
        with open(log_path, "r") as f:
            logs = json.load(f)
    else:
        logs = []
    
    logs.append(results)
    
    with open(log_path, "w") as f:
        json.dump(logs[-50:], f, indent=2)  # Keep last 50 runs
    
    print(f"\nLog saved to {log_path}")