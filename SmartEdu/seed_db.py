#!/usr/bin/env python
"""Seed the database with initial data"""
from app import create_app
from app.models import db, Course, Book, User

app = create_app()

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()
    
    # Create sample courses
    courses = [
        Course(
            title="Python Basics",
            description="Learn Python from scratch. Perfect for beginners who want to start their programming journey.",
            instructor="John Smith",
            duration="8 weeks",
            level="Beginner",
            students=1245,
            rating=4.8,
            price=29.99
        ),
        Course(
            title="Web Development with Flask",
            description="Master web development with Flask. Build real-world applications and deploy them to the cloud.",
            instructor="Jane Doe",
            duration="10 weeks",
            level="Intermediate",
            students=892,
            rating=4.7,
            price=49.99
        ),
        Course(
            title="Data Science Fundamentals",
            description="Learn data science, machine learning, and data analysis with Python and popular libraries.",
            instructor="Mike Johnson",
            duration="12 weeks",
            level="Intermediate",
            students=567,
            rating=4.9,
            price=59.99
        ),
        Course(
            title="Advanced JavaScript",
            description="Take your JavaScript skills to the next level with advanced concepts and modern frameworks.",
            instructor="Sarah Wilson",
            duration="8 weeks",
            level="Advanced",
            students=445,
            rating=4.6,
            price=39.99
        ),
        Course(
            title="Database Design",
            description="Learn to design efficient and scalable databases. Master SQL, normalization, and optimization.",
            instructor="Tom Brown",
            duration="6 weeks",
            level="Intermediate",
            students=623,
            rating=4.8,
            price=34.99
        ),
        Course(
            title="Cloud Computing with AWS",
            description="Deploy and manage applications on AWS. Learn EC2, S3, Lambda, and other AWS services.",
            instructor="Emily Davis",
            duration="10 weeks",
            level="Advanced",
            students=789,
            rating=4.7,
            price=69.99
        ),
    ]
    
    # Create sample books
    books = [
        Book(
            title="Introduction to Algorithms",
            author="T.H. Cormen",
            description="A comprehensive guide to algorithms and data structures. The definitive textbook used in universities worldwide.",
            isbn="978-0262033848",
            category="Computer Science",
            pages=1328,
            rating=4.9
        ),
        Book(
            title="Clean Code",
            author="Robert Martin",
            description="A practical guide to writing clean, maintainable code. Learn best practices from industry experts.",
            isbn="978-0132350884",
            category="Programming",
            pages=464,
            rating=4.8
        ),
        Book(
            title="The Pragmatic Programmer",
            author="Andrew Hunt, David Thomas",
            description="Your journey to mastery in software development. Practical wisdom from experienced developers.",
            isbn="978-0201616224",
            category="Programming",
            pages=352,
            rating=4.7
        ),
        Book(
            title="Design Patterns",
            author="Gang of Four",
            description="Elements of Reusable Object-Oriented Software. The essential guide to design patterns.",
            isbn="978-0201633610",
            category="Software Design",
            pages=416,
            rating=4.6
        ),
        Book(
            title="Python Crash Course",
            author="Eric Matthes",
            description="Learn Python through hands-on projects. A beginner-friendly introduction to programming.",
            isbn="978-1593275990",
            category="Programming",
            pages=544,
            rating=4.7
        ),
        Book(
            title="The Art of Computer Programming",
            author="Donald Knuth",
            description="Fundamental algorithms and programming techniques. The programmer's bible.",
            isbn="978-0201896831",
            category="Computer Science",
            pages=1520,
            rating=4.9
        ),
    ]
    
    # Add all to session
    for course in courses:
        db.session.add(course)
    
    for book in books:
        db.session.add(book)
    
    # Commit changes
    db.session.commit()
    
    print("✓ Database seeded successfully!")
    print(f"  - Created {len(courses)} courses")
    print(f"  - Created {len(books)} books")
