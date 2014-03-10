import math
#from numpy import linalg as LA
import numpy as np
import time
from sys import maxint

class similarity():

	def __init__(self, dictBase, querry_dict):
		self.tf_mat= dictBase.tf_mat
		self.idf_list=dictBase.idf_list
		self.word_dict= dictBase.word_dict
		self.querry_dict= querry_dict
		self.doc_word_dict=dictBase.doc_word_dict
	
	def tf(self,ind_word, ind_doc):
		return self.tf_mat[ind_word][ind_doc]
		
	# def df(self,ind_word):
	# 	return len(self.tf_mat[ind_word])
		
	def idf(self,ind_word):
		return self.idf_list[ind_word]
		

	def product(self, ind_querry):
		doc_score={}
		for ind_word in self.querry_dict[ind_querry]:
			for ind_doc in self.tf_mat[ind_word]:
				if ind_doc in doc_score:
					doc_score[ind_doc]+= self.tf(ind_word, ind_doc)*self.idf(ind_word)
				else:
					doc_score[ind_doc]=self.tf(ind_word, ind_doc)*self.idf(ind_word)
		return doc_score
	

	def product_log(self,ind_querry):
		doc_score={}
		for ind_word in self.querry_dict[ind_querry]:
			for ind_doc in self.tf_mat[ind_word]:
				if ind_doc in doc_score:
					doc_score[ind_doc]+= (1+math.log(self.tf(ind_word, ind_doc))) * self.idf(ind_word)
				else:
					doc_score[ind_doc]= (1+math.log(self.tf(ind_word, ind_doc))) * self.idf(ind_word)
		return doc_score

	def cosinus(self,ind_querry):
		doc_tf={}
		doc_idf={}
		doc_score={}
		
		for ind_word in self.querry_dict[ind_querry]:
			for ind_doc in self.tf_mat[ind_word]:
				if ind_doc in doc_tf:
					doc_tf[ind_doc].append(self.tf(ind_word,ind_doc))
					doc_idf[ind_doc].append(self.idf(ind_word))
				else:
					doc_tf[ind_doc]=[]
					doc_idf[ind_doc]=[]
					doc_tf[ind_doc].append(self.tf(ind_word,ind_doc))
					doc_idf[ind_doc].append(self.idf(ind_word))
			
	def cosinus_log(self,ind_querry, ind_doc):
		sum=0.0
		tmpTF=[]
		tmpIDF=[]
		for word in self.querry_dict[ind_querry]:
			tmpTF= self.tf(word, ind_doc)
			if (tmpTF>0):
				w1=	(1+math.log(tmpTF))
				w2=	self.idf(word)
				sum+=w1*w2
				tmpTF.append(w1)
				tmpIDF.append(w2)
		return sum/LA.norm(tmpTF)/LA.norm(tmpIDF)
