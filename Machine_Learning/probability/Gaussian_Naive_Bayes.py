import numpy as np
import matplotlib.pyplot as plt

#-------------------------------------------------------------------------------------------------------------------------------
#Example taken from https://en.wikipedia.org/wiki/Naive_Bayes_classifier#Examples
#Sex     height(feet)    weight(lbs)    foot size(inches)
#male      6                180                12
#male      5.92 (5'11")     190                11
#male      5.58 (5'7")      170                12
#male      5.92 (5'11")     165                10
#female    5                100                6
#female    5.5 (5'6")       150                8
#female    5.42 (5'5")      130                7
#female    5.75 (5'9")      150                9

def gaussian_pdf_function(mu,sigma,x):
    pi=np.pi
    e=np.e
    denominator=1/((2*pi*sigma**2)**0.5 )
    y=denominator  * e** (-(x-mu)**2/(2*sigma**2)) 
    return y


#Training Data, male
height_male=[6, 5.92, 5.58, 5.92]
weight_male=[180,190,170,165]
foot_size_male=[12,11,12,10]

#Training Data, female
height_female=[5,5.5,5.42,5.75]
weight_female=[100,150,130,150]
foot_size_female=[6,8,7,9]


#Mean, Var male
height_male_variance= np.var(height_male)
weight_male_variance= np.var(weight_male)
foot_size_male_variance= np.var(foot_size_male)
height_male_mean=np.mean(height_male)
weight_male_mean=np.mean(weight_male)
foot_size_male_mean=np.mean(foot_size_male)


#Mean, Var female
height_female_variance= np.var(height_female)
weight_female_variance= np.var(weight_female)
foot_size_female_variance= np.var(foot_size_female)
height_female_mean=np.mean(height_female)
weight_female_mean=np.mean(weight_female)
foot_size_female_mean=np.mean(foot_size_female)


#male data ploting


x_min_range=4
x_max_range=7
step=0.05
x=np.arange(x_min_range,x_max_range,step)
y=gaussian_pdf_function( height_male_mean ,height_male_variance**(0.5),x)
fig = plt.figure()
ax1 = fig.add_subplot(231)
#ax1.text(1,1,"sssss", fontdict=None, withdash=False)
ax1.set_ylabel('height male')
ax1.plot(x, y, 'r-')

x_min_range=40
x_max_range=220
step=1
x=np.arange(x_min_range,x_max_range,step)
y=gaussian_pdf_function( weight_male_mean ,weight_male_variance**(0.5),x)
ax2 = fig.add_subplot(232)
ax2.set_ylabel('weight male')
ax2.plot(x, y, 'k-')

x_min_range=4
x_max_range=20
step=0.1
x=np.arange(x_min_range,x_max_range,step)
y=gaussian_pdf_function( foot_size_male_mean ,foot_size_male_variance**(0.5),x)
ax3 = fig.add_subplot(233)
ax2.set_ylabel('foot size male')
ax3.plot(x, y, 'b-')

#female data ploting

x_min_range=4
x_max_range=7
step=0.05
x=np.arange(x_min_range,x_max_range,step)
y=gaussian_pdf_function( height_female_mean ,height_female_variance**(0.5),x)

ax4 = fig.add_subplot(234)
ax4.plot(x, y, 'k-')
ax4.set_ylabel('height female')




x_min_range=40
x_max_range=220
step=1
x=np.arange(x_min_range,x_max_range,step)
y=gaussian_pdf_function( weight_female_mean ,weight_female_variance**(0.5),x)
ax5 = fig.add_subplot(235)
ax5.set_ylabel('weight female')
ax5.plot(x, y, 'k-')


x_min_range=4
x_max_range=20
step=0.1
x=np.arange(x_min_range,x_max_range,step)
y=gaussian_pdf_function( foot_size_female_mean ,foot_size_female_variance**(0.5),x)
ax6 = fig.add_subplot(236)
ax6.set_ylabel('foot size female')
ax6.plot(x, y, 'b-')

plt.show()

#Testing
height=6
weight=130
foot_size=8

#Calculating the probabilities
P_male=0.5
P_female=0.5

#P(height|male)
P_height_male=gaussian_pdf_function(height_male_mean,height_male_variance**(0.5),height)

#P(weight|male)
P_weight_male=gaussian_pdf_function(weight_male_mean,weight_male_variance**(0.5),weight)

#P(foot_size|male)
P_foot_size_male=gaussian_pdf_function(foot_size_male_mean,foot_size_male_variance**(0.5),foot_size)

#P(height|female)
P_height_female=gaussian_pdf_function(height_female_mean,height_female_variance**(0.5),height)

#P(weight|female)
P_weight_female=gaussian_pdf_function(weight_female_mean,weight_female_variance**(0.5),weight)

#P(foot_size|female)
P_foot_size_female=gaussian_pdf_function(foot_size_female_mean,foot_size_female_variance**(0.5),foot_size)

#evidence=P(male)*P(height|male)*P(weight|male)*P(foot_size|male) + P(female)*P(height|female)*P(weight|female)*P(foot_size|female)
evidence=P_male*P_height_male*P_weight_male*P_foot_size_male + P_female*P_height_female*P_weight_female*P_foot_size_female


#male posterior:
male_posterior=(P_male*P_height_male*P_weight_male*P_foot_size_male)/evidence
female_posterior=(P_female*P_height_female*P_weight_female*P_foot_size_female)/evidence

print "male posterior is:"
print male_posterior
print "female posterior is:"
print female_posterior
print "Then our data must belong to the female class"

#Solving problem using sklearn package

height_male=[6, 5.92, 5.58, 5.92]
weight_male=[180,190,170,165]
foot_size_male=[12,11,12,10]

#Training Data, female
height_female=[5,5.5,5.42,5.75]
weight_female=[100,150,130,150]
foot_size_female=[6,8,7,9]

#our data is expected to be tabular form 8x3

height=np.hstack((height_male,height_female))
weight=np.hstack((weight_male,weight_female))
foot_size=np.hstack((foot_size_male,foot_size_female))
record=zip(height,weight,foot_size)
record=np.array(record)

class_labels=np.array([1,1,1,1,2,2,2,2])

test_data=np.array([6,130,8])

test_data=test_data.reshape(1, -1)

 
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
clf.fit(record, class_labels)
GaussianNB()
print "Then our data must belong to the class number:"

print clf.predict(test_data)