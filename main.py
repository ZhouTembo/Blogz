from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://bloogz:blogz@localhost:8889/bloogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    blogs= db.relationship('blog', backref='user')
    def __init__(self, username, password):
        
        self.username = username
        self.password = password


class blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(120))
    content = db.Column(db.String(700))
    

    def __init__(self, name, content,owner_id):
        self.name = name
        self.content=content
        self.owner_id=owner_id

        
@app.route('/blog', methods=[ 'GET','POST'])
def blogs():
    
    
    
   
    user=request.args.get('userid')
    if user:
        owner_id=user
        auth2=User.query.filter_by(username=owner_id).first()
        
        blogs=blog.query.filter_by(owner_id=auth2.id).all()
        return render_template('singleUser.html',blogs=blogs, maam=auth2.username)
    num=request.args.get('id')
   
    if num:
        post=blog.query.get(num)
        owner_id=post.owner_id
        auth2=User.query.filter_by(id=owner_id).first()
        
        return render_template('blogpage.html',kook=post.content,look=post.name, maam=auth2.username )
    else:
        return render_template('home.html')
    


@app.route('/newpost', methods=['POST', 'GET'])
def addindex():
    titleerror=''
    contenterror=''
    blogs=blog.query.all()
    owner=User.query.filter_by(username=session['username']).first()
    
    if request.method == 'POST':
        owner_id=owner.id
        name = request.form['blog']
        content=request.form['blogtext']
        
        new_blog = blog(name, content,owner_id)
        db.session.add(new_blog)
        db.session.commit()
        
        if name=='':
            titleerror='Not a valid title'
        elif content=='':
            contenterror='Not valid entry'

        if not titleerror and not contenterror:
            return redirect('/newpost')
    return render_template('addblogs.html',title="Write a blog!",blogs=blogs, titleerror=titleerror,contenterror=contenterror)
    
    



@app.before_request
def require_login():
    allowed_routes = ['login', 'register','index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    usererror=''
    passworderror=''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username=='' or password=='':
            usererror='Username or password not valid'
            return render_template('login.html', usererror=usererror,passworderror=passworderror)

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            
            flash("Logged in")
            return redirect('/newpost')
    else:
        return render_template('login.html', usererror=usererror,passworderror=passworderror)


@app.route('/signup', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        usererror=''
        passworderror=''
        password_error=''
        id=0
        id+=1
        username = request.form['new_username']
        password = request.form['new_password']
        vpassword=request.form['new_vpassword']
        if username=='' or len(username)<3:
            usererror='Not a valid username'
        if password=='' or len(password)<3:
            passworderror='Not valid password'
        if password!=vpassword:
            password_error='Passwords do not match'
            passworderror='Passwords do not match'
            

        if usererror!='' or passworderror!='' or password_error!='':
            return render_template('signup.html', usererror=usererror,passworderror=passworderror, home=username)
  
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User( username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            
            return redirect('/newpost')
        else:
           
            return "<h1>Username already in use</h1>"

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/login')



@app.route('/')
def index():
    users=User.query.all()
    return render_template('index.html', users=users)







if __name__ == '__main__':
    app.run()