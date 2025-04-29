import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
from reddit_scraper import scrape_reddit
from data_cleaning import clean_reddit_data
import eda

# Load environment variables
load_dotenv()

auth = {
    'client_id': os.getenv('REDDIT_CLIENT_ID'),
    'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
    'user_agent': os.getenv('REDDIT_USER_AGENT')
}

# 1. Scrape Reddit
df_raw = scrape_reddit(auth)

# 2. Clean Data
df_clean = clean_reddit_data(df_raw)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_csv = f'reddit_scrape_cleaned_{timestamp}.csv'
df_clean.to_csv(output_csv, index=False)
print(f"\n✓ Cleaned data saved to {output_csv}\n")

# 3. EDA
eda.show_summary_statistics(df_clean)
eda.plot_posts_per_subreddit(df_clean)
eda.plot_upvotes_comments_distribution(df_clean)
eda.list_common_keywords(df_clean)