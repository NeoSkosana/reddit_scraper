import os
from dotenv import load_dotenv
import praw
import pandas as pd
from datetime import datetime

# Subreddits and keywords
SUBREDDITS = [
    'healthcare', 'HealthIT', 'medicine', 'medical', 'nursing', 'digitalhealth', 'HealthTech',
    'Construction', 'ConstructionIndustry', 'ConstructionManagement', 'civilengineering', 'architecture', 'skilledtrades',
    'education', 'Teachers', 'EdTech', 'teaching', 'OnlineLearning', 'homeschool',
    'personalfinance', 'Finance', 'FinancialPlanning', 'FinTech', 'investing', 'accounting',
    'ecommerce', 'retail', 'Entrepreneur', 'smallbusiness', 'Shopify', 'AmazonFBA'
]
KEYWORDS = [
    'pain point', 'problem', 'struggle', 'challenge', 'frustration', 'issue', 'difficult', 'hard',
    'need help', 'solution', 'feature request', 'wish', 'improve', 'broken', 'bug', 'limitation', 'missing'
]


def scrape_reddit(auth, subreddits=SUBREDDITS, keywords=KEYWORDS, limit=100):
    reddit = praw.Reddit(**auth)
    results = []
    for subreddit in subreddits:
        print(f"Scraping r/{subreddit}...")
        try:
            for submission in reddit.subreddit(subreddit).hot(limit=limit):
                if any(kw.lower() in submission.title.lower() or kw.lower() in submission.selftext.lower() for kw in keywords):
                    results.append({
                        'subreddit': subreddit,
                        'title': submission.title,
                        'body': submission.selftext,
                        'author': str(submission.author),
                        'created_utc': datetime.fromtimestamp(submission.created_utc),
                        'upvotes': submission.score,
                        'url': submission.url,
                        'num_comments': submission.num_comments
                    })
        except Exception as e:
            print(f"Error scraping r/{subreddit}: {str(e)}")
            continue
    print(f"✓ Scraping complete. {len(results)} posts found.")
    return pd.DataFrame(results)