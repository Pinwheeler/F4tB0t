KILOGRAMS = "kilograms"
POUNDS = "pounds"

class WeightResponse(object):
  """WeightResponse takes a list of tuples and packages it nicely into an object"""
  def __init__(self, responseTuple):
    super(WeightResponse, self).__init__()
    self.responseTuple = responseTuple
    self.weight = self.getWeightValue(self.responseTuple)
    self.units  = self.getUnits(self.responseTuple)
    self.author = ""
  def weight_in_pounds(self):
    if self.units == KILOGRAMS:
      return int(self.weight * 2.2)
    else:
      return int(self.weight)
      
  def pretty_print(self):
    if self.is_this_reasonable():
      weightString = "%s weighs %d pounds" % (self.author, self.weight_in_pounds())
      print weightString
    else:
      pass
    
  def getUnits(self, l):
    if l[2][0].lower() == 'k':
      return KILOGRAMS
    elif l[2][0].lower() == 'l' or 'p':
      return POUNDS
      
  def getWeightValue(self, l):
    return float(l[1])
    
  def is_this_reasonable(self):
    if self.weight_in_pounds() < 80 or self.weight_in_pounds() > 600:
      return False
    return True