# RedditOldModmail-to-Sqlite

Archives up to 1000 parent messages in Reddit old modmail with all replies to those messages.

In its current form it only archives the last 1000 parent messages (with all replies) as I only needed about 130 or so for the only subreddit I moderate which used old modmail.

If your mod team has been ride-or-die with old modmail until the bitter end you'll need to edit the script into a while loop using the "after" param to make it pull older messages.

# Requirements:

* Python 3
  * dotenv
  * praw
  * sqlite3

* A Reddit API account with modmail access in your target subreddit.

Create the Reddit API key as a personal script. I do not recommend using your main reddit account for this. Make a separate bot account and add it to your mod team.

# Config

Create a .env file in the top level directory with the following params:

REDDIT_CLIENT=your_reddit_client  
REDDIT_SECRET=your_reddit_secret  
REDDIT_USERNAME=reddit_api_account_username  
REDDIT_PASS=reddit_api_account_password

Edit lines 14-16 with the name of your target subreddit, your desired database filename, and your unique useragent for the Reddit API account.

The database with your filename of choice will be created in the top level directory upon running the script for the first time.

# Disclaimer

I would recommend only using this script to archive to a local database on your hard drive. If you must make your old modmail archives public on the web for other members of your team, protect it heavily with passwords and 2FA.
