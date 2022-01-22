import sys, random
from collections import Counter
from wordle_data import valid_words, answer_words


class Wordle(object):
  def __init__(self, word):
    self.word = word
    self.counts = Counter(word) 
    self.guesses = []
    self.solved = False
  def append(self, guess):
    c = self.check(guess)
    if c:
      self.guesses.append((guess, c))
      if c == 'G' * 5:
        self.solved = True
  def check(self, guess):
    if guess not in valid_words:
        print("Not valid word", guess)
        return None
    lcounts = Counter(self.counts)
    result = ['_']*len(self.word)
    # first mark the greens
    for (i,l) in enumerate(guess):
      if (self.word[i] == guess[i]):
        lcounts[l] -= 1
        result[i] = 'G'
    for (i,l) in enumerate(guess):
      if (l in self.word and result[i] != 'G'):
        if (lcounts[l] > 0):
            lcounts[l] -= 1
            result[i] = 'Y'
    return "".join(result)
  def output(self):
    green = lambda s : "\033[01m\033[93m{}\033[00m".format(s)
    yellow = lambda s : "\033[01m\033[93m{}\033[00m".format(s)
    for (g,r) in self.guesses:
      line = ""
      for (l,c) in zip(g,r):
        if c == 'G':
          line = line+green(l)
        elif c == 'Y':
          line  = line+yellow(l)
        else:
          line  = line + l
      print(line, r)
    

def test_wordles():
  w = Wordle("hello")
  assert "_"*5 == w.check("traps")
  assert None == w.check("olleh")
  assert "__YG_" == w.check("aioli")
  w.append("traps")
  w.append("olleh")
  w.append("aioli")
  w.output()

        
def main(args): 
  if (len(args) > 0 and args[0] == "test"):
      test_wordles()
      return
  word = random.choice(answer_words)
  print (word)
  w = Wordle(word)
  while not w.solved:
    i = len(w.guesses)
    guess = input("[{}] Enter guess:".format(i))
    w.append(guess)
    w.output()
  

if __name__ == "__main__":
  main(sys.argv[1:])

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
