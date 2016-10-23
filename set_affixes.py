from ecsstemmer import EcsStemmer
import re
import random

def stopwordremoval(text):
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

def tokenizing(text):
		DELIMETERS = "\"", "\'", "{", "}", "(", ")", "[", "]", ">", "<", "_", "=", "+", "|", "\\", ":", ";", " ", ",", ".", "/", "?", "~", "!", "@", "#", "$", "%", "^", "&", "*", "\r", "\n", "\t", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
	
		regexPattern = '|'.join(map(re.escape, DELIMETERS))
		texts = re.split(regexPattern, text.lower())
		return texts

def main():
	pp = EcsStemmer()

	path = 'E:\\Workspace\\python\\sim_measure\\basedoc.txt'
	content = open(path, 'r').read()
	# content.close()

	# create affix----------------------------------------------------------
	listcontent = tokenizing(content)
	listcontent = stopwordremoval(listcontent)

	handle = open('E:\\Workspace\\python\\sim_measure\\doc_original.txt', 'w')
	
	for item in listcontent:
		handle.write('%s\n' %item)
	handle.close()

	num_iter = int(0.1 * len(listcontent))

	result = []
	temp = ''
	i = 0

	for word in listcontent:
		if i < num_iter:
			temp = pp.doStemming(word)

			if temp != word:
				i+=1

			result.append(temp)
		else:
			result.append(word) 

	handle = open('E:\\Workspace\\python\\sim_measure\\doc_affixes.txt', 'w')
	# print content
	for item in result:
		handle.write('%s\n' %item)
	handle.close()

	# # create data set modification 20%, 40%, 60%, 80%-----------------------------
	# listcontent = tokenizing(content)

	# # document 20%
	# contenttodelet = int(0.8 * len(listcontent))

	# print len(listcontent)
	# print contenttodelet

	# temp = []

	# n = range(len(listcontent))
	# randnum = random.sample(n, contenttodelet)
	# # len(randnum)

	# for i in randnum:
	# 	# print i
	# 	# print listcontent[int(i)]
	# 	temp.append(listcontent[int(i)])


	# for i in range(len(temp)):
	# 	if temp[i] in listcontent:
	# 		listcontent.remove(temp[i])


	# handle = open('E:\\Workspace\\python\\sim_measure\\mod80.txt', 'w')
	# # print content
	# for item in listcontent:
	# 	handle.write('%s\n' %item)
	
	# handle.close()



if __name__ == '__main__':
	main()
	print 'completed'