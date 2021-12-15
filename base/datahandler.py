import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import datetime as d
from datetime import datetime,timedelta
from firebase_admin import auth

cred = credentials.Certificate("./serviceAccountKey.json")
fb = firebase_admin.initialize_app(cred, {
    'projectId': "mukhamapp",
})
db = firestore.client()

# register in firebase
def setUserRegistration(data,uid):
    #user = auth.create_user(
    #    email=data[1]['email'],
    #    email_verified=True,
    #    password=data[2]['pwd'],
    #    disabled=False)
    x = uid
    print('Successfully created new user: {0}', x)

    # db.collection('Users').add(data)
    db.collection('Users').document(x).set(data[1])


# get user's personal details
def getUserDetails(email):
    docs = db.collection("Users").where('email', '==', email).stream()
    for doc in docs:
        print(f'{doc.id}')

    ref = db.collection("Users").document(doc.id)

    doc = ref.get()
    if doc.exists:
        data = doc.to_dict()
        userDetails = {
            'empId': data['EmpId'],
            'fullName': data['fullName'],
            'school': data['school'],
        }
        print(userDetails)
        print(doc.id)
        return userDetails
    else:
        return None


# send percentage
def getPercentageAttendance(fromDate, toDate, uid):
    range_of_date = []
    attendance_dict=[]
    total_present_in_range=0
    total_absent_in_range=0
    first_date = fromDate
    to_date = toDate
    total_days=0
    o=0
    fromD = datetime.strptime(first_date, "%Y-%m-%d").date()
    toD = datetime.strptime(to_date, "%Y-%m-%d").date()
    fromD.strftime('%d-%m-%Y')
    toD.strftime('%d-%m-%Y')
    print(fromD,toD)
    # print(toD.date()+timedelta(days=1))
    fromMonthInNum = fromD.month
    toMonthInNum = toD.month
    while fromD<= toD:
        print(fromD.strftime('%d-%m-%Y'))
        range_of_date.append(fromD.strftime('%d-%m-%Y'))
        fromD = fromD + timedelta(days=1)
    print(range_of_date)
    print(fromMonthInNum,toMonthInNum)
    s=0
    print(type(fromMonthInNum))

    if toMonthInNum==fromMonthInNum:
        s=1
        month = d.date(2001, fromMonthInNum, 1).strftime('%B')
        print(month)
        docs = db.collection("AttendanceData").document(uid).collection("Years"). \
            document('2021').collection('Months').document(month). \
            collection('Days').stream()
        c = 0.0
        total_days = 0
        print(range_of_date)
        attendance_dict = []
        o = 0
        for doc in docs:
            per_day_attendance_status = {}
            # extracts the documents i.e., dates marked in Days collection i.e.,for sure present dates-half/full
            get_date = list(doc.to_dict().keys())[0]
            if get_date in range_of_date:
                per_day_attendance_status["date"] = get_date
                print(get_date)
                total_days = total_days + 1
                for i in range(0, 2):
                    z = list(doc.to_dict().values())[0][i]
                    l = len(list(doc.to_dict().values())[0])
                    print(z)
                    # morning attendance data
                    if i == 0:
                        if isinstance(z, (bool)):
                            per_day_attendance_status["morningStatus"] = 0
                        else:
                            per_day_attendance_status["morningStatus"] = 1
                            c = c + 0.5
                    # evening attendance data
                    elif i == 1:
                        if isinstance(z, (bool)):
                            per_day_attendance_status["eveningStatus"] = 0
                        else:
                            per_day_attendance_status["eveningStatus"] = 1
                            c = c + 0.5
                print(per_day_attendance_status)
                attendance_dict.append(per_day_attendance_status)
                o=o+1
        if o> 0:
            total_present_in_range = (c * 100) / o
            total_absent_in_range = (o - c) * 100 / o
            # print(total_present_in_range,total_absent_in_range)
            print(attendance_dict)

        return {'p': total_present_in_range, 'a': total_absent_in_range, 'total_days': total_days,
                'attendance': attendance_dict}
    check=False

    if fromMonthInNum!=toMonthInNum:
        while fromMonthInNum<=toMonthInNum:
            month = d.date(2001, fromMonthInNum, 1).strftime('%B')
            print(month)
            docs = db.collection("AttendanceData").document(uid).collection("Years"). \
                document('2021').collection('Months').document(month). \
                collection('Days').stream()
            for doc in docs:
                check=True
                print("Yes exists!")
                break
            if check==True:
                c = 0.0
                total_days = 0
                print(range_of_date)
                attendance_dict = []
                o = 0
                for doc in docs:
                    print("I am inside")
                    per_day_attendance_status = {}
                    # extracts the documents i.e., dates marked in Days collection i.e.,for sure present dates-half/full
                    get_date = list(doc.to_dict().keys())[0]
                    print(range_of_date)
                    if get_date in range_of_date:
                        per_day_attendance_status["date"] = get_date
                        print(get_date)
                        total_days = total_days + 1
                        for i in range(0, 2):
                            z = list(doc.to_dict().values())[0][i]
                            l = len(list(doc.to_dict().values())[0])
                            print(z)
                            # morning attendance data
                            if i == 0:
                                if isinstance(z, (bool)):
                                    per_day_attendance_status["morningStatus"] = 0
                                else:
                                    per_day_attendance_status["morningStatus"] = 1
                                    c = c + 0.5
                            # evening attendance data
                            elif i == 1:
                                if isinstance(z, (bool)):
                                    per_day_attendance_status["eveningStatus"] = 0
                                else:
                                    per_day_attendance_status["eveningStatus"] = 1
                                    c = c + 0.5
                        print(per_day_attendance_status)
                        attendance_dict.append(per_day_attendance_status)
                    o = o + 1
            fromMonthInNum=fromMonthInNum+1

        print("o",o)
        if o>0:
            total_present_in_range = (c*100)/o
            total_absent_in_range = (o- c)*100/o
            # print(total_present_in_range,total_absent_in_range)
            print(attendance_dict)

        return {'p': total_present_in_range, 'a': total_absent_in_range, 'total_days':o,
                'attendance': attendance_dict}


