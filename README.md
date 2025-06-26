# 📰 Personal RSS News Aggregator

A beautiful, newspaper-style RSS feed aggregator that automatically creates a personalized news digest with images, categorized sections, and hourly updates. Each run generates a randomly named newspaper for a fun, personalized experience!

## ✨ Features

- **🕐 Hourly Updates**: Automatically fetches fresh content every hour via GitHub Actions
- **📰 Authentic Newspaper Design**: Traditional newspaper layout with columns, typography, and styling
- **🎲 Random Names**: Each update gets a cute, randomly generated newspaper name
- **🖼️ Smart Image Extraction**: Automatically finds and displays article images
- **🎯 Categorized Sections**: Breaking news (red highlight), technology, development, security, lifestyle
- **📱 Fully Responsive**: Beautiful on desktop, tablet, and mobile
- **🔗 Smooth Navigation**: Jump between sections with smooth scrolling
- **📊 Statistics Tracking**: Articles, sources, and image counts
- **⚡ Fast & Reliable**: Timeout handling and error recovery

## 🚀 Quick Start (Fork This Repo)

### 1. Fork & Clone
```bash
# Fork this repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/rss_feed.git
cd rss_feed
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Test Locally
```bash
# Generate your first news digest
python feeds.py feeds.yaml temp.db > feeds.md

# Start local server
python3 -m http.server 8000

# Open http://localhost:8000 in your browser
```

### 4. Set Up GitHub Actions (Automated Updates)

#### A. Create GitHub Token
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` permissions
3. Copy the token

#### B. Add Secret to Your Repo
1. In your forked repo: Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `GH_TOKEN`
4. Value: Your personal access token
5. Click "Add secret"

#### C. Enable GitHub Pages
1. Settings → Pages
2. Source: "Deploy from a branch"
3. Branch: `main` / `(root)`
4. Save

🎉 **Done!** Your RSS aggregator will now update every hour and be live at:
`https://YOUR-USERNAME.github.io/rss_feed`

## 🎨 Customization Guide

### Add Your Own RSS Feeds

Edit `feeds.yaml` to add your favorite sources:

```yaml
# Your custom feed
-   url: https://your-favorite-site.com/rss
    freq: 1                    # How often to check (1 = every time)
    icon: fa-newspaper         # Font Awesome icon
    title: Your Site Name
    category: breaking         # breaking, tech, dev, security, lifestyle, general
```

### Popular RSS Feeds to Add

**News Sources:**
```yaml
-   url: https://rss.cnn.com/rss/edition.rss
    icon: fa-globe
    category: breaking

-   url: https://feeds.washingtonpost.com/rss/world
    icon: fa-newspaper  
    category: breaking
```

**Tech Blogs:**
```yaml
-   url: https://feeds.arstechnica.com/arstechnica/index
    icon: fa-microchip
    category: tech

-   url: https://rss.slashdot.org/Slashdot/slashdotMain
    icon: fa-comments
    category: tech
```

### Customize Newspaper Names

Edit the `NEWSPAPER_NAMES` list in `feeds.py`:

```python
NEWSPAPER_NAMES = [
    "📰 Your Custom Herald",
    "🗞️ Daily Tech Digest",
    "📰 The Code Chronicle",
    # Add your own creative names!
]
```

### Modify Update Frequency

Edit `.github/workflows/actions.yml`:

```yaml
schedule:
  - cron: '0 */2 * * *'  # Every 2 hours
  - cron: '0 8,20 * * *' # 8 AM and 8 PM daily
```

### Style Customization

Edit `feeds.css` to change colors, fonts, or layout:

```css
/* Change breaking news color */
.breaking-news .section-header {
    background: #your-color;
}

/* Modify newspaper title font */
.newspaper-title {
    font-family: 'Your-Font', serif;
    font-size: 4em;
}
```

## 🔧 Advanced Configuration

### Environment Variables

Create a `.env` file for custom settings:

```bash
NEWSPAPER_TITLE="My Custom News"
UPDATE_FREQUENCY="hourly"
MAX_ARTICLES_PER_SECTION=20
```

### Custom Categories

Add new categories by editing both `feeds.py` and `feeds.css`:

```python
# In feeds.py - category_info dictionary
'science': ('🔬 Science', 'science-news'),
```

```css
/* In feeds.css */
.science-news .section-header {
    background: #27ae60;
}
```

### Image Settings

Modify image extraction in `feeds.py`:

```python
# Change image size in feeds.css
.story-image {
    width: 100px;    # Make larger
    height: 75px;
}
```

## 📱 Deployment Options

### GitHub Pages (Recommended)
- Automatic with the included GitHub Action
- Free hosting
- Custom domain support

### Netlify
```bash
# Connect your GitHub repo to Netlify
# Deploy command: python feeds.py feeds.yaml temp.db > feeds.md
# Publish directory: ./
```

### Vercel
```bash
# Add vercel.json:
{
  "functions": {
    "feeds.py": {
      "runtime": "python3.9"
    }
  }
}
```

## 🛠️ Troubleshooting

### GitHub Action Not Running?
- Check if `GH_TOKEN` secret is set correctly
- Verify the token has `repo` permissions
- Check Actions tab for error logs

### Feeds Not Loading?
- Some RSS feeds block automated requests
- Check feed URL validity
- Increase timeout in `feeds.py`

### Images Not Showing?
- Some sites block hotlinking
- Images may have authentication requirements
- Check browser console for CORS errors

### Local Development Issues?
```bash
# Common fixes:
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
python3 -m venv venv --clear  # Reset virtual environment
```

## 🎯 Performance Tips

- **Reduce Feed Frequency**: Set `freq: 2` for less important feeds
- **Limit Articles**: Decrease `MAX_ARTICLES_PER_SECTION`
- **Optimize Images**: Consider using a CDN for image proxying
- **Cache Control**: Implement browser caching headers

## 📊 Analytics & Monitoring

Add analytics to `index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin amazing-feature`
5. Open a Pull Request

## 📄 License

MIT License - feel free to use, modify, and distribute!

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/jjasghar/rss_feed/issues)
- **Discussions**: [GitHub Discussions](https://github.com/jjasghar/rss_feed/discussions)
- **Email**: Open an issue instead for community benefit

## 🎉 Showcase

Share your customized RSS aggregator! Tag us or open a discussion to show off your news site.

---

**Built with ❤️ using Python, RSS feeds, and GitHub Actions**

### Recent Updates
- ✅ Added random newspaper names
- ✅ Smart image extraction from RSS feeds  
- ✅ Mobile-responsive newspaper design
- ✅ Comprehensive fork & customization guide
- ✅ Advanced deployment options

