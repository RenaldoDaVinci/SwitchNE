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
from instrument import Keith2400
from instrument import PlotBuilding as PlotBuilder
import serial
import SaveLibrary as SaveLib

#open the set up files, this is not fully incorporated yet (needs to figure out how to sort out the each procedures)
exec(open("setup.txt").read())
#setup keithley
keithley = Keith2400.Keithley_2400('keithley', 'GPIB0::11')
#set the compliance current
keithley.compliancei.set(CompI)

#in case it's set way too high, scratch the whole process
if (Compv > 4):
	generations = 0
	genes = 0
	devs = 0
	genomes = 0

keithley.compliancev.seet(CompV)
#set the voltage (in volts)
keithley.volt.set(Volts)

#Initialize the serial connection to the arduino
ser = serial.Serial(port='/dev/cu.usbmodem1411',baudrate=9600, bytesize=8, parity='N', stopbits=1, write_timeout = 10)
#Initialize the directory to save the files
savedirectory = SaveLib.createSaveDirectory(filepath, name)
#generate necessary arrays to save the datas


genearray = np.zeros((generations, genomes, genes, devs))
outputarray = np.zeros((generations, genomes, devs, devs))
fitnessarray = np.zeros((generations, genomes))
successarray = np.zeros((generations, genomes))

#define the initial switches
array1 = np.random.rand(genomes,genes,devs)
#said arrays contain random value from 0 to 1, round it so it's a same array with binary bits
NewGenConfigs = np.around(array1)

mainFig = PlotBuilder.MainfigInit(genes = genes, generations = generations)

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

		#Send 8 byte info to the switch, it is configured in a certain interconnectivity
		PlotBuilder.UpdateSwitchConfig(mainFig, array = NewGenConfigs[i])
		ser.write(bytelist)
		#print (ser.readline())
		evaluateinput =[]
		evaluateoutput = []

		#Make list = [128,64,32,16,8,4,2,1]

		for a in range(devs):
			evaluateinput.append(2**(7-a))
			evaluateoutput.append(2**(7-a))


		for a in range(len(evaluateinput)):
			for b in range(len(evaluateoutput)):
				#set the byte(input) into only one port opening
				bytelist[InputElec-1] = evaluateinput[a]
				#set the last byte(output) into only one port opening
				bytelist[OutputElec-1] = evaluateinput[b]
				#send a bytelist where the first and the last lines are modified, input and output path
				ser.write(bytelist)
				#I like sleeping
				time.sleep(0.3)

				#Read current values, store into an output array
				current = keithley.curr.get()
				Outputresult[a][b] = current
		PlotBuilder.UpdateIout(mainFig, array = Outputresult)

		F = 0
		success = 0
		#Tolerance. if set 0.5, it considers any output that has more than 50% of the highest current as "non-distinguishable"
		threshold = tolerance
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

	print('with a fitness score of ' + str(F))
	Hermafrodite = np.copy(NewGenConfigs[winner])

	#Save the generation result
	SaveLib.saveMain(savedirectory, genearray, outputarray, fitnessarray, successarray)

	#Mutation
	#Winner remains = 1
	NewGenConfigs[0] = np.copy(Hermafrodite)
	PlotBuilder.UpdateBestConfig(mainFig, array = Hermafrodite)

	#Mutate with 10% chance
	for i in range(1, int(genome*4/5)):
		templist = np.copy(Hermafrodite)
		duplicate = True
		while(duplicate):
			for j in range(genes):
				for k in range(devs):
					if(np.random.rand() < 0.2):
						if templist[j, k] == 1:
							templist[j, k] = 0
						elif templist[j, k] == 0:
							templist[j, k] = 1
			stack = 0
			for a in range(len(genearray)):
				for b in range(len(genearray[a])):
					if np.array_equal(templist, genearray[a][b]):
						stack = stack + 1
			if stack < 1:
				NewGenConfigs[i] = np.copy(templist)
				duplicate = False

	#complete random 
	for i in range(int(genome*4/5),genome):
		duplicate = True
		while(duplicate):
			templist = np.random.rand(genes,devs)
			templist = np.around(templist)
			stack = 0
			for a in range(len(genearray)):
				for b in range(len(genearray[a])):
					if np.array_equal(templist, genearray[a][b]):
						stack = stack + 1
			if stack < 1:
				NewGenConfigs[i] = np.copy(templist)
				duplicate = False		

#Repeat until all generations meet 
#don't know why I need this. But the window disappears without this command.
PlotBuilder.finalMain(mainFig)