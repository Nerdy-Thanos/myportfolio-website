import pandas as pd
import praw

class FetchData(object):
	reddit_api_key = "6pT8rJ3M7DJSiZ7fOxU0Eg"
	reddit_api_key_secret = "QVACoIC-HstocS-DTegj8URIsEfl6w"
	user_agent = "my app"

	reddit = praw.Reddit(
			client_id=reddit_api_key,
			client_secret=reddit_api_key_secret,
			user_agent=user_agent
		)
	def fetch_reddit_comment_data(reddit):
		comments=[]
		subreddit = reddit.subreddit("RoastMe")
		print(subreddit.title)
		for post in subreddit.hot(limit=5):
			post.comments.replace_more(limit=None)
			for top_level_comment in post.comments:
				comments.append(top_level_comment.body)
				print("Appending Comments...")
			print("fetching comments from",post)
		print(comments)
		return comments
	
	def fetch_reddit(reddit):
		posts = []
		subreddit = reddit.subreddit("oneliners")
		for post in subreddit.top(limit=1800):
			posts.append(post.title)
			print("Appending post", post)
		return posts

#comments_list = FetchData.fetch_reddit_comment_data()
#commentsdf = pd.DataFrame(comments_list, columns=["Roasts"])
#commentsdf.to_csv("comments.csv")

title_list = FetchData.fetch_reddit(FetchData.reddit)
titledf = pd.DataFrame(title_list, columns=['jokes'])
titledf.to_csv("jokes.csv")



