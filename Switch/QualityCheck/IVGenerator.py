#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 17:25:11 2018

@author: renhori
"""

import numpy as np
import matplotlib.pyplot as plt

<<<<<<< HEAD

'''
voltrange = []
Vabs = 1.5
Vstep = 0.005
steps = Vabs/Vstep + 1
steps = int(steps)

a = np.zeros((4,1,steps))

#Set of voltage range is appended to the voltagerange
first =(np.linspace(0,-Vabs, steps))
a[0] = first
second= (np.linspace(-Vabs, 0,steps))
a[1] = second
third= (np.linspace(0, Vabs, steps))
a[2] = third
fourth = (np.linspace(Vabs, 0, steps))
a[3] = fourth
for b in range(4):
    for c in range(steps):
        voltrange.append(a[b][0][c])
        
test = np.random.rand(8,7,2,1204)
test = np.round(test)

for a in range(len(test)):
    for b in range(len(test[a])):
        i = -1.5
        for c in range(len(test[a][b][0])):
            test[a][b][0][c] = voltrange[c]
            test[a][b][1][c] = i
            i = i+ 0.005
'''

data= np.load('D:\RenDrive\SwiNEt_02_08_2018_175621_IVTest/IVDataz.npz')
test =data.f.currentlist

b = 8

for a in range(len(test[b])):
    plt.figure()
    plt.plot(test[b][a][0], test[b][a][1])
    plt.show()
=======
data= np.load('/Users/renhori/Desktop/SwiNEt_03_08_2018_185531_IVTest/IVDataz.npz')
result =data.f.currentlist

b = 1

plt.figure(1)
j = 421
for a in range(len(result[b])):
    plt.subplot(j)
    plt.plot(result[b][a][0], result[b][a][1])
    plt.ylabel('Amp')
    plt.xlabel('Volt')
    plt.grid(True)
    plt.title('E1 to E' + str(a+2))
    j = j + 1

plt.show()
>>>>>>> 26776d894bac719bd2f78651e0c7b66ecde17355
