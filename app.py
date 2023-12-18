from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    text = db.Column(db.Text, nullable = False)

with app.app_context():
    db.create_all()

@app.route("/create", methods=['POST','GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        post = Post(title=title, text = text)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except:
            return 'При добавлении новости произошла ошибка'
    
    else:
        return render_template('create.html')

@app.route("/posts")
def posts():
    posts=Post.query.all()
    return render_template('posts.html', posts=posts)

@app.route("/index")
@app.route("/")
def index():
    return render_template ('index.html')

@app.route("/about")
def about():
    return render_template ('about.html')




@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
   if request.method == 'POST':
       Login = request.form.get('Login')
       Password = request.form.get('Password')

       db_lp = sqlite3.connect('login_password.db')
       cursor_db = db_lp.cursor()
       cursor_db.execute(('''SELECT password FROM passwords
                                               WHERE login = '{}';
                                               ''').format(Login))
       pas = cursor_db.fetchall()

       cursor_db.close()
       try:
           if pas[0][0] != Password:
               return render_template('authorization.html')
       except:
           return render_template('authorization.html')

       db_lp.close()
       return render_template('index.html')

   return render_template('authorization.html')

@app.route('/registration', methods=['GET', 'POST'])
def form_registration():

   if request.method == 'POST':
       Login = request.form.get('Login')
       Password = request.form.get('Password')

       db_lp = sqlite3.connect('login_password.db')
       cursor_db = db_lp.cursor()
       sql_insert = '''INSERT INTO passwords VALUES('{}','{}');'''.format(Login, Password)


       cursor_db.execute(sql_insert)

       cursor_db.close()

       db_lp.commit()
       db_lp.close()

       return render_template('index.html')

   return render_template('registration.html')

if __name__ == '__main__':
    app.run(debug=True)