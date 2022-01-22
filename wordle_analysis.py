import sys, random
from collections import Counter
from wordle_data import valid_words, answer_words
from wordle import Wordle
from wordle_solver import NaiveWordleSolver

import timeit

def pruning_ranking():
  for guess in valid_words:
    start = timeit.default_timer()  
    max_pruning = 0
    total_pruning = 0
    for word in answer_words:
      if guess == word: 
        continue
      wp = Wordle(word)
      result = wp.check(guess)
      wp.append(guess)
      ws = NaiveWordleSolver(guess, result)
      n = ws.prune()
      max_pruning = max(n, max_pruning)
      total_pruning += n
    stop = timeit.default_timer()
    print (stop - start, guess, total_pruning, max_pruning)
    yield (guess, total_pruning, max_pruning)

def main(args):
  for (guess, total, maximum) in pruning_ranking():
    print (guess, total,maximum)




if __name__ == "__main__":
  main(sys.argv[1:])



# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
