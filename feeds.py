import argparse
import yaml
import jsonpickle
import random
import feedparser
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from collections import defaultdict
import html
import socket
import urllib.request
import re

# Set default socket timeout to prevent hanging
socket.setdefaulttimeout(10)

# Cute newspaper names - randomly selected each run
NEWSPAPER_NAMES = [
    "📰 The Daily Digest",
    "🗞️ Morning Brew News",
    "📰 The Tech Tribune",
    "🗞️ Digital Daily",
    "📰 The News Nest",
    "🗞️ Fresh Feed Times",
    "📰 The Info Gazette",
    "🗞️ Byte-Sized Bulletin",
    "📰 The Link Ledger",
    "🗞️ Feed & Fortune",
    "📰 The Daily Scoop",
    "🗞️ News Nugget Herald",
    "📰 The Update Universe",
    "🗞️ Digital Dispatch",
    "📰 The RSS Reporter",
    "🗞️ Feed Forward Times",
    "📰 The Content Chronicle",
    "🗞️ Info Ink Daily",
    "📰 The Byte Beacon",
    "🗞️ News Nest Network"
]

@dataclass
class Feed:
    url: str
    title: str = None
    icon: str = None
    frequency: int = 1
    category: str = "general"

    def shouldUpdate(self):
        f = self.frequency * 2
        return random.randint(1, f) == 1

    def extract_image_from_entry(self, entry):
        """Extract image URL from RSS entry using multiple methods"""
        image_url = None
        
        # Method 1: Check for media:thumbnail
        if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            image_url = entry.media_thumbnail[0]['url']
        
        # Method 2: Check for enclosures (images)
        elif hasattr(entry, 'enclosures') and entry.enclosures:
            for enclosure in entry.enclosures:
                if enclosure.type and enclosure.type.startswith('image/'):
                    image_url = enclosure.href
                    break
        
        # Method 3: Check for media:content
        elif hasattr(entry, 'media_content') and entry.media_content:
            for media in entry.media_content:
                if media.get('type', '').startswith('image/'):
                    image_url = media.get('url')
                    break
        
        # Method 4: Parse description/summary for img tags
        if not image_url:
            content = ''
            if hasattr(entry, 'description'):
                content = entry.description
            elif hasattr(entry, 'summary'):
                content = entry.summary
            
            if content:
                # Look for img tags in the content
                img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content, re.IGNORECASE)
                if img_match:
                    image_url = img_match.group(1)
        
        # Method 5: Check for links with image extensions
        if not image_url and hasattr(entry, 'links'):
            for link in entry.links:
                if link.get('type', '').startswith('image/'):
                    image_url = link.get('href')
                    break
        
        return image_url

    def lastArticle(self):
        try:
            # Set timeout for feedparser
            old_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(5)
            
            f = feedparser.parse(self.url)
            
            # Restore original timeout
            socket.setdefaulttimeout(old_timeout)
            
            if not f.entries:
                return None
            e = f.entries[0]
            t = f.feed.title
            if not t:
                t = self.title or "Unknown Feed"
            if not e.title:
                e.title = self.title or "No Title"
            
            # Get published date if available
            published = getattr(e, 'published', '')
            published_datetime = None
            if hasattr(e, 'published_parsed') and e.published_parsed:
                try:
                    published_datetime = datetime(*e.published_parsed[:6], tzinfo=timezone.utc)
                    published = published_datetime.strftime('%Y-%m-%d %H:%M')
                except:
                    published = ''
            
            # Extract image from entry
            image_url = self.extract_image_from_entry(e)
            
            return Post(e.link, self.icon, t, e.title, self.category, published, image_url, published_datetime)
        except Exception as ex:
            print(f"<!-- Error processing {self.url}: {ex} -->")
            return None


@dataclass
class Post:
    link: str
    icon: str
    site: str
    title: str
    category: str = "general"
    published: str = ""
    image_url: str = None
    published_datetime: datetime = None

    def print(self):
        # Escape HTML in title for safety
        safe_title = html.escape(self.title)
        time_info = f'<span class="time">{self.published}</span>' if self.published else ''
        
        # Add image if available
        image_html = ''
        if self.image_url:
            image_html = f'<img src="{self.image_url}" alt="{safe_title}" class="story-image" loading="lazy" onerror="this.style.display=\'none\'">'
        
        output = f'''<div class="story">
            {image_html}
            <div class="story-content">
                <span class="fa fa-fw {self.icon}"></span>
                <span class="title"><a href="{self.link}" target="_blank">{safe_title}</a></span>
                <span class="feed">{self.site}</span>
                {time_info}
            </div>
        </div>'''
        return output


