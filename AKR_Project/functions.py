from Crypto.PublicKey import RSA
from hashlib import sha512
import time

# Functions
def GenerateKeyPair():
	# function to generate a pair of public key, private key and modulo
	keyPair = RSA.generate(bits=1024)
	return keyPair


def formatTime(timestamp):
	year = timestamp[2:6]
	month = timestamp[6:8]
	day = timestamp[8:10]
	
	dictionary = {
	"year" : year,
	"month" : month,
	"day" : day}
	
	return dictionary


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


				start_index = data_in.find("/Signature:") + 12

				end_index = data_in.find("/ModDate")

				signature_in_file = data_in[start_index : end_index]
				print(signature_in_file)
				print(signature)
				if signature_in_file == signature:
					data_in = data_in.replace(data_in[data_in.find('b\"\\\\u2557b') : ], "")
					print(data_in)
					hash = str(sha512(data_in.encode('unicode-escape')).hexdigest())
					dec_hash = int(hash, 16)
				else:
					print("Signature in file doesn't match signature given by argument.")
					return False
		else:
			fi = open(file_name, "rb")
			data_in = fi.read()
			
			hash = str(sha512(data_in).hexdigest())
			dec_hash = int(hash, 16)
			fi.close()
	else:
		dec_hash = int.from_bytes(sha512(bytes(msg)).digest(), byteorder='big')
	
	hashFromSignature = pow(int(signature, 16), e, n)
	print("Hash received: {0}\nHash calculated: {1}\nHashes match: {2}\n".format(hex(dec_hash), hex(hashFromSignature), dec_hash == hashFromSignature))
		
	if dec_hash == hashFromSignature:
		return True
	else:
		return False
