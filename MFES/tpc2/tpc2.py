from z3 import *

# retorna a matriz no formato numeral, sem especificação de condicoes
def getmatrix(file):
	fo = open(file).readlines()
	filas = [elem.rstrip() for elem in fo]
	lista = []
	matrixOG = []

	size = len([elem for elem in filas[0] if elem.isdigit()])
	
	for elem in filas:
		lista = []
		for word in elem:

			if word.isdigit():
				lista.append(word)
		matrixOG.append(lista)

	return matrixOG,size

def defineRestrictions(matrix):
	linha = 0
	coluna = 0 
	for lines in matrix:
		coluna=0
		for elem in lines:
			if elem.isdigit() and int(elem)>0:
				s.add(x[linha][coluna]==int(elem))
			coluna+=1
		linha+=1

def getConds(file):
	fo = open(file).readlines()
	filas = [elem.rstrip().replace('.','') for elem in fo]
	print(filas)

	linha = 0


	for lines in filas:
		coluna=0
		for elem in lines:
			if elem.isdigit():
				coluna+=1
			
			if elem=='>':
				s.add(x[linha][coluna-1] > x[linha][coluna])	
		
			elif elem=='<':
				s.add(x[linha][coluna-1] < x[linha][coluna])
			elif elem=='_': #elemento atual ser inferior ao elemento da linha acima
				s.add(x[linha][coluna-1] < x[linha-1][coluna-1])
			elif elem=='^': #elemento atual ser superior ao elemento da linha acima
				s.add(x[linha][coluna-1] > x[linha-1][coluna-1])
				
			
		linha+=1



s = Solver()

x = {}


def main():
	matrix, N = getmatrix("example.txt")

	for i in range(N):
		x[i] = {}
		for j in range(N):
			x[i][j] = Int('x'+str(i)+str(j))           # declaração de variáveis
			s.add(And(1<= x[i][j], x[i][j]<=(N)))    # restrições de valor

# restrições linha
	for i in range(N):
		s.add(Distinct([x[i][j] for j in range(N)]))

# restricoes coluna
	for j in range(N):
		s.add(Distinct([x[i][j] for i in range(N)]))
	
	defineRestrictions(matrix)
	getConds("example.txt")


	print(s.check())
	if s.check() == sat:
		m = s.model()
		for i in range(N):
			print([ m[x[i][j]].as_long() for j in range(N) ])
	else:
		print("não tem solução")


main()
