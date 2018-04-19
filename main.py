from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:MyNewPass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.TEXT)

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<User %r>' % self.title

@app.route("/newpost", methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':

        blog_title = request.form['title']
        blog_body = request.form['body']
        title_error = ""
        body_error = ""

        if blog_title == "":
            title_error = "Title was missing."
            return render_template('new.html', title_error=title_error, body_error=body_error)
        
        elif blog_body == "":
            body_error = "Body was missing."
            return render_template('new.html', title_error=title_error, body_error=body_error)

        else:
            new_post = Blog(title=blog_title, body=blog_body)
            db.session.add(new_post)
            db.session.commit()
            id = new_post.id
            new_post = Blog.query.filter_by(id=id).all()
            return render_template('post.html', new_post=new_post, id=id)

    else:
         return render_template('new.html')

@app.route('/blog', methods=['POST', 'GET'])
def index():

    id = request.args.get('id')
    print(id)

    if(id):
        new_post = Blog.query.filter_by(id=id).all()
        return render_template('post.html', new_post=new_post, id=id)
    else:
        posts = Blog.query.all()
        return render_template('blog.html', posts=posts, id=id)

if __name__ == '__main__':
    app.run()
