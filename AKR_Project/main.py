import json

from Crypto.PublicKey import RSA
from functions import GenerateKeyPair
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
