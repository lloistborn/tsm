from __future__ import division

from doc_handle import DocumentHandle

class RabinKarpParallel():
	q = 1079
	# d = 26
	doc = DocumentHandle()
		
	def sub_search(self, x, y, subpat, txt):
		pattern = subpat.split()
		# print '\npattern'
		# print pattern

		patlen = len(pattern)
		txtlen = len(txt)

		hashpat = 0
		hashtxt = 0

		# hash for pattern
		for i in range(0, patlen):
			hashpat = (hashpat + hash(pattern[i])) % self.q
			# print pattern[i]
			hashtxt = (hashtxt + hash(txt[i])) % self.q

		# hash for txt
		# print '[%d][%d]' %(x, y-patlen)
		# for i in range(x, x + patlen):
		# 	hashtxt = (hashtxt + hash(txt[i])) % self.q
						
		for i in range(0, txtlen - patlen + 1):
			if hashpat == hashtxt:
				for j in range(patlen):
					if txt[i + j] != pattern[j]:
						break
					if j == patlen - 1:
						# print 'sama'
						return 1
			# print 'if %d < %d stop' %(i, (y-patlen))  
			if i < txtlen - patlen:				
				hashtxt = ((hashtxt - hash(txt[i])) + hash(txt[i+patlen])) % self.q
		return 0

	def full_search(self, x, y, pat, txt):
		# print 'TEXT = %s ' %txt

		found = 0
		pattern = pat
		
		# for subpat in pattern:
		# 	# print 'PATTERN = %s' %subpat

		# 	if self.sub_search(x, y, subpat, txt):
		# 		found += 1

		for i in range(x, y - 4):
			# print 'index[%d] %s ' %(i, pattern[i])

			if self.sub_search(x, y, pattern[i], txt):
				found += 1

		# print found
		return found

	def sim(self, x, y, pat, txt, R):
		# l.acquire()

		intersect = 0
		similarity = 0
		# print txt
		
		txtlen = len(self.doc.wordshingling(txt))
		
		intersect = self.full_search(x, y, pat, txt)
		# print intersect
		
		similarity = 1 - ((txtlen - intersect) / txtlen)
		# print similarity

		R.put(similarity)

		# l.release()