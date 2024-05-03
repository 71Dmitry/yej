from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from flask import Flask, request,render_template, redirect

engine = create_engine('sqlite:///news.db')
Base = declarative_base()

class Post(Base):
  __tablename__ = 'posts'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  content = Column(Text)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()



app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html",title='123')

@app.route("/news")
def news():
    posts = session.query(Post).all()
    return render_template("news.html", posts=posts)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
       title = request.form['title']
       content = request.form['content']
       post = Post(title = title, content = content)
       session.add(post)
       session.commit()
       return redirect('/')
    return render_template('add.html')

@app.route('/help',methods=['GET'])
def hlp():
    return render_template('help.html')

@app.route('/delete/<int:id>')
def delete(id):
   post = session.query(Post).filter_by(id=id).first()
   session.delete(post)
   session.commit()
   return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)