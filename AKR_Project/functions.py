import re

from Crypto.PublicKey import RSA  # pip install pycryptodome
from hashlib import sha512
from PyPDF2 import PdfFileReader
import time
from tika import parser  # pip install tika
import json


def GenerateKeyPair(idcko, name):
    # function to generate a pair of public key, private key and modulo
    keyPair = RSA.generate(bits=1024)
    save_keypair_to_file(idcko, str(name), keyPair)
    return keyPair


def ShowKeys(entity):
    print(entity.name + '\'s keys:')
    print(f"Public key:  (e={hex(entity.keyPair.e)})")
    print(f"Private key: (d={hex(entity.keyPair.d)})")
    print(f"Modulo: (n={hex(entity.keyPair.n)})")


def formatTime(timestamp):
    year = timestamp[2:6]
    month = timestamp[6:8]
    day = timestamp[8:10]

    dictionary = {
        "year": year,
        "month": month,
        "day": day}

    return dictionary


def does_containt(name, file):
    if name in file.read():
        return True
    else:
        return False


def save_keypair_to_file(idcko, name, keypair):
	contains = False
	with open("keypairs.json", "r") as fo:
		if does_containt(name, fo):
			contains = True
	if not contains:
		strKey = keypair.exportKey().decode('UTF-8')
		data = {}
		with open("keypairs.json", "r") as f:
			data = json.load(f)

		with open("keypairs.json", "w") as f:

			toWrite = {
				"id": idcko,
				"name": name,
				"key": strKey
			}
			data["objects"].append(toWrite)
			f.write(json.dumps(data, indent=4))
			return None
	else:
		print ("Keypair from this entity is already saved in the file.")


def entities_authorities_name_list(Auth):
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

		return names


def VerifyCertificate(certificate, entity):
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
						data_in = data_in.replace(data_in[data_in.find('b\"\\\\u2557b') : ], "")  # Hashes not match for some reason...


						with open(file_name, "w") as f:
							f.write(data_in)
						with open(file_name, "rb") as f:
							data_in = f.read()
						with open(file_name, "w") as f:
							f.write(full_data)

						hash = str(sha512(data_in).hexdigest())
						# print(data_in)
						dec_hash = int(hash, 16)  # Is same only for first cycle. Hashes don't match on signed documents.
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


	hashFromSignature = pow(int(signature, 16), e, n)  # PKs are different for every rerun.
	print("Hash received: {0}\nHash calculated: {1}\nHashes match: {2}\n".format(hex(dec_hash), hex(hashFromSignature), dec_hash == hashFromSignature))

	if dec_hash == hashFromSignature:
		return True
	else:
		return False

field_metadata = []
def VerifySig_apk(msg):

	# RSA verification of the signature
	# User will send Public Key to Authority to verify it
	# Authority will sign the Public Key with its private key

	if type(msg) == str:

		file_name = msg
		type_of_file = file_name[file_name.find("."):]

		if type_of_file == ".txt":
			with open(file_name, 'r') as f:
				content = f.read()
				if find_sig_in_file(content) != None:
					try:
						entity = re.search('Owner: (.+?) ', str(content)).group(1)
						authority = re.search('From_Authority: (.+?) ', str(content)).group(1)
						Valid_F = re.search('ValidFrom: (.+?) ', str(content)).group(1)
						Valid_T = re.search('ValidTo: (.+?) ', str(content)).group(1)
						field_metadata.insert(0, entity)
						field_metadata.insert(1, authority)
						field_metadata.insert(2, Valid_F)
						field_metadata.insert(3, Valid_T)
						return field_metadata
					except:
						return None

				else:
					print("Document is not signed")
					return False
		else:
			with open(file_name, "rb") as fi:
				pdf_reader = PdfFileReader(fi)
				metadata = pdf_reader.getDocumentInfo()

				if '/Certificate' in metadata:
					try:
						entity = re.search('Owner: (.+?) ', str(metadata)).group(1)
						authority = re.search('From_Authority: (.+?) ', str(metadata)).group(1)
						Valid_F = re.search('ValidFrom: (.+?) ', str(metadata)).group(1)
						Valid_T = re.search('ValidTo: (.+?) ', str(metadata)).group(1)
						field_metadata.insert(0, entity)
						field_metadata.insert(1, authority)
						field_metadata.insert(2, Valid_F)
						field_metadata.insert(3,Valid_T)
						return field_metadata
					except:
						return None

				else:
					return False
			close(fi)
	else:
		return False