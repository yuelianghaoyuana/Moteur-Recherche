import re
class DictRelevant():
	def __init__(self):
		self.dict_Rel={}


	def readRelevantQuerry(self,filePath):
		f= open(filePath)
		for line in f:
			tokens=re.findall('\d+',line)
			querry=int(tokens[0])
			article=int(tokens[1])
			if (querry in self.dict_Rel.keys()):
				self.dict_Rel[querry].append(article)
			else:
				self.dict_Rel[querry]=[]
				self.dict_Rel[querry].append(article)

		f.close()

if __name__ == '__main__':
	filePath='cisi/CISI.REL'
	dict_Rel=DictRelevant()
	dict_Rel.readRelevantQuerry(filePath)
	print dict_Rel.dict_Rel[1]

