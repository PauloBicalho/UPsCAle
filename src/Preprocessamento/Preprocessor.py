
class Preprocessor:
  cleanedFile = None
  uniqFile = None
  histogram = None
  finalFile = None


  def Preprocessor(self, inFile, outPath)

  def clean_text(self)

  def remove_duplicates(self)

  def generate_histogram(self)

  def remove_stopwords(self)

  def save_file(self, out)

  def save_files(self)
  

  def run(self):
    currentFile = self.clean_text(currentFile)
    currentFile = self.remove_duplicates(currentFile)
    currentFile = self.generate_histogram(currentFile)
    currentFile = self.remove_stopwords(currentFile)

    self.save_files()


if __name__ == '__main__':
  pass

