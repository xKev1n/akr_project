from functions import VerifyCertificate, VerifySignature
from entity import Entity
from authority import Authority

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

i = 0
while i<5:

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
	txt_signature = entity1.GenerateSignature("signed_text.txt",entity1.keyPair.d, entity1.keyPair.n)
	VerifySignature("signed_text.txt", txt_signature, entity1.keyPair.e, entity1.keyPair.n)
	i += 1