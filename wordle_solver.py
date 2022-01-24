import sys, random, string
from collections import Counter
from wordle_data import valid_words, answer_words
from wordle import Wordle


rand123 = random.Random(1234)

class NaiveWordleSolver(object):
  def __init__(self, root, result):
    self.answer_set = set(answer_words)
    self.guesses = [(root, result)]
    self.removed = set()
    self.unknowns = set(string.ascii_lowercase)
  def feed(self, guess, result):
    self.guesses.append((guess, result))
  def next(self):
    return rand123.choice(list(self.answer_set))
  def prune(self):
    # collapse greens
    result = ['_']*5
    freqs = Counter()
    included = set()
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
    for (g,c) in self.guesses:
      for (i,a) in enumerate(g):
        if c[i] == '_' and freqs[a] == 0:
          self.removed.add(a)
    knowns = set()
    for (g,c) in self.guesses:
      knowns = knowns| set(g)
    self.unknowns = self.unknowns - knowns
    pruned_set = set()
    position_miss = 0
    missing_letters = 0
    frequency_miss = 0
    already = set([g for (g,c) in self.guesses])
    for word in self.answer_set:
      prune = False
      if word in already:
        prune = True
      for c in self.removed:
        if prune:
          break
        if c in word:
          prune = True
          missing_letters += 1
      for (i,c) in enumerate(result):
        if prune:
          break
        if c != '_' and word[i] != c:
          prune = True
          position_miss += 1
      wfreq = Counter(word)
      for c in freqs:
        if prune:
          break
        if wfreq[c] < freqs[c]:
          prune = True
          frequency_miss += 1
      if not prune:
        pruned_set.add(word)
    pruned_count = len(self.answer_set) - len(pruned_set)
    self.answer_set = pruned_set
    #print("Reduced to {} words, answer_set has {} items".format(len(pruned_set), len(self.answer_set)))
    #print("Unknowns left : {}".format("".join(sorted(self.unknowns))))
    return pruned_count 

class UnknownsWordleSolver(NaiveWordleSolver):
  def __init__(self, root, result):
    super().__init__(root, result)
  def rank_unknowns(self, option):
    commons = set(self.unknowns) & set("aeiourtpsh")
    r = lambda c: ((c in commons) and 2) or 1
    return -1*sum([r(c) for c in self.unknowns if c in option])
  def next(self):
    # pick maximum unknowns
    if (len(self.answer_set) > 64 and len(self.guesses) < 3):
      avoid = set(dict(self.guesses))
      return sorted([v for v in valid_words if v not in avoid], key=lambda k : self.rank_unknowns(k))[0]
    return sorted(self.answer_set, key=lambda k : self.rank_unknowns(k))[0]

def main(args):
  if len(args) == 1:
    if args[0][0] in "123456789":
      n = int(args[0])
      return test(n)
    else:
      steps = solve(args[0])
      print("Took {} steps".format(len(steps)))
  else:
    wguess = input("Enter guess word: ")
    wresult = input("Enter result: ")
    ws = UnknownsWordleSolver(wguess, wresult)
    ws.prune()
    while len(ws.answer_set)>1:
      print (ws.answer_set)
      wguess = input("Enter guess word: ")
      wresult = input("Enter result: ")
      ws.feed(wguess, wresult)
      ws.prune()
    print (ws.answer_set)



def test(n):
  maxsteps = 0
  totalsteps = 0.0
  hard = []
  for i in range(n):
    word = random.choice(answer_words)
    steps = solve(word)
    maxsteps = max(len(steps), maxsteps)
    totalsteps = totalsteps + len(steps)
    if (len(steps) > 6):
        hard.append(word)
  print("Completed {} iterations, max = {}, avg = {}".format(n, maxsteps, totalsteps/n))
  print("Hard words = {}".format(set(hard)))

def solve(word):
    print (word)
    wp = Wordle(word)
    guess0 = random.choice(list(valid_words))
    guess0 = "later"
    result0 = wp.check(guess0)
    wp.append(guess0)
    print ("Randomly guessing {} : {}".format(guess0,result0))
    ws = UnknownsWordleSolver(guess0, result0)
    ws.prune()
    while not wp.solved:
      guess = ws.next()
      result = wp.check(guess)
      wp.append(guess)
      print ("Randomly guessing {} : {}".format(guess,result))
      ws.feed(guess, result)
      ws.prune()
    return ws.guesses


if __name__ == "__main__":
  main(sys.argv[1:])
  

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
