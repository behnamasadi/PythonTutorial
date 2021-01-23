import numpy as np
import matplotlib.pyplot as plt





k=7
def classifier(x):
    return (1 + np.tanh(k * x - 3)) / 2


def confusion_matrix(weights):
    TP, FP, TN, FN = 0, 0, 0, 0
    for i,w in enumerate (weights):
        # our classifier predicted not obese
        if classifier(w)<cut_of_value:
            # data is actually obese (Positive), our classifier predicted not obese
            if true_obesity_labels[i]:
                FN=FN+1
            # data is not obese (Negative), our classifier predicted not obese
            else:
                TN=TN+1
        # our classifier predicted obese
        else:
            # data is actually obese (Positive), our classifier predicted  obese
            if true_obesity_labels[i]:
                TP=TP+1
            # data is actually not obese (Negative), our classifier predicted  obese
            else:
                FP=FP+1
    return TP, FP, TN, FN

x=np.linspace(0,1,100)
y=classifier(x)

weights=np.array([0.15,0.20,0.28,0.4,0.61,0.70,0.95,1.0])

# 0 means not obese, 1 means obese
true_obesity_labels=np.array([0,0,1,0,0,1,1,1])

classifier_prediction_obesity_labels=classifier(weights)



colors=[]
for i in true_obesity_labels:
    if i==0:
        colors.append('blue')
    else:
        colors.append('red')


obese=plt.scatter(weights,classifier_prediction_obesity_labels,color=colors,label='obese'
                  ,facecolor='red',edgecolor='red')
not_obese=plt.scatter(weights,classifier_prediction_obesity_labels,color=colors,label='not obese')

plt.plot(x,y)
plt.legend(handles=[obese,not_obese])

plt.xlabel('weights')
plt.ylabel('classifier output probability of being obese')
plt.legend()

classifier_cut_off_value=1.0
plt.plot([0,1],[classifier_cut_off_value,classifier_cut_off_value])
plt.show()


# obese P
# not obese N
# Positive or Negative comes from actual data.
# True or False comes from correspondence of prediction with actual data, if both are same it is True otherweise False.

TPRs=[]
FPRs=[]

cut_of_values=classifier_prediction_obesity_labels-0.01

for cut_of_value in cut_of_values:
    TP, FP, TN, FN = confusion_matrix(weights)
    print("Classifier Cut Off Value is :{}".format(cut_of_value))
    print("TP={},FP={},TN={},FN={}".format(TP,FP,TN,FN) )

    #TPR=TP/P => TP/TP+FN
    TPR=TP /( TP + FN)
    print("TPR={}".format(TPR) )
    TPRs.append(TPR)

    #FPR=FP/N => FP/FP+TN
    FPR=FP /(FP + TN)
    print("FPR={}".format(FPR) )
    FPRs.append(FPR)

plt.scatter(FPRs,TPRs)
for i,txt in enumerate(cut_of_values):
    plt.annotate(cut_of_values[i],  (FPRs[i],TPRs[i]))

plt.xlabel('FPR (Fall Out, 1-Specificity)')
plt.ylabel('TPR (Sensitivity, Recall )')
plt.show()