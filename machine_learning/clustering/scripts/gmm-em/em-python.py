#!/usr/bin/python
#-*- coding: utf-8 -*-


"""
Usage()
"""
def usage():
    print """
An implementation of the EM algorithm described in page 254 of the
textbook "Foundations of Statistical Natural Language Processing", 
wrote by Christopher D. Manning & Hinrich Schütze. 
[ISBN: 0-262-13360-1]

Coded by WU, Zhaojun < wuzhaojun at gmail dot com>
Tue Jul  1 22:11:14 HKT 2008

Usage:

python em.py <threshold> <max_iter> <cluster_no> <feature_file> [output_file]

  <threshold>   : a float. When the likelihood is increasing less than 
                  'threshold', stop the algorithm)
               
  <max_iter>    : an integer. When the iteration number is larger than 
                  'max_iter', stop the algorithm)
  <cluster_no>  : an integer. How many clusters the algorithm should classify.
                  [ todo: automatically determine the best cluster number ]

  <feature_file>: the name of the file that contains the feature vectors.
                  The format of the feature file looks like:

                  

                   feature column j
          ...
        context i  0 1 0 1 0 0 0 0 1
                   1 0 0 0 1 1 0 0 0
          ...

               Each row represents one context (or, one sentence), 
               and each column represents one feature, where '1' 
               denotes the existence of the feature in this context, 
               and 0 denotes the nonexistence. 
               Note that columns should be separated by spaces.

  [output_file] : (optional) the name of the file that stores the clustering 
                  results.

Usage example:
     python em.py 0.001 20 2 fake_feature.txt output

"""
    return

"""
Initialize
"""
def initialize():

    if debug:
        print "Initializing the EM algorithm ... "
    # randomly initialize P(Sk)
    # note: the total probability of P(Sk) should be 1.0   
    remaining_prob = 1.0 

    for k in range(K-1):
        #P_Sk_array[k] = random.random() / K
        P_Sk_array[k] = 1.0 / K
        remaining_prob -= P_Sk_array[k] 
        
    P_Sk_array[K-1] = remaining_prob

    if debug:
        print P_Sk_array
        #pause = raw_input("Pause...")

    # randomly initialize P(Vj|Sk)
    for j in range(J):
        for k in range(K):
            P_Vj_g_Sk_array[j][k] = random.random()

    #if debug:
        #print P_Vj_g_Sk_array
        #pause = raw_input("Pause...")

    return

"""
Calculate the likelihood score of the model.
Formula: l(C|u) = Sum_I[Log_K(P(Ci|Sk)*P(Sk))]
"""
def calc_model_likelihood():
    log_score = .0

    for i in range(I):
        temp_sum = .0
        for k in range(K):
            P_Ci_g_Sk_array[i][k] = calc_P_Ci_g_Sk(i, k)
            if (P_Ci_g_Sk_array[i][k] < epsilon):
                P_Ci_g_Sk_array[i][k] = epsilon
            temp_sum += P_Ci_g_Sk_array[i][k] * P_Sk_array[k]
            P_Ci_array[i] += P_Ci_g_Sk_array[i][k]
        #if (temp_sum != 0):
        if (temp_sum < epsilon):
            log_score += math.log10(epsilon)
        else:
            log_score += math.log10(temp_sum)

    return log_score


"""
Calculate the probability of Ci given Sk.
Formula: P(Ci|Sk) = Multiply_J[P(Vj|Sk)]
"""
def calc_P_Ci_g_Sk(i, k):
    score = 1.0 
    for j in range(J):
        v = context_feature_array[i][j]
        # need carefully think! fix me!!
        # since the features are binary one
        if v == 1:      # vword v exists in the context
            score *= P_Vj_g_Sk_array[j][k]
        else:
            score *= (1.0 - P_Vj_g_Sk_array[j][k])

    return score


"""
Calculate the posterior probability that Sk generated Ci.
Formula: Hik = P(Ci|Sk)/Sum_K[P(Ci|Sk)]
"""
def calc_Hik(i, k):
    numerator = calc_P_Ci_g_Sk(i, k)
    denominator = 0
    for kk in range(K):
        denominator += calc_P_Ci_g_Sk(i, kk)

    if (denominator == 0):
        denominator = epsilon
    return (numerator / denominator)


"""
    do the E-step
"""
def E_step():
    for i in range(I):
        for k in range(K):
            Hik_array[i][k] = calc_Hik(i, k)

    #print Hik_array;
    return


"""
Update the probability of Vj given Sk
Formula:
    P(Vj|Sk) = Sum_<Ci: Vj in Ci>[Hik] / Zj
    Zj = Sum_K[Sum_<Ci: Vj in Ci>[Hik]]
"""
def update_P_Vj_g_Sk():

    for k in range(K):
        for j in range(J):
            sum_Hik_j = .0
            Zj = .0
            for i in range(I):
                if (context_feature_array[i][j] == 1):
                    # feature Vj exsits in context i
                    sum_Hik_j += Hik_array[i][k]
                    
                    # well, let's calculate the normalizing constant Zj 
                    for kk in range(K):
                        Zj += Hik_array[i][kk]
                   
            if (Zj == 0):
                Zj = epsilon

            # once Sum_Hik_j and Zj are available, we can get the 
            # P(Vj|Sk) as follows:
            P_Vj_g_Sk_array[j][k] =  sum_Hik_j / Zj

            # to avoid the error of log10(0) latter
            #if (P_Vj_g_Sk_array[j][k] == 0):
            if (P_Vj_g_Sk_array[j][k] < epsilon):
                P_Vj_g_Sk_array[j][k] = epsilon

    return


