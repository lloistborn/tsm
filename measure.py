from minhash import MinHash
from rabinkarp_serial import RabinKarpSerial
from rabinkarp_parallel import RabinKarpParallel
from preprocess import Preprocess

from multiprocessing import Process, Queue
from doc_handle import DocumentHandle
from minhash import MinHash
import time

def main():
	rk = RabinKarpSerial()
	prk = RabinKarpParallel()
	doc = DocumentHandle()
	mh = MinHash()
	pp = Preprocess()

	similarity = 0

	# get textname and content original document
	textname, txt = doc.get_txt()	

	# get filepattern name
	filenames = doc.get_pat()
	# total file
	totaldoc = len(doc.get_pat())

# ---------------------------------------------------------------------------------------------------

	print 'RABIN KARP SERIAL'
	for i in range(1, totaldoc):
		start = time.time()
		patname = filenames[i].replace('\n', '')
		with open (patname, 'r') as pattern:
			pattern = pattern.read().replace('\n', ' ').replace('\r', ' ')
		
		pattern = pp.prep_text(pattern)		
		pattern = doc.wordshingling(pattern)
		
		# similarity measure by Rabin Karp Serial
		similarity = rk.sim(txt, pattern)

		end = time.time()
		print 'sim(%s, %s)= %.4f on %.4f second' %(textname, patname, similarity, (end-start))
	# 	similarity = 0
# -----------------------------------------------------------------------------------------------------

	print 'RABIN KARP PARALLEL'
	# define number of thread
	k = 3
	
	processes = []

	R = Queue()
	# lock = Lock()

	for i in range(1, totaldoc):
		start = time.time()
		
		# open the pattern one by one through the loop
		patname = filenames[i].replace('\n', '')
		with open (patname, 'r') as pattern:
			pattern = pattern.read().replace('\n', ' ').replace('\t', ' ')

		pattern = pp.prep_text(pattern)
		patlen = len(pattern)
		# 5 is length of pattern
		d = int((patlen - 5 + 1) / k+1)
		
		pattern = doc.wordshingling(pattern)

		# print patname
		# print pattern

		for j in range(k - 1):
			# print '[%d][%d]' %(int(d * j), int((j + 1) * d) + 5 - 1)
			p = Process(target=prk.sim, args=(int(d * j), int((j+1) * d) + 5 - 1, pattern, txt, R,)) 
			processes.append(p)
			p.start()


		# print '[%d][%d]' %(int(d * (k-1)), patlen)
		p = Process(target=prk.sim, args=(int(d * (k-1)), patlen, pattern, txt, R,)) 
		processes.append(p)
		p.start()

		for pr in processes:
			pr.join()

		while not R.empty():
			similarity += R.get()
			# print similarity

		end = time.time()
		print "sim(%s, %s) = %.4f on %.4f" %(textname, patname, similarity, (end-start))
		
		# refresh similarity
		similarity = 0
		
#----------------------------------------------------------------------------------------------------- 

	print 'MINHASH'
	txt = doc.wordshingling(txt)

	for i in range(1, totaldoc):
		start = time.time()

		patname = filenames[i].replace('\n', '')
		
		with open (patname, 'r') as pattern:
			pattern = pattern.read().replace('\n', ' ').replace('\r', ' ')
		
		# pattern = pattern.split()		
		
		pattern = pp.prep_text(pattern)
		# singling pattern
		pattern = doc.wordshingling(pattern)
	
		# similarity measure by MinHash
		similarity = mh.get_score(txt, pattern)

		end = time.time()
		print 'sim(%s, %s)= %.4f on %.4f second' %(textname, patname, similarity, (end-start))

if __name__ == '__main__':
	main()