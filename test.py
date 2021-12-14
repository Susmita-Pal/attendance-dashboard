import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'projectId': "mukhamapp",
})
db = firestore.client()
''''''
c=0
docs = db.collection("Admins").get()
for doc in docs:
    c=c+1
    print(doc.id)

print(c)
''''''



'''
#docs = db.collection("Users").where('email', '==', 'piyush@vitap.ac.in').stream()
docs = db.collection("AttendanceData").document('0brxjCHHh7MKdlJaNdMcF4aKp733').collection("Years").\
    document('2021').collection('Months').document('November').\
    collection('Days').stream();
c=0.0
total_days=0
dates_present_array=[]
for doc in docs:
    #extracts the documents i.e., dates marked in Days collection i.e.,for sure present dates-half/full
    dates_present=list(doc.to_dict().keys())[0]
    #dates_present_array.append(dates_present)
    print(dates_present)
    total_days=total_days+1
    #print(type(doc))
    for i in range(0,2):
        z=list(doc.to_dict().values())[0][i]
        l=len(list(doc.to_dict().values())[0])
        #print(list(doc.to_dict().values())[0])
        #print("Length",l)
        print(z)
        if isinstance(z,(bool)):
            print("yes bool")
        else:
            c=c+0.5
            #print("here")

print("Total attendance: ",c)
print("Total days: ",total_days)
'''



'''
import calendar

def findDay(date):
    day, month, year = (int(i) for i in date.split(' '))
    dayNumber = calendar.weekday(year, month, day)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"]
    return (days[dayNumber])


# Driver program
date = '03 02 2019'
print(findDay(date))
'''



'''
from datetime import datetime, timedelta

first_date = "25-10-2017"
to_date = "30-10-2017"
fromD = datetime.strptime(first_date, "%d-%m-%Y").date()
toD = datetime.strptime(to_date, "%d-%m-%Y").date()
present = datetime.now()
#print(toD.date()+timedelta(days=1))
while fromD<=toD:
    print(fromD)
    fromD=fromD+timedelta(days=1)
    
'''

'''
def getPresentAbsent(docs_id):
    c = 0.0
    total_days = 0
    attendance_dict = []
    o = 0
    for doc in docs_id:
        per_day_attendance_status = {}
        # extracts the documents i.e., dates marked in Days collection i.e.,for sure present dates-half/full
        get_date = list(doc.to_dict().keys())[0]
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
    total_present = c
    total_absent = total_days - c
    print('absent days', total_absent)
    print('present days',total_present)
    return {'p':total_present,'a':total_absent}



def getDashboardAdmin():
    docs = db.collection("Users").where('school','==','SCOPE').stream()
    tp=0
    ta=0
    for doc in docs:
        #print(doc.id)
        uid=doc.id
        print("uid- ",uid)
        docs_id = db.collection("AttendanceData").document(uid).collection("Years"). \
        document('2021').collection('Months').document('November'). \
        collection('Days').stream()
        present_absent_detail_per_user=getPresentAbsent(docs_id)
        tp=tp+ present_absent_detail_per_user['p']
        ta=ta+ present_absent_detail_per_user['a']
    print('total present ',tp)
    print('total absent ',ta)

if __name__ == '__main__':
    getDashboardAdmin()
'''
'''docs=db.collection("AttendanceData").document('Dd2IJgKH3YP6nd0okJ7D88OqaZF3').collection("Years"). \
        document('2021').collection('Months').document('December').collection('Days').stream()
print(docs)
c=0
for doc in docs:
    print(doc)
    print(list(doc.to_dict().keys())[0])
    print(type(doc.id),list(doc.to_dict().values())[0][0],list(doc.to_dict().values())[0][1])

print(c)

'''