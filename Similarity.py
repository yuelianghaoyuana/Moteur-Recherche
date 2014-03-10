import math
#from numpy import linalg as LA
import numpy as np
import time
from sys import maxint

class similarity():

	def __init__(self, dictBase, querry_dict, ind):
		self.tf_mat= dictBase.tf_mat
		self.idf_list=dictBase.idf_list
		self.word_dict= dictBase.word_dict
		self.querry_dict= querry_dict
		self.doc_word_dict=dictBase.doc_word_dict
		self.df_list=dictBase.df_list
		self.doc_pos_dict=dictBase.doc_pos_dict
		if ind==5:
			self.fill_docLength_dict()
		if ind==6:
			self.fill_docLength_dict()
			self.fill_p_collection()
		if ind==7: #BM25
			self.fill_docLength_dict()
			self.fill_probaIdf()
			self.Lmoy= np.mean(self.docLength_dict.values())





	
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
				if ind_doc not in doc_tf:
					doc_tf[ind_doc]=[]
					doc_idf[ind_doc]=[]
				doc_tf[ind_doc].append(self.tf(ind_word,ind_doc))
				doc_idf[ind_doc].append(self.idf(ind_word))					

		for ind_doc in doc_tf:
			doc_score[ind_doc]= np.dot(doc_tf[ind_doc],doc_idf[ind_doc])/np.linalg.norm(doc_tf[ind_doc])/np.linalg.norm(doc_idf[ind_doc])

		return doc_score
			
	def cosinus_log(self,ind_querry):
		doc_tf={}
		doc_idf={}
		doc_score={}
		
		for ind_word in self.querry_dict[ind_querry]:
			for ind_doc in self.tf_mat[ind_word]:
				if ind_doc not in doc_tf:
					doc_tf[ind_doc]=[]
					doc_idf[ind_doc]=[]
				doc_tf[ind_doc].append(1+math.log(self.tf(ind_word,ind_doc)))
				doc_idf[ind_doc].append(self.idf(ind_word))

		for ind_doc in doc_tf:
			doc_score[ind_doc]= np.dot(doc_tf[ind_doc],doc_idf[ind_doc])/np.linalg.norm(doc_tf[ind_doc])/np.linalg.norm(doc_idf[ind_doc])
		return doc_score

	def langue(self,ind_querry):
		doc_score={}
		for ind_word in self.querry_dict[ind_querry]:
			for ind_doc in self.tf_mat[ind_word]:
				if ind_doc in doc_score:
					doc_score[ind_doc]+= math.log(self.tf(ind_word, ind_doc)/float(self.docLength_dict[ind_doc]))
				else:
					doc_score[ind_doc]= math.log(self.tf(ind_word, ind_doc)/float(self.docLength_dict[ind_doc]))
		return doc_score

	def langue_corr(self,ind_querry):
		doc_score={}
		mu=0.5
		for ind_word in self.querry_dict[ind_querry]:
			for ind_doc in self.tf_mat[ind_word]:
				to_add=math.log( (self.tf(ind_word, ind_doc)+mu*self.p_collection_list[ind_word]) /float( (self.docLength_dict[ind_doc]+mu)) )
				if ind_doc in doc_score:
					doc_score[ind_doc]+= to_add
				else:
					doc_score[ind_doc]= to_add
		return doc_score



	def fill_docLength_dict(self):
		doc_size=len(self.doc_word_dict)
		docLength_list=[0]*doc_size
		self.docLength_dict={}
		for ind_word in self.tf_mat:
			for ind_doc in self.tf_mat[ind_word]:
				docLength_list[self.doc_pos_dict[ind_doc]]+=self.tf_mat[ind_word][ind_doc]
		
		for ind_doc in self.doc_word_dict:
			self.docLength_dict[ind_doc]= docLength_list[self.doc_pos_dict[ind_doc]]
		# print self.docLength_dict






	def fill_p_collection(self):
		word_size=len(self.word_dict)
		word_freq_list=[]
		total_freq=0
		for ind_word in xrange(word_size):
			word_freq=sum(self.tf_mat[ind_word].itervalues())
			total_freq+= word_freq
			word_freq_list.append(word_freq)

		self.p_collection_list= np.array(word_freq_list)/float(total_freq)


	def fill_probaIdf(self):
		word_size=len(self.word_dict)
		doc_size=len(self.doc_word_dict)
		self.probaIdf_list=[]
		for ind_word in xrange(word_size):
			self.probaIdf_list.append(self.func_probaIdf( self.df_list[ind_word],doc_size))


	def BM25(self,ind_querry):
		k1=1
		b=0.75
		
		doc_score={}
		for ind_word in self.querry_dict[ind_querry]:
			for ind_doc in self.tf_mat[ind_word]:
				tmp_tf=self.tf(ind_word,ind_doc)
				to_add= self.probaIdf_list[ind_word]*( (k1+1)*tmp_tf 
					/(k1*((1-b)+b*self.docLength_dict[ind_doc]/self.Lmoy)+tmp_tf)) 
				if ind_doc in doc_score:
					doc_score[ind_doc]+= to_add
				else:
					doc_score[ind_doc]= to_add
		return doc_score



	def func_probaIdf(self, tf_t, doc_size):
		return max(0, math.log(  (doc_size-tf_t+0.5)/(tf_t+0.5) ))