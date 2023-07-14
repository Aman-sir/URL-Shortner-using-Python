from flask import Flask,render_template,request,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:@localhost/url_shortner"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

data=[]


 
def shortUrled():
  import string
  b=[]
  h=[]

  for i in range(0,10,1):
    b.append(str(i))
  a=string.ascii_letters
  for i in a:
    h.append(str(i))
  A=[]
  c=b+h
  for i in range(6):
    f=random.choice(c)
    A.insert(i,f)
  A="".join(A)
  return A

db = SQLAlchemy(app)

class Url_list(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    full_length = db.Column(db.String(255), nullable=False)
    short_length = db.Column(db.String(12), nullable=False)
    date = db.Column(db.String(12), nullable=False)
   

@app.route('/',methods=["POST","GET"])
def HOME():
  if request.method=='POST':
    fullUrl=request.form.get('fullUrl')
    shortUrl=shortUrled()
    entry = Url_list(full_length = fullUrl,short_length =shortUrl, date= datetime.now()) 
    db.session.add(entry)
    db.session.commit()
  if request.method=='GET':
    data=Url_list.query.all()
  return render_template('index.html',data=data)




    

@app.route('/<shortUrl>')
def findurl(shortUrl):
  fullUrl=''
  if request.method=='GET':
    data=Url_list.query.all()
    for i in data:
      if(i.short_length==shortUrl):
        fullUrl=i.full_length
        
  if fullUrl:
    return redirect(fullUrl)
  else:
    return "This Url Does'nt exists"
        
      
app.run(debug=True)
