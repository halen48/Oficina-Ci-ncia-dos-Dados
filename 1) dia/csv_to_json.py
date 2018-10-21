import csv
import json

numeros_m = ["nenhum", "um", "dois", "três", "quatro", "cinco", "seis", "sete"]
numeros_f = ["nenhuma", "uma", "duas", "três", "quatro", "cinco", "seis", "sete"]
numeros_err = ["nada", "hum", 'doiz', 'treix', 'cuatro', 'sinco', 'seiz', 'set']
vezes = [' vez', ' vezes', ' veis', ' ves']

estilo_musical = ["Axé","Clássico","Folk","Funk","Jazz","Pagode","Pop","Rock","Samba","Techno"]

def clean(value):
	'''
	Possiveis valores:
	[Numero]x;
	[Numero]
	[String]
	[Numero] Vez/Vezes
	[String] Vez/Vezes

	Queremos converter tudo para [Numero]
	'''
	#input(value)
	value = value.lower()
	if('x' in value): 
		#'x' está sempre no final
		value = value[:-1]
	elif([True for x in vezes if (value).find(x) != -1]):
		# limpa qualquer informação adjacente ao numero
		value = value.split(' ')[0].lower()
	index_m = -1
	index_f = -1
	index_err = -1
	try:
		#procura por numeros 'masculino'
		index_m = numeros_m.index(value)
	except ValueError:
		try:
			#procura por numeros 'feminino'
			index_f = numeros_f.index(value)
		except ValueError:
			try:
				#procura por numeros 'errados'
				index_err = numeros_err.index(value)
			except ValueError:
				#eh importante notar que aqui, o valor
				#'treix' pode estar como 'trei'
				#caso contrário, value é um número
				return 3 if(value.find('trei')!=-1) else int(value)
	#caso contrario, verifica qual dos arrays
	#o número está relacionado
	return index_f if(index_m == -1) else index_m
	
	return int(value)


try:
	arq_csv = open('dataset.csv', 'r')
except:
	arq_raw = open('dataset.dat')
	arq_csv = open('dataset.csv',"w+")
	arq_csv.write( arq_raw.read().replace("\x01",";").replace("#","\n"))
	arq_raw.close()
	arq_csv.close()
	arq_csv = open('dataset.csv' , 'r')

arq_json = open('dataset.json', 'w',encoding="utf8")

campos = ["CorrePraiaSemana","PraticaAcadSemana","FaculEstudaSemana","GeneroMusicalFavorito"]
f = csv.DictReader(arq_csv, campos,delimiter=';')

#A primeira linha contem as informacoes das colunas, então devemos pular
next(f)

clean_csv = []

for row in f: #para cada linha
	new_row = row
	for c in campos[:-1]: #para cada campo do csv, exceto o ultimo
		new_row[c] = clean(new_row[c])
	new_row["GeneroMusicalFavorito"] = estilo_musical.index(new_row["GeneroMusicalFavorito"])
	clean_csv.append(new_row)

arq_json.write(json.dumps([row for row in clean_csv], ensure_ascii=False))

arq_csv.close()
arq_json.close()