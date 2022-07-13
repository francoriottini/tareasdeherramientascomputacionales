
#f.close()

import urllib2
import json
import math
toWrite = []
#http = urllib3.PoolManager()

start_lat = 48.80
start_long = -125.80
end_lat  = 25.80
end_long = -68.80
total1 = 0

#start_lat = 41.87 
#start_long = -87.7 
#end_lat = 41.85 
#end_long = -88.72 

def getData(start_lat, start_long, end_lat, end_long, divider):
  global total1
  global toWrite

  #if total1 >300:
  #  return

  if end_lat - start_lat > -1.2 and end_long - start_long < 1:
   # print (end_lat - start_lat, end_long - start_long, divider)

    print (start_lat, start_long, end_lat, end_long, total1)
    slat = start_lat
    slong = start_long
    elat = end_lat 
    elong = end_long 
   
    url = 'https://www.crimereports.com/api/crimes/details.json?days=sunday,monday,tuesday,wednesday,thursday,friday,saturday&end_date=2017-08-31&end_time=23&incident_types=Assault,Assault+with+Deadly+Weapon,Breaking+%26+Entering,Disorder,Drugs,Homicide,Kidnapping,Liquor,Other+Sexual+Offense,Property+Crime,Property+Crime+Commercial,Property+Crime+Residential,Quality+of+Life,Robbery,Sexual+Assault,Sexual+Offense,Theft,Theft+from+Vehicle,Theft+of+Vehicle&include_sex_offenders=false&lat1='+str(slat)+'&lat2='+str(elat)+'&lng1='+str(slong)+'&lng2='+str(elong)+'&sandbox=false&start_date=2017-06-02&start_time=0'
    #print(url)
    #r = http.request('GET',url)
    #jsondata = json.loads(r.data)
    response = None
    try:
      response = urllib2.urlopen(url)
    except:
      f1=open("todofiles","a")
      f1.write(url)
      f1.close()
      return
    r = response.read()
    jsondata = json.loads(r)


    if 'error' in jsondata:
      print(jsondata)
    elif jsondata['instance_count'] > 0 and len(jsondata['agencies']) ==0:
      mid = start_lat - (start_lat - end_lat)/2
      getData(start_lat, start_long, mid, end_long, 1)
      getData(mid, start_long, end_lat, end_long, 1)
    elif jsondata['instance_count'] > 0:
      print("writing.......")

      for data in jsondata["agencies"]:
        toWrite.extend(data["crimes"])
     # print(jsondata.keys())
    #print(jsondata['instance'])
    #if 'error' in jsondata:
    #  if 'greater than threshold(180.0)' in jsondata['error']:
    #    f.write("-------------------")



    total1 = total1 + 1
    return
 # total1 = 1 +total1
  
  if end_lat - start_lat < -1 :
    mid = start_lat - (start_lat - end_lat)/2
    getData(start_lat, start_long, mid, end_long, 1)
    getData(mid, start_long, end_lat, end_long, 1)
  elif end_long - start_long > 1.2:
    mid = start_long + (end_long-start_long)/2
    getData(start_lat, start_long, end_lat, mid, 1)
    getData(start_lat, mid, end_lat, end_long, 1)





lat2 = lat1 = start_lat
log2 = log1 = start_long

getData(start_lat, start_long, end_lat, end_long,1)




import csv
total1 = total1 +1
alldata = open('Data'+str(total1)+'.csv', 'a')
#csvwriter = csv.writer(alldata)
count = 0
header = []

for item in toWrite:
  #if count == 0:
  for h in item.keys():
    if h not in header:
      header.append(h)
    #csvwriter.writerow(header)
  count += 1
  st = ''
  try:
    for h in header:
      if h in item:
        e =  json.dumps(item[h])
        e = e.replace(',', ';')
        st = st + e +','
      else:
        st = st +','
      st.strip("\n")
      st = st.replace('"', '')
    st=st[0:-1]
    st=st+'\n'
    alldata.write(st)
  except:
    print ("---------------------")
    print(item.values())
    f1=open("todofiles","a")
    f1.write("Problem")
    f1.close()

st=''
for h in header:
  st = st+h+',' 
st = st[0:-1]
st=st+'\n'
print (st)
alldata.write(st)


alldata.close()
print(count)


#f=open("filex","a")
#f.write(json.dumps({"data":toWrite}))
#f.close()
#print(len(toWrite))
#print(total1)


