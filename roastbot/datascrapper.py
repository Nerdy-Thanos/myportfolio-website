import pandas as pd
import praw

class FetchData(object):
	def fetch_reddit_data():
		reddit_api_key = "6pT8rJ3M7DJSiZ7fOxU0Eg"
		reddit_api_key_secret = "QVACoIC-HstocS-DTegj8URIsEfl6w"
		user_agent = "my app"

		reddit = praw.Reddit(
			client_id=reddit_api_key,
			client_secret=reddit_api_key_secret,
			user_agent=user_agent
		)
		subreddit = reddit.subreddit("RoastMe")
		print(subreddit.title)

		comments=[]
		for post in subreddit.hot(limit=2):
			post.comments.replace_more(limit=None)
			for top_level_comment in post.comments:
				comments.append(top_level_comment.body)
			print("fetching comments from",post)
		print(comments)
		return comments

comments_list = FetchData.fetch_reddit_data()
commentsdf = pd.DataFrame(comments_list)
commentsdf.to_csv("comments.csv")



