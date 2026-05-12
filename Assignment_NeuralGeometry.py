#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author    : Younes Valibeigi  
Date      : Thu Jan 23, 2025
Description:    Supervised and unsupervised techniques to decode signals from a 
                population of neurons: the case of head-direction cells (Python version). 
Contact   : younes.valibeigi@mcgill.ca  
"""

"""
TA-Important Note:  
    
I have made every effort to convert the MATLAB assignment into Python as accurately  
as possible. However, there may be some details from the original assignment that  
I might have missed.  

Please refer to the MATLAB version of each question to ensure nothing is overlooked.  
It is your responsibility to verify that all questions are addressed thoroughly.  

I tried to make the code as error-free as possible, but there might still be 
errors in the Python version of the code or in the functions. Please let me 
know about any errors via email, and I will work on fixing them and upload the 
corrected version.

"""



# %% Supervised and unsupervised techniques to decode signals from a
# population of neurons: the case of head-direction cells.
# NEUR-503, McGill
#
# The assignment consists of answering the "QUESTIONS" below (all caps
# to make sure you don't miss them).
# Don't get stuck on one question if you don't know how to do it!
#
# This tutorial will guide you through the analysis of HD cell population data
# and how to extract head-direction and simple topological features from
# the population activity. It starts with PCA and then demonstrates how to use
# IsoMap to extract the topology without the inherent constraints of PCA.

# Copyright (C) 2021 Adrien Peyrache
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# %% Import necessary libraries
import scipy.io as sio  # For loading .mat files
import numpy as np  # For numerical operations

#  Load data
data = sio.loadmat('dataHD.mat')  # Load the MATLAB file

# Extract and inspect the components of the data
# Assuming the structure is as described in the comments

# - Q{run, sws, rem}: Three binned spike trains from 19 HD neurons
# Extract each condition and convert them into NumPy arrays
Q_run = np.array(data['Qrun'])   # Binned spike trains during running
Q_sws = np.array(data['Qsws'])   # Binned spike trains during slow-wave sleep
Q_rem = np.array(data['Qrem'])   # Binned spike trains during REM sleep

# - angRun: Animal's HD during running (time and HD data)
angRun = np.array(data['angRun'])  # Two-column matrix (times, data)

# - prefHD: Preferred HD of each neuron
prefHD = np.array(data['prefHD']).flatten()  # Flatten in case it's loaded as a 2D array

# - hdTuning: Tuning curves of the neurons
# First column contains the angular bin values
hdTuning = np.array(data['hdTuning'])

# Display data structure to confirm loading
print("Shape of Q_run:", Q_run.shape)
print("Shape of Q_sws:", Q_sws.shape)
print("Shape of Q_rem:", Q_rem.shape)
print("Shape of angRun:", angRun.shape)
print("Preferred HD:", prefHD)
print("Shape of hdTuning:", hdTuning.shape)

# %% QUESTION:
# Using the function np.correlate (Python equivalent of xcorr in MATLAB),
# plot the cross-correlation of two cells pointing to similar directions
# during wakefulness and two pointing to opposite directions in a window
# of +/- 500ms.
# Provide some interpretation of what you observe in comments here.

# %% BONUS QUESTION
# Plot all the cross-correlograms in a matrix format, sorted by angular
# difference in preferred directions.
# Plot the resulting matrix using "plt.imshow" after normalizing each cross-correlogram
# by its maximum value.
# See Peyrache et al. 2015, Figure 2d for an example.

# We will now try to decode the head-direction (HD) signal in PCA space during exploration.


# %% QUESTION: 
# Compute the correlation matrix for the run and rem data.


C_run = 
C_rem = 

# %% QUESTION:
# Plot all the pairwise correlations in REM as a function of the correlations in run.
# What do you see? How would you quantify this effect?

# %% Some help here, no questions
# Compute PCA from the correlation matrix
PC_weights = np.linalg.eig(C_run)[1]  # Use eigenvectors for PCA

# Sort the neurons by preferred direction
pref_ix = np.argsort(prefHD)

# Renaming the variables and plot them twice
theta = prefHD[pref_ix]
theta = np.concatenate([theta, theta + 2 * np.pi])

w1 = PC_weights[pref_ix, 0]
w1 = np.concatenate([w1, w1])

w2 = PC_weights[pref_ix, 1]
w2 = np.concatenate([w2, w2])


# %% QUESTION:
# Plot the weights of the first two PCs as a function of each cell's preferred HD ("theta").
# Use the function plt.stem to plot the PC weights, better to plot data twice.
# What is your interpretation (think: what is the best fit?)


# %% QUESTION:
# Compute the score of the first two PCs (two column matrix):
# The PC score is the projection of the z-scored binned spike trains onto the principal
# vectors.

PC_score_run = 

# %% Plotting the result, no questions

import numpy as np
from scipy.signal import convolve
import matplotlib.pyplot as plt

"""
TA: Please note that I have made an effort to convert gaussFilt to Python to closely 
match the behavior of the MATLAB version. 
However, I am not entirely certain if it behaves identically for all input cases.
"""

# Python equivalent of the MATLAB function
def gaussFilt(X, N1, N2=0, normBool=True):
    """
    1 or 2-d Gaussian filtering with border correction
    MATLAB-like syntax: gaussFilt(y, N1, N2)
    
    Input:
        X: vector (or matrix) to smooth
        N1: standard deviation of the Gaussian window for the first dimension
        N2: (optional) standard deviation for the second dimension (default is 0)
        normBool: normalize the Gaussian window (default is True)
    Output:
        Smoothed matrix or vector
    """
    X = np.asarray(X)  # Ensure X is a NumPy array

    if len(X.shape) > 2:
        raise ValueError("Too many dimensions!")

    if N2 == 0:
        N2 = N1  # Use the same smoothing for the second dimension if unspecified

    transpX = False
    if N1 == 0 and N2 > 0:
        X = X.T  # Transpose if smoothing only on the second dimension
        N1, N2 = N2, N1
        transpX = True

    if X.ndim > 1:  # 2D case
        l1, l2 = X.shape
        Xf = np.flipud(X)

        # Handle edge correction
        if N2 > 0:
            X0 = np.hstack([np.fliplr(Xf), Xf, np.fliplr(Xf)])
            X0 = np.vstack([X0, np.hstack([np.fliplr(X), X, np.fliplr(X)])])
            X0 = np.vstack([X0, np.hstack([np.fliplr(Xf), Xf, np.fliplr(Xf)])])
            X = X0
        else:
            X = np.vstack([Xf, X, Xf])

        if N1 != 0 or N2 != 0:
            N1 = max(3, int(2 * np.ceil(3 * N1) + 1))  # Corrected scaling
            N2 = max(3, int(2 * np.ceil(3 * N2) + 1))  # Corrected scaling

            if N1 > 0 and N2 == 0:
                gw = np.hanning(N1)[:, None]  # Make 2D for consistency
            elif N1 > 0 and N2 > 0:
                gw = np.outer(np.hanning(N1), np.hanning(N2))

            if normBool:
                gw /= np.sum(gw)

            X = convolve(X, gw, mode='same')

        # Remove edges
        if N2 > 0:
            X = X[l1:2*l1, l2:2*l2]
        else:
            X = X[l1:2*l1, :]

    else:  # 1D case
        if X.shape[0] == 1:
            X = X.T
            transpX = True

        if N1 != 0:
            l1 = X.shape[0]
            X = np.hstack([np.flipud(X), X, np.flipud(X)])
            N1 = max(3, int(2 * np.ceil(3 * N1) + 1))  # Corrected scaling
            gw = np.hanning(N1)

            if normBool:
                gw /= np.sum(gw)

            X = convolve(X, gw, mode='same')
            X = X[l1:2*l1]

    if transpX:
        X = X.T

    return X


# Smoothing of the score in time to remove noise
PCscoreRun = gaussFilt(PCscoreRun, 20, 0)

# Compute the color code to display HD
cmap = plt.cm.hsv(np.linspace(0, 1, 64))

# 1st column of angRun is time, 2nd is data.
ang = angRun[:, 1]
angContrast = (ang - np.min(ang)) / (np.max(ang) - np.min(ang))
colRunIx = np.floor(angContrast * 63).astype(int)

# Here we plot PCA decoding coloured by HD
plt.figure(2)
plt.clf()
plt.scatter(PCscoreRun[:, 0], PCscoreRun[:, 1], s=10, c=cmap[colRunIx, :])
plt.xlabel('PC1 score')
plt.ylabel('PC2 score')
plt.show()


# %% QUESTION:
# How can you decode an HD signal from the 2D PCA projection?
angPCA = 

# %% Realigning decoded and actual angles, no questions
# Problem! The angular offset of PCA decoding is arbitrary.
# Let's find it by estimating the average offset with actual HD.

angDiff = angPCA - angRun[:, 1]

# Here, let's compute angular mean
angDiff = np.column_stack([np.cos(angDiff), np.sin(angDiff)])
angDiff = np.arctan2(np.mean(angDiff[:, 1]), np.mean(angDiff[:, 0]))

# Correct for the offset
angPCA = np.mod(angPCA - angDiff, 2 * np.pi)

# Plotting the result
import matplotlib.pyplot as plt

plt.figure(3)
plt.clf()
plt.plot(angRun[:, 0], angRun[:, 1], label='True HD')
plt.plot(angRun[:, 0], angPCA, label='PCA HD')
plt.legend()
plt.show()

# %% QUESTION
# Compute the score of the first two PCs during REM.
# Smooth it as above and plot the 2D projection

PCscoreREM = 

# %% QUESTION (tough one!)
# How can we test that the HD system is a 'ring attractor' during
# exploration and REM sleep? 
# Tip: ask yourself "what is the common property of all points on a circle?"
# Don't panic. Just let me know what you think about it, and share with me any crazy
# idea you may come up with.

# %% Other unsupervised technique: IsoMap, no questions

"""
TA: Please note that in the MATLAB version, this toolbox is being used:
    https://lvdmaaten.github.io/drtoolbox/
