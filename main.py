import numpy as np
import random
from matplotlib import pyplot as plt
import math
from algorithms import func, funcMM, NLS, MedianMethod 		# Algorithms
from get_xls import generate_xls	 # Generate xls file

###### Definition of S and P data to work with ######

s_data = np.array([0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0])     # S values
p_data = np.array([0, 5, 10, 20, 40])        				# P values
N_s = len(s_data)											# Number of S values
N_p = len(p_data)											# Number of P values
N_sim = 10                  #Number of simulations

###### Parameters to estimate ######

VMAX = 1	# True value of Vmax
KM = 1		# True value of Km
KP = 10		# True value of Kp

variance = 0.001	# Variance of the normal error

variance_outlier = 0.1        #	Variance of the normal error for the outlier
n_outlier = 0                 #	Number of outliers

estimate_NLS = list()			# Estimated parameters by the Non Linear Least Squares Method
estimate_Median1 = list()		# Estimated parameters by the Median Method, Kp is estimated directly from Kp
estimate_Median2 = list()		# Estimated parameters by the Inverse Median Method, Kp is estimated inversely from Km/Kp

RSS_NLS = list()			# Residuals obtained from computation of Kp in Non Linear Least Squares Method
RSS_Median1 = list()		# Residuals obtained from computation of Kp in Median Method, directly from Kp
RSS_Median2 = list()		# Residulas obtained from computation of Kp in Median Method, inversely from Kp

###### Normal Error ######
    
mean = np.zeros(N_s) 			# Mean of the normal error
cov = np.zeros((N_s,N_s)) 		
i,j = np.indices(cov.shape)
cov[i==j] = variance 			# Covariance Matrix of the normal error

###### Outlier Data ######

cov_outlier = np.zeros((N_s,N_s))	   
k,l = np.indices(cov.shape)
cov_outlier[k==l] = variance_outlier		#Covariance Matrix of Outlier

###### Simulation ######

for i in range(N_sim):

    datos = list()			# Set of data, where each data is in the form [S, P, v]

    relative_error = np.random.multivariate_normal(mean, cov)		# Error obtained from the normal distribution

    relative_error_outlier = np.random.multivariate_normal(mean, cov_outlier) 		# Error of outlier obtained from the normal distribution

    ind_rand = list()		# Index of outlier data, obtained randomly

    for i in range(n_outlier):
        ind_rand.append(random.randint(1,N_s*N_p))		# Computation of outlier index

    #### Computation of v data ####

    v_noise = list()		# Set of perturbed velocity. Is a list of lists, where each list have a value of P fixed

    for i in range(N_p):
        v_noise.append(list())
        for j in range(N_s):
            vpert = func(s_data[j], p_data[i], VMAX, KM, KP)*(1 + relative_error[j])		# Perturbed v
            datos.append([p_data[i], s_data[j], vpert])
            v_noise[i].append(vpert)
            if len(datos) in ind_rand:
                vpert_outlier = func(s_data[j], p_data[i], VMAX, KM, KP)*(1 + relative_error_outlier[j])		#Perturbed outlier v
                datos[len(datos)-1][2] = vpert_outlier
                v_noise[i].pop()
                v_noise[i].append(vpert_outlier)
        
    datosNLS = NLS(datos, s_data, p_data, v_noise)		# Computation of estimated parameters with Non Linear Least Squares Method
    estimate_NLS.append(datosNLS)
    ErrorNLS = abs(KP-datosNLS[2])/KP 					# Computation of error for estimation of Kp in Non Linear Least Squares Method

    datosMM1 = MedianMethod(datos, 'case1')			# Computation of estimated parameters with Median Method, and Kp obtained directly from Kp
    estimate_Median1.append(datosMM1)
    ErrorMM1 = abs(KP-datosMM1[2])/KP 				# Computation of error for estimation of Kp in Median Method, obtained directly from Kp

    datosMM2 = MedianMethod(datos, 'case2')			# Computation of estimated parameters with Median Method, and Kp obtained inversely from Km/Kp
    estimate_Median2.append(datosMM2)
    ErrorMM2 = abs(KP-datosMM2[2])/KP 				# Computation of error for estimation of Kp in Median Method, obtained inversely from Km/Kp

    RSS_NLS.append(ErrorNLS)
    RSS_Median1.append(ErrorMM1)
    RSS_Median2.append(ErrorMM2)

###### Generate xls file with summary table

generate_xls(N_sim, estimate_NLS, estimate_Median1, estimate_Median2, RSS_NLS, RSS_Median1, RSS_Median2)
