import praw
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import time

def sentimentAnalysis(stocks):
    import praw
    import pandas as pd
    import time
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    # Set up PRAW
    reddit = praw.Reddit(
        user_agent="Comment Extraction",
        client_id="k4XwIidw1oXBzfHstp2g7w",
        client_secret="wdZOEnrmJhdefBnSTd2XgYyVRGo4lQ"
    )

    # Set up NLTK sentiment analyzer
    sid = SentimentIntensityAnalyzer()

    # Define subreddits
    subreddits = ['EarningsWhispers', 'WallStreetBets', 'ThetaGang']

    # Create dictionary of stock scores
    stock_scores = {}
    for stock in stocks:
        sentiment_score = 0
        mentions = 0

        for subreddit in subreddits:
            subreddit = reddit.subreddit(subreddit)
            posts = subreddit.hot(limit=1000) # Get 1000 hottest posts from subreddit

            for post in posts:
                if post.created_utc < (time.time() - 604800): # Skip posts older than 1 week
                    break

                try:
                    post_comments = post.comments.list()
                except praw.exceptions.RedditAPIException:
                    break
                
                for comment in post_comments:
                    if isinstance(comment, praw.models.MoreComments):  # Skip MoreComments objects
                        continue

                    comment_text = comment.body.lower()

                    # Check if comment contains the stock symbol
                    if f" {stock.lower()} " in comment_text:
                        # Analyze sentiment of comment
                        comment_sentiment = sid.polarity_scores(comment_text)

                        # Calculate score for stock
                        stock_score = comment_sentiment['pos'] - comment_sentiment['neg']
                        sentiment_score += stock_score
                        mentions += 1

        if mentions != 0:
            stock_scores[stock] = sentiment_score / mentions
        else:
            stock_scores[stock] = 0

    # Create pandas dataframe of top 10 stocks based on score
    df = pd.DataFrame.from_dict(stock_scores, orient='index', columns=['Score']).sort_values('Score', ascending=False).head(10)

    # Create bar chart visualization of top 10 stocks
    ax = df.plot(kind='bar', title='Top 10 Stocks by Sentiment Score', legend=True)
    ax.set_xlabel('Stock Symbol')
    ax.set_ylabel('Sentiment Score')

    return df

import pandas as pd
import yfinance as yf

import pandas as pd
import yfinance as yf

import pandas as pd
import requests

def fundamental_analysis(stocks_list):
    # Define the criteria for selecting the best performing stocks
    min_roe = 0.10  # Minimum return on equity
    max_pe_ratio = 20.0  # Maximum price-to-earnings ratio
    min_operating_cash_flow_growth = 0.05  # Minimum operating cash flow growth rate
    max_debt_equity_ratio = 0.5  # Maximum debt-to-equity ratio
    
    # Create a new dataframe to store the results
    results_df = pd.DataFrame(columns=['Ticker', 'ROE', 'P/E Ratio', 'Operating Cash Flow Growth', 'Debt-to-Equity Ratio'])

    # Loop through each stock in the input list
    for ticker in stocks_list:
        try:
            # Pull the fundamental data for the stock using the Alpha Vantage API
            response = requests.get(f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey=SAXMJP1U7ZN7OR11")
            data = response.json()
            print(data)
            # Extract the relevant fundamental data from the API response
            roe = float(data.get('ReturnOnEquityTTM', 0))
            pe_ratio = float(data.get('PERatioTTM', 0))
            operating_cash_flow_growth = float(data.get('OperatingCashFlowTTM', 0)) / float(data.get('OperatingCashFlowTTM', 1))
            debt_equity_ratio = float(data.get('DebtToEquity', 0))
            
            # Check if the stock meets the performance criteria
            if roe > min_roe and pe_ratio < max_pe_ratio and operating_cash_flow_growth > min_operating_cash_flow_growth and debt_equity_ratio < max_debt_equity_ratio:
                # Add the stock to the results dataframe
                results_df = results_df.append({'Ticker': ticker, 'ROE': roe, 'P/E Ratio': pe_ratio, 'Operating Cash Flow Growth': operating_cash_flow_growth, 'Debt-to-Equity Ratio': debt_equity_ratio}, ignore_index=True)
        except Exception as e:
            # If there is an error, skip the stock and print the error message
            print(f"Error occurred while analyzing {ticker}: {e}")
            pass
    
    # Sort the results dataframe by ROE in descending order
    results_df = results_df.sort_values(by='ROE', ascending=False)
    
    # Return the top performing stocks
    return results_df


def technicalAnalysis():
    print("technical analysis")

stocks = ['AAPL', 'GOOG', 'TSLA', 'AMZN', 'FB']
print(fundamental_analysis(stocks))