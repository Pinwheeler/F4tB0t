def looper(listo):
    #print listo
    for item in listo:
       if do_we_have_enough(item):
           listo.remove(item)
    return listo
           
shopping_list = ["apple", "apple", "banana", "cherry", "butter", "milk"]

def do_we_have_enough(item):
    return item == "apple" or item == "milk" or item == "toothpaste"


def blah():
    for i in looper(shopping_list):
        print i
    
blah()

class Glass(object):
    def __init__(self, color, height, circumference):
        self.color = color
        self.height = height
        self.circumference = circumference
        self.capacity = height * circumference * 3.14
        self.fullness = 0
    def fill(self):
        self.fullness = self.capacity
    def drink_out_of(self, gulp_size):
        self.fullness = self.fullness - gulp_size 
        if self.fullness < 0:
            self.fullness = 0
        
this_glass = Glass("clear", 4, 7)
this_glass.fill()
this_glass.drink_out_of(10)

another_glass = Glass("red", 4, 7)

print this_glass.fullness < another_glass.fullness