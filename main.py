from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog2:boom@localhost:8889/build-a-blog2'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    content = db.Column(db.String(700))
    

    def __init__(self, name, content):
        self.name = name
        self.content=content

        
@app.route('/', methods=[ 'GET','POST'])
def index():
    if request.method=='POST'and'GET':
        id=request.args.get('id')
        post=Blog.query.get(id)
        return render_template('blogpage.html',kook=post.content,look=post.name)
    elif request.method=='GET':
        return render_template('home.html')


@app.route('/newpost', methods=['POST', 'GET'])
def addindex():
    titleerror=''
    contenterror=''
    blogs=Blog.query.all()
    if request.method == 'POST':
        name = request.form['blog']
        content=request.form['blogtext']
        new_blog = Blog(name, content)
        db.session.add(new_blog)
        db.session.commit()
        
        if name=='':
            titleerror='Not a valid title'
        elif content=='':
            contenterror='Not valid entry'

        if not titleerror and not contenterror:
            return redirect('/newpost')
    return render_template('addblogs.html',title="Write a Blog!",blogs=blogs, titleerror=titleerror,contenterror=contenterror)
    
    


@app.route('/blog')
def viewindex():
    id=request.args.get('id')

    if id:
        blog=Blog.query.get(id)
        return render_template('blogpage.html', blog=blog)

    blogs=Blog.query.all()
    return render_template('blogs.html',title='Blogs',blogs=blogs)



if __name__ == '__main__':
    app.run()