from requests_oauthlib import OAuth1
import json
import sys
import requests
import nltk
nltk.download("punkt")
import secret_data # file that contains OAuth credentials
# import nltk # uncomment line after you install nltk

## SI 206 - HW
## COMMENT WITH:
## Your section day/time:
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3:Caching
#Finish parts 1 and 2 and then come back to this

#Code for Part 1:Get Tweets
baseurl = "https://api.twitter.com/1.1/statuses/user_timeline.json"
params = {"screen_name":username, "count":num_tweets }
response = requests.get(baseurl, params, auth=auth)
json_data = json.loads(response.text)

with open('tweet.json', 'w') as outfile:
    file_name = json.dumps(json_data,indent=4,sort_keys=True)
    outfile.write(file_name)


#Code for Part 2:Analyze Tweets
def analyze_tweets(json_datas):
    for text in range(len(json_datas)):
        text_file = json_data[text]["text"]
        tokens = nltk.word_tokenize(text_file)
        freqDist = nltk.FreqDist(token for token in tokens
                                if token.isalpha() and "http" not in token and "https"
                                not in token and "RT" not in token)

    for word, frequency in freqDist.most_common(5):
        print(word + " " + str(frequency))
        
analyze_tweets(json_data)
# Code for Part 3: Implement Caching

CACHE_FNAME = 'cache_file_name.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)
# print(params_unique_combination(baseurl, params))
# The main cache function: it will always return the result for this
# url+params combo. However, it will first look to see if we have already
# cached the result and, if so, return the result from cache.
# If we haven't cached the result, it will get a new one (and cache it)
def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Fetching cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl, params, auth=auth)

        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

# print(make_request_using_cache(baseurl, params))


if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
