import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'projectId': "mukhamapp",
})

db = firestore.client()

#docs = db.collection("Users").where('email', '==', 'piyush@vitap.ac.in').stream()
docs = db.collection("AttendanceData").document('0brxjCHHh7MKdlJaNdMcF4aKp733').collection("Years").\
    document('2021').collection('Months').document('November').\
    collection('Days').stream();
c=0.0
total_days=0
dates_present_array=[]
for doc in docs:
    #extracts the documents--dates marked in Days collection i.e.,for sure present dates-half/full
    dates_present=list(doc.to_dict().keys())[0]
    dates_present_array.append(dates_present)
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