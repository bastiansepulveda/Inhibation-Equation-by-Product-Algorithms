import numpy as np
import random
import itertools
from scipy.optimize import curve_fit
import math

###### Equations to find parameters ######

def func(S, P, Vmax, K, Kp):                # Inhibation Equation by Product
    return (Vmax*S)/(K + S + (K/Kp)*P)

def funcMM(S, Vmax, KmAp):                  # Michaelis Menten Equation
    return (Vmax*S)/(KmAp+S)

def KmAP(P, Km, Kp):                        # Apparent Km
    return Km + (Km/Kp)*P

###### Non Linear Least Square Method ######

def NLS(data, s_data, p_data, v_noise):        
    N_s = len(s_data)       # Number of S values
    N_p = len(p_data)       # Number of P values

    Vmax_estimated = list()     # Estimated Vmax for each P value
    KmAp_estimated = list()     # Estimated KmAp for each P value

    for n in range(N_p):
        V0 = max(data[n*N_s:(n+1)*N_s], key = lambda x : x[2])[2]                   # Initial value of Vmax, considered as the maximum value in data for P fixed
        Km0 = min(data[n*N_s:(n+1)*N_s], key = lambda x : abs(x[2]-V0/2))[1]        # Initial value of Km, considered as the value that minimize |S-V0/2|, for P fixed
        parameters, pcov0 = curve_fit(funcMM, s_data, v_noise[n], p0=[V0, Km0])     # Non Linear Regression
        Vmax_estimated.append(parameters[0])
        KmAp_estimated.append(parameters[1])

    Vmax = max(Vmax_estimated)          # Vmax, estimated es the maximum of all the Vmax estimated previously

    K, pcov = curve_fit(KmAP, p_data, KmAp_estimated)       # Regression over Apparent Km to estimate Km and Kp

    return Vmax, K[0], K[1]

###### Median Method ######

def MedianMethod(datos, case):
    comb = list(itertools.combinations(datos,3))        # Compute all the combinations of data
    params_V = list()           # Parameter Vmax computed for each linear sistem
    params_K = list()           # Parameter Km computed for each linear sistem
    params_Kp = list()          # Parameter Kp computed for each linear sistem, obtained directly from Kp
    params_Kpi = list()         # Parameter Kp computed for each linear sistem, obtained inversely from Km/Kp

    #### Solve linear sistems to compute paratemers ####

    for i in comb:
            A = np.array([[i[0][2], -i[0][1], i[0][2]*i[0][0]], [i[1][2], -i[1][1], i[1][2]*i[1][0]], [i[2][2], -i[2][1], i[2][2]*i[2][0]]])
            det = np.linalg.det(A)
            if(det != 0):           # Evaluate condition det(A)!=0 to ensure that the sistem has solutions
                b = np.array([-i[0][2]*i[0][1], -i[1][2]*i[1][1], -i[2][2]*i[2][1]])
                x = np.linalg.solve(A,b)        # Solution of linear system Ax = b
                if x[2] != 0:
                    params_V.append(x[1]), params_K.append(x[0]), params_Kp.append(x[0]/x[2]), params_Kpi.append(x[2]) # (Vmax, Km, Kp1, Kp2)

    V_Median = np.median(np.array(params_V))            # Estimated Vmax
    K_Median = np.median(np.array(params_K))            # Estimated Km

    if(case == 'case1'):
        Kp1 = np.median(np.array(params_Kp))            # Estimated Kp obtained directly from Kp
        Kp_Median = Kp1
    elif(case == 'case2'):
        Kp2 = np.median(np.array(params_Kpi))           # Estimated Kp obtained inversely from Km/Kp 
        Kp_Median = K_Median/Kp2
    
    return V_Median, K_Median, Kp_Median
