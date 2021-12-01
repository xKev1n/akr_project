from functions import formatTime
import time
from hashlib import sha512
from PyPDF2 import PdfFileReader, PdfFileMerger  # pip install PyPDF2
import pprint
from tika import parser


class Entity():

	def __init__(self, name):
		self.name = name
		self.id = "Entity"
		self.keyPair = None
		self.certificate = None
		self.message = None


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
					values = time.strftime('%Y-%m-%d', time.localtime(self.certificate['ValidFrom']))

				if keys == "ValidTo":
					values = time.strftime('%Y-%m-%d', time.localtime(self.certificate['ValidTo']))

				cert_formatted += str(keys) + ": " + str(values) + " "
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
			raw = parser.from_file(file_name)
			data_in = raw['content']

			if type(data_in) == str:
				data_in = data_in.translate(str.maketrans('', '', ' \n\t\r'))
				data_in = data_in.encode()
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
			file_name = file_name.replace(type_of_file, "")

			fo = open(file_name + '_signed.pdf', 'wb')
			pdf_merger.write(fo)
			fo.close()

			fo_signed = open(file_name + '_signed.pdf', 'rb')

			print("Metadata:")
			pdf_reader = PdfFileReader(fo_signed)
			metadata = pdf_reader.getDocumentInfo()
			pprint.pprint(metadata)
			print()

			fi.close()
			fo_signed.close()

			return str(hex(signature))

		else:
			return str(hex(signature))