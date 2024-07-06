import argparse
from twikit import Client
from dotenv import load_dotenv
from datetime import datetime
import os
import csv

class TwitterScraper:
    def __init__(self, locale='en-US'):
        # Load environment variables from .env file
        load_dotenv()

        # Retrieve credentials from environment variables
        self.username = os.getenv('USERNAME')
        self.email = os.getenv('EMAIL')
        self.password = os.getenv('PASSWORD')

        # Initialize the Twitter client with a specified locale
        self.client = Client(locale)

    def save_cookies(self):
        """Save session cookies to a file for future use."""
        self.client.save_cookies('cookies.json')

    def load_cookies(self):
        """Load session cookies from a file to maintain session."""
        self.client.load_cookies('cookies.json')

    def login(self):
        """Login to the Twitter client using provided credentials and save cookies."""
        self.client.login(auth_info_1=self.username, auth_info_2=self.email, password=self.password)
        self.save_cookies()

    def clean_text(self, text):
        """Remove blank lines and replace commas with spaces in the given text.
        
        Parameters:
        text (str): The text to be cleaned.
        
        Returns:
        str: The cleaned text.
        """
        result = text.replace(',', ' ')
        result = result.replace('\n', ' ')
        return result

    def get_tweets(self, identifier, page_limit: int, by_user_id: bool = True):
        """Fetch tweets from a user by either user ID or screen name, and save to a CSV file.
        
        Parameters:
        identifier (int/str): The user ID (if by_user_id is True) or screen name (if by_user_id is False) of the user.
        page_limit (int): The number of additional pages of tweets to fetch.
        by_user_id (bool): Flag indicating whether the identifier is a user ID (True) or screen name (False). Default is True.
        """
        start_time = datetime.now()
        
        if by_user_id:
            tweets = self.client.get_user_tweets(identifier, 'Tweets')
        else:
            user = self.client.get_user_by_screen_name(identifier)
            tweets = self.client.get_user_tweets(user.id, 'Tweets')
        
        # Generate a timestamp for the CSV filename
        timestamp = datetime.now().strftime('%Y_%m_%d_%H%M%S')
        filename = f'tweets_{identifier}_{timestamp}.csv'
        
        initial_page = 1

        # Open a CSV file for writing
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(['created_at', 'text', 'view_count'])

            print(f"Scraping page.. {initial_page}")
            
            # Write the tweets
            for tweet in tweets:
                writer.writerow([tweet.created_at, self.clean_text(tweet.text), tweet.view_count])

            for i in range(page_limit):
                more_tweets = tweets.next()
                if not more_tweets:
                    break
                for tweet in more_tweets:
                    writer.writerow([tweet.created_at, self.clean_text(tweet.text), tweet.view_count])
                tweets = more_tweets
                
                print(f"Scraping page.. {i + 2}")
                
        end_time = datetime.now()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")

if __name__ == '__main__':
    scraper = TwitterScraper()

    parser = argparse.ArgumentParser(description='Twitter scraper using twikit.')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Sub-parser for login command
    parser_login = subparsers.add_parser('login', help='Login and save cookies')

    # Sub-parser for scraping command
    parser_scrape = subparsers.add_parser('scrape', help='Scrape tweets using saved cookies')
    parser_scrape.add_argument('identifier', type=str, help='User ID or screen name of the Twitter account')
    parser_scrape.add_argument('page_limit', type=int, help='Number of additional pages of tweets to fetch')
    parser_scrape.add_argument('--by_user_id', action='store_true', help='Specify if the identifier is a user ID')

    args = parser.parse_args()

    if args.command == 'login':
        scraper.login()
    elif args.command == 'scrape':
        scraper.load_cookies()
        scraper.get_tweets(args.identifier, args.page_limit, args.by_user_id)
