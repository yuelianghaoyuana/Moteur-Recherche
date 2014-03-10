import re, string
import scipy.sparse as spsp
import math

class DictBase():
	def __init__(self, startPoint):
		self.startPoint= startPoint
		self.doc_word_dict={}  # article: words list
		self.word_dict={} # word: index
		self.doc_pos_dict={}  #position of doc: 1:0 2:1 
		#self.idf_list   word: idf
		#self.tf_mat

		
		


	def readDoc(self, filePath):
	 	f= open(filePath, "r")
		modeLecture=False
		doc=""
		indexOld=-1
		indexNew=-1
		count=0
		for line in f:
			if line[0:2]==".I":
				tokens=line.split(" ")
				indexNew= int(tokens[1])
				if indexOld != -1:
					doc= split_by_non_alphabet(doc).lower()
					self.doc_word_dict[indexOld]=doc.split()
					self.doc_pos_dict[indexOld]=count
					count+=1
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
			if line[0]==".":
				modeLecture=False
				continue
  		if (doc !=""):
			doc=split_by_non_alphabet(doc).lower()
			self.doc_word_dict[indexNew]= doc.split()
			self.doc_pos_dict[indexNew]=count
		f.close()


	def drop_commonWords(self,file_commonWords):
		f=open(file_commonWords,'r')
		#~ commonWords=f.read().replace('\n',' ').split()
		commonWords=[]
		for line in f:
			commonWords.append(line.replace('\n',''))
		
		for index, doc in self.doc_word_dict.items(): 
			new=[word for word in doc if word not in commonWords]
			self.doc_word_dict[index]= new
	
	def fill_word_dict(self):
		#create the list of all words possible
		set_word=set()
		for index, doc in self.doc_word_dict.items():
			set_word= set_word.union(set(doc))

		ind=0
		for word in set_word:
			self.word_dict[word]=ind
			ind+=1
		# t1: { D1: f1, D2: f2}
		self.tf_mat={}
		for ind_doc, doc in self.doc_word_dict.items():
			for word in doc:
				ind_word=self.word_dict[word]
				if ind_word not in self.tf_mat:
					self.tf_mat[ind_word]={}
					self.tf_mat[ind_word][ind_doc]=1
				else:
					if ind_doc not in self.tf_mat[ind_word]:
						self.tf_mat[ind_word][ind_doc]=1
					else:
						self.tf_mat[ind_word][ind_doc]+=1
		#print self.tf_mat[9831]
		

	def fill_idf_list(self):
		word_size=len(self.word_dict)
		doc_size=len(self.doc_word_dict)
		self.idf_list=[0.0]*word_size
		self.df_list=[0.0]*word_size
		for ind_word in range(word_size):
			self.df_list[ind_word]+=self.df(ind_word)
			self.idf_list[ind_word]+=math.log(doc_size/float(self.df(ind_word)))


	def df(self,ind_word):
		return len(self.tf_mat[ind_word])
		

		
	def execute(self,fileDoc, fileStopList):
		self.readDoc(fileDoc)
		self.drop_commonWords(fileStopList)
		self.fill_word_dict()
		self.fill_idf_list()
	
	
	
	
	def getIndex(self, wordSearch):
		col= self.word_dict[wordSearch]
	
		doc_returned=[pos[0]+1 for pos in self.tf_mat.keys() if pos[1]==col]
		'''
		shoud find a more brilliant way, perhapse lil matrix and access to col?
		'''
		if len(doc_returned)==0:
			print "Non documents found"
		else:
			print "for word ", wordSearch," related articles are: ", doc_returned
			return doc_returned
		
	
	
		
		
		
def split_by_non_alphabet(doc):
	pattern = re.compile('[\W_]+')
	return pattern.sub(' ', doc)
		
		



if __name__ == '__main__':
	startPoint=[".A",".T",".W",".B"]
	fileDoc="cisi/CISI.ALL"
	fileStopList="cacm/common_words"
	querry= DictBase(startPoint)
	querry.execute(fileDoc, fileStopList)
	
	print querry.doc_word_dict[1]
	
