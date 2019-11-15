from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import tweepy
from textblob import TextBlob



consumer_key = 'OQlTtOmd9GVgdTOIvaOxsYaJg'
consumer_secret = 'gqj4glKohpZzqYUHAQo5nG6kbSnKE7bUz5UHvqiFE8faRuGfpD'

access_token = '2333062622-pYWn2sIT6fCQoU8BghfDelTq5ylc4lQdPhGPcxU'
access_token_secret = 'ZHzJwvddyaaJLSWqswa5ZKgNWpUzcjn9tsOjMp2yFGV9k'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

@api_view(["GET"])
def textanalyzer(request):

    positive = 0
    neutral = 0
    negative = 0
    for tweet in tweepy.Cursor(api.search,q=request.GET.get("text"), rpp=100, count=20, result_type="recent", include_entities=True,lang="en", tweet_mode='extended').items(100):
        analysis=TextBlob(tweet.full_text)
        if analysis.sentiment.polarity > 0:
            positive += 1
        elif analysis.sentiment.polarity == 0:
            neutral += 1
        else:
            negative += 1
    return JsonResponse({"positive":positive,"neutral":neutral,"negative":negative})

@api_view(["GET"])
def gettweets(request):
    tweets = []
    for tweet in tweepy.Cursor(api.search,q=request.GET.get("text"), rpp=100, count=20, result_type="recent", include_entities=True,lang="en", tweet_mode='extended').items(50):
        temp = {}
        temp["tweet"] = tweet.full_text
        temp["username"] = tweet.user.name
        temp["profileimg"] = tweet.user.profile_image_url_https
        temp["screenname"] = tweet.user.screen_name
        # # with graph.as_default():
        # analysis = TextBlob(tweet.full_text)
        polarity = TextBlob(tweet.full_text).sentiment.polarity
        # temp["label"] = analysis["label"]
        temp["score"] = polarity
        if polarity>0:
            temp["sentiment"] = 'positive'
        elif polarity<0:
            temp["sentiment"] = 'negative'
        else:
            temp["sentiment"] = 'neutral'
        tweets.append(temp)
    return JsonResponse(tweets,safe=False)
