from preprocess import Preprocess

class DocumentHandle():
	path = 'E:\\Workspace\\python\\sim_measure\\filenames.txt'
	files = open(path).readlines()

	def wordshingling(self, word):
		shingle = []

		for i in range(0, len(word) - 4):
			shingle.append(word[i] + " " + word[i + 1] + " " + word[i + 2] + " " + word[i + 3] + " " + word[i + 4])
			
		return shingle

	def get_pat(self):
		# open many files
		return self.files

	def get_txt(self):
		pp = Preprocess()
		# open doc original
		filename = self.files[0].replace('\n', '')
		# print filename
		with open (filename, 'r') as txt:
			txt = txt.read().replace('\n', ' ').replace('\r', ' ')
			txt = pp.prep_text(txt)
		
		return ((filename, txt))