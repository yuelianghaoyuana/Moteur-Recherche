from DictBase import *
from Querry import *
from Similarity import *
from Evaluation import *
from DictRelevant import *
import time

startPoint=[".A",".T",".W",".B"]
fileDoc="cisi/CISI.ALL"
fileStopList="cacm/common_words"
fileQuerry="cisi/CISI.QRY"
fileRel='cisi/CISI.REL'


if __name__=="__main__":
	db= DictBase(startPoint)
	db.execute(fileDoc, fileStopList)
	# print db.word_dict['recognition']  #2634   OK
	#print db.tf_mat[2634]     #OK
	'''
	{396: 1, 653: 1, 1426: 1, 1044: 1, 89: 1, 474: 2, 927: 1, 1458: 2, 797: 2, 48: 1, 1202: 2, 94: 1, 568: 2, 1337: 1, 799: 1, 1341: 2, 908: 1, 1421: 1, 601: 1, 858: 1, 861: 1, 990: 1, 863: 1, 102: 2, 108: 1, 1134: 1, 495: 1, 241: 1, 890: 3, 1403: 1, 895: 1}
	'''
	qr=Querry(startPoint,db.word_dict)
	qr.readQuerry(fileQuerry)
	sim =similarity(db, qr.querry_dict)
	dr=DictRelevant()
	dr.readRelevantQuerry(fileRel)
	print "finish readRel Dictionary"
	eva= Evaluation(db, dr, -1, sim.cosinus)
	#eva= Evaluation(db, dr, 100, sim.cosinus )
	print eva.mean_avg_prec()
