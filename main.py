# import os
# from werkzeug.utils import secure_filename
from flask import Flask, request, render_template ,send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///hello.db'
db=SQLAlchemy(app)

class AddingFiles(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  data = db.Column(db.LargeBinary)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/upload",methods=['GET','POST'])
def upload():
  if request.method=='POST':
    file= request.files['file']
    newFile=AddingFiles(name=file.filename,data=file.read())
    db.create_all()
    db.session.add(newFile)
    db.session.commit()
    return file.filename+" is successfully added to your database" 
  return "Something Wrong"

@app.route("/download")
def download():
  test=AddingFiles.query.filter_by(id=1).first()
  db.drop_all()

  return send_file(BytesIO(test.data),attachment_filename=test.name,as_attachment=True)


# @app.route('/',methods = ['GET','POST'])
# def hello_world():
#   if request.method == 'POST':
#     file = request.files['files'] 
#     file.save(secure_filename(file.filename))  
#     print(file.filename)   
#     return render_template("index.html", text=file.filename)
#   return render_template("index.html")

# @app.route("/files/<name>")
# def display(name):
#   print(name)
#   return render_template("display.html",data= name+'.png')
if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8080, debug=True)

