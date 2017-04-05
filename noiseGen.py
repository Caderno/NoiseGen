#Thiago Ledur Lima

import numpy as np, cv2, argparse, os
from tkinter import filedialog

############################################################
# definição de funções

#ruído Gaussiano
def gaussNoise(imagem, std):
	noise = np.zeros(imagem.shape)
	for i in range(imagem.shape[0]):
		for j in range(imagem.shape[1]):
			noise[i][j] = np.random.normal(0, std)
	return imagem + noise

#ruído Salt&Pepper
def saltpepperNoise(imagem, prob):
	spNoise = np.copy(imagem)
	for x in range(imagem.shape[0]):
		for y in range(imagem.shape[1]):
			rn = np.random.uniform(0,100)
			#pepper
			if (rn < float(prob/2)):
				spNoise[x][y] = 0
			#salt
			elif (rn > (100-prob/2)):
				spNoise[x][y] = 255
	return spNoise

############################################################
# parser de argumentos

parser = argparse.ArgumentParser()
parser.add_argument('-g', '--gauss', help='Aplica ruído Gaussiano.', dest='nG', type=float)
parser.add_argument('-sp', '--saltp', help='Aplica ruído Salt&Pepper.', dest='nSP', type=float)
parser.add_argument('-nd', '--nodir', help='Desativa a criação de diretórios com resultados.', dest='nodir', action='store_true', default=False)
args = parser.parse_args()

############################################################
# lógica do programa

files = filedialog.askopenfilenames()
if not files:
	exit(-1)

if not args.nodir:
	os.mkdir("Noise")

for filename in files:
	imgOriginal = cv2.imread(filename, 0)

	if args.nG is not None:
		if args.nG < 0:
			print("Valor incorreto para ruído gaussiano. Correto: valor>=0.")
		else:
			#aplica ruído gaussiano e salva a imagem
			imgGauss = gaussNoise(imgOriginal, args.nG)
			if not args.nodir:
				cv2.imwrite(os.path.join("Noise", "Gauss_" + str(args.nG) + "_" + filename.split("/")[-1]), imgGauss)
			else:
				cv2.imwrite("Gauss_" + str(args.nG) + "_" + filename.split("/")[-1], imgGauss)

	if args.nSP is not None:
		if args.nSP < 0 or args.nSP > 100:
			print("Valor incorreto para ruído salt&pepper. Correto: 0<=valor<=100.")
		else:
			#aplica ruído salt&pepper e salva a imagem
			imgSaltPepper = saltpepperNoise(imgOriginal, args.nSP)
			if not args.nodir:
				cv2.imwrite(os.path.join("Noise", "SaltPepper_" + str(args.nSP) + "_" + filename.split("/")[-1]), imgSaltPepper)
			else:
				cv2.imwrite("SaltPepper_" + str(args.nSP) + "_" + filename.split("/")[-1], imgSaltPepper)