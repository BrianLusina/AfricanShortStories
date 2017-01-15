from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from abc import ABCMeta, abstractmethod
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager
from datetime import datetime


class Base(db.Model):
    """
    Base class where all tables inherit from
    """
    __metaclass__ = ABCMeta
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    @abstractmethod
    def __repr__(self):
        """
        :return: representation of this object as a Human readable string
        """
        pass


class Author(Base, UserMixin):
    """
    Table for authors of Hadithi
    :cvar __tablename__ name of this table in the database
    :cvar uuid the unique user id, that will be autogenerated
    :cvar full_name, the full name of the user
    :cvar email, the email of the user
    :cvar password_hash, the password that will be hashed and hidded from other users
    :cvar admin, whether this user is an admin, default is false
    :cvar registered_on, date this account was registered
    :cvar confirmed, whether this identity has been verified by the user
    :cvar confirmed_on, the date this account was confirmed
    """

    __tablename__ = "author"
    uuid = Column(String(250), default=str(uuid.uuid4()), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    password_hash = Column(String(250), nullable=False)
    admin = Column(Boolean, nullable=False, default=False)
    registered_on = Column(DateTime, nullable=False)
    confirmed = Column(Boolean, nullable=False, default=False)
    confirmed_on = Column(DateTime, nullable=True)

    def __init__(self, full_name, email, confirmed, admin=False, confirmed_on=None):
        """
        Creates a new Author object
        :param full_name: Full name for user
        :param email: the user's email
        :param confirmed: When the user confirmed this email account
        :param admin: whether they are admin
        :param confirmed_on: When their email was confirmed
        """
        self.full_name = full_name
        self.email = email
        self.confirmed = confirmed
        self.admin = admin
        self.confirmed_on = confirmed_on
        self.registered_on = datetime.now()

    @property
    def password(self, password):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<UserId:%r Name :%r, Email: %r>" % (self.uuid, self.full_name, self.email)


# This callback is used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_author(user_id):
    return Author.query.get(int(user_id))


class Story(Base):
    """
    Story table. Contains all the stories in the database
    :cvar __tablename__ Name of class as a table in SQL db
    """

    __tablename__ = 'story_table'

    title = Column(String, nullable=False)
    tagline = Column(String(50), default=title)
    category = Column(String(100), default="Other")
    content = Column(String(10000), nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'))

    author = relationship(Author)

    def __init__(self, title, tagline, category, content, author_id):
        """
        :param title: Title of this story in the database
        :param tagline: Tagline of this story
        :param content: Content of this story
        :param author_id: The author id of whoever wrote this story
        """
        self.title = title
        self.tagline = tagline
        self.category = category
        self.content = content
        self.author_id = author_id

    def __repr__(self):
        return "Story: <Title: %r, Category: %r, Tagline: %r> AuthorId: %r" % \
               (self.title, self.category, self.tagline, self.author_id)
