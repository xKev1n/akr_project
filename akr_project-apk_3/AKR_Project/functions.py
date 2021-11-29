from Crypto.PublicKey import RSA  					# pip install pycryptodome
from hashlib import sha512
from PyPDF2 import PdfFileReader					# pip install PyPDF2
import time
from tika import parser  							# pip install tika
from collections import namedtuple
import json



# Functions
def GenerateKeyPair(id, name):
    # function to generate a pair of keys (public key, private key) and modulus
    keyPair = RSA.generate(bits=1024)
    save_keypair_to_file(id, str(name), keyPair)		# Saving the keypair to file
    return keyPair


def ShowKeys(entity):
	# Function to print key details of entity
    print(entity.name + '\'s keys:')
    print(f"Public key:  (e={hex(entity.keyPair.e)})")
    print(f"Private key: (d={hex(entity.keyPair.d)})")
    print(f"Modulo: (n={hex(entity.keyPair.n)})")


def formatTime(timestamp):
	# Function to split timestamp into years, months and days
	# Returns time in a dictionary
    year = timestamp[2:6]
    month = timestamp[6:8]
    day = timestamp[8:10]

    dictionary = {
        "year": year,
        "month": month,
        "day": day}

    return dictionary


def does_contain(name, file):
	# Function to check if given name is contained in file
    if name in file.read():
        return True
    else:
        return False


def save_keypair_to_file(id, name, keypair):
	# A Function to save a keypairs to a file
	contains = False
	with open("keypairs.json", "r", encoding="ISO-8859-1") as fo:
		if does_contain(name, fo):
			contains = True						# Entity already has saved keypair
	if not contains:		
		data = {}
		with open("keypairs.json", "r") as f:
			data = json.load(f)

		with open("keypairs.json", "w") as f:
			toWrite = {							# Formatting the details into dictionary
				"id": id,
				"name": name,
				"d"	:	str(keypair.d),
				"e"	:	str(keypair.e),
				"n"	:	str(keypair.n)
			}
			data["objects"].append(toWrite)
			f.write(json.dumps(data, indent=4))
			return None
	else:
		print ("Keypair from this entity is already saved in the file.")


def entities_authorities_name_list(Auth):
	# Function to generate name list of entities or authorities
	names = []
	with open("keypairs.json", "r") as f:

		data = json.load(f)

		theArray = data["objects"]

		for item in theArray:
			if Auth:
				if item["id"] == "Authority":
					names.append(item["name"])
			else:
				if item["id"] == "Entity":
					names.append(item["name"])

		return names					# Returns list of all names


def get_keypair_from_file(name):
	# A function that loads a keypair from a file
	with open("keypairs.json" ,"r") as f:
		data = json.load(f)
		e = ""
		d = ""
		n = ""

		theArray = data["objects"]
		for item in theArray:
			if item["name"] == name:
				e = item["e"]
				d = item["d"]
				n = item["n"]


		keyPair = namedtuple('keyPair', ['e', 'd', 'n'])
		return keyPair(int(e), int(d), int(n))


def VerifyCertificate(certificate, entity):
	# A function to verify validity of a certificate
	if entity.EntityHasCertificate():
		actual_time = time.time()
		validity = True
		if certificate != entity.certificate or certificate["Owner"] != entity.name or certificate["ValidTo"] < actual_time or certificate["ValidFrom"] > actual_time or certificate["Public_Key"] != hex (entity.keyPair.e) or certificate["From_Authority"] != entity.certificate["From_Authority"]:
			validity = False
			print("Certificate is invalid!")
			return validity
		print("Certificate is valid.")
		return validity
	else:
		print("Entity {0} doesn't have any certificates".format(entity.name))


def find_sig_in_file(data):
	# A function that finds signature in txt file.
	# It searches for a specific unicode sequence
	if data.find('\\u2557') != -1 or data.find('\\u255d') != -1:
		start_index = data.find("/Signature:") + 12

		end_index = data.find("/ModDate")

		signature_in_file = data[start_index : end_index]

		return signature_in_file
	else:
		return None

def VerifySignature(msg, signature, e, n):
	# RSA verification of the signature
	# Entity will send Public Key to Authority to verify it
	# Authority will sign the Public Key with its private key
	# Improved functionality = now accepts files and integers

	if type(msg) == str:		# passing file name as a string

		file_name = msg
		type_of_file = file_name[file_name.find("."):]				# recognizing file extension

		if type_of_file == ".txt":
			with open(file_name, "r") as fi:
				data_in = fi.read()

				signature_in_file = find_sig_in_file(data_in)		# searching for a signature in file

				if signature_in_file != None:						# If there is none

					if signature_in_file == signature:
						full_data = data_in							# Holding the initial data in memory
						data_in = data_in.replace(data_in[data_in.find('b\"\\\\u2557b') : ], "")		# Removing the signature to get raw data 


						with open(file_name, "w") as f:
							f.write(data_in)
						with open(file_name, "rb") as f:
							data_in = f.read()						# Reading the data in binary
						with open(file_name, "w") as f:
							f.write(full_data)						# Writing the initial data

						hash = str(sha512(data_in).hexdigest())

						dec_hash = int(hash, 16)  					# Conversion to decimal 
					else:
						print("Signature in file doesn't match signature given by argument.")
						return False
				else:
					print("There is no signature in file, thus the verification process failed.")
					return False
		else:
			with open(file_name, "rb") as fi:

				pdf_reader = PdfFileReader(fi)				# Reading the PDF

				metadata = pdf_reader.getDocumentInfo()		# Retrieving the metadata from the PDF
				raw = parser.from_file(file_name)
				data_in = raw['content']					# Extracting the raw content of the PDF

				if type(data_in) == str:
					data_in = data_in.translate(str.maketrans('', '', ' \n\t\r'))		# The file has different whitespace characters for some reason, this needs to be done.
					data_in = data_in.encode()
				if '/Signature' in metadata:				# The file has to be signed

					hash = str(sha512(data_in).hexdigest())
					dec_hash = int(hash, 16)
				else:
					print("Document is not signed")
					return False
	else:
		dec_hash = int.from_bytes(sha512(bytes(msg)).digest(), byteorder='big')			# Verify validity of signed Public key


	hashFromSignature = pow(int(signature, 16), e, n) 		# Calculating hash from passed signature
	print("Hash received: {0}\nHash calculated: {1}\nHashes match: {2}\n".format(hex(dec_hash), hex(hashFromSignature), dec_hash == hashFromSignature))

	if dec_hash == hashFromSignature:
		return True
	else:
		return False
