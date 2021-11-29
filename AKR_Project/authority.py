from hashlib import sha512
import time


class Authority():

    def __init__(self, name):
        self.name = name
        self.id = "Authority"
        self.keyPair = None

    def GenerateCertificate(self, e, entity):
        if entity.keyPair.e == e:
            hash = int.from_bytes(sha512(bytes(e)).digest(), byteorder='big')

            certificate_hash = hex(pow(hash, self.keyPair.d, self.keyPair.n))

            owner = entity.name
            validFrom = time.time()
            validTo = validFrom + 31556926  # Certificate is valid for one year
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

