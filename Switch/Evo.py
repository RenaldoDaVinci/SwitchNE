'''
from numpy import * 
x = range(15)
x = reshape(x,(5,3)) 

print(x)
'''
import numpy as np

class GeneMatrix(object):

	def __init__(self, genes, genomes):
		self.genes = genes
		self.genomes = genomes
		#bigdaddy = np.random.rand(genes,genomes,genomes)
		#bigmommy = np.around(bigdaddy)
		

		#self.pool = random.rand(genes,genomes)
		#self.fitness = np.empty(genomes)