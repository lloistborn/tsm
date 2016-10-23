
from rabinkarp_parallel import RabinKarpParallel

from multiprocessing import Process, Queue, Lock
from doc_handle import DocumentHandle
import sys

def main(lock):
	processes = []
	R = Queue()

	# number of threads
	k = 3

	prk = RabinKarpParallel()
	doc = DocumentHandle()

	# open name and content original document
	textname, txt = doc.get_txt()
	# print txt

	# open pattern name
	filenames = doc.get_pat()

	d = int((len(txt) - 5 + 1) / k + 1)

	for i in range(1, len(filenames)):
		# open pattern one by one through the loop
		patname = filenames[i].replace('\n', '')
		with open (patname, 'r') as pattern:
			pattern = pattern.read().replace('\n', ' ').replace('\t', ' ')

		pattern = pattern.split()
		# pattern = doc.wordshingling(pattern)

		# print pattern
		# print patname
		# print pattern

		for j in range(k - 1):
			p = Process(target=all_position, args=(lock, int(j * d), int((j+1) * d) + 5 - 1, pattern, txt, i, R,)) 
			processes.append(p)
			p.start()

		p = Process(target=all_position, args=(lock, int(d * (k-1)), len(txt) + 5 - 1, pattern, txt, i, R,)) 
		processes.append(p)
		p.start()



def all_position(l, x, y, pat, txt, i, R):
		l.acquire()
		print pat
		l.release()

if __name__ == '__main__':
	lock = Lock()
	main(lock)