import re, string
import scipy.sparse as spsp
from DictBase import split_by_non_alphabet 


class Querry():
	
	def __init__(self,startPoint,word_dict):
		self.startPoint=startPoint
		self.querry_dict={}  # querry: words   ex: 1: [31,233]
		self.word_dict=word_dict

	def readQuerry(self, filePath):
	 	f= open(filePath, "r") 
		modeLecture=False
		doc=""
		indexOld=-1
		indexNew=-1	
		for line in f:
			if line[0:2]==".I":
				tokens=line.split(" ")
				indexNew= int(tokens[1])
				if indexOld != -1:
					doc= split_by_non_alphabet(doc).lower()
					qry_words= doc.split()
					self.querry_dict[indexOld]=[self.word_dict[qry_word] for qry_word in qry_words if qry_word in self.word_dict]
				indexOld=indexNew
				doc=""
				modeLecture=False
				continue

			if line[0]!="." and modeLecture:
				doc+=" "+line
				continue

			if line[0:2] in self.startPoint:
				modeLecture=True
				continue
				
  		if (doc !=""):
			doc=split_by_non_alphabet(doc).lower()
			qry_words= doc.split()
			self.querry_dict[indexNew]=[self.word_dict[qry_word] for qry_word in qry_words if qry_word in self.word_dict]
		f.close()
