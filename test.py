import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'projectId': "mukhamapp",
})

db = firestore.client()

docs = db.collection("Users").where('EmpId', '==', 'varun1').stream()

for doc in docs:
    print(f'{doc.id}')
