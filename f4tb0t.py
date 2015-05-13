import praw
import pdb
import re
import os
import csv

from bot_config import *
from IPython import embed
from nltk import *

if not os.path.isfile('bot_config.py'):
  print "You must create config file with your reddit username and password."
  print "Please see config_skel.py"
  exit(1)

user_agent = ("F4tB0t v0.1")
r = praw.Reddit(user_agent=user_agent)
r.login(REDDIT_USERNAME, REDDIT_PASS)

if not os.path.isfile("users.csv"):
  users = []
else:
  with open("users.csv", "rb") as f:
    fieldnames = ['username', 'weight']
    userreader = csv.reader(f, delimiter=',')
    for row in userreader:
      user = {}
      user.username = row['username']
      user.weight   = row['weight']
      users.append(user)

post = r.get_submission(POST_ENDPOINT)

def extract(list):
  items = []
  while list[list.count] is not '':
    items.append(list.pop())

  return items

def weightFromText(text):
  regex = re.compile('([0-9]+)')
  return regex.findall(text)

for comment in post.comments[1:]:
  print comment.author
  name = comment.author
  weight = weightFromText(comment.body)
  print weight

