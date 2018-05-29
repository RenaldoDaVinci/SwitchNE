__author__ = 'RenH'
'''
This is a rudimentary model of switch network python code, the first row is dedicated for the input and the last row for the output
'''

#import necessary libraries
import time
import Evo as Evo
import numpy as np
import operator
from time import sleep
import serial
import SaveLibrary as SaveLib

#open the set up files, this is not fully incorporated yet (needs to figure out how to sort out the each procedures)
exec(open("setup.txt").read())
#Initialize the serial connection to the arduino
#ser = serial.Serial(port='/dev/cu.usbmodem1411',baudrate=9600,parity=serial.PARITY_NONE,bytesize=serial.EIGHTBITS)
#Initialize the directory to save the files
savedirectory = SaveLib.createSaveDirectory(filepath, name)
#generate necessary arrays to save the datas


genearray = np.zeros((generations, genomes, genes, genes))
outputarray = np.zeros((generations, genomes, genes,genes))
fitnessarray = np.zeros((generations, genomes))
successarray = np.zeros((generations, genomes))
run = 0
#define the initial switches
array1 = np.random.rand(genomes,genes,genes)
#said arrays contain random value from 0 to 1, round it so it's a same array with binary bits
NewGenConfigs = np.around(array1)

#start the process, per generation
for m in range(generations):
	#Define the array to insert the fitness scores
	Fitnessscore = []
	successrate = []
	#per genomes
	for i in range(len(NewGenConfigs)):
		bytelist = []
		
		for j in range(len(NewGenConfigs[i])):
			tempbits = 0
			for k in range(len(NewGenConfigs[i][j])):
				if NewGenConfigs[i][j][k] == 1:
					tempbits += 2**(7-k)
			bytelist.append(tempbits)
		#Sanity Check
		#print(bytelist)

		#Send 8 byte info to the switch
		#ser.write(bytelist)
		#print (ser.readline())


		evaluateinput = [128,64,32,16,8,4,2,1]
		evaluateoutput = [128,64,32,16,8,4,2,1]

		for a in range(len(evaluateinput)):
			for b in range(len(evaluateoutput)):
				#set the first byte(input) into only one port opening
				bytelist[0] = evaluateinput[a]
				#set the last byte(output) into only one port opening
				bytelist[7] = evaluateinput[b]
				#sleep
				#Read current values, store into an output array

		#suppose we have an output result:
		Outputresult = np.random.rand(genes,genes)
		TransOutputresult = np.transpose(Outputresult)
		F = 0
		success = 0
		#Tolerance. if set 0.5, it considers any output that has more than 50% of the highest current as "non-distinguishable"
		threshold = 0.9
		#Criteria 1
		for a in range(len(Outputresult)):
			count = 0
			tempout = Outputresult[a]
			maxi = max(tempout)
			for b in range(len(Outputresult[a])):
				#If the read current is higher than the threshold, add 1 to the count
				if Outputresult[a,b]/maxi > threshold:
					count = count + 1
			#if only one output was HIGH for the given input, that's success!
			if count == 1:
				F = F + 3
			#if more than 1 output was HIGH for the given input, we give -1 for the number of outputs that were HIGH
			elif count > 1:
				F = F+ -1*count
			#if no output was HIGH for a particular input, we either have to lower the threshold, or just punish the fitness score
			elif count == 0:
				F = F - 10

		#Criteria 2
		#Do exactly the same but transposed matrix. Vertical check
		
		for a in range(len(Outputresult)):
			count = 0
			tempout = TransOutputresult[a]
			maxi = max(tempout)
			for b in range(len(Outputresult[a])):
				#If the read current is higher than the threshold, add 1 to the count
				if TransOutputresult[a,b]/maxi > threshold:
					count = count + 1
			#if only one output was HIGH for the given input, that's success!
			if count == 1:
				F = F + 3
			#if more than 1 output was HIGH for the given input, we give -1 for the number of outputs that were HIGH
			elif count > 1:
				F = F+ -1*count
			#if no output was HIGH for a particular input, we either have to lower the threshold, or just punish the fitness score
			elif count == 0:
				F = F - 10
		#Append the fitness score of that genome to the fitnessscore
		Fitnessscore.append(F)

		#count how many distinctions it made
		for a in range(len(Outputresult)):
			tempout = Outputresult[a]
			maxi = max(tempout)
			for l in range(len(Outputresult[a])):
				if Outputresult[a][l] == maxi:
					tempx = l
					tempy = a
			#now that the locaiton of max is found, transpose and check
			tempout = TransOutputresult[tempx]
			maxi = max(tempout)
			if TransOutputresult[tempx][tempy] == maxi:
				success = success + 1

		successrate.append(success)

		#Genome operation done
		genearray[m,i, :, :] = NewGenConfigs[i,:]
		outputarray[m,i, :, :]=Outputresult
		fitnessarray[m,i] = F
		successarray[m,i] = success




	winner = Fitnessscore.index(max(Fitnessscore))

	#Announcement
	print('The winner is the index' + str(winner))
	print(NewGenConfigs[winner])
	run = run + 1
	print('with a fitness score of ' + str(F))
	Hermafrodite = NewGenConfigs[winner]

	#Save the generation result
	SaveLib.saveMain(savedirectory, genearray, outputarray, fitnessarray, successarray)

	#Mutation
	#Winner remains = 1
	NewGenConfigs[0] = Hermafrodite

	#Mutate with 10% chance
	for i in range(1, 8):
		templist = Hermafrodite
		for j in range(genes):
			for k in range(genes):
				if(np.random.rand() < 0.2):
					if templist[j, k] == 1:
						templist[j, k] = 0
					elif templist[j, k] == 0:
						templist[j, k] = 1
		NewGenConfigs[i] = templist

	#complete random 
	for i in range(8,10):
		templist = np.random.rand(genes,genes)
	NewGenConfigs[i] = np.around(templist)
#Repeat until all generations meet 