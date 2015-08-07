import praw
import pdb
import re
import os
import csv

from bot_config import *
from IPython import embed
from nltk import *

KILOGRAMS = "kilograms"
POUNDS = "pounds"

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

class WeightResponse(object):
  """WeightResponse takes a list of tuples and packages it nicely into an object"""
  def __init__(self, responseTuple):
    super(WeightResponse, self).__init__()
    self.responseTuple = responseTuple
    self.weight = getWeightValue(self.responseTuple)
    self.units  = getUnits(self.responseTuple)
  def weight(self):
    return self.weight
  def units(self):
    return self.units
  def weight_in_pounds(self):
    if self.units == KILOGRAMS:
      return self.weight * 2.2
    else:
      return self.weight


def extract(list):
  items = []
  while list[list.count] is not '':
    items.append(list.pop())

  return items

def weightFromText(text):
  regex = re.compile('(([0-9]+) ?([lpkLPK][\w]+))')
  return regex.findall(text)

def main():
  for comment in post.comments[1:]:
    print comment.author
    name = comment.author
    weightResponse = WeightResponse(weightFromText(comment.body)[0])
    print weightResponse.weight_in_pounds()

def getUnits(l):
  if l[2][0] == 'k':
    return KILOGRAMS
  elif l[2][0] == 'l' or 'p':
    return POUNDS

def getWeightValue(l):
  return float(l[1])





main()