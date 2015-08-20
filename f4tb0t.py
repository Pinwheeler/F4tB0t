import praw
import pdb
import re
import os
import csv
import pdb

from bot_config import *
from IPython import embed
from nltk import *
from weight_response import WeightResponse
from subreddit_dictionary import SubredditDictionary


if not os.path.isfile('bot_config.py'):
  print "You must create config file with your reddit username and password."
  print "Please see config_skel.py"
  exit(1)

user_agent = ("F4tB0t v0.1")
r = praw.Reddit(user_agent=user_agent)
r.login(REDDIT_USERNAME, REDDIT_PASS)
users = []

if os.path.isfile("users.csv"):
  with open("users.csv", "rb") as f:
    fieldnames = ['username', 'weight']
    userreader = csv.reader(f, delimiter=',')
    for row in userreader:
      user = {}
      user.username = row['username']
      user.weight   = row['weight']
      users.append(user)

post = r.get_submission(POST_ENDPOINT)

def weightFromText(text):
  regex = re.compile('(([0-9]+) ?([lpkLPK][\w]+))')
  return regex.findall(text)

def main():
  good_entries = 0
  bad_entries = 0
  weightlist = [] 
  namelist = []
  subs = []
  for comment in post.comments[1:]:
    name = comment.author
    try:
      weightResponse = WeightResponse(weightFromText(comment.body)[0])
      weightResponse.author = name 
      good_entries = good_entries + 1 
      if weightResponse.is_this_reasonable():
        weightlist.append(weightResponse.weight_in_pounds()) 
        namelist.append(weightResponse.author)
        newUser = {}
        newUser['username'] = weightResponse.author
        newUser['weight'] = weightResponse.weight_in_pounds()
        users.append(newUser)
      else:
        pass
    except Exception, e:
      bad_entries = bad_entries + 1
    
  for name in namelist:
    try:
      user = r.get_redditor(name)
      subs.append(subredditsForUser(user))
    except Exception, e:
      pass
  subrDict = SubredditDictionary(subs, weightlist)
  subrDict.pretty_print()

def commentsForUser(user):
  return user.get_comments()

def subredditForComment(comment):
  return comment.subreddit.display_name

def subredditsForUser(user):
  subreddits = []
  for comment in commentsForUser(user):
    subreddits.append(subredditForComment(comment))
  return list(set(subreddits))

def writeData():
  with open('users.csv', 'wb') as csvfile:
    userWriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for user in users:
      userWriter.writerow([user['username'], user['weight']])

main()
writeData()