class SubredditDictionary(object):
  def __init__(self, subs, weights):
    self.dictionary = self.compiler(subs, weights)
    
  def compiler(self, subs, weights):
    dictionary = {}
    for idx in range(len(subs)):
      for idy in range(len(weights)):
        if idx == idy:
          for user_subreddit in subs[idx]:
            key = user_subreddit
            if key in dictionary:
              dictionary[key].append(weights[idy])
            else:
              dictionary[key] = [weights[idy]]
        else:
          pass
    return dictionary
    
  def pretty_print(self):
    print "Subreddit | responses | mean |"
    for subreddit_name, list_of_weights in self.dictionary.iteritems():
      count = len(list_of_weights)
      mean = float(sum(list_of_weights)) / float(len(list_of_weights))
      print "%s | %d | %f" % (subreddit_name, count, mean)