def filter_recent_posts(posts, max_articles=6):
    """Filter posts to show only those from last 24 hours OR max 6 articles, whichever is fewer"""
    now = datetime.now(timezone.utc)
    twenty_four_hours_ago = now - timedelta(hours=24)
    
    # Filter posts from last 24 hours
    recent_posts = []
    for post in posts:
        if post.published_datetime and post.published_datetime >= twenty_four_hours_ago:
            recent_posts.append(post)
        elif not post.published_datetime:
            # If no datetime available, include it but it will be limited by max_articles
            recent_posts.append(post)
    
    # Sort by published datetime (newest first), handling None values
    recent_posts.sort(key=lambda x: x.published_datetime or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    
    # Return the smaller of: recent posts or max_articles limit
    return recent_posts[:max_articles]


def generate_newspaper_header():
    current_time = datetime.now(timezone.utc).strftime('%A, %B %d, %Y - %H:%M UTC')
    newspaper_name = random.choice(NEWSPAPER_NAMES)
    return f'''<div class="newspaper-header">
    <h1 class="newspaper-title">{newspaper_name}</h1>
    <div class="newspaper-date">{current_time}</div>
    <div class="newspaper-subtitle">Your Personal News Aggregator</div>
</div>

<div class="newspaper-nav">
    <a href="#breaking">Breaking News</a> |
    <a href="#tech">Technology</a> |
    <a href="#dev">Development</a> |
    <a href="#security">Security</a> |
    <a href="#lifestyle">Lifestyle</a>
</div>
'''


def write_page(state):
    # Group posts by category
    categories = defaultdict(list)
    for p in state['posts'][::-1]:  # Reverse to show newest first
        categories[p.category].append(p)
    
    # Print newspaper header
    print(generate_newspaper_header())
    
    # Category display order and titles
    category_info = {
        'breaking': ('🚨 Breaking News', 'breaking-news'),
        'tech': ('💻 Technology', 'tech-news'),
        'dev': ('🛠️ Development', 'dev-news'),
        'security': ('🔒 Security', 'security-news'),
        'lifestyle': ('🎮 Lifestyle & Culture', 'lifestyle-news'),
        'general': ('📰 General News', 'general-news')
    }
    
    total_displayed = 0
    for category, (title, css_class) in category_info.items():
        if category in categories and categories[category]:
            # Filter to recent posts (last 24h) or max 6, whichever is fewer
            filtered_posts = filter_recent_posts(categories[category], max_articles=6)
            
            if filtered_posts:  # Only show section if it has posts
                print(f'<div class="news-section {css_class}" id="{category}">')
                print(f'<h2 class="section-header">{title}</h2>')
                print('<div class="stories-container">')
                
                for post in filtered_posts:
                    print(post.print())
                    total_displayed += 1
                
                print('</div>')
                print('</div>')
    
    # Stats footer
    total_posts = len(state['posts'])
    total_sources = len(set(p.site for p in state['posts']))
    images_count = len([p for p in state['posts'] if p.image_url])
    
    # Calculate how many posts are from last 24 hours
    now = datetime.now(timezone.utc)
    twenty_four_hours_ago = now - timedelta(hours=24)
    recent_count = len([p for p in state['posts'] if p.published_datetime and p.published_datetime >= twenty_four_hours_ago])
    
    print(f'''
<div class="newspaper-footer">
    <div class="stats">
        📊 Displayed: {total_displayed} | 📅 Last 24h: {recent_count} | 📡 Total Sources: {total_sources} | 📸 With Images: {images_count} |
        🔄 Last Updated: {datetime.now(timezone.utc).strftime('%H:%M UTC')}
    </div>
    <div class="footer-note">
        Showing recent articles (max 6 per section) • Updated every hour • Built with ❤️ using RSS feeds
    </div>
</div>''')


def save_to_json_pickle(filename, data):
    with open(filename, 'w') as file:
        json_data = jsonpickle.encode(data)
        file.write(json_data)

def load_json_pickle(filename):
    try:
        with open(filename, 'r') as file:
            json_data = file.read()
            data = jsonpickle.decode(json_data)
            return data
    except:
        return {'last': {}, 'posts': []}


def parse_yaml_file(filename):
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
        return data

def main():
    parser = argparse.ArgumentParser(description="Update RSS feeds")
    parser.add_argument("feeds", help="Path to feeds file")
    parser.add_argument("db", help="Path to db file")
    args = parser.parse_args()

    feedlist = parse_yaml_file(args.feeds)
    state = load_json_pickle(args.db)

    feeds = []

    for f in feedlist:
        feeds.append(Feed(
            f.get('url', None), 
            f.get('title', None), 
            f.get('icon', None), 
            f.get('freq', 1),
            f.get('category', 'general')
        ))

    new_posts_count = 0
    processed_feeds = 0
    
    print(f"<!-- Processing {len(feeds)} RSS feeds at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} -->")
    
    for f in feeds:
        if f.shouldUpdate():
            processed_feeds += 1
            print(f"<!-- Processing: {f.title or f.url} -->")
            p = f.lastArticle()

            if not p:
                continue

            # Check if this is a new post (comparing URL and title)
            post_key = f"{p.link}_{p.title}"
            existing_keys = [f"{existing.link}_{existing.title}" for existing in state['posts']]
            
            if post_key not in existing_keys:
                state['posts'].append(p)
                new_posts_count += 1

    # Keep last 500 posts instead of 200 for better archive
    if len(state['posts']) > 500:
        state['posts'] = state['posts'][-500:]

    print(f"<!-- Generated {new_posts_count} new posts out of {processed_feeds} feeds processed -->")
    save_to_json_pickle(args.db, state)
    write_page(state)


if __name__ == "__main__":
    main()
