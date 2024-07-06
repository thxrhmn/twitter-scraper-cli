
# Twitter Scraper CLI

A command-line interface (CLI) tool to scrape tweets from a specified Twitter user using the `twikit` library. This tool supports logging in to Twitter and saving session cookies for persistent scraping sessions.

## Features

- Login to Twitter and save session cookies.
- Scrape tweets by user ID or screen name.
- Save scraped tweets to a CSV file.

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/thxrhmn/twitter-scraper-cli.git
    cd twitter-scraper-cli
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up your environment variables:**

    Create a `.env` file in the project root directory with the following content:

    ```env
    USERNAME=your_username
    EMAIL=your_email
    PASSWORD=your_password
    ```

## Usage

### Login and Save Cookies

Before scraping, you need to log in to your Twitter account to save the session cookies. Run the following command:

```sh
python main.py login
```

This will log in using the credentials stored in the `.env` file and save the session cookies to `cookies.json`.

### Scrape Tweets

To scrape tweets from a user, run the following command:

```sh
python main.py scrape <identifier> <page_limit> [--by_user_id]
```

#### Arguments

- `identifier`: The user ID or screen name of the Twitter account.
- `page_limit`: The number of additional pages of tweets to fetch.
- `--by_user_id`: Optional flag to specify that the identifier is a user ID. If omitted, the identifier is assumed to be a screen name.

#### Examples

1. **Scraping by Screen Name:**

    ```sh
    python main.py scrape elonmusk 100
    ```

    This command scrapes tweets from the user with the screen name `elonmusk` and fetches 100 additional pages of tweets.

2. **Scraping by User ID:**

    ```sh
    python main.py scrape 12345678 100 --by_user_id
    ```

    This command scrapes tweets from the user with the ID `12345678` and fetches 100 additional pages of tweets.

## Output

The scraped tweets are saved in a CSV file named `tweets_<identifier>_<timestamp>.csv`, where `<identifier>` is the user ID or screen name, and `<timestamp>` is the current date and time.

Each row in the CSV file contains the following fields:

- `created_at`: The timestamp when the tweet was created.
- `text`: The text content of the tweet.
- `view_count`: The view count of the tweet.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
