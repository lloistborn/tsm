import re

class EcsStemmer():

	def doStemming(self, words):
		result = []
		for word in words:
			if len(word) <= 3:
				result.append(word)

			elif self.is_rootword(word):
				result.append(word)

			# elif "-" in word:
			# 	hasil = self.hyphenatedword(word)
			# 	result.append(hasil)
		
			else:
				hasil = self.remove_inflection_suffixes(word)
				hasil = self.remove_derivation_suffixes(hasil)
				hasil = self.remove_derivation_prefixes(hasil)
				
				result.append(hasil)
				
		return result

		# word = words
		# if len(word) <= 3:
		# 		return word

		# elif self.is_rootword(word):
		# 	return word

		# 	# elif "-" in word:
		# 	# 	hasil = self.hyphenatedword(word)
		# 	# 	result.append(hasil)
		
		# else:
		# 	hasil = self.remove_inflection_suffixes(word)
		# 	hasil = self.remove_derivation_suffixes(hasil)
		# 	hasil = self.remove_derivation_prefixes(hasil)

		# 	return hasil

		# return words


	def is_rootword(self, word):
		handle = open('E:\\Workspace\\corpus\\rootwordkbbi.txt', 'r')
		var = handle.read()
		handle.close()
		LIST_ROOTWORD = var.split()
		if word in LIST_ROOTWORD:
			return True
		else:
			return False

		return result

	# /* check the Rule Precedence
	# * combination of Prefix and Suffix
	# * "be-lah" "be-an" "me-i" "di-i" "pe-i" or "te-i"
	# */
	def is_rule_precedence(self, word):
		if re.search(r"^(be)([A-Za-z\-]+)(lah|an)$", word):
			return 1
		if re.search(r"^(di|[mpt]e)([A-Za-z\-]+)(i)$", word):
			return 1
		return 0

	# /* check Disallowed Prefix-Suffix Combinations
	# * "be-i" . "di-an" . "ke-i|kan" . "me-an" . "se-i|kan" or "te-an"
	# * **/
	def is_disallowed_prefix_suffixes(self, word):
		if re.search(r"^(be)([A-Za-z\-]+)(i)$", word):
			return 1
		if re.search(r"^(di)([A-Za-z\-]+)(an)$", word):
			return 1
		if re.search(r"^(ke)([A-Za-z\-]+)(i|kan)$", word):
			return 1
		if re.search(r"^(me)([A-Za-z\-]+)(an)$", word):
			return 1
		if re.search(r"^(se)([A-Za-z\-]+)(i|kan)$", word):
			return 1
		if re.search(r"^(te)([A-Za-z\-]+)(an)$", word):
			return 1
		return 0

	# /* remove Inflection Suffixes, 
	# * 1. Particle "-lah" "-kah" "-tah" and "-pun" 
	# * 2. Possesive Pronoun "-ku" "-mu" "-nya"
	# */
	def remove_inflection_suffixes(self, word):
		baseWord = word
		if re.search(r"([klt]ah|pun|[km]u|nya)$", word):
			infSuf = re.sub(r"([klt]ah|pun|[km]u|nya)$", "", word)
			if re.search(r"([klt]ah|pun)$", word):
				if re.search(r"([km]u|nya)$", word):
					posPron = re.sub(r"([km]u|nya)$", "", infSuf)
					return posPron
			return infSuf
		return baseWord

	# /* remove Derivation Suffixes
	# * "-i" . "-kan" . "-an"
	# * **/
	def remove_derivation_suffixes(self, word):
		baseWord = word

		if re.search(r"(kan)$", word):
			baseWord = re.sub(r"(kan)$", "", word)
			if self.is_rootword(baseWord):
				return baseWord

		if re.search(r"(an|i)$", word):
			baseWord = re.sub(r"(an|i)$", "", word)
			if self.is_rootword(baseWord):
				return baseWord

		if self.is_disallowed_prefix_suffixes(baseWord):
			return word

		return word

	# /* remove Derivation Prefixes
	# * "di-" . "ke-" . "se-" . "me-" . "be-" . "pe-" or "te-"
	# * */
	def remove_derivation_prefixes(self, word):
		baseWord = word
		strRemovedDerivSuff = ""
		strRemovedStdPref = ""
		strRemovedCmplxPref = ""

		# /************** check Standard Prefix "di-" . "ke-" . "se-" **************/
		if re.search(r"^(di|[ks]e)\S{1,}", word):
			strRemovedStdPref = re.sub(r"^(di|[ks]e)", "", word)
			if self.is_rootword(strRemovedStdPref):
				return strRemovedStdPref

			strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedStdPref)
			if self.is_rootword(strRemovedDerivSuff):
				return strRemovedDerivSuff

		# /* rule 35 */
		if re.search(r"^([^aiueo])e\1[aiueo]\S{1,}", word):
			prefixes = re.sub(r"^([^aiueo])e", "", word)
			if self.is_rootword(prefixes):
				return prefixes

			strRemovedDerivSuff = self.remove_derivation_suffixes(prefixes)
			if self.is_rootword(strRemovedDerivSuff):
				return strRemovedDerivSuff

		# /************** check Complex Prefixes "te-"."me-"."be-"."pe-" **************/
		if re.search(r"^([tmbp]e)\S{1,}", word):
			# /************** Prefix "be-" **************/
			if re.search(r"^(be)\S{1,}", word):
				# /* if prefix "be-" */
				if re.search(r"^(ber)[aiueo]\S{1,}", word):
					# /* rule 1 */
					strRemovedCmplxPref = re.sub(r"^(ber)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

					strRemovedCmplxPref = re.sub(r"^(ber)", "r", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(ber)[^aiueor]([A-Za-z\-]+)(?!er)\S{1,}", word):
					# /* rule 2 */
					strRemovedCmplxPref = re.sub(r"^(ber)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(ber)[^aiueor]([A-Za-z\-]+)er[aiueo]\S{1,}", word):
					# /* rule 3 */
					strRemovedCmplxPref = re.sub(r"^(ber)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^belajar\S{0,}", word):
					# /* rule 4 */
					strRemovedCmplxPref = re.sub(r"^(bel)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(be)[^aiueolr]er[^aiueo]\S{1,}", word):
					# /* rule 5 */
					strRemovedCmplxPref = re.sub(r"^(be)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff
			# /************** end Prefix "be-" **************/

			# /************** Prefix "te-" **************/
			if re.search(r"^(te)\S{1,}", word):
				if re.search(r"^(terr)\S{1,}", word):
					return word

				if re.search(r"^(ter)[aiueo]\S{1,}", word):
					# /* rule 6 */
					strRemovedCmplxPref = re.sub(r"^(ter)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedDerivSuf

					strRemovedCmplxPref = re.sub(r"^(ter)", "r", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(ter)[^aiueor]er[aiueo]\S{1,}", word):
					# /* rule 7 */
					strRemovedCmplxPref = re.sub(r"^(ter)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(ter)[^aiueor](?!er)\S{1,}", word):
					# /* rule 8 */
					strRemovedCmplxPref = re.sub(r"^(ter)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(te)[^aiueor]er[aiueo]\S{1,}", word):
					# /* rule 9 */
					strRemovedCmplxPref = re.sub(r"^(te)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(ter)[^aiueor]er[^aiueo]\S{1,}", word):
					# /* rule 35 */
					strRemovedCmplxPref = re.sub(r"^(ter)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff
			# /************** end Prefix "te-" **************/

			# /************** Prefix "me-" **************/
			if re.search(r"^(me)\S{1,}",word):
				if re.search(r"^(me)[lrwyv][aiueo]",word):
					# /* rule 10 */
					strRemovedCmplxPref = re.sub(r"^(me)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(mem)[bfvp]\S{1,}",word):
					# /* rule 11 */
					strRemovedCmplxPref = re.sub(r"^(mem)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				# # rule 12
				# if re.search(r"^(mempe)[rl]\S{1,}", word):
				# 	strRemovedCmplxPref = re.sub(r"^(mem)", "", word)
				# 	if self.is_rootword(strRemovedCmplxPref):
				# 		return strRemovedCmplxPref
				# 	strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
				# 	if self.is_rootword(strRemovedDerivSuff):
				# 		return strRemovedDerivSuff

				# modified rules, cause ecs cannot stem any of these words
				# memperhatikan with affix memper- hati -kan
				if re.search(r"^(memper)[^aiueor]\S{1,}", word):
					strRemovedCmplxPref = re.sub(r"^(memper)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref
					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(mem)((r[aiueo])|[aiueo])\S{1,}", word):
					# /* rule 13 */
					strRemovedCmplxPref = re.sub(r"^(mem)", "m", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

					strRemovedCmplxPref = re.sub(r"^(mem)", "p", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(men)[cdjszt]\S{1,}", word):
					# /* rule 14 */
					strRemovedCmplxPref = re.sub(r"^(men)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(men)[aiueo]\S{1,}", word):
					# /* rule 15 */
					strRemovedCmplxPref = re.sub(r"^(men)", "n", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

					strRemovedCmplxPref = re.sub(r"^(men)", "t", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(meng)[ghqk]\S{1,}", word):
				   # /* rule 16 */
					strRemovedCmplxPref = re.sub(r"^(meng)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(meng)[aiueo]\S{1,}", word):
				   # /* rule 17 */
					strRemovedCmplxPref = re.sub(r"^(meng)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

					strRemovedCmplxPref = re.sub(r"^(meng)", "k", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

					strRemovedCmplxPref = re.sub(r"^(menge)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(meny)[aiueo]\S{1,}", word):
					# /* rule 18 */
					strRemovedCmplxPref = re.sub(r"^(meny)", "s", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

					strRemovedCmplxPref = re.sub(r"^(me)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff
			# /************** end Prefix "me-" **************/

			# /************** Prefix "pe-" **************/
			if re.search(r"^(pe)\S{1,}", word):
				if re.search(r"^(pe)[wy]\S{1,}", word):
				   # /* rule 20 */
					strRemovedCmplxPref = re.sub(r"^(pe)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(per)[aiueo]\S{1,}", word):
					# /* rule 21 */
					strRemovedCmplxPref = re.sub(r"^(per)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

					strRemovedCmplxPref = re.sub(r"^(per)", "r", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(per)[^aiueor]([A-Za-z\-]+)(?!er)\S{1,}", word):
					# /* rule 23 */
					strRemovedCmplxPref = re.sub(r"^(per)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(per)[^aiueo]([A-Za-z\-]+)(er)[aiueo]\S{1,}", word):
					# /* rule 24 */
					strRemovedCmplxPref = re.sub(r"^(per)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(pem)[bfv]\S{1,}", word):
					# /* rule 25 */
					strRemovedCmplxPref = re.sub(r"^(pem)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(pem)(r[aiueo]|[aiueo])\S{1,}", word):
					# /* rule 26 */
					strRemovedCmplxPref = re.sub(r"^(pem)", "m", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

					strRemovedCmplxPref = re.sub(r"^(pem)", "p", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(pen)[cdjzt]\S{1,}", word):
					# /* rule 27 */
					strRemovedCmplxPref = re.sub(r"^(pen)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(pen)[aiueo]\S{1,}", word):
					# /* rule 28 */
					strRemovedCmplxPref = re.sub(r"^(pen)", "n", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

					strRemovedCmplxPref = re.sub(r"^(pen)", "t", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(peng)[^ghq]\S{1,}", word):
					# /* rule 29 */
					strRemovedCmplxPref = re.sub(r"^(peng)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(peng)[aiueo]\S{1,}", word):
					# /* rule 30 */
					strRemovedCmplxPref = re.sub(r"^(peng)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

					strRemovedCmplxPref = re.sub(r"^(peng)", "k", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

					strRemovedCmplxPref = re.sub(r"^(penge)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(peny)[aiueo]\S{1,}", word):
					# /* rule 31 */
					strRemovedCmplxPref = re.sub(r"^(peny)", "s", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

					strRemovedCmplxPref = re.sub(r"^(pe)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(pel)[aiueo]\S{1,}", word):
					# /* rule 32 */
					strRemovedCmplxPref = re.sub(r"^(pel)", "l", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(pelajar)\S{0,}", word):
					strRemovedCmplxPref = re.sub(r"^(pel)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(pe)[^rwylmn]er[aiueo]\S{1,}", word):
					# /* rule 33 */
					strRemovedCmplxPref = re.sub(r"^(pe)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(pe)[^rwylmn](?!er)\S{1,}", word):
					# /* rule 34 */
					strRemovedCmplxPref = re.sub(r"^(pe)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff

				if re.search(r"^(pe)[^aiueor]er[^aiueo]\S{1,}", word):
					# /* rule 36 */
					strRemovedCmplxPref = re.sub(r"^(pe)", "", word)
					if self.is_rootword(strRemovedCmplxPref):
						return strRemovedCmplxPref

					strRemovedDerivSuff = self.remove_derivation_suffixes(strRemovedCmplxPref)
					if self.is_rootword(strRemovedDerivSuff):
						return strRemovedDerivSuff
			# /************** end Prefix "pe-" **************/

		return baseWord