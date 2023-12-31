#all imports!
from flask import Flask,render_template,url_for,request
import requests
from geopy.geocoders import ArcGIS
import folium as f


#API definition!
url = "https://api.apilayer.com/number_verification/validate?number="
payload = {}
headers= {
  "apikey": "CSXdyBMEmGWItH9jfpfKv5meo8OmBeci"
}
#Flask definition!
app = Flask(__name__)
@app.route('/', methods=['POST','GET'])
def index():
    if request.method=='POST':
        #Number request!
        number=request.form['number']
        #Details request rom API!
        response = requests.request("GET", url + number, headers=headers, data=payload)
        #Status code!
        status_code = response.status_code
        #Splitting the result!
        result = response.text
        #Simplifying the result!
        x = result.split('{')
        x.remove(x[0])
        y = x[0].split('}')
        z = y[0].split('\n')
        z.remove(z[0])
        z.remove(z[10])
        y = ''
        for i in z:
            y = y + i
        u = y.split(',')
        for i in range(0, len(u)):
            u[i] = u[i].strip()
        #Choosing the required details!
        #required Definition
        l=[]
        def simplify(i):
            x=u[i]
            y=x.split(':')
            y.remove(y[0])
            l.append(y[0].strip())
        simplify(0)
        simplify(1)
        simplify(2)
        simplify(3)
        simplify(4)
        simplify(5)
        simplify(6)
        simplify(7)
        simplify(8)
        simplify(9)
        global k
        if (l[7]=='"Andhra Pradesh"'):
            l[7]='Telangana or Andhra Pradesh - (United Andhra Pradesh)'
        k = l[7]+l[6]
        #Returning the result!
        if l[0] == 'true':
            return render_template('result.html', inter=l[3], pref=l[4], code=l[5], name=l[6], loc=l[7], carr=l[8], type=l[9])
        else:
            return render_template('error.html')
    else:
        return render_template('index.html')
@app.route('/map')
def map():
    strh=k
    nom=ArcGIS()
    s=nom.geocode(strh)
    m=None
    if(type(s)==type(m)):
        return render_template('maperror.html')
    else:
        lat=s.latitude
        longt=s.longitude
        map=f.Map(location=[lat,longt])
        f.Marker(location=[lat,longt],popup=strh,icon=f.Icon(color='green')).add_to(map)
        map.save('templates/map.html')
        return(map._repr_html_())