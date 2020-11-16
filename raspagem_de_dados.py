import csv
import re
import requests
from bs4 import BeautifulSoup
		

def raspagem_dos_dados_para_treinamento(lista_url):
	lista_comentarios=[]
	for url in lista_url:
		r = requests.get(url)
		soup = BeautifulSoup(r.content, 'html.parser')

		comentarios = soup.find_all('div', class_='sd-review-content') #tabela com todas as opiniões
		pontos_avaliados = soup.find_all('strong', class_='sd-review-rating') #tabela com todas as estrelas

		qtd_comentarios = (len(comentarios))

		for i in range(1, qtd_comentarios):

			comentario = comentarios[i].div.get_text()
			avaliacao = pontos_avaliados[i].text
			
			avaliacao = int(avaliacao) #transformando avaliação em  número inteiro


			if avaliacao >= 4:
				avaliacao = "positivo"
			elif avaliacao == 3:
				avaliacao = "neutro"
			elif avaliacao >= 1 and avaliacao <=2:
				avaliacao = "negativo"
			else:
				avaliacao = "neutro"

			#tratando textos recuperados
			comentario = comentario.split(':') # separando texto "opinião geral"
			comentario = comentario[1]
			
			 
			comentario = comentario.strip(" ") # removendo espaços no inicio e no final do comentário
			comentario = re.sub(r'^ |"$', '', comentario)
			comentario = re.sub(r'^"|"', '', comentario)
			comentario = re.sub(r'^\n|\n', '', comentario)


			comentarios_geral = {comentario:avaliacao}
			lista_comentarios.append(comentarios_geral) #salvando comentarios em lista


	#criando excel com os comentários
	with open('review.csv', 'w', newline='') as file:
		writer = csv.writer(file, delimiter=';')

		writer.writerow(["Texto", "Classificador"])
		for c in lista_comentarios:
		
			for k,v in c.items():
				writer.writerow([k, v])  
	
	#print(lista_comentarios)


#lista de links de produtos do site da KaBum!
lista_url = [
			'https://www.kabum.com.br/produto/69273/cooler-fan-c3-tech-f7-100-bk-storm-12cm-c3t',
			'https://www.kabum.com.br/produto/100220/cooler-fan-corsair-af120-white-single-co-9050079', 
			'https://www.kabum.com.br/produto/99232/climatizador-de-ar-elgin-smart-frio-110v-branco-com-ionizador-que-elimina-99-de-virus-e-bact-rias-fsfn04n1ia', 
			'https://www.kabum.com.br/produto/104811/climatizador-de-ar-philco-pcl1qf-quente-e-frio-220v-56252014-', 
			'https://www.kabum.com.br/produto/104752/placa-de-video-asus-tuf3-nvidia-geforce-gtx-1660-s-',
			'https://www.kabum.com.br/produto/129451/processador-amd-ryzen-5-5600x-cache-35mb-3-7ghz-',
			'https://www.kabum.com.br/produto/128561/console-microsoft-xbox-series-s-512gb-branco-r-',
			'https://www.kabum.com.br/produto/85197/ssd-kingston-a400-240gb-sata-leitura-500mb-s-g-',
			'https://www.kabum.com.br/produto/121164/mouse-gamer-razer-deathadder-v2-mini-chroma-opti-',
			'https://www.kabum.com.br/produto/111540/notebook-asus-amd-ryzen-5-3500u-vega-8-8gb-1tb-',
			'https://www.kabum.com.br/produto/113993/microfone-condensador-usb-husky-howl-hmc-uh',
			'https://www.kabum.com.br/produto/94938/ssd-wd-green-240gb-sata-leitura-545mb-s-gravac-',
			'https://www.kabum.com.br/produto/79112/fonte-evga-600w-80-plus-white-100-w1-0600-k',
			'https://www.kabum.com.br/produto/115067/webcam-husky-snow-full-hd-1080p-25fps-com-ilum-',
			'https://www.kabum.com.br/produto/104667/headset-gamer-razer-kraken-x-lite-multi-platform-',
			'https://www.kabum.com.br/produto/102649/mouse-gamer-logitech-g403-hero-16k-rgb-lightsync-6-bot-es-16000-dpi-910-005631',
			'https://www.kabum.com.br/produto/99137/mousepad-gamer-redragon-pisces-speed-m-dio-330x260mm-p016',
			'https://www.kabum.com.br/produto/97092/mouse-sem-fio-gamer-logitech-g305-hero-lightspeed-6-bot-es-12000-dpi-910-005281',
			'https://www.kabum.com.br/produto/120485/mouse-gamer-logitech-g203-rgb-lightsync-6-bot-es-8000-dpi-azul-910-005795',
			'https://www.kabum.com.br/produto/100723/mousepad-gamer-havit-m-dio-300x700mm-hv-mp861',
			'https://www.kabum.com.br/produto/59450/mouse-gamer-multilaser-2400dpi-7-bot-es-preto-e-verde-mo208',
			'https://www.kabum.com.br/produto/71996/mouse-gamer-redragon-centrophorus-v3-3200dpi-6-bot-es-e-8-ajustes-de-peso-usb-m601-3',
			'https://www.kabum.com.br/produto/102651/mouse-sem-fio-gamer-logitech-g703-hero-16k-lightspeed-recarreg-vel-rgb-lightsync-6-bot-es-16000-dpi-910-005639',
			'https://www.kabum.com.br/produto/96628/drive-asus-gravador-externo-cd-dvd-zendrive-u9m-ultra-slim-1-tipo-c-1-tipo-a-windows-e-mac-nero-backitup-sdrw-08u9m-u-blk-g-as',
			'https://www.kabum.com.br/produto/113606/gravador-de-dvd-externo-bluecase-slim-usb-2-0-bgde03case',
			'https://www.kabum.com.br/produto/96629/drive-asus-gravador-externo-cd-dvd-zendrive-u9m-ultra-slim-1-tipo-c-1-tipo-a-windows-e-mac-nero-backitup-sdrw-08u9m-u-sil-g-as',
			'https://www.kabum.com.br/produto/65472/drive-lite-on-gravador-externo-de-dvd-8x-slim-writer-ebau108-preto-',
			'https://www.kabum.com.br/produto/111085/ssd-gigabyte-256gb-sata-leituras-520mb-s-e-grava-es-500mb-s-gp-gstfs31256gtnd',
			'https://www.kabum.com.br/produto/95651/roteador-facebook-hotspot-multilaser-300mbps-duas-antenas-preto-re300',
			'https://www.kabum.com.br/produto/114904/kit-gamer-elg-combo-4-em-1-striker-teclado-mouse-mousepad-headset-cgsr41',
			'https://www.kabum.com.br/produto/15031/kit-gamer-razer-teclado-cyclosa-mouse-abyssus-1800dpi-rz84-00410200-b1z1',

			]
