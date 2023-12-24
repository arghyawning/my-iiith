import string
import tweepy

bearer_token="AAAAAAAAAAAAAAAAAAAAAFl%2BYwEAAAAA5Nz%2BUfcx%2FB5pH8a4UgCMuJh6G0M%3D7Ve2Qy0nEMwLl0cGgIm9S3sr2oicrBoiS3Pi287pE2QdydmUTK"

obj=tweepy.Client(bearer_token)

hashtag_file={
    "#novaxdjokovic": "novaxdjokovic.txt",
    "#westandwithnovak": "westandwithnovak.txt",
    "#novakdjokovic": "novakdjokovic.txt",
    "#australiahasfallen": "australiahasfallen.txt"
}
allowed_chars = set(string.ascii_letters + string.digits + string.punctuation + string.whitespace)

def clean_string(text):
    text = [x for x in text if x in allowed_chars]
    text = "".join(text)
    return text

hashtags=["#novaxdjokovic","#westandwithnovak","#novakdjokovic","#djocovid","#nolegohome"]
for hashtag in hashtags:
    with open(hashtag[1:] + ".txt", "w", encoding="utf-8") as f:
        for tweet in tweepy.Paginator(
            obj.search_recent_tweets, hashtag + " lang:en -is:retweet", max_results=100
        ).flatten(limit=100):
            text = clean_string(tweet.text)
            text = text.replace("\n", " ")
            text = text.replace("\r", " ")
            f.write(f"{text}\n")
            #id=clean_string(tweet.id)
            id=tweet.id