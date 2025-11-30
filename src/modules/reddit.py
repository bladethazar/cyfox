"""Reddit post fetcher module"""
import threading
import time
from typing import List, Dict, Optional, Callable
from datetime import datetime
import requests
from src.core.config import Config
from src.core.state import StateManager


class RedditPost:
    """Represents a Reddit post"""

    def __init__(self, title: str, subreddit: str, score: int, url: str,
                 selftext: str = "", author: str = ""):
        # pylint: disable=too-many-arguments,too-many-positional-arguments
        self.title = title
        self.subreddit = subreddit
        self.score = score
        self.url = url
        self.selftext = selftext
        self.author = author
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'title': self.title,
            'subreddit': self.subreddit,
            'score': self.score,
            'url': self.url,
            'selftext': self.selftext,
            'author': self.author,
            'timestamp': self.timestamp.isoformat()
        }
    
    # pylint: disable=too-few-public-methods


class RedditFetcher:
    """Fetches Reddit posts from IT/DevOps subreddits"""

    def __init__(self, config: Config, state_manager: StateManager):
        # pylint: disable=too-many-instance-attributes
        self.config = config
        self.state_manager = state_manager
        self.subreddits = config.get('cyfox.reddit.subreddits', [
            'ProgrammerHumor', 'sysadmin', 'devops', 'linuxmemes'
        ])
        self.fetch_interval = config.get('cyfox.reddit.fetch_interval', 1800)
        self.max_posts = config.get('cyfox.reddit.max_posts', 10)
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.posts: List[RedditPost] = []
        self.current_post_index = 0
        self.callback: Optional[Callable] = None
        self.user_agent = "CyfoxBot/1.0 (by /u/cyfox)"

    def register_callback(self, callback: Callable):
        """Register callback for new posts"""
        self.callback = callback

    def _fetch_posts(self) -> List[RedditPost]:
        """Fetch posts from Reddit"""
        all_posts = []

        for subreddit in self.subreddits:
            try:
                url = f"https://www.reddit.com/r/{subreddit}/hot.json"
                headers = {'User-Agent': self.user_agent}
                response = requests.get(url, headers=headers, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    posts_data = data.get('data', {}).get('children', [])

                    for post_data in posts_data[:5]:  # Top 5 from each subreddit
                        post = post_data.get('data', {})
                        reddit_post = RedditPost(
                            title=post.get('title', ''),
                            subreddit=subreddit,
                            score=post.get('score', 0),
                            url=post.get('url', ''),
                            selftext=post.get('selftext', ''),
                            author=post.get('author', '')
                        )
                        all_posts.append(reddit_post)

                time.sleep(1)  # Rate limiting

            except Exception as e:  # pylint: disable=broad-exception-caught
                print(f"Error fetching from r/{subreddit}: {e}")

        # Sort by score and limit
        all_posts.sort(key=lambda x: x.score, reverse=True)
        return all_posts[:self.max_posts]

    def fetch_new_posts(self) -> List[RedditPost]:
        """Fetch new posts and update internal list"""
        posts = self._fetch_posts()
        if posts:
            self.posts = posts
            self.current_post_index = 0

            if self.callback:
                try:
                    self.callback(posts)
                except Exception as e:  # pylint: disable=broad-exception-caught
                    print(f"Error in Reddit callback: {e}")

        return self.posts

    def get_current_post(self) -> Optional[RedditPost]:
        """Get current post being displayed"""
        if self.posts and 0 <= self.current_post_index < len(self.posts):
            return self.posts[self.current_post_index]
        return None

    def next_post(self):
        """Move to next post"""
        if self.posts:
            self.current_post_index = (self.current_post_index + 1) % len(self.posts)

    def _periodic_fetch(self):
        """Periodic fetching thread"""
        while self.running:
            if self.state_manager.mode.name == 'REDDIT':
                self.fetch_new_posts()

            # Wait for fetch interval
            time.sleep(self.fetch_interval)

    def start(self):
        """Start periodic fetching"""
        if self.running:
            return

        self.running = True
        # Fetch immediately
        self.fetch_new_posts()
        # Start periodic thread
        self.thread = threading.Thread(target=self._periodic_fetch, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop fetching"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)

