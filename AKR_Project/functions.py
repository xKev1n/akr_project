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
					
					print(signature)
					print(signature_in_file)

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
						#print(data_in)
						dec_hash = int(hash, 16)						#Is same only for first cycle. Hashes don't match on signed documents.
					else:
						print("Signature in file doesn't match signature given by argument.")
						return False
				else:
					print("There is no signature in file, thus the verification process failed.")
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
