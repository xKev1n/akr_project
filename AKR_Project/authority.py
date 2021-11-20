from hashlib import sha512
from functions import GenerateKeyPair
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
