from hashlib import sha512
from functions import GenerateKeyPair, VerifyCertificate, formatTime, VerifySignature
import pprint
from PyPDF2 import PdfFileReader, PdfFileMerger
import time

class Authority():
	def __init__(self, name):
		self.keyPair = GenerateKeyPair()
		self.name = name

	def GenerateCertificate(self, e, entity):
		if entity.keyPair.e == e:	
			hash = int.from_bytes(sha512(bytes(e)).digest(), byteorder='big')
			
			certificate_hash = hex(pow(hash, self.keyPair.d, self.keyPair.n))
			
			owner = entity.name
			validFrom = time.time()
			validTo = validFrom + 31556926			# Certificate is valid for one year
			algorithm = "RSA"
			public_key = hex(e)
			from_authority = self.name
			

			certificate = {
			"Owner": owner,
			"ValidFrom": validFrom,
			"ValidTo": validTo,
			"Algorithm": algorithm,
			"Public_Key": public_key,
			"From_Authority": from_authority,
			"Certificate": certificate_hash
			}

			return certificate
	
	
	def ShowKeys(self):
		print(f"Public key:  (e={hex(self.keyPair.e)})")
		print(f"Private key: (d={hex(self.keyPair.d)})")
		print(f"Modulo: (n={hex(self.keyPair.n)})")
		
		

class Entity():
	def __init__(self, name):
		self.keyPair = GenerateKeyPair()
		self.name = name
		self.certificate = None
		self.message = None

	def ShowKeys(self):
		print(f"Public key:  (e={hex(self.keyPair.e)})")
		print(f"Private key: (d={hex(self.keyPair.d)})")
		print(f"Modulo: (n={hex(self.keyPair.n)})")

	def EntityHasCertificate(self):
		if self.certificate != None:
			return True
		else:
			return False

	def PrintCertificate(self):
		if self.EntityHasCertificate():
			cert_formatted = ""
			for keys, values in self.certificate.items():
				
				if keys == "ValidFrom":
					values = time.strftime('%Y-%m-%d',time.localtime(self.certificate['ValidFrom']))		
				
				if keys == "ValidTo":
					values = time.strftime('%Y-%m-%d',time.localtime(self.certificate['ValidTo']))			
				
				cert_formatted += str(keys)+": "+str(values)+" "
			return cert_formatted

	def ShowCertificates(self):
		if self.EntityHasCertificate():
			print("Entity {0} has Certificate: ".format(self.name))
			print(self.PrintCertificate())
		else:
			print("Entity {0} is not trusted.\n".format(self.name))

	def GenerateSignature(self, msg, d, n):
		# RSA signature of the message

		type_of_file = ""

		if type(msg) == str:
			file_name = msg
			type_of_file = file_name[file_name.find("."):]

			fi = open(file_name, "rb")
			data_in = fi.read()
			hash = str(sha512(data_in).hexdigest())
			dec_hash = int(hash, 16)
			fi.close()
		else:
			dec_hash = int.from_bytes(sha512(bytes(msg)).digest(), byteorder='big')
		
		signature = pow(dec_hash, d, n)
		# print("Signature: "+str(hex(signature))+"\n")

		if type_of_file == ".pdf":

			fi = open(file_name, "rb")
			pdf_reader = PdfFileReader(fi)

			metadata = pdf_reader.getDocumentInfo()

			pdf_merger = PdfFileMerger()
			pdf_merger.append(fi)

			if self.EntityHasCertificate() == True:
				pdf_merger.addMetadata({
					'/Certificate': self.PrintCertificate()
				})

			pdf_merger.addMetadata({
				'/Signature': str(hex(signature))
			})
			
			
			for keys, values in metadata.items():
				if keys == '/CreationDate':
					values = formatTime(values)
					pdf_merger.addMetadata({
					keys: "{0}-{1}-{2}".format(values["year"], values["month"], values["day"])
					})
				elif keys == '/ModDate':
					values = time.strftime('%Y-%m-%d', time.localtime(time.time()))
					pdf_merger.addMetadata({
					keys: values
					})
				else:
					pdf_merger.addMetadata({
					keys: values
				})
			file_name.replace(type_of_file,"")
			fo = open(file_name+'_signed.pdf', 'wb')
			pdf_merger.write(fo)
			fo.close()

			fo_signed = open(file_name+'_signed.pdf', 'rb')

			print("Metadata:")
			pdf_reader = PdfFileReader(fo_signed)
			metadata = pdf_reader.getDocumentInfo()
			pprint.pprint(metadata)
			print()
			
			fi.close()
			fo_signed.close()

			return str(hex(signature))
		elif type_of_file == '.txt':
			with open(file_name, 'r') as f:
				content = f.read()
				if content.find('\\u2557') == -1 or content.find('\\u255d') == -1:
					data = ""
					if self.EntityHasCertificate() == True:
						data += '/Certificate: '+self.PrintCertificate()
			
					data += '/Signature: '+str(hex(signature))
					data += '/ModDate: '+ time.strftime('%Y-%m-%d', time.localtime(time.time()))

			
					with open(file_name, "a") as fo:
						output = "╗"+str(data.encode('unicode-escape'))+"╝"		#ALT+187, 188
						fo.write(str(output.encode('unicode-escape')))

					return str(hex(signature))
				else:
					print ("File has already been signed")
					return str(hex(signature))
					#TODO: Implement functionality of either replacing old signature or alter verification mechanism to handle null passing.
		else:
			return str(hex(signature))


# Entities
entity1 = Entity("Entity1")
# creating new entity

entity2 = Entity("Entity2")
# creating new entity


# Authorities
authority1 = Authority("CZ_AUTHORITY")
# creating new authority

sigE1 = entity1.GenerateSignature(entity1.keyPair.e, entity1.keyPair.d, entity1.keyPair.n)
# signing the message with entity's private key

# verifying signature with entity's public key
if VerifySignature(entity1.keyPair.e, sigE1, entity1.keyPair.e, entity1.keyPair.n) == True:
	entity1.certificate = authority1.GenerateCertificate(entity1.keyPair.e, entity1)
	# if hashes match, generating certificate for the entity

print("Certificates:")
entity1.ShowCertificates()
entity2.ShowCertificates()

VerifyCertificate(entity1.certificate, entity2)


print("Testing valid file")
with open("text.txt", "r") as f:
	entity1.message = f.read().encode()
	
	sigF1 = entity1.GenerateSignature(entity1.message, entity1.keyPair.d, entity1.keyPair.n)
	# signing the message with entity's private key

	VerifySignature(entity1.message, sigF1, entity1.keyPair.e, entity1.keyPair.n)
	# verifying signature with entity's public key

print("Testing altered file")
with open("text_altered.txt", "r") as f_altered:
	altered_message = f_altered.read().encode()

	sigF1 = entity1.GenerateSignature(entity1.message, entity1.keyPair.d, entity1.keyPair.n)

	VerifySignature(altered_message, sigF1, entity1.keyPair.e, entity1.keyPair.n)


print("Signature into metadata:")
sig = entity1.GenerateSignature('doc.pdf', entity1.keyPair.d, entity1.keyPair.n)
VerifySignature('doc.pdf', sig, entity1.keyPair.e, entity1.keyPair.n)

txt_signature = entity1.GenerateSignature("signed_text.txt",entity1.keyPair.d, entity1.keyPair.n)
VerifySignature("signed_text.txt", txt_signature, entity1.keyPair.e, entity1.keyPair.n)