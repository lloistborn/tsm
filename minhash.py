from __future__ import division
import mmh3

class MinHash():
	MIN_HASH_VALUE = 2 ** 128
	k = 2 ** 10

	def min_hash(self, words, seed):
		min_hash_word = None
		min_hash_value = self.MIN_HASH_VALUE

		for word in words:
			hash_ = mmh3.hash128(word, seed)

			if hash_ < min_hash_value:
				min_hash_word = word
				min_hash_value = hash_

		return min_hash_word

	def get_score(self, txtshingle, patshingle):
		splitpat = patshingle
		splittxt = txtshingle

		num_match = 0

		for seed in xrange(self.k):
			if self.min_hash(splittxt, seed) == self.min_hash(splitpat, seed):
				num_match += 1

		return num_match / self.k


