import oauth2
import time
import urllib2
import json

#Get Twitter Handles
def GetHandles():
  handles=[]
  text_file = open("handles.txt", "r")
  handles=text_file.read().split('\n')
  text_file.close()
  return handles



#Call Twitter API and fetch tweets
def callTwitter(urlIn,otherParams,callType):
  CONSUMER_KEY = "B6Mtk1aoEmflLm7aXbYlIl4Dq"
  CONSUMER_SECRET = "UJtCziVAuij7MoWc0Kglby0v0YiGoc074VuuoPKxqOZg4oIbKz"
  TOKEN_KEY = "1224665718-cJ9HabxQVpfR6r71Trs0RJYQuAsVaBt8n20QXTj"
  TOKEN_SECRET = "zLoD4uo4ZIyHu666cOLqjpgVLBQBRQm7VM5eakcFnp8X5"
  url = urlIn
  reqParams = {
  "oauth_version": "1.0",
  "oauth_nonce": oauth2.generate_nonce(),
  "oauth_timestamp": int(time.time())
  }
  params = dict(reqParams.items() + otherParams.items()) 
  consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
  token = oauth2.Token(key=TOKEN_KEY, secret=TOKEN_SECRET)
  params["oauth_consumer_key"] = consumer.key
  params["oauth_token"] = token.key    
  req = oauth2.Request(method=callType, url=url, parameters=params)
  signature_method = oauth2.SignatureMethod_HMAC_SHA1()
  req.sign_request(signature_method, consumer, token)
  headers = req.to_header()
  url = req.to_url()
  response = urllib2.Request(url)
  data = json.load(urllib2.urlopen(response))
  return data


def findUser(screen_name):
  API = "https://api.twitter.com/1.1/users/show.json"
  body_list=[]
  params={}
  params["screen_name"]=screen_name
  dataOut=callTwitter(API,params,"GET")
  print dataOut
  name=dataOut["name"]
  description=dataOut["description"]
  print description
  return name, description

def userSearch(tweeter):
  USER_API = "https://api.twitter.com/1.1/statuses/user_timeline.json"
  body_list = []
  params = {}
  params["screen_name"] = tweeter
  params["count"] = 50
  params["include_rts"] = "true"
  dataOut = callTwitter(USER_API,params,"GET")
  for tweet in range(len(dataOut)):
    body_list.append(dataOut[tweet]["text"])
  return "".join(body_list)


#Search Twitter for users by their Twitter handle
def getTweets(tweeter):
  USER_API = "https://api.twitter.com/1.1/statuses/user_timeline.json"
  body_list = []
  params = {}
  params["screen_name"] = tweeter
  params["count"] = 50
  params["include_rts"] = "true"
  dataOut = callTwitter(USER_API,params,"GET")
  print dataOut
  print dataOut[0]["user"]["screen_name"]
  for tweet in range(len(dataOut)):
    body_list.append(dataOut[tweet]["text"])
  return "".join(body_list)


#Fetch Tweets of the users tweeting out the news links
def twitterSearch():
  bodyText = {}
  RATE_API = "https://api.twitter.com/1.1/application/rate_limit_status.json"
  
  handles = GetHandles()
  for i in range(len(handles)):
    #print "\n" + str(handles[i])
    bodyText[handles[i]] = ""
    userBody = userSearch(handles[i])
    bodyText[handles[i]] = bodyText[handles[i]] + userBody  
  outputFile = "BodyTexts.json"
  with open(outputFile, "w") as outfile:
      json.dump(bodyText, outfile, indent=4)
  listOfTextFiles = [outputFile]
  return listOfTextFiles

def main():
  twitterSearch()
    
if __name__ == '__main__':
  main()
