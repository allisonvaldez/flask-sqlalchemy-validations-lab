# Import all modules and utilities
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

# Create an author class for the model to depict an author who blogs/posts
class Author(db.Model):

    # Detail what db this model maps to
    __tablename__ = 'authors'
    
    # Create unique id for each author as the primary key
    id = db.Column(db.Integer, primary_key=True)
    # Provide other attributes for the model
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Provide a decorator and define a validator function to ensure each author has a name
    @validates("name")
    def validate_name(self, key, value):
        # Provide error handling if it is empty
        if not value:
            raise ValueError("Author must have a name.")
        # Check for duplicate authors
        existing = Author.query.filter_by(name=value).first()
        if existing:
            raise ValueError("Author name must be unique.")
        return value
    
    # Provide a decorator and define a validator function to ensure phone number is accurate
    @validates("phone_number")
    def validate_phone_number(self, key, value):
        # Provide error handling if phone number is wrong
        if value and (len(value) != 10 or not value.isdigit()):
            raise ValueError("Phone number must be exactly 10 digits.")
        return value
    
    # Provide data as a string when author is printed
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
    
# Create an post class for the model to depict posts
class Post(db.Model):

    # Detail what db this model maps to
    __tablename__ = 'posts'
    
    # Create unique id for each post as the primary key
    id = db.Column(db.Integer, primary_key=True)
    # Provide other attributes for the model
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Provide a decorator and define a validator function to ensure post is correct length
    @validates("content")
    def validate_content(self, key, value):
        # Provide error handling if not correct length or empty
        if not value or len(value) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return value
    
    # Provide a decorator and define a validator function to ensure summary is correct length
    @validates("summary")
    def validate_summary(self, key, value):
        # Provide error handling if not correct length
        if value and len(value) > 250:
            raise ValueError("Post summary must be a maximum of 250 characters.")
        return value
    
    # Provide a decorator and define a validator function to ensure correct category
    @validates('category')
    def validate_category(self, key, value):
        # Provide error handling for proper category
        if value not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Post category must be either 'Fiction' or 'Non-Fiction'.")
        return value

    # Provide a decorator and define a validator function to ensure post title has clickbait words
    @validates('title')
    def validate_title(self, key, value):
        # Define clickbait words
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]

        # Provide error handling for clickbait
        if not value or not any(keyword in value for keyword in clickbait_keywords):
            raise ValueError(
                "Post title must contain one of: \"Won't Believe\", \"Secret\", \"Top\", \"Guess\"."
            )
        return value

    # Provide data as a string when post is printed
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'