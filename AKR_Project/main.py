import json

from functions import VerifyCertificate, VerifySignature, save_keypair_to_file, get_keypair_from_file
from entity import Entity
from authority import Authority
import apk
import os

"""
# Entities
entity1 = Entity("Entity1")
# creating new entity

# testing saving and retrieving keypair from file
keypairE1 = get_keypair_from_file(entity1.name)

print("Entity 1")
print(f"Public key:  (e={hex(keypairE1.e)})")
print(f"Private key: (d={hex(keypairE1.d)})")
print(f"Modulo: (n={hex(keypairE1.n)})")
print(hex(keypairE1.e) == hex(entity1.keyPair.e))
print(hex(keypairE1.d) == hex(entity1.keyPair.d))
print(hex(keypairE1.n) == hex(entity1.keyPair.n))

entity2 = Entity("Entity2")
# creating new entity

keypairE2 = get_keypair_from_file(entity2.name)

print("Entity2")
print(f"Public key:  (e={hex(keypairE2.e)})")
print(f"Private key: (d={hex(keypairE2.d)})")
print(f"Modulo: (n={hex(keypairE2.n)})")
print(hex(keypairE2.e) == hex(entity2.keyPair.e))
print(hex(keypairE2.d) == hex(entity2.keyPair.d))
print(hex(keypairE2.n) == hex(entity2.keyPair.n))

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

i = 0
while i < 1:
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

	print("Signature into metadata for PDF:")
	sig = entity1.GenerateSignature('doc.pdf', entity1.keyPair.d, entity1.keyPair.n)
	VerifySignature('doc_signed.pdf', sig, entity1.keyPair.e, entity1.keyPair.n)

	print("Signature into metadata for TXT:")
	txt_signature = entity1.GenerateSignature("signed_text.txt", entity1.keyPair.d, entity1.keyPair.n)
	VerifySignature("signed_text.txt", txt_signature, entity1.keyPair.e, entity1.keyPair.n)
	i += 1
"""


def signEval():
	filePath = apk.checkFile.cget("text")
	ent = os.path.basename(apk.checkFile.cget("text"))
	print(ent)
	print(filePath)

	if Entity(ent).EntityHasCertificate():
		print(get_keypair_from_file(ent))

	entity = ent
	entitySign = "d140111263614299868872663750368351800971083278637884970743158207444012665140553235144935653785840711317036916465673765901092001888475433221014130877911534940683"
	authority = "CZ_Authority"
	certificate = "d30921321136354723555129712496783865765041623320981679747660392471935620997016659980413184346423485846515413769506734297"
	try:
		sign = {
			"Entity": entity,
			"EntitySign": entitySign,
			"Authority": authority,
			"Certificate": certificate,
		}
		return sign
	except:
		return None


def apkSignFile(file, entName):
	ent = Entity(entName)
	keys = get_keypair_from_file(entName)
	d = keys.d
	n = keys.n
	ent.GenerateSignature(file, int(d), int(n))


def addCertificate(entName, authName):
	ent = Entity(entName)
	auth = Authority(authName)
	keys = get_keypair_from_file(entName)
	ent.certificate = auth.GenerateCertificate(keys.e, ent)



"""
def entityCall():			#no idea what this does
	ent= Entity(str(apk.eSign.get()))
	sigE1 = ent.GenerateSignature(ent.keyPair.e, ent.keyPair.d, ent.keyPair.n)
	if VerifySignature(ent.keyPair.e, sigE1, ent.keyPair.e, ent.keyPair.n) == True:
		ent.certificate = apk.autClick().authority.GenerateCertificate(ent.keyPair.e, ent)
	#VerifySignature(ent+'_signed.pdf', sigE1, ent.keyPair.e, ent.keyPair.n)
	return True
"""