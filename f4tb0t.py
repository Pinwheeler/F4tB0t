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


if not os.path.isfile('bot_config.py'):
  print "You must create config file with your reddit username and password."
  print "Please see config_skel.py"
  exit(1)

user_agent = ("F4tB0t v0.1")
r = praw.Reddit(user_agent=user_agent)
r.login(REDDIT_USERNAME, REDDIT_PASS)

"""if not os.path.isfile("users.csv"):
  users = []
else:
  with open("users.csv", "rb") as f:
    fieldnames = ['username', 'weight']
    userreader = csv.reader(f, delimiter=',')
    for row in userreader:
      user = {}
      user.username = row['username']
      user.weight   = row['weight']
      users.append(user)"""

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
      #weightResponse.pretty_print()
      good_entries = good_entries + 1 
      if weightResponse.is_this_reasonable():
        weightlist.append(weightResponse.weight_in_pounds()) 
        namelist.append(weightResponse.author)
      else:
        pass
    except Exception, e:
      bad_entries = bad_entries + 1
    
  print "The average weight of commenters is %d pounds" % int(mean(weightlist))
  tot_entries = good_entries + bad_entries
  print "There were %d entries of %d total without data" % (bad_entries, tot_entries)
  for name in namelist:
    try:
      user = r.get_redditor(name)
      subs.append(subredditsForUser(user))
    except Exception, e:
      pass
  print compiler(subs, weightlist)

def compiler(subs, weight):
  dictionary = {}
  for x in range(len(subs)):
    for y in range(len(weight)):
      if x == y:
        for z in subs[x]:
          if z in dictionary:
            dictionary[z].append(weight[y])
          else:
            dictionary[z] = [weight[y]]
      else:
        pass
  for d in dictionary:
    dictionary[d] = mean(dictionary[d])
  return dictionary

def condense(list):  
  for x in range(len(list)):
    for y in range(len(list)):
      if list[x] != "Null" and list[x] == list[y] and y > x:
        list[y] = "Null"
      else:
        pass
  list[:] = [value for value in list if value != "Null"]
  return list

def commentsForUser(user):
  return user.get_comments()

def subredditForComment(comment):
  return comment.subreddit.display_name

def subredditsForUser(user):
  subreddits = []
  for comment in commentsForUser(user):
    subreddits.append(subredditForComment(comment))
  return condense(subreddits)

def mean(list):
  summ = 0
  for i in list:
    summ = summ + i
  return float(summ)/len(list)

main()