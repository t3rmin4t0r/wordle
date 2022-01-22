import sys
from collections import Counter
from wordle_data import valid_words, answer_words


class Wordle(object):
  def __init__(self, word):
    self.word = word
    self.counts = Counter(word) 
    self.guesses = []
  def append(self, guess):
    self.guesses.append((guess, self.check(guess)))
  def check(self, guess):
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

def test_wordles():
  w = Wordle("hello")
  assert "_"*5 == w.check("traps")
  assert "YYGYY" == w.check("olleh")

        
def main(args): 
  if (len(args) > 0 and args[0] == "test"):
      test_wordles()
  pass

if __name__ == "__main__":
  main(sys.argv[1:])
