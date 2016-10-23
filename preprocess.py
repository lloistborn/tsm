import re
import string
from ecsstemmer import EcsStemmer

class Preprocess():
	DELIMETERS = "\"", "\'", "{", "}", "(", ")", "[", "]", ">", "<", "_", "=", "+", "|", "\\", ":", ";", " ", ",", ".", "/", "?", "~", "!", "@", "#", "$", "%", "^", "&", "*", "\r", "\n", "\t", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
	ecs = EcsStemmer()

	def prep_text(self, text):
		texts = self.tokenizing(text)
		texts = self.stopwordremoval(texts)
		texts = self.ecs.doStemming(texts)

		return texts

	# tokenizing, casefolding(lowercase)z
	def tokenizing(self, text):
		regexPattern = '|'.join(map(re.escape, self.DELIMETERS))
		texts = re.split(regexPattern, text.lower())
		return texts
		# exclude = set(string.punctuation)
		# return ''.join(x.lower() for x in text if x not in exclude)

	# removing stopword
	def stopwordremoval(self, text):
		handle = open('E:\\Workspace\\corpus\\stopwords.txt', 'r+')
		var = handle.read()
		handle.close()

		LIST_STOP_WORD = var.split()

		result = []
		# result = list(set(text).difference(set(LIST_STOP_WORD)))

		for txt in text:
			if txt:
				if txt not in LIST_STOP_WORD:
					result.append(txt)

		return result