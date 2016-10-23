from __future__ import division

class RabinKarpSerial():
	q = 1079

	def wordshingling(self, word):
		shingle = []

		for i in range(0, len(word) - 4):
			shingle.append(word[i] + " " + word[i + 1] + " " + word[i + 2] + " " + word[i + 3] + " " + word[i + 4])
		
		return shingle

	def sub_search(self, txt, pat):
		pattern = pat.split()
		
		patlen = len(pattern)
		txtlen = len(txt)
		
		num_iterations = txtlen - patlen + 1

		hashpat = 0
		hashtxt = 0

		for i in range(0, patlen):
			hashpat = (hashpat + hash(pattern[i])) % self.q
			hashtxt = (hashtxt + hash(txt[i])) % self.q

		for i in range(0, num_iterations):
			# if the hash value is different then it's posible that they are a different string
			if hashpat == hashtxt:
				for j in range(0, patlen):
					if txt[i + j] != pattern[j]:
						break
					if j == patlen - 1:
						return 1
			
			if i < txtlen - patlen:
				hashtxt = ((hashtxt - hash(txt[i])) + hash(txt[i+patlen])) % self.q
		return 0

	def full_search(self, text, pat):
		found = 0
		splitpat = pat
		
		for subpat in splitpat:
			if self.sub_search(text, subpat):
				found += 1

		return found

	def sim(self, txt, pat):
		txtlen = len(self.wordshingling(txt))
		intersect = 0

		intersect = self.full_search(txt, pat)

		return 1 - ((txtlen - intersect) / txtlen)