#!/usr/bin/env python3

#NOTE: You are using TWEEPY, use TWEEPY docuemntation, Duh
#searchTweets needs: The string to search, the date from which to collect, number of tweets to collect.
#Keys are found and regenerated at https://developer.twitter.com/en/portal/projects/1494803038925508608/apps/23432712/keys
#You must reset the collection tweets.num_tweets to 0 after each iteration
#10 each
#hashes from Suresha and Tiwari

import os
import tweepy as tw
import pandas as pd
import csv
import hashlib
from datetime import datetime
import keys

def main():
    #Establish number of tweets
    numTweets = 100
    
    #Authorize
    auth, api = authorize()
    
    #Initialize Search Arrays
    keywords = initSearchArray()
    
    #Perform Searches
    searchLoop(keywords, auth, api, int(numTweets))


def authorize():
    auth = tw.OAuthHandler(keys.key, keys.keySecret)
    auth.set_access_token(keys.token, keys.tokenSecret)
    api = tw.API(auth, wait_on_rate_limit=True)
    return auth, api
    
def searchLoop(keywords, auth, api, numTweets):
    #Search keywords
    for word in keywords:
        tweets = searchTweets(auth, api, word, int(numTweets))
        writeToCSV(api, tweets, numTweets, word)
    
def searchTweets(auth, api, searchString, numberOfTweets):
    tweets = tw.Cursor(api.search_tweets,
              q=searchString,
              tweet_mode="extended",
              lang="en").items(numberOfTweets)
    return tweets

def getFullText(api, idNumber):
    try:
        status = api.get_status(idNumber, tweet_mode="extended")
        try:
            full_text = status.retweeted_status.full_text
        except AttributeError:  # Not a Retweet
            full_text = status.full_text
    except:
        full_text = "No full text"
    return full_text
    
def writeToCSV(api, collection, numTweets, searchString):

    if(checkHeader()):
        writeHeader()
            
    time = datetime.utcnow()

    for tweet in collection:
        print("Text: " + tweet.full_text)
        f = open("TweetsData.csv", "a")
        writer = csv.writer(f)
        full_text = getFullText(api, tweet.id)
        hash_text = makeHash(full_text)
        retweet = isRetweet(tweet)
        userId = ":" + str(tweet.user.id)
        tweetId = ":" + str(tweet.id)
        inReplyID = ":" + str(tweet.in_reply_to_user_id)
        place = getPlace(tweet.place)
        tempRow = [time, str(tweet.created_at), str(tweet.user.name), str(tweet.user.screen_name), userId, tweetId, str(retweet), inReplyID, str(tweet.in_reply_to_screen_name) ,str(tweet.coordinates), place, str(tweet.retweet_count), str(tweet.favorite_count), searchString, str(tweet.lang), hash_text, full_text]
        writer.writerow(tempRow)
        f.close()

    collection.num_tweets = 0
    
def writeHeader():
    f = open("TweetsData.csv", "a")
    header = ['Collected At (UTC)','Created At (UTC)','User Name','Screen Name','User ID','Tweet ID','Is Retweet','In Reply To This User ID','In Reply To This Screen Name','Coordinates','Place','Retweet Count','Favorite Count','Search Keyword','Language','Full Text hash','Full Text']
    writer = csv.writer(f)
    writer.writerow(header)
    f.close()
    
def isRetweet(tweet):
    isItRetweet = "False"
    try:
        tweet.retweeted_status
        isItRetweet = "True"
    except:
        isItRetweet = "False"
    return isItRetweet
    
def makeHash(inputString):
    hashedInput = hashlib.sha256(inputString.encode('utf-8')).hexdigest()
    return hashedInput
    
def checkHeader():
    newFile = False
    try:
        data = pd.read_csv("TweetsData.csv", nrows=1)
        newFile = False
    except:
        newFile = True
    return newFile
    
def getPlace(placeObject):
    place = "None"
    if(placeObject != None):
        print(placeObject)
        place = placeObject.full_name + ", " + placeObject.country
    return place
    
#Based on Hashtags from Suresha and Tiwari 2021
def initSearchArray():
    keywords = readInKeywords()
    keywords = addHashtags(keywords)
    return keywords

def addHashtags(inArray):
    outArray = [];
    for word in inArray:
        temp = "#" + word.replace(" ","")
        outArray.append(word)
        outArray.append(temp)
    return outArray
    
def readInKeywords():
    keywords = [];
    with open('Keywords.txt') as f:
        keywords = f.readlines()
    return keywords
    
def printArray(inArray):
    for word in inArray:
        print(word)
    
if __name__ == '__main__':
    main()
