def obter_dados():

	diretorio = 'C:/Users/Gabriel Santos/Desktop/Selenium - Python/'
	with open(diretorio + "reviews.txt", 'r', encoding='latin-1', sep="\t" ) as arquivo_texto:
		dados = arquivo_texto.read().split('\n')

	return dados


def RemoveStopWords(instancia):
    
    stopwords = set(nltk.corpus.stopwords.words('portuguese'))
    palavras = [i for i in instancia.split() if not i in stopwords]
    return (" ".join(palavras))

def Stemming(instancia):
    stemmer = nltk.stem.RSLPStemmer()
    palavras = []
    for w in instancia.split():
        palavras.append(stemmer.stem(w))
    return (" ".join(palavras))


def Preprocessing(instancia):
    stemmer = nltk.stem.RSLPStemmer()
    instancia = re.sub(r"http\S+", "", instancia).lower().replace('.','').replace(';','').replace('-','').replace(':','').replace(')','')
    stopwords = set(nltk.corpus.stopwords.words('portuguese'))
    palavras = [stemmer.stem(i) for i in instancia.split() if not i in stopwords]
    return (" ".join(palavras))


def tratamento_dos_dados(dados):
    dados_tratados = []

    
    for dado in dados:
    	if len(dado.split(";")) == 2 and dado.split(";")[1] != "":
    		
    		comentario = Preprocessing(dado.split(";")[0])
    		avaliacao = dado.split(";")[1]

    		comentario = comentario.strip(" ") #removendo espaços    		
    		avaliacao = avaliacao.strip(" ") #removendo espaços

    		dados_tratados.append([comentario, avaliacao])

    #print(dados_tratados)
    return dados_tratados


def dividir_dados_para_treino_e_validacao(dados):
    quantidade_total = len(dados) #recupera a quantidade total de dados
    percentual_para_treino = 0.75 #percentual de treino
    
    treino = []
    validacao = []

    for indice in range(0, quantidade_total):
        if indice < quantidade_total * percentual_para_treino:
            treino.append(dados[indice])
        else:
            validacao.append(dados[indice])

    return treino, validacao


def pre_processamento():
    dados = obter_dados()
    dados_tratados = tratamento_dos_dados(dados)
    return dividir_dados_para_treino_e_validacao(dados_tratados)



def realizar_treinamento(registros_de_treino, vetorizador):
    treino_comentarios = [registro_treino[0] for registro_treino in registros_de_treino]
    treino_avaliacoes = [registro_treino[1] for registro_treino in registros_de_treino]

    treino_comentarios = vetorizador.fit_transform(treino_comentarios)

    return BernoulliNB().fit(treino_comentarios, treino_avaliacoes)



def exibir_resultado(valor):
    frase, resultado = valor
    resultado = "Frase positiva" if resultado[0] == '1' else "Frase negativa"
    
    print(frase,": ",resultado) 


def analisar_frase(classificador, vetorizador, frase):
    return frase, classificador.predict(vetorizador.transform([frase]))


def realizar_avaliacao_simples(registros_para_avaliacao):
    avaliacao_comentarios = [registro_avaliacao[0] for registro_avaliacao in registros_para_avaliacao]
    avaliacao_respostas   = [registro_avaliacao[1] for registro_avaliacao in registros_para_avaliacao]

    total = len(avaliacao_comentarios)
    acertos = 0

    for indice in range(0, total):
        resultado_analise = analisar_frase(classificador, vetorizador, avaliacao_comentarios[indice])
        frase, resultado = resultado_analise
        acertos += 1 if resultado[0] == avaliacao_respostas[indice] else 0

    return acertos * 100 / total


def realizar_avaliacao_completa(registros_para_avaliacao):
    avaliacao_comentarios = [registro_avaliacao[0] for registro_avaliacao in registros_para_avaliacao]
    avaliacao_respostas   = [registro_avaliacao[1] for registro_avaliacao in registros_para_avaliacao]

    total = len(avaliacao_comentarios)
    verdadeiros_positivos = 0
    verdadeiros_negativos = 0
    falsos_positivos = 0
    falsos_negativos = 0

    for indice in range(0, total):
        resultado_analise = analisar_frase(classificador, vetorizador, avaliacao_comentarios[indice])
        frase, resultado = resultado_analise
        if resultado[0] == '0':
            verdadeiros_negativos += 1 if avaliacao_respostas[indice] == '0' else 0
            falsos_negativos += 1 if avaliacao_respostas[indice] != '0' else 0
        else:
            verdadeiros_positivos += 1 if avaliacao_respostas[indice] == '1' else 0
            falsos_positivos += 1 if avaliacao_respostas[indice] != '1' else 0

    return ( verdadeiros_positivos * 100 / total, 
             verdadeiros_negativos * 100 / total,
             falsos_positivos * 100 / total,
             falsos_negativos * 100 / total
           )



#Recuperar páginas com produtos para treinar 
def busca_comentario(url):
	
	lista_comentarios = []
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')

	comentarios = soup.find_all('div', class_='sd-review-content') #tabela com todas as opiniões
	
	#qtd_comentarios = (len(comentarios))
	
	for i in range(1, 5):
		
		comentario = comentarios[i].div.get_text()
		#tratando textos recuperados
		comentario = comentario.split(':') # separando texto "opinião geral"
		comentario = comentario[1]
		

		comentario = comentario.strip(" ") # removendo espaços no inicio e no final do comentário
		comentario = re.sub(r'^ |"$', '', comentario)
		comentario = re.sub(r'^"|"', '', comentario)
		comentario = re.sub(r'^\n|\n', '', comentario)

		lista_comentarios.append(comentario) #salvando comentarios em lista


	return lista_comentarios
	

##################### testando manualmente #########################

comentarios = busca_comentario("https://www.kabum.com.br/produto/102746/mem-ria-xpg-spectrix-d41-tuf-rgb-8gb-3000mhz-ddr4-cl16-ax4u300038g16-sb41")

registros_de_treino, registros_para_avaliacao = pre_processamento()
vetorizador = CountVectorizer(binary = 'true')
classificador = realizar_treinamento(registros_de_treino, vetorizador)

print("#-------------------------------------------#")
print("#-------------------------------------------#")

#for comentario in comentarios:
#	exibir_resultado( analisar_frase(classificador, vetorizador, comentario))

exibir_resultado( analisar_frase(classificador, vetorizador, "Não gostei do produto, me trouxe muitos problemas"))
exibir_resultado( analisar_frase(classificador, vetorizador, "Não funcionou"))
exibir_resultado( analisar_frase(classificador, vetorizador, "Muito ruim"))
exibir_resultado( analisar_frase(classificador, vetorizador, "Adorei o produto, funcionou perfeitamente"))

percentual_acerto = realizar_avaliacao_simples(registros_para_avaliacao)
informacoes_analise = realizar_avaliacao_completa(registros_para_avaliacao)
verdadeiros_positivos,verdadeiros_negativos,falsos_positivos,falsos_negativos = informacoes_analise


print("#-------------------------------------------#")
print("#-------------------------------------------#")

print("O modelo teve uma taxa de acerto de", percentual_acerto, "%")

print("Onde", verdadeiros_positivos, "% são verdadeiros positivos")
print("e", verdadeiros_negativos, "% são verdadeiros negativos")

print("e", falsos_positivos, "% são falsos positivos")
print("e", falsos_negativos, "% são falsos negativos")

print("#-------------------------------------------#")
print("#-------------------------------------------#")

