import som_tf
import tensorflow as tf
import numpy as np
import csv

import pymongo

'''
Objetivo: Ver o perfil de cada grupo
'''

campos = ["CorrePraiaSemana","PraticaAcadSemana","FaculEstudaSemana","GeneroMusicalFavorito"]
estilo_musical = ["Axé","Clássico","Folk",
				  "Funk","Jazz","Pagode",
				  "Pop","Rock","Samba",
				  "Techno"]

with tf.device("cpu:0"):
	#===============================================
	#conecta ao banco de dados
	#==============================================
	client = pymongo.MongoClient('localhost', 27017)
	db = client['Exatec2018']

	tamanho_banco = db.Pessoas.find().count()
	#==============================================
	#Inicializada o TF
	#==============================================
	sess = tf.InteractiveSession()

	#treinar com 25% dos dados do banco
	num_training = int(tamanho_banco*0.25)
	#Será criada 4x4 classes (16 ao todo)
	#Nós podemos reduzir para 3 (3x3) e criar uma aproximação de 9 grupos musicais,
	#já que possuimos 10 grupos
	dimensões_do_mapa  = 4

	s = som_tf.SOM( (4,), dimensões_do_mapa, num_training, sess )

	sess.run(tf.global_variables_initializer())
	#==============================================
	coleção = []
	for i in range(0,len(estilo_musical)):
		'''
		iremos treinar o SOM 25k vezes (25% de 10k)
		dessa forma, como possuimos 10 estilos musicais
		iremos selecionar 2,5k de amostras de cada estilo
		
		é importante notar aqui, que esse valor depende
		do menor valor desejado. Por exemplo, em nosso banco,
		o menor grupo em relação a estilo musical são os das
		pessoas que escutam Axé: 3,4k e o maior é ~13k (Acho que era Folk)
		Logo, é possível selecionar 2,5k de amostras para cada estilo.

		Existem tecnicas estatísticas para redução de dimensionalidade, como
		PCA: 
		*https://pt.wikipedia.org/wiki/An%C3%A1lise_de_componentes_principais
		Análise de Valores aberrantes: 
		*https://pt.wikipedia.org/wiki/Outlier
		*https://pt.wikipedia.org/wiki/Diagrama_de_caixa

		É importante notar que estas técnicas devem ser adotadas em casos específicos,
		pois muitas vezes a 'sujeira' pode ser parte do nosso problema.
		'''
		dados = []
		for documento in db.Pessoas.find({campos[3]:i}):
			#Converte o JSON para a entrada da rede
			dados.append([documento[campos[0]],
						  documento[campos[1]],
						  documento[campos[2]],
						  i])
		coleção.append(dados)
	#========================
	for dados in coleção:
		for j in range(int(num_training/len(estilo_musical))):
			rnd_ind = np.random.randint(0, len(dados))
			s.train(dados[rnd_ind])
	#===============================================
	#classificacao
	#===============================================
	dados_classificados = []
	for dados in coleção:
		for documento,classe in zip(dados, s.get_batch_winner(dados)[0]):
			#classificados[classe].append(documento)
			documento.append(classe)
			dados_classificados.append(documento)
	
	grupos = [None]*(dimensões_do_mapa*dimensões_do_mapa)
	for dado in dados_classificados:
		if(not grupos[dado[4]]):
			grupos[dado[4]] = []
		grupos[dado[4]].append([dado[0],dado[1],dado[2],dado[3]])
	#===============================================
	#análise
	#histograma de cada valor/grupo
	#cada grupo possui 4 histogramas (16*4 = 64 ao todo)
	#===============================================
	Histograma_Grupos = [None]*(dimensões_do_mapa*dimensões_do_mapa)
	for i in range(len(Histograma_Grupos)):
		#no ultimo campo, sera armazenado o tamanho do grupo
		Histograma_Grupos[i] = [None]*(len(campos)+1)

	for i_grupo, grupo in enumerate(grupos):
		Histograma_Grupos[i_grupo][4] = len(grupo)
		for documento in grupo:
			#Para os 3 primeiros histogramas,
			#valores entre 0~7 estão ok, fora disso são aberrantes
			#para o 4º histograma, os valores variam de 0 até len(estilo_musical)
			for i in range(0,3):
				if(not Histograma_Grupos[i_grupo][i]):
					Histograma_Grupos[i_grupo][i] = [0]*9 #8 valores + aberrante
				indice = documento[i] if (documento[i] >= 0 and documento[i] <= 7) else 8
				Histograma_Grupos[i_grupo][i][indice] += 1
			#===================================================
			if(not Histograma_Grupos[i_grupo][3]):
				Histograma_Grupos[i_grupo][3] = [0]*len(estilo_musical)
			Histograma_Grupos[i_grupo][3][documento[3]] += 1


	for i_grupo, grupo in enumerate(Histograma_Grupos):
		f = open("Grupo "+ str(i_grupo)+".txt","w+")
		f.write("*************************************\n")
		f.write("Grupo "+str(i_grupo)+" ("+str(grupo[4])+" Pessoas):\n")
		f.write("*************************************\n")
		for i,c in enumerate(campos):
			f.write("=========="+c+"==========\n")
			for index,valor in enumerate(grupo[i]):
				if(i < 3):
					f.write(str(index)+":") if (index < 8) else f.write("aberrantes:")
				else:
					f.write(estilo_musical[index]+":")
				f.write(" "+str(valor)+"("+str(round(100*valor/grupo[4],2))+"%)\n")

	#===============================================
	#exportar
	#===============================================
	
	for i_grupo, grupo in enumerate(grupos):
		export = open('Grupo'+ str(i_grupo)+ '.csv','w+')
		f = csv.writer(export, delimiter=';')
		f.writerow(campos)
		for documento in grupo:
			f.writerow(documento)
