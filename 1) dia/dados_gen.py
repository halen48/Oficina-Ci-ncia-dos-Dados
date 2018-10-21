import random

errado = True

estilo_musical = ["Jazz","Clássico","Funk","Pop","Folk","Rock","Techno","Samba","Axé","Pagode"]

#Praia;Acad;Estuda
rotina_musica = {
	"Jazz":	    [2,0,7],
	"Clássico": [4,0,6],
	"Funk":		[6,6,1],
	"Pop":		[4,4,4],
	"Folk":		[7,2,4],
	"Rock":		[2,6,5],
	"Techno":	[1,5,6],
	"Samba":	[5,0,3],
	"Axé":		[6,4,0],
	"Pagode":	[5,3,1]
}

#1 = 0.1%
#https://pt.wikipedia.org/wiki/Algoritmo_do_vizinho_mais_pr%C3%B3ximo
chance_musica_rnd = 100

def rotinaXmusica(rotina):
	if(random.randint(0,1000) < chance_musica_rnd):
		return estilo_musical[random.randint(0,len(estilo_musical)-1)]
	else:
		distancias = []
		for nome,estilo in rotina_musica.items():
			distancias.append((nome,sum([(x-y)**2 for x,y in zip(rotina,estilo)])))
		
		best_match = (min(distancias,key = lambda t:t[1]))
		
		
		return best_match[0]

	


numeros_m = ["Nenhum", "Um", "Dois", "Três", "Quatro", "Cinco", "Seis", "Sete"]
numeros_f = ["Nenhuma", "Uma", "Duas", "Três", "Quatro", "Cinco", "Seis", "Sete"]

modfier_mf = [" Vez", " Vez", " Vezes", " Vezes", " Vezes", " Vezes", " Vezes", " Vezes"]

modfier_n = [" Vezes", " Vez", " Vezes", " Vezes", " Vezes", " Vezes", " Vezes", " Vezes"]

numeros_ab = ["Nada", "hum", 'doiz', 'treix', 'cuatro', 'sinco', 'seiz', 'set']
modfier_ab = [' veis', ' ves']

aberrante = ["Apenas quando ", "Só quando "]
aberrante2 = [" está Sol", " está Chuva", " é feriado", " é final de semana", " não está chovendo"]

#Ele escreve 'Nenhuma Vez' ou "0" ou '0x' ou '0 Vezes'
n_dados = 100000
#1 = 0.1%
chance_de_numeral = 750
#1 = 0.1%
chance_aberrante = 3

if(not errado):
	f = open("dataset.csv",'w')
else:
	f = open("dataset.dat",'w')

if(not errado):
	f.write("CorrePraiaSemana;PraticaAcadSemana;FaculEstudaSemana;GeneroMusicalFavorito\n")
else:
	f.write("CorrePraiaSemana\x01PraticaAcadSemana\x01FaculEstudaSemana\x01GeneroMusicalFavorito\x23")

#================================================
def generate_string():
	string = ''
	numero = random.randint(0,7)
	if(random.randint(0,1000) < chance_aberrante):
		if(random.randint(0,1) != 0):
			#qualquer numero
			string = str(random.randint(8,40))
		else:
			#numero escrito errado
			string = numeros_ab[numero]
			if(random.randint(0,1) != 0):
				#+ 'veis' ou 'ves'
				string += modfier_ab[random.randint(0,1)]
			else:
				#+ 'vez' ou 'vezes'
				if(random.randint(0,1) != 0):
					string += modfier_n[numero]
	else:
		#numeral
		if(random.randint(0,1000) < chance_de_numeral):
			string = str(numero)
			if(random.randint(0,10) < 3):
				#Ex: 3x
				string += 'x'
			elif(random.randint(0,10) < 3):
				#Ex: 3 vezes
				string += modfier_n[numero]
		else:
		#extenso
			string = numeros_f[numero]
			if(random.randint(0,10) < 3):
				#Ex: Quatro vezes
				string += modfier_mf[numero]	
	return [numero,string]
#================================================

for i in range(0,n_dados):
	rotina = [generate_string(),generate_string(),generate_string()]
	if(not errado):
		f.write(rotina[0][1]+';'+rotina[1][1]+';'+rotina[2][1]+rotinaXmusica(rotina)+'\n')
	else:
		f.write(rotina[0][1]+'\x01'+rotina[1][1]+'\x01'+rotina[2][1]+'\x01'+rotinaXmusica([r[0] for r in rotina])+'\x23')