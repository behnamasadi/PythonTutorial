#https://stats.stackexchange.com/questions/7207/roc-vs-precision-and-recall-curves
import numpy as np
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report 

import matplotlib.pyplot as plt

weights = [1,2,4,5,7,8,9,10]
actual_labels = [0,0,1,0,0,1,1,1]

prediction_values=[0.1,0.1, 0.2,0.4,0.8,0.89,0.95,0.98  ]

#get_color=lambda x:'blue' if x==1 else 'red'

color_dict={1:'blue', 0:'red'}
get_color=lambda x:  color_dict[x]
get_prediction_labels=lambda prediction_values, cut_off:  1 if (prediction_values>=cut_off)  else 0


true_positive_rates=[]
false_positive_rates=[]
F1_scores=[]



for cut_off in np.unique(prediction_values):

	data_confusion_matrix=confusion_matrix(actual_labels , [ get_prediction_labels(prediction_value,cut_off)  for prediction_value in prediction_values   ]   )

	#print(data_confusion_matrix)

	tn, fp, fn, tp =data_confusion_matrix.ravel()
	true_positive_rate=tp/(tp+fn)
	false_positive_rate=1-tn/(tn+fp)

	false_positive_rates.append(false_positive_rate)
	true_positive_rates.append(true_positive_rate)
	#print("cut_off:",cut_off)
	#print("true_positive_rate:",true_positive_rate)
	#print("false_positive_rate:",false_positive_rate)
	#print("tn={} fp={} fn={} tp={}".format(tn, fp, fn, tp))
	colors=[get_color(x) for x in actual_labels ]


	precision=tp/(tp+fp)
	recall=tp/(tp+fn)
	F1_score= 2*precision*recall/(precision+recall)
	F1_scores.append(F1_score)

	plt.scatter(weights,prediction_values,color=colors   )
	plt.plot([0,10], [cut_off,cut_off],color='green')
	plt.show()

	
plt.plot(false_positive_rates,true_positive_rates)
plt.show()




import numpy as np
from sklearn import metrics


fpr, tpr, thresholds = metrics.roc_curve(actual_labels, prediction_values, pos_label=None)

print("true positive rates:",tpr)
print("false positive rates:",fpr)
print("thresholds:",thresholds)


#print("true positive rates:",true_positive_rates[::-1])
print("true positive rates:",true_positive_rates)
print("false positive rates:",false_positive_rates)
print("thresholds:",np.unique(prediction_values) )
print("F1_scores:",F1_scores)



cut_off=0.89
print ('Accuracy Score :',accuracy_score(actual_labels, [ get_prediction_labels(prediction_value,cut_off)  for prediction_value in prediction_values   ]) )

print (classification_report(actual_labels, [ get_prediction_labels(prediction_value,cut_off)  for prediction_value in prediction_values   ]) )




