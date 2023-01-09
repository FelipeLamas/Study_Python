import pprint
import pymongo as pym
import datetime

client = pym.MongoClient('mongodb+srv://felipedevjob28:fl09031977@cluster0.ulvvq5s.mongodb.net/?retryWrites=true&w=majority')

db = client.test 

post = {
    "author": "felipe",
    "address": "Rio de Janeiro / Realengo",
    "cpf": "05355206112",
    "tipo_conta": "conta corrente",
    "agencia": "0001",
    "numero": 21334562,
    "saldo": 500.0,
    "tags": ["felipe lamas", "corrente", "pf", "adulto", "masculino"],
    "date": datetime.datetime.utcnow()
}

posts = db.posts
post_id = posts.insert_one(post).inserted_id
print(post_id)

print(db.list_collection_names)

# informações

print("\n Recuperando informações de cadastro:\n")
print(db.posts.find_one())
pprint.pprint(db.posts.find_one())

new_posts = [{
    "author": "gabriela",
    "address": "Rio de Janeiro / Bangu",
    "cpf": "01182294025",
    "tipo_conta": "conta corrente",
    "numero": 25263788,
    "agencia": "0001",
    "saldo": 432.25,
    "tags": ["gabriela", "corrente", "pf", "adulto", "feminino"],
    "date": datetime.datetime.utcnow()
},
{
    "author": "craudia",
    "address": "São Paulo / Morumbi",
    "cpf": "01178596283",
    "tipo_conta": "conta corrente",
    "numero": 25263785,
    "agencia": "0001",
    "saldo": 300.0,
    "tags": ["craudia lamas", "corrente", "pj", "adulto", "feminino"],
    "date": datetime.datetime.utcnow()
}]

result = posts.insert_many(new_posts)
print("\n Ids para os novos cadastros:\n")
print(result.inserted_ids)

# buscando clientes da mesma familia
print("\n Clientes da mesma família:\n")
pprint.pprint(db.posts.find_one({"tags": "lamas"}))

# cadastros que estão na coleção
print("\n Documentos presentes na coleção Posts")
for post in posts.find():
    pprint.pprint(post)