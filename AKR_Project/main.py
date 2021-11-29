import json

from Crypto.PublicKey import RSA
from functions import GenerateKeyPair, VerifyCertificate, VerifySignature, save_keypair_to_file
from entity import Entity
from authority import Authority
import apk
import os


def initialize_entities_authorities():
	with open("keypairs.json" ,"r") as f:
		data = json.load(f)
		theArray = data["objects"]
		for item in theArray:
			name = item["name"]
			key = item["key"]
			bitKey = key.encode('UTF-8')
			finKey = RSA.importKey(bitKey)

			if item["id"] == "Authority":
				authDic[name] = Authority(name)
				authDic[name].keyPair = finKey

			elif item["id"] == "Entity":
				entDic[name] = Entity(name)
				entDic[name].keyPair = finKey


def signEval():
	filePath = apk.checkFile.cget("text")
	ent = os.path.basename(apk.checkFile.cget("text"))
	print(ent)
	print(filePath)

	if Entity(ent).EntityHasCertificate():
		print("hello")
		#print(get_keypair_from_file(ent))

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
	ent = entDic[entName]
	keys = ent.keyPair
	ent.GenerateSignature(file, ent.keyPair.d, ent.keyPair.n)


def addCertificate(entName, authName):
	ent = entDic[entName]
	auth = authDic[authName]
	ent.certificate = auth.GenerateCertificate(ent.keyPair.e, ent)


def create_auth_ent(authority, name):
	if authority:
		aut = Authority(name)
		aut.keyPair = GenerateKeyPair(aut.id, aut.name)
		authDic[name] = aut
	else:
		ent = Entity(name)
		ent.keyPair = GenerateKeyPair(ent.id, ent.name)
		entDic[name] = ent


entDic = {}
authDic = {}
initialize_entities_authorities()
