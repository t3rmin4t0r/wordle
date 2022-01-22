import sys, random
from collections import Counter
from wordle_data import valid_words, answer_words
from wordle import Wordle

class NaiveWordleSolver(object):
  def __init__(self, root, result):
    self.answer_set = set(answer_words)
    self.guesses = [(root, result)]
    self.removed = set()
  def feed(self, guess, result):
    self.guesses.append((guess, result))
  def next(self):
    return random.choice(list(self.answer_set))
  def prune(self):
    # collapse greens
    result = ['_']*5
    freqs = Counter()
    for (g,c) in self.guesses:
      lfreq = Counter()
      for (i,a) in enumerate(g):
        if c[i] == 'G':
          result[i] = a
          lfreq[a] += 1
      for a in lfreq:
        freqs[a] = max(freqs[a], lfreq[a])
    # collect yellows
    for (g,c) in self.guesses:
      # freq for the yellow (this might overlap the greens)
      lfreq = Counter()
      for (i,a) in enumerate(g):
        if c[i] == 'Y':
          lfreq[a] += 1
      for a in lfreq:
        freqs[a] = max(freqs[a], lfreq[a])
    # collect reds, but consider frequency
    reds = set()
    for (g,c) in self.guesses:
      for (i,a) in enumerate(g):
        if c[i] == '_' and freqs[a] == 0:
          self.removed.add(a)
    pruned = set()
    position_miss = 0
    missing_letters = 0
    frequency_miss = 0
    for word in self.answer_set:
      for c in self.removed:
        if c in word:
          pruned.add(word) 
          missing_letters += 1
      for (i,c) in enumerate(result):
        if c != '_' and word[i] != c:
          pruned.add(word)
          position_miss += 1
      wfreq = Counter(word)
      for c in freqs:
        if wfreq[c] < freqs[c]:
          if word == "lease":
            print (c, wfreq, freqs)
            print("WTF 3")
          pruned.add(word)
          frequency_miss += 1
    print ("Missing letter: {}".format(missing_letters))
    print ("Position miss: {}".format(position_miss))
    print ("Freuency miss: {}".format(frequency_miss))
    self.answer_set = self.answer_set - pruned
    print("Pruned {} words, answer_set has {} items".format(len(pruned), len(self.answer_set)))
    if len(self.answer_set) < 16:
      print(self.answer_set)

      
  def __repr__(self):
    return ""

def main(args):
  word = random.choice(answer_words)
  word = "lease"
  print (word)
  wp = Wordle(word)
  guess0 = random.choice(list(valid_words))
  guess0 = "blast"
  result0 = wp.check(guess0)
  wp.append(guess0)
  print ("Randomly guessing {} : {}".format(guess0,result0))
  ws = NaiveWordleSolver(guess0, result0)
  ws.prune()
  while not wp.solved:
    guess = ws.next()
    result = wp.check(guess)
    wp.append(guess)
    print ("Randomly guessing {} : {}".format(guess,result))
    ws.feed(guess, result)
    ws.prune()


if __name__ == "__main__":
  main(sys.argv[1:])
  

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
