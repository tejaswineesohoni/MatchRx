import json
from datetime import datetime
from elasticsearch import Elasticsearch
import fetchtweets
import json
import pickle
import sys
from flask import Flask
from pyelasticsearch import ElasticSearch


#Find the most relevant articles by matching documents in ElasticSearch
def findmatchingpeople(user):
    
  hitcount=0  
  es1 = Elasticsearch()
  comparetweet = fetchtweets.userSearch(user)
  comparetweet1 = comparetweet.split()
  ct1 = ""
  for wc in range(10):
    ct1 = ct1 + " " + comparetweet1[wc]  
  q2= {
  "size": 8,
    "query": {
        "match": {"text": ct1}
  }}    
  resA = es1.search(index='twf-index',body = q2)
  personList = []
  for hit in resA['hits']['hits']:
    if hitcount==0:
      person="%(url)s" % hit["_source"]
      break
  print "\n\n\nPerson who matches most closely is : ",person
  return person


#Fill ElasticSearch database with Tweets indexed by news links
def fillElasticSearch():
    
    listOfTextFiles = ["BodyTexts.json"]
        
    es1 = Elasticsearch()
            
    es1.indices.create(index='twf-index', ignore=400)
    i = 0
    for fileName in listOfTextFiles:
        with open(fileName) as bodytx:
            tweets = {}
            tweets = json.load(bodytx)
        for key in tweets.keys():
            doc = {
                'url' : key,
                'text' : tweets[key]
                }
            es1.index(index = 'twf-index' , doc_type='tweet',id = i, body = doc)
            i = i+1
    es1.indices.refresh(index='twf-index')

  
def main():
  fillElasticSearch()
  findmatchingpeople()

   
if __name__ == '__main__':
    main()
