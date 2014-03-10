from Similarity import *
import numpy as np
import operator

class Evaluation():
	def __init__(self, DictBase, DictRelevant,outSize,sim_func):
		self.index_of_qry= DictRelevant.dict_Rel.keys()
		self.index_of_doc= DictBase.doc_word_dict.keys()
		self.dict_Rel=DictRelevant.dict_Rel
		self.outSize=outSize  #output how many result, -1:output all
		self.res_dict={}
		self.sim_func=sim_func
	

	#get the relevant documents list of a querry
	def get_RelDoc_list(self, ind_qry, dict_Rel):	
		res_sim= self.sim_func(ind_qry)  #a dict with doc: score
		mr_res=[i[0] for i in sorted(res_sim.iteritems(), key=operator.itemgetter(1), reverse=True)] #sorted mr result

		if (self.outSize==-1) or (len(mr_res)< self.outSize):
			return mr_res
		else:
			return mr_res[0:(self.outSize-1)]

	def get_relative_ind(self, ind_qry, mr_res):

		rel_doc= self.dict_Rel[ind_qry]
		'''
		ind_relevant stock the relative index in the doc list
		'''
		ind_relevant=[]
		show=[]
		for i in range(len(mr_res)):
			if mr_res[i] in rel_doc:
				show.append(mr_res[i])
				ind_relevant.append(i)

		'''
		important:
		'''
		# if ind_qry==1:
		# 	print len(ind_relevant),ind_relevant
		# 	print show			
		return ind_relevant


	def avg_prec(self, ind_relevant, all_relDoc_size):
		sum=0.0
		count=0
		for i in  ind_relevant:
			count+=1
			sum+= count/ float(i+1)
										
		avg= sum/ float(all_relDoc_size)
		return avg



	def mean_avg_prec(self):
		sum=0.0
		for ind_qry in self.index_of_qry:
			mr_res= self.get_RelDoc_list(ind_qry, self.dict_Rel)
			ind_relevant= self.get_relative_ind(ind_qry, mr_res)
			all_relDoc_size=len(self.dict_Rel[ind_qry])
			sum+= self.avg_prec(ind_relevant, all_relDoc_size)
			self.res_dict[ind_qry]= ind_relevant
		return sum/ float(len(self.index_of_qry))
				