"""
Update the Probability of Sk.
Formula: P(Sk) = Sum_I[Hik]/I
"""
def update_P_Sk():
    for k in range(K):
        sum_Hik = .0
        for i in range(I):
            sum_Hik += Hik_array[i][k]
        P_Sk_array[k] = sum_Hik / I

        #if (P_Sk_array[k] == 0):
        if (P_Sk_array[k] < epsilon):
            P_Sk_array[k] = epsilon
            #P_Sk_array[k] = 1e-10

    if debug:
        print "P(Sk)\n", P_Sk_array
    return

"""
    do the M-step: re-estimate P(Vj|Sk) and P(Sk)
"""
def M_step():

    update_P_Vj_g_Sk()
    update_P_Sk()

    return


"""
Output the final clustering result
s'=argmax_Sk[logP(Sk) + Sum_<Vj_in_C>[logP(Vj|Sk)]
"""
def make_decision(decision_list):
    for i in range(I):
        # decision array
        tmp_Sk_array = numpy.zeros(K, float) 
        for k in range(K):
            tmp_score = .0
            for j in range(J):
                if context_feature_array[i][j] == 1: # feature Vj exists
                    if (P_Vj_g_Sk_array[j][k] != 0):
                        tmp_score += math.log10(P_Vj_g_Sk_array[j][k])
                else:
                    # Vj is a binary feature, so the probability of the 
                    # non-existence of Vj given Sk is calculated as follows:
                    if (P_Vj_g_Sk_array[j][k] != 1.0):
                        tmp_score += math.log10(1 - P_Vj_g_Sk_array[j][k])

            tmp_Sk_array[k] = tmp_score + math.log10(P_Sk_array[k])

        max_score = tmp_Sk_array[0]
        decision = 0
        for k in range(K):
            if (tmp_Sk_array[k] > max_score):
                max_score = tmp_Sk_array[k]
                decision = k

        decision_list.append(str(decision))

    return



"""
Main program.
"""
if __name__ == "__main__":

    import sys

    if len(sys.argv) < 5:
        usage()
        sys.exit(1)

    
    debug = True
    #debug = False

    threshold  = float(sys.argv[1])
    max_iter   = int(sys.argv[2])
    cluster_no = int(sys.argv[3]) 

    if (cluster_no <= 1):
        print "You just want " + str(cluster_no) + " cluster?"
        print "Must be kidding me. :) Anyway, I am quitting now..."
        sys.exit(1)

    import random 
    import numpy
    import math

    feature_file = open(sys.argv[4], 'r')
    feature_lines = feature_file.readlines()

    I = len(feature_lines)               # number of contexts
    J = len(feature_lines[0].split());   # number of features 
    K = cluster_no                       # number of senses

    epsilon = 1e-30
    if debug:
        print "Context No.:", I
        print "Feature No.:", J
        print "Sense No.  :", K
        print

    # STEP-O: Preparation, Data Structure

    # the probability array of the sense Sk P(Sk)
    P_Sk_array = numpy.zeros(K, float)  
    # the probability array of Vj given sense SK array P(Vj|Sk)
    P_Vj_g_Sk_array = numpy.zeros((J,K), float) 
    # the probability array of context Ci P(Ci)
    P_Ci_array = numpy.zeros(I, float) 

    # the probability array of context Ci given sense SK
    P_Ci_g_Sk_array = numpy.zeros((I,K), float)

    # posterior probability that Sk generated Ci
    Hik_array = numpy.zeros((I,K), float)

    # context feature array
    context_feature_array = numpy.zeros((I, J), int)

    # build the context feature array
    if debug:
        print "Reading feature file ..."
    for i in range(I):
        features = feature_lines[i].split()
        for j in range(J):
            context_feature_array[i][j] = int(features[j])

    feature_file.close()

    # STEP-1: Initialization
    initialize()

    old_model_score = calc_model_likelihood()
    if debug:
        print "Old model score:", old_model_score

    iter = 0

    while iter < max_iter: 
        iter += 1
        if debug:
            print "Iteration " + str(iter) + "...";

        # STEP 2: E-step
        E_step()

        # STEP 3: M-step
        M_step()

        # Recompute the log of the likelihood of the context C
        new_model_score = calc_model_likelihood()

        if debug:
            print "New model score: ", new_model_score

        if (abs(new_model_score - old_model_score) < threshold):
            break

        if debug:
            print (new_model_score - old_model_score), "\n"
        old_model_score = new_model_score

    if debug:
        print "EM algorithm converged..."

    cluster_result = []
    make_decision(cluster_result)

    if debug:
        print P_Sk_array

    print "\n".join(cluster_result)

    # if the output file is specified.
    if (len(sys.argv) == 6):
        outfile = open(sys.argv[5], 'w')
        outfile.write("=======R E P O R T==========\n")
        outfile.write("Context No.: %d\n" % I)
        outfile.write("Feature No.: %d\n" % J)
        outfile.write("Sense No.  : %d\n" % K)
        outfile.write("Converged Iteration: %d\n" % iter)
        outfile.write("============================")

        outfile.write("\n".join(cluster_result))
        outfile.write("\n")
        outfile.close()
    
    sys.exit(0)