def getPresentAbsent(doc):
    print('I am here')
    c = 0.0
    for i in range(0, 2):
        z = list(doc.to_dict().values())[0][i]
        print(z)
        if isinstance(z, (bool)):
            print("yes bool")
        else:
            c = c + 0.5
    total_present = c
    total_absent = 1 - c
    print('absent days', total_absent)
    print('present days', total_present)
    return {'p': total_present, 'a': total_absent}


def getDashboardAdmin(fromDate, toDate):
    total_display=[]
    temp_date_act=[]
    range_of_date = []
    totalDay = 0
    first_date = fromDate
    to_date = toDate
    fromD = datetime.strptime(first_date, "%Y-%m-%d").date()
    toD = datetime.strptime(to_date, "%Y-%m-%d").date()
    fromD.strftime('%d-%m-%Y')
    toD.strftime('%d-%m-%Y')
    fromMonthInWords = fromD.strftime("%B")
    toMonthInWords = toD.strftime("%B")
    fromMonthInNum = fromD.month
    toMonthInNum = toD.month
    print(fromMonthInNum,toMonthInNum)
    # print(toD.date()+timedelta(days=1))
    print("From date- UI, ", fromD.strftime('%d-%m-%Y'))
    print("To date- UI, ", toD.strftime('%d-%m-%Y'))
    while fromD.strftime('%d-%m-%Y') <= toD.strftime('%d-%m-%Y'):
        print(fromD.strftime('%d-%m-%Y'))
        range_of_date.append(fromD.strftime('%d-%m-%Y'))
        fromD = fromD + timedelta(days=1)
    print("Range of date to be searched: ",range_of_date)
    school=['SCOPE','SENSE','VSL','VISH','VSB','HR','STAFF','RESEARCH SCHOLAR','OTHERS']
    tp = 0
    ta = 0
    present_absent_detail_per_user={}
    present_absent_detail_per_user['p']=0
    present_absent_detail_per_user['a'] = 0
    for particular_school in school:
        docs_user = db.collection("Users").where('school', '==', particular_school).stream()
        for particular_date in range_of_date:
            pd_m=datetime.strptime(particular_date,"%d-%m-%Y").strftime("%B")
            print("Date: ", particular_date)
            for doc in docs_user:
                print("User id: ", doc.id)
                for i in range(fromMonthInNum, toMonthInNum + 1):
                    d = datetime.strptime(str(i), "%m")
                    dW = d.strftime("%B")
                    if dW!=pd_m:
                        continue
                    else:
                        print("For month-", dW)
                        # print(doc.id)
                        uid = doc.id
                        #date extract
                        docs_id = db.collection("AttendanceData").document(uid).collection("Years"). \
                            document('2021').collection('Months').document(dW). \
                            collection('Days').stream()
                        # dates time by a user in a month
                        for doco in docs_id:
                            AttendanceData_particularDate = list(doco.to_dict().keys())[0]
                            print("Particular date: ",particular_date,"\tfound the doc: ",AttendanceData_particularDate)
                            if AttendanceData_particularDate != particular_date:
                                continue
                            else:
                                present_absent_detail_per_user = getPresentAbsent(doco)
                                totalDay = totalDay + 1
                                print(present_absent_detail_per_user)
                                tp = tp + present_absent_detail_per_user['p']
                                ta = ta + present_absent_detail_per_user['a']

            if totalDay>0:
                temp_date_act.append({'present':tp*100/totalDay,'absent':ta*100/totalDay,'days':totalDay,'date':particular_date,'school':particular_school})
                print(temp_date_act)
                tp=0
                ta=0
                totalDay=0
                docs_user = db.collection("Users").where('school', '==', particular_school).stream()
    return temp_date_act

# get user's cred verified
def userVerify(email, pwd):
    pass


def reset_password(email):
    return auth.generate_password_reset_link(email, action_code_settings=None)
