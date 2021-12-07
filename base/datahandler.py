import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from datetime import datetime, timedelta
from firebase_admin import auth

cred = credentials.Certificate("./serviceAccountKey.json")
fb=firebase_admin.initialize_app(cred, {
    'projectId': "mukhamapp",
})
db = firestore.client()


#register in firebase
def setUserRegistration(data):
    user = auth.create_user(
        email=data[1]['email'],
        email_verified=True,
        password=data[2]['pwd'],
        disabled=False)
    x=format(user.uid)
    print('Sucessfully created new user: {0}',x)

   # db.collection('Users').add(data)
    db.collection('Users').document(x).set(data[1])

# get user's personal details
def getUserDetails(userId):
    ref = db.collection("Users").document(userId)

    doc = ref.get()
    if doc.exists:
        data = doc.to_dict()
        userDetails = {
            'empId': data['EmpId'],
            'fullName': data['fullName'],
            'school': data['school'],
        }
        return userDetails
    else:
        return None

#get user's cred verified
def userVerify(email,pwd):
    pass

#get attendance
def getAttendance(userId, fromDate=datetime.today().replace(day=1), toDate=datetime.today()):
    ref = db.collection("Attendance").document(userId)

    doc = ref.get()
    if doc.exists:
        data = doc.to_dict()
    else:
        return None

    attendance = []
    totalPositiveCount = 0
    totalNegativeCount = 0

    delta = timedelta(days=1)
    while fromDate <= toDate:
        stringDate = fromDate.strftime('%d-%m-%Y')
        tempDict = {
            'date': stringDate,
            'morningStatus': 0,
            'eveningStatus': 0
        }
        fromDate += delta
        try:
            attendanceForEachDay = data[stringDate]
            if attendanceForEachDay[0] is not False:
                tempDict['morningStatus'] = 1
            if attendanceForEachDay[1] is not False:
                tempDict['eveningStatus'] = 1
        except:
            pass

        if tempDict['morningStatus'] == 1 and tempDict['eveningStatus'] == 1:
            totalPositiveCount += 1
        else:
            totalNegativeCount += 1

        attendance.insert(0, tempDict)

    positivePercent = totalPositiveCount / \
                      (totalPositiveCount + totalNegativeCount) * 100
    negativePercent = totalNegativeCount / \
                      (totalPositiveCount + totalNegativeCount) * 100
    percentage = {
        'attendance': attendance,
        'positivePercent': positivePercent,
        'negativePercent': negativePercent,
    }
    return percentage

def reset_password(email):
    return auth.generate_password_reset_link(email,action_code_settings=None)