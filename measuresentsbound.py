from minhash import MinHash
from rabinkarp_serial import RabinKarpSerial
from rabinkarp_parallel import RabinKarpParallel
from preprocess import Preprocess

from multiprocessing import Process, Queue
from doc_handle import DocumentHandle
from minhash import MinHash
import time

def main():
	prk = RabinKarpParallel()
	doc = DocumentHandle()
	pp = Preprocess()

	similarity = 0

	textname, txt = doc.get_txt()

	filenames = doc.get_pat()
	# total file
	totaldoc = len(doc.get_pat())

	k = 3
	
	processes = []

	R = Queue()
	# lock = Lock()

	for i in range(1, totaldoc):
		start = time.time()


if __name__ == '__main__':
	main()