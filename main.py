from flask import Flask, request, render_template ,send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///hello.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()
# db.init_app(app)


with app.app_context():
    db.create_all()

class Adding(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  data = db.Column(db.LargeBinary)

  
@app.route("/")
def index():
  db.drop_all()
  with app.app_context():
    db.create_all()
  return render_template("index.html")

@app.route("/upload",methods=['GET','POST'])
def upload():
  if request.method=='POST':
    file= request.files['file']
    newFile=Adding(name=file.filename,data=file.read())
    # db.create_all()
    db.session.add(newFile)
    db.session.commit()
    for i in Adding.query.all():
      print(i.id, i.name)
    return file.filename+" is successfully added to your database" 
  return "Something Wrong"

@app.route("/download")
def download():
  test=Adding.query.filter_by(id=1).first()
  # db.drop_all()
  return send_file(BytesIO(test.data),download_name=test.name,as_attachment=True)

if __name__ == "__main__":
  app.run()
