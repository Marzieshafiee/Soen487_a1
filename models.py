from flask_sqlalchemy import SQLAlchemy
from main import app

db = SQLAlchemy(app)

def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(), nullable=False)
    papers = db.relationship('Paper', backref='author', lazy=True)
    professors = db.relationship('Professor', backref='student', lazy=True)

    def __repr__(self):
        return "<Student {}: {}>".format(self.id, self.username)

class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

    def __repr__(self):
        return "<Paper {}: {}>".format(self.id, self.title, self.content)


class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

    def __repr__(self):
        return "<Paper {}: {}>".format(self.id, self.title)





