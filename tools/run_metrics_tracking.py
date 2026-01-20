"""
Automated Metrics Tracking Runner
Scheduled task to track success metrics daily
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent))

from metrics_tracker import MetricsDashboard


def run_daily_metrics():
    """Run daily metrics tracking"""
    print(f"Running daily metrics tracking - {datetime.now().isoformat()}")
    print("=" * 60)
    
    dashboard = MetricsDashboard()
    
    # Generate daily report
    report = dashboard.generate_daily_report()
    
    print("\nDaily Report Generated:")
    print(f"- Date: {report['date']}")
    print(f"- Traffic: {report['traffic']['page_views']} page views")
    print(f"- Repository: {report['repository']['stars']} stars, {report['repository']['forks']} forks")
    print(f"- Course: {report['course']['completion_rate']:.1f}% completion rate")
    
    # Generate weekly summary if it's the end of the week
    if datetime.now().weekday() == 6:  # Sunday
        print("\nGenerating weekly summary...")
        summary = dashboard.generate_weekly_summary()
        print(f"- Stars gained this week: {summary['repository']['stars_gained']}")
        print(f"- New completions: {summary['course']['new_completions']}")
    
    print("\n" + "=" * 60)
    print("Metrics tracking complete!")


if __name__ == "__main__":
    run_daily_metrics()