"""

# This section needs the following toolbox to work:
# https://scikit-learn.org/stable/modules/generated/sklearn.manifold.Isomap.html

# see these three papers:
#      Original IsoMap paper:
#      J. B. Tenenbaum, V. de Silva, J. C. Langford (2000).  A global
#      geometric framework for nonlinear dimensionality reduction.  
#      Science 290 (5500): 2319-2323. 
#
#      Topology of HD cell population:
#      R. Chaudhuri et al., (2019). The intrinsic attractor manifold and
#      population dynamics of a canonical cognitive circuit across waking
#      and sleep. Nature Neuroscience 22(9):1512-1520
#
#      An example of HD decoding using IsoMap:
#      G. Viejo and A. Peyrache (2019). Precise coupling of the thalamic
#      head-direction system to hippocampal ripples. bioRxiv 
#      https://doi.org/10.1101/809657 
#

# We need to downsample data (IsoMap needs a lot of memory...)
import numpy as np
from sklearn.manifold import Isomap
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


dataSelect = np.arange(0, min(100000, Qrem.shape[0]), 50)
data = gaussFilt(Qrun, 50, 0)  # Apply Gaussian filtering
data = StandardScaler().fit_transform(data[dataSelect, :])  # Z-score normalization

# Use Isomap from scikit-learn
isomap = Isomap(n_neighbors=5, n_components=2)
mapRun = isomap.fit_transform(data)

data = gaussFilt(Qrem, 50, 0)  # Apply Gaussian filtering for REM data
data = StandardScaler().fit_transform(data[dataSelect, :])  # Z-score normalization
mapRem = isomap.fit_transform(data)

# Plot the results
plt.figure(6)
plt.clf()

# RUN plot
plt.subplot(1, 2, 1)
plt.scatter(mapRun[:, 0], mapRun[:, 1], s=10, c=cmap[colRunIx(dataSelect), :])  # Adjust colRunIx as needed
plt.xlabel('IsoMap dim. 1')
plt.ylabel('IsoMap dim. 2')
plt.title('RUN')

# REM plot
plt.subplot(1, 2, 2)
plt.scatter(mapRem[:, 0], mapRem[:, 1], s=10, c='k')
plt.xlabel('IsoMap dim. 1')
plt.ylabel('IsoMap dim. 2')
plt.title('REM')

plt.show()

# %% Bayesian decoding, no questions
"""
TA: Please note that I have made an effort to convert BayesReconstruction_1D to 
Python to closely match the behavior of the MATLAB version. 
However, I am not entirely certain if it behaves identically for all input cases.
If you noticed any error, please let me know and I will fix it.
"""

def BayesReconstruction_1D(pf, Q, thetaVec, tau, Px=None):
    """
    Bayesian reconstruction of a one-dimensional signal based on neuron tuning curves and instantaneous firing.
    
    Parameters:
    - pf: Nbins x Ncells matrix of tuning curves (Hz)
    - Q: T x Ncells matrix of binned spike trains (T time bins)
    - thetaVec: Nbins position values
    - tau: Time bin duration (in seconds)
    - Px: Optional occupancy map (histogram of time spent in each bin)
    
    Returns:
    - thetaEst: Estimated values of theta (the 1D position value)
    - thetaP: Posterior probabilities of the reconstructed positions
    - thetaMat: Matrix of posterior probabilities (all position bins)
    """
    N = pf.shape[1]
    if Q.shape[1] != N:
        raise ValueError("Inconsistent size between place field array and binned spike train matrix")
    
    n = pf.shape[0]
    nt = len(thetaVec)
    if n != nt:
        raise ValueError("Inconsistent size between place field array and spatial bin vector")
    
    if Px is not None:
        if n != len(Px):
            raise ValueError("Inconsistent size between place field array and occupancy map")
        Px = np.clip(Px, a_min=np.min(Px[Px > 0]), a_max=None)
        Px = Px / np.sum(Px)
        constTerm = np.log(Px) - tau * np.sum(pf, axis=1)
    else:
        constTerm = -tau * np.sum(pf, axis=1)
    
    B = Q.shape[0]
    thetaEst = np.zeros(B)
    thetaMat = np.zeros((B, len(thetaVec)))
    thetaP = np.zeros(B)

    pf = np.log(pf)
    pf[pf < -16] = -16

    lChunk = 100
    nbChunk = B // lChunk
    cT = np.tile(constTerm, (lChunk, 1))
    pfR = np.tile(pf[np.newaxis, :, :], (lChunk, 1, 1))
    pfR = np.transpose(pfR, (0, 2, 1))

    for ii in range(nbChunk - 1):
        ix = slice(ii * lChunk, (ii + 1) * lChunk)
        dq = Q[ix, :]
        pv = np.tile(dq[:, :, np.newaxis], (1, 1, n))
        logPxn = np.sum(pv * pfR, axis=1) + cT
        logPxn = np.exp(logPxn)
        logPxn /= np.sum(logPxn, axis=1, keepdims=True)
        thetaP[ix] = np.max(logPxn, axis=1)
        maxIx = np.argmax(logPxn, axis=1)
        thetaEst[ix] = thetaVec[maxIx]
        thetaMat[ix, :] = logPxn

    remainderChunk = B - (nbChunk - 1) * lChunk
    if remainderChunk > 0:
        ix = slice((nbChunk - 1) * lChunk, B)
        cT = np.tile(constTerm, (remainderChunk, 1))
        dq = Q[ix, :]
        pv = np.tile(dq[:, :, np.newaxis], (1, 1, n))
        pfR = np.tile(pf[np.newaxis, :, :], (remainderChunk, 1, 1))
        pfR = np.transpose(pfR, (0, 2, 1))
        logPxn = np.sum(pv * pfR, axis=1) + cT
        logPxn = np.exp(logPxn)
        logPxn /= np.sum(logPxn, axis=1, keepdims=True)
        thetaP[ix] = np.max(logPxn, axis=1)
        maxIx = np.argmax(logPxn, axis=1)
        thetaEst[ix] = thetaVec[maxIx]
        thetaMat[ix, :] = logPxn
    
    return thetaEst, thetaP, thetaMat


q = gaussFilt(Qrun, 20, 0)  # non-normalized smoothing (to preserve actual number of spikes)

angBayes = BayesReconstruction_1D(hdTuning[:, 1:], q, hdTuning[:, 0], 0.01)
angBayes = np.mod(angBayes, 2 * np.pi)

# time:
t = angRun[:, 0]

plt.figure(5)
plt.clf()
plt.plot(t, angRun[:, 1])
plt.plot(t, angPCA)
plt.plot(t, angBayes)


# %% QUESTION: 
# Quantify the quality of each decoder and compare the methods
# Warning: these are angular values, be careful!







