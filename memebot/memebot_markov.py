__author__ = 'jonathan'

import random
import os

from memebot_config import CORPUS_PATH
import memebot_classifier


class Markov(object):

  def __init__(self, open_file=None):
    self.cache = {}
    self.open_file = open_file
    #self.words = self.file_to_words()
    self.words = self.comments_to_words()
    self.word_size = len(self.words)
    self.database()


  def file_to_words(self):
    self.open_file.seek(0)
    data = self.open_file.read()
    words = data.split()
    return words

  def comments_to_words(self):
      words = []
      for cdir in os.listdir(CORPUS_PATH):
          cdir_path = os.path.join(CORPUS_PATH,cdir)
          print cdir_path
          if os.path.isdir(cdir_path):
            for cfile in os.listdir(cdir_path):
                cfile_path = os.path.join(cdir_path,cfile)
                f = open( cfile_path, 'r' );
                text = ' '.join( f.readlines() )
                f.close()
                words.extend( memebot_classifier.get_msg_words(text, sw=None))
      return words



  def triples(self):
    """ Generates triples from the given data string. So if our string were
	"What a lovely day", we'd generate (What, a, lovely) and then
	(a, lovely, day).
    """

    if len(self.words) < 3:
      return

    for i in range(len(self.words) - 2):
      yield (self.words[i], self.words[i+1], self.words[i+2])

  def database(self):
    for w1, w2, w3 in self.triples():
      key = (w1, w2)
      if key in self.cache:
	self.cache[key].append(w3)
      else:
	self.cache[key] = [w3]

  def generate_markov_text(self, size=25):
    seed = random.randint(0, self.word_size-3)
    seed_word, next_word = self.words[seed], self.words[seed+1]
    w1, w2 = seed_word, next_word
    gen_words = []
    for i in xrange(size):
      gen_words.append(w1)
      w1, w2 = w2, random.choice(self.cache[(w1, w2)])
    gen_words.append(w2)
    return ' '.join(gen_words)


if __name__ == '__main__':
    m = Markov();
    while True:
        t = m.generate_markov_text()
        print t
        print memebot_classifier.karma_classify(t)
        raw_input("[Press Enter]")