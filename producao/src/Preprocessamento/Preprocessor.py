#!/usr/bin/python2.7

import sys
import operator
import Dictionary
import Filters
import re


class Preprocessor:
  cleanedFile = None
  uniqFile = None
  finalFile = None

  #columns starts in 0
  def __init__(self, inFile, outPath, columnStart):
    self.columnStart = columnStart

    self.outPath = outPath
    
    fin = open(inFile, 'r')
    self.inputContent = fin.read().splitlines()
    fin.close()
    self.histogram = {}


  def clean_text(self,minWordLen):

    dictionary = Dictionary.Dictionary2()
    for i in range(len(self.inputContent)):
      line = self.inputContent[i].rstrip('\n').split('\t')

      text = " ".join(line[self.columnStart:]).strip()
      text = Filters.filter_url( text )
      text = Filters.filter_accents(text.decode('utf8', 'ignore'))
      text = Filters.filter_punct( text )
      text = Filters.filter_charRepetition( text ).split()

      words = [ word for word in text if word.find('@') == -1 and not word.isdigit() \
          and len(word) > minWordLen]

      newLine = "\t".join( line[:self.columnStart] ) + "\t"
      for word in words:
        if word[0].isupper():
          newWord = word
        else:
          newWord = dictionary.getWord(word, False, False)
        
        if( word not in self.histogram ):
          self.histogram[word] = 0

        self.histogram[word] += 1
        newLine += newWord + " "
     
      self.inputContent[i] = newLine.strip()
  
  def generate_histogram(self, PRECISION):
    self.sorted_histogram = sorted(self.histogram.iteritems(), 
        key=operator.itemgetter(1), reverse = True)

    sigma = []
    fout = open(self.outPath + "/histogram.txt",'w')
    for word,value in self.sorted_histogram:
      print >> fout, "%s %s" % (word, value)
      sigma.append(value)
    fout.close()

    second_norm = sigma[1]

    f = lambda x: x / float(second_norm)
    sigma_norm = map(f,sigma)

    second_derivative = []
    second_derivative.append(0)
    for i in range(1,( len(sigma)-1) ):
      v = sigma_norm[i-1] - 2*sigma_norm[i] + sigma_norm[i+1]
      second_derivative.append( v )

    rank = len(sigma_norm) - 1;
    while( rank > 1 ):
      rank -= 1
      if( abs(second_derivative[rank]) >= PRECISION ):
        break

    if( rank < 100 ):
      self.breakPoint = rank
    else:
      self.breakPoint = 100

  def remove_stopwords(self, LANGUAGE):
    stopWords = set()
    fStop = open("StopWords/%s_stop.txt" % LANGUAGE, 'r')

    for line in fStop:
      stopWords.add( line.strip().split()[0].lower() )
    fStop.close()

    regex = r'([0-9]+)'
    r = re.compile(regex)

    fout = open(self.outPath + "/validWords.txt",'w')
    contador = 0;
    
    entrada = open(self.outPath + '/histogram.txt', 'r')

    for line in entrada:
      word, value = line.strip().split()
      value = int(value)
      
      contador += 1
      if( contador <= self.breakPoint ):
        stopWords.add( word.strip().lower() )
        continue


      if len(r.findall(word)) != 0 or value <= 0 \
        or word in stopWords:
          continue

      print >> fout, line.strip()
    fout.close()

    fout = open(self.outPath + "/cleanedDB.txt", 'w')
    
    for line in self.inputContent:
      line = line.strip('\n').split('\t')
      newLine = "\t".join( line[:self.columnStart] ) + "\t"

      text = " ".join(line[self.columnStart:]).strip()
      for word in text.split():
        if( word not in stopWords ):
          newLine = newLine + word + " "
      print >> fout, newLine.strip()
    fout.close()

  def run(self,minWordLen,language):
    self.clean_text(minWordLen)
    self.generate_histogram(0.001)
    self.remove_stopwords(language)



if __name__ == '__main__':
  if( len(sys.argv) != 6 ):
    print sys.argv[0], " <inputFile> <outputPath> <textColumnStart> <minWordLen> <language>"
    sys.exit(1)

  pre = Preprocessor(sys.argv[1],sys.argv[2],int(sys.argv[3]))
  pre.run(int(sys.argv[4]),sys.argv[5])

