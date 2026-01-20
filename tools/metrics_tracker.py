"""
Success Metrics Tracker
Tracks website traffic, repository stars/forks, and course completion rates
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import requests
from datetime import date


@dataclass
class TrafficMetrics:
    """Website traffic metrics"""
    date: str
    page_views: int
    unique_visitors: int
    sessions: int
    bounce_rate: float
    avg_session_duration: float
    top_pages: List[Dict[str, int]]
    traffic_sources: Dict[str, int]


@dataclass
class RepositoryMetrics:
    """GitHub repository metrics"""
    date: str
    stars: int
    forks: int
    watchers: int
    open_issues: int
    closed_issues: int
    pull_requests: int
    contributors: int
    commits_last_week: int


@dataclass
class CourseMetrics:
    """Course completion metrics"""
    date: str
    total_students: int
    active_students: int
    completions: int
    completion_rate: float
    progress_by_level: Dict[str, float]
    average_progress: float
    students_by_tool_usage: Dict[str, int]


class GoogleAnalyticsTracker:
    """Track website traffic using Google Analytics API"""
    
    def __init__(self, ga_property_id: Optional[str] = None, 
                 ga_api_key: Optional[str] = None):
        self.ga_property_id = ga_property_id or os.getenv("GOOGLE_ANALYTICS_PROPERTY_ID")
        self.ga_api_key = ga_api_key or os.getenv("GOOGLE_ANALYTICS_API_KEY")
        self.metrics_dir = Path(__file__).parent.parent / "content" / "metrics"
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
    
    def fetch_traffic_metrics(self, start_date: str = None, 
                              end_date: str = None) -> TrafficMetrics:
        """Fetch traffic metrics from Google Analytics"""
        if start_date is None:
            start_date = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
        if end_date is None:
            end_date = date.today().strftime("%Y-%m-%d")
        
        # Mock implementation - replace with actual GA API calls
        # For production, use: google-analytics-data python library
        metrics = TrafficMetrics(
            date=end_date,
            page_views=self._fetch_page_views(start_date, end_date),
            unique_visitors=self._fetch_unique_visitors(start_date, end_date),
            sessions=self._fetch_sessions(start_date, end_date),
            bounce_rate=self._fetch_bounce_rate(start_date, end_date),
            avg_session_duration=self._fetch_avg_duration(start_date, end_date),
            top_pages=self._fetch_top_pages(start_date, end_date),
            traffic_sources=self._fetch_traffic_sources(start_date, end_date)
        )
        
        self._save_metrics(metrics, "traffic")
        return metrics
    
    def _fetch_page_views(self, start_date: str, end_date: str) -> int:
        """Fetch total page views"""
        # Mock - replace with actual GA API
        if self.ga_api_key:
            # Actual implementation would use GA4 Data API
            pass
        return 0  # Placeholder
    
    def _fetch_unique_visitors(self, start_date: str, end_date: str) -> int:
        """Fetch unique visitors"""
        # Mock - replace with actual GA API
        return 0  # Placeholder
    
    def _fetch_sessions(self, start_date: str, end_date: str) -> int:
        """Fetch total sessions"""
        # Mock - replace with actual GA API
        return 0  # Placeholder
    
    def _fetch_bounce_rate(self, start_date: str, end_date: str) -> float:
        """Fetch bounce rate"""
        # Mock - replace with actual GA API
        return 0.0  # Placeholder
    
    def _fetch_avg_duration(self, start_date: str, end_date: str) -> float:
        """Fetch average session duration"""
        # Mock - replace with actual GA API
        return 0.0  # Placeholder
    
    def _fetch_top_pages(self, start_date: str, end_date: str) -> List[Dict[str, int]]:
        """Fetch top pages"""
        # Mock - replace with actual GA API
        return []
    
    def _fetch_traffic_sources(self, start_date: str, end_date: str) -> Dict[str, int]:
        """Fetch traffic sources"""
        # Mock - replace with actual GA API
        return {}
    
    def _save_metrics(self, metrics: TrafficMetrics, metric_type: str):
        """Save metrics to file"""
        filename = f"{metrics.date}_{metric_type}.json"
        filepath = self.metrics_dir / filename
        
        with open(filepath, "w") as f:
            json.dump(asdict(metrics), f, indent=2)


class GitHubMetricsTracker:
    """Track repository stars, forks, and activity"""
    
    def __init__(self, repo_owner: str = "ElaMCB", 
                 repo_name: str = "AI-Prompt-Engineering",
                 github_token: Optional[str] = None):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.metrics_dir = Path(__file__).parent.parent / "content" / "metrics"
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        self.api_base = "https://api.github.com"
    
    def fetch_repository_metrics(self) -> RepositoryMetrics:
        """Fetch current repository metrics from GitHub API"""
        repo_data = self._fetch_repo_data()
        stats_data = self._fetch_repo_stats()
        
        metrics = RepositoryMetrics(
            date=date.today().strftime("%Y-%m-%d"),
            stars=repo_data.get("stargazers_count", 0),
            forks=repo_data.get("forks_count", 0),
            watchers=repo_data.get("watchers_count", 0),
            open_issues=repo_data.get("open_issues_count", 0),
            closed_issues=stats_data.get("closed_issues", 0),
            pull_requests=stats_data.get("pull_requests", 0),
            contributors=stats_data.get("contributors", 0),
            commits_last_week=stats_data.get("commits_last_week", 0)
        )
        
        self._save_metrics(metrics, "repository")
        return metrics
    
    def _fetch_repo_data(self) -> Dict:
        """Fetch basic repository data"""
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}"
        headers = {}
        
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching repo data: {e}")
            return {}
    
    def _fetch_repo_stats(self) -> Dict:
        """Fetch repository statistics"""
        stats = {
            "closed_issues": 0,
            "pull_requests": 0,
            "contributors": 0,
            "commits_last_week": 0
        }
        
        if not self.github_token:
            return stats
        
        headers = {"Authorization": f"token {self.github_token}"}
        
        # Fetch closed issues
        try:
            url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/issues"
            params = {"state": "closed", "per_page": 1}
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                # Get total from Link header or fetch all
                stats["closed_issues"] = len(response.json())
        except:
            pass
        
        # Fetch pull requests
        try:
            url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/pulls"
            params = {"state": "all", "per_page": 100}
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                stats["pull_requests"] = len(response.json())
        except:
            pass
        
        # Fetch contributors count
        try:
            url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/contributors"
            response = requests.get(url, headers=headers, params={"per_page": 100}, timeout=10)
            if response.status_code == 200:
                stats["contributors"] = len(response.json())
        except:
            pass
        
        # Fetch commits from last week
        try:
            url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/commits"
            since = (date.today() - timedelta(days=7)).isoformat()
            params = {"since": since, "per_page": 100}
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                stats["commits_last_week"] = len(response.json())
        except:
            pass
        
        return stats
    
    def _save_metrics(self, metrics: RepositoryMetrics, metric_type: str):
        """Save metrics to file"""
        filename = f"{metrics.date}_{metric_type}.json"
        filepath = self.metrics_dir / filename
        
        with open(filepath, "w") as f:
            json.dump(asdict(metrics), f, indent=2)


class CourseCompletionTracker:
    """Track course completion rates and student progress"""
    
    def __init__(self):
        self.metrics_dir = Path(__file__).parent.parent / "content" / "metrics"
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        self.progress_file = Path(__file__).parent.parent / "content" / "student_progress.json"
        
        # Initialize progress file if it doesn't exist
        if not self.progress_file.exists():
            self.progress_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.progress_file, "w") as f:
                json.dump({}, f)
    
    def calculate_completion_metrics(self) -> CourseMetrics:
        """Calculate course completion metrics from student progress data"""
        progress_data = self._load_progress_data()
        
        total_students = len(progress_data)
        active_students = sum(1 for p in progress_data.values() if p.get("last_activity_date"))
        
        completions = sum(1 for p in progress_data.values() 
                         if p.get("completion_rate", 0) >= 100)
        
        completion_rate = (completions / total_students * 100) if total_students > 0 else 0
        
        # Calculate progress by level
        progress_by_level = {
            "foundations": self._calculate_level_progress(progress_data, "foundations"),
            "engineering": self._calculate_level_progress(progress_data, "engineering"),
            "professional": self._calculate_level_progress(progress_data, "professional")
        }
        
        # Calculate average progress
        total_progress = sum(p.get("completion_rate", 0) for p in progress_data.values())
        average_progress = total_progress / total_students if total_students > 0 else 0
        
        # Track tool usage
        tool_usage = {}
        for progress in progress_data.values():
            tools = progress.get("tools_used", [])
            for tool in tools:
                tool_usage[tool] = tool_usage.get(tool, 0) + 1
        
        metrics = CourseMetrics(
            date=date.today().strftime("%Y-%m-%d"),
            total_students=total_students,
            active_students=active_students,
            completions=completions,
            completion_rate=completion_rate,
            progress_by_level=progress_by_level,
            average_progress=average_progress,
            students_by_tool_usage=tool_usage
        )
        
        self._save_metrics(metrics, "course")
        return metrics
    
    def _load_progress_data(self) -> Dict:
        """Load student progress data"""
        try:
            with open(self.progress_file, "r") as f:
                return json.load(f)
        except:
            return {}
    
    def _calculate_level_progress(self, progress_data: Dict, level: str) -> float:
        """Calculate average progress for a specific level"""
        level_completions = []
        for progress in progress_data.values():
            level_progress = progress.get("levels", {}).get(level, {}).get("completion_rate", 0)
            level_completions.append(level_progress)
        
        if not level_completions:
            return 0.0
        
        return sum(level_completions) / len(level_completions)
    
    def update_student_progress(self, student_id: str, progress_data: Dict):
        """Update individual student progress"""
        all_progress = self._load_progress_data()
        all_progress[student_id] = {
            **all_progress.get(student_id, {}),
            **progress_data,
            "last_updated": date.today().isoformat()
        }
        
        with open(self.progress_file, "w") as f:
            json.dump(all_progress, f, indent=2)
    
    def _save_metrics(self, metrics: CourseMetrics, metric_type: str):
        """Save metrics to file"""
        filename = f"{metrics.date}_{metric_type}.json"
        filepath = self.metrics_dir / filename
        
        with open(filepath, "w") as f:
            json.dump(asdict(metrics), f, indent=2)


class MetricsDashboard:
    """Aggregated metrics dashboard"""
    
    def __init__(self):
        self.traffic_tracker = GoogleAnalyticsTracker()
        self.repo_tracker = GitHubMetricsTracker()
        self.course_tracker = CourseCompletionTracker()
        self.metrics_dir = Path(__file__).parent.parent / "content" / "metrics"
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_daily_report(self) -> Dict:
        """Generate daily metrics report"""
        report = {
            "date": date.today().isoformat(),
            "timestamp": datetime.now().isoformat(),
            "traffic": asdict(self.traffic_tracker.fetch_traffic_metrics()),
            "repository": asdict(self.repo_tracker.fetch_repository_metrics()),
            "course": asdict(self.course_tracker.calculate_completion_metrics())
        }
        
        # Save daily report
        report_file = self.metrics_dir / f"daily_report_{date.today().strftime('%Y-%m-%d')}.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def generate_weekly_summary(self) -> Dict:
        """Generate weekly metrics summary"""
        # Load last 7 days of reports
        week_start = date.today() - timedelta(days=7)
        
        reports = []
        for i in range(7):
            report_date = (week_start + timedelta(days=i)).strftime("%Y-%m-%d")
            report_file = self.metrics_dir / f"daily_report_{report_date}.json"
            
            if report_file.exists():
                with open(report_file, "r") as f:
                    reports.append(json.load(f))
        
        if not reports:
            return {"error": "No reports available"}
        
        # Calculate weekly summary
        summary = {
            "week_start": week_start.isoformat(),
            "week_end": date.today().isoformat(),
            "traffic": {
                "total_page_views": sum(r["traffic"]["page_views"] for r in reports),
                "total_unique_visitors": max(r["traffic"]["unique_visitors"] for r in reports),
                "avg_bounce_rate": sum(r["traffic"]["bounce_rate"] for r in reports) / len(reports)
            },
            "repository": {
                "stars_gained": reports[-1]["repository"]["stars"] - reports[0]["repository"]["stars"],
                "forks_gained": reports[-1]["repository"]["forks"] - reports[0]["repository"]["forks"],
                "current_stars": reports[-1]["repository"]["stars"],
                "current_forks": reports[-1]["repository"]["forks"]
            },
            "course": {
                "new_completions": reports[-1]["course"]["completions"] - reports[0]["course"]["completions"],
                "completion_rate_change": reports[-1]["course"]["completion_rate"] - reports[0]["course"]["completion_rate"],
                "current_total_students": reports[-1]["course"]["total_students"]
            }
        }
        
        # Save weekly summary
        summary_file = self.metrics_dir / f"weekly_summary_{date.today().strftime('%Y-%m-%d')}.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)
        
        return summary


def main():
    """Example usage"""
    print("Success Metrics Tracker")
    print("=" * 50)
    
    dashboard = MetricsDashboard()
    
    print("\n1. Fetching traffic metrics...")
    traffic = dashboard.traffic_tracker.fetch_traffic_metrics()
    print(f"   Page Views: {traffic.page_views}")
    print(f"   Unique Visitors: {traffic.unique_visitors}")
    
    print("\n2. Fetching repository metrics...")
    repo = dashboard.repo_tracker.fetch_repository_metrics()
    print(f"   Stars: {repo.stars}")
    print(f"   Forks: {repo.forks}")
    print(f"   Contributors: {repo.contributors}")
    
    print("\n3. Calculating course completion metrics...")
    course = dashboard.course_tracker.calculate_completion_metrics()
    print(f"   Total Students: {course.total_students}")
    print(f"   Completion Rate: {course.completion_rate:.1f}%")
    print(f"   Average Progress: {course.average_progress:.1f}%")
    
    print("\n4. Generating daily report...")
    report = dashboard.generate_daily_report()
    print(f"   Report saved: daily_report_{date.today().strftime('%Y-%m-%d')}.json")
    
    print("\n" + "=" * 50)
    print("Metrics tracking complete!")
    print(f"Check content/metrics/ directory for saved metrics.")


if __name__ == "__main__":
    main()