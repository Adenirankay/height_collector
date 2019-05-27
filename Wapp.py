'''
Created on Feb 7, 2019

@author: LONGBRIDGE
'''
from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy import  func

app=Flask(__name__)
#SPECIFYING THE DATABASE PATH WHICH INCLUDES THE USERNAME, PORT, AND DATABASE NAME
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres321@localhost/height_collector'
db = SQLAlchemy(app)


#DATABASE MODEL: A DATABASE MODEL IS USED TO  CAPTURE OR ACQUIRE THE ATTRIBUTES OF  TABLE CREATED IN A DATABASE.

class Data (db.Model):
    __tablename__ = "data"
    id= db.Column(db.Integer, primary_key= True)
    email_=db.Column(db.String(120), unique= True)
    height_=db.Column(db.Integer)
    
#INITIALIZING THE  EMAIL AND HEIGHT VARIABLES CREATED IN THE TABLE NAMED DATA.

    def __init__(self,email_,height_):
        self.email_ = email_
        self.height_= height_
    
#db.create_all ()

@app.route("/")
def Index():
    return render_template("index.html")

#THE POST METHOD IS A METHOD THAT CAPTURES INPUT VARIABLE FROM TEH FRONT END USING THE REQUEST.FORM FORMULAE.
@app.route("/success", methods=['POST'])

def Success():
#SO IF METHOD IS EQUALS TO POST AS STATED ABOVE.....
    if request.method=='POST' :
    
#THE INPUTS ARE GOTTEN AND PASSED TO A VARIABLE
        email =request.form["email_name"]
        height =request.form["height_name"]
        print(request.form)
        
#AVOIDING THE ISSUE OF HAVING DUPLICATE EMAILS IN THE DATABASE.
        if db.session.query(Data).filter(Data.email_== email).count() == 0 :
            data=Data(email,height)
            db.session.add(data)
            
#COMMIT ALL ADDED DATA TO THE TABLE TO MAINTAIN PERMANENT INSERT.
            db.session.commit()
            
#GETTING THE AVERAGE COUNT OF ALL HEIGHT IN THE TABLE
            average_height_= db.session.query(func.avg(Data.height_)).scalar()
            average_height_= round(average_height_,1)
            count= db.session.query(Data.height_).count()
            send_email(email, height,average_height_,count)
            print(average_height_)
            return render_template("success.html")
    return render_template("index.html",
                            text="seems like we've got something from that email address already!")
    


if __name__== "__main__" :
    app.run(port=5001)
    app.debug=True
    
    
     