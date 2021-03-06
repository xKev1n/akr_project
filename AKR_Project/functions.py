from Crypto.PublicKey import RSA			#pip install pycryptodome
from hashlib import sha512
from PyPDF2 import PdfFileReader
import time
from tika import parser 					# pip install tika

from collections import namedtuple


# Functions
def GenerateKeyPair(name):
	# function to generate a pair of public key, private key and modulo
	keyPair = RSA.generate(bits=1024)
	save_keypair_to_file(name, keyPair)
	return keyPair

def ShowKeys(entity):
	print (entity.name+'\'s keys:')
	print(f"Public key:  (e={hex(entity.keyPair.e)})")
	print(f"Private key: (d={hex(entity.keyPair.d)})")
	print(f"Modulo: (n={hex(entity.keyPair.n)})")

def formatTime(timestamp):
	year = timestamp[2:6]
	month = timestamp[6:8]
	day = timestamp[8:10]
	
	dictionary = {
	"year" : year,
	"month" : month,
	"day" : day}
	
	return dictionary


def save_keypair_to_file(name, keypair):
	contains = False 
	with open("keypairs.txt","r") as fo:
		if name in fo.read() :
			contains = True
	if not contains:
		with open("keypairs.txt","a") as f:
			f.write(name+':d'+str(keypair.d)+':e'+str(keypair.e)+':n'+str(keypair.n)+'\n')
	else:
		print ("Keypair from this entity is already saved in the file.")


def get_keypair_from_file(name):
	with open("keypairs.txt","r") as f:
		data = f.read()

		key_info = ''
		key_info = data[data.find(name) : data.find('\n', data.find(name))]
		
		d = int(key_info[key_info.find(':d')+2 : key_info.find(':e')])
		e = int(key_info[key_info.find(':e')+2 : key_info.find(':n')])
		n = int(key_info[key_info.find(':n')+2 : ].removesuffix('\n'))

		keyPair = namedtuple('keyPair', 'e d n')
		return keyPair(e, d, n)


def VerifyCertificate(certificate, entity):
	if entity.EntityHasCertificate():
		actual_time = time.time()
		validity = True
		if certificate != entity.certificate or certificate["Owner"] != entity.name or certificate["ValidTo"] < actual_time or certificate["ValidFrom"] > actual_time or certificate["Public_Key"] != hex(entity.keyPair.e) or certificate["From_Authority"] != entity.certificate["From_Authority"]:
			validity = False
			print("Certificate is invalid!")
			return validity
		print("Certificate is valid.")
		return validity
	else:
		print("Entity {0} doesn't have any certificates".format(entity.name))

def find_sig_in_file(data):
	if data.find('\\u2557') != -1 or data.find('\\u255d') != -1:
		start_index = data.find("/Signature:") + 12

		end_index = data.find("/ModDate")

		signature_in_file = data[start_index : end_index]

		return signature_in_file
	else:
		return None

def VerifySignature(msg, signature, e, n):
	# RSA verification of the signature
	# User will send Public Key to Authority to verify it
	# Authority will sign the Public Key with its private key

	if type(msg) == str:
		
		file_name = msg
		type_of_file = file_name[file_name.find("."):]	

		if type_of_file == ".txt":
			with open(file_name, "r") as fi:
				data_in = fi.read()
				
				signature_in_file = find_sig_in_file(data_in)

				if signature_in_file != None:

					if signature_in_file == signature:
						full_data = data_in
						data_in = data_in.replace(data_in[data_in.find('b\"\\\\u2557b') : ], "")		#Hashes not match for some reason...

						
						with open(file_name, "w") as f:
							f.write(data_in)
						with open(file_name, "rb") as f:
							data_in = f.read()
						with open(file_name, "w") as f:
							f.write(full_data)					

						hash = str(sha512(data_in).hexdigest())
						dec_hash = int(hash, 16)						#Is same only for first cycle. Hashes don't match on signed documents.
					else:
						print("Signature in file doesn't match signature given by argument.")
						return False
				else:
					print("There is no signature in file, thus the verification process failed.")
					return False
		else:
			with open(file_name, "rb") as fi:

				pdf_reader = PdfFileReader(fi)

				metadata = pdf_reader.getDocumentInfo()
				raw = parser.from_file(file_name)
				data_in = raw['content']

				if type(data_in) == str:
					data_in = data_in.translate(str.maketrans('', '', ' \n\t\r'))
					data_in = data_in.encode()

				if '/Signature' in metadata:
					hash = str(sha512(data_in).hexdigest())
					dec_hash = int(hash, 16)
				else:
					print("Document is not signed")
					return False
	else:
		dec_hash = int.from_bytes(sha512(bytes(msg)).digest(), byteorder='big')
	

	hashFromSignature = pow(int(signature, 16), e, n)					#PKs are different for every rerun. 
	print("Hash received: {0}\nHash calculated: {1}\nHashes match: {2}\n".format(hex(dec_hash), hex(hashFromSignature), dec_hash == hashFromSignature))
		
	if dec_hash == hashFromSignature:
		return True
	else:
		return False
