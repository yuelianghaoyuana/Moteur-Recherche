import math
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
		self.doc_pos_dict=dictBase.doc_pos_dict
	
	def tf(self,ind_word, ind_doc):
		return self.tf_mat[ind_word][ind_doc]
		
	def idf(self,ind_word):
		return self.idf_list[ind_word]
	
	def productM(self, ind_querry):
		sim_array= np.zeros(len(self.doc_word_dict))

		for ind_word in self.querry_dict[ind_querry]:
			for ind_doc in self.tf_mat[ind_word]:
				sim_array[self.doc_pos_dict[ind_doc]]+= self.tf(ind_word, ind_doc)*self.idf(ind_word)

		ind_doc_kept=find_non_zeros(sim_array)
		return get_doc_score(ind_doc_kept,sim_array)
	

	def product_log(self,ind_querry):
		sim_array= np.zeros(len(self.doc_word_dict))
		for ind_word in self.querry_dict[ind_querry]:
			for ind_doc in self.tf_mat[ind_word]:
				sim_array[self.doc_pos_dict[ind_doc]]+=(1+math.log(self.tf(ind_word, ind_doc))) * self.idf(ind_word)
		ind_doc_kept=find_non_zeros(sim_array)
		return get_doc_score(ind_doc_kept,sim_array)

	def cosinusM(self,ind_querry):
		print "in here::::::::"
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
					doc_tf.append(self.tf(ind_word,ind_doc))
					doc_idf.append(self.idf(ind_word))

		for ind_doc in doc_tf:
			doc_score[ind_doc]= np.dot(doc_tf[ind_doc],doc_idf[ind_doc])/np.linalg.norm(doc_tf[ind_doc])/np.linalg.norm(doc_idf[ind_doc])
		print doc_score
		return doc_score

	#return the index of document which score !=0
def find_non_zeros(sim_array):
	return list(np.where(sim_array!=0)[0]+1)

	#create a dict: doc:score
def get_doc_score(ind_doc_kept, sim_array):
	doc_score={}
	for ind_doc in ind_doc_kept:
		doc_score[ind_doc]=sim_array[ind_doc-1]
	return doc_score