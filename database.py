from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

import datetime

db = SQLAlchemy()

class User(db.Model):
    """ Handle clients table and operations """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32),unique=True, nullable=False)
    salt = db.Column(db.String(3), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    tasks = db.relationship("Task",backref="owner")

    def jsonize(self):
        """ yup I know this is not even a word """
        return {
            'id': self.id,
            'name': self.name
        }
    
    def __repr__(self):
        return self.name


class Project(db.Model):
    """ Handle products areas table and operations """
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    tasks = db.relationship("Task",backref="project")

    def jsonize(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    def __repr__(self):
        return self.name

class Category(db.Model):
    """ Task category (front, back etc) """
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(32), unique=True, nullable=False)
    tasks = db.relationship("Task",backref="category")

    def jsonize(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    def __repr__(self):
        return self.name
    
class Task(db.Model):
    """ Tasks table """
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(512))
    priority = db.Column(db.Integer)
    target_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    def jsonize(self):
        
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'target_date': self.target_date,
            'owner' : self.owner.jsonize(),
            'project' : self.project.jsonize(),
            'category': self.category.jsonize()
        }

    def __repr__(self):
        return "%s : %s" % (self.title, self.description)

