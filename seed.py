# seed.py - create demo data for TMJ

from datetime import date
from app import create_app, db
from app.models import User, Course, Module, ModuleNote

app = create_app()

with app.app_context():
    # ️ This will wipe existing tables in the dev DB
    db.drop_all()
    db.create_all()

    # --- 1) Create a demo student user ---
    student = User(username="student1")

    # If your User model has set_password(), use it:
    if hasattr(student, "set_password"):
        student.set_password("password123")

    db.session.add(student)
    db.session.flush()  # so student.id is available

    # --- 2) Create two courses for that student ---

    # Completed course (to test completion badge + 100% progress)
    python_course = Course(
        user_id=student.id,
        title="Intro to Python",
        progress_percent=100,
        completed_at=date.today(),
    )

    # In-progress course (to test partial progress UI)
    habits_course = Course(
        user_id=student.id,
        title="Study Skills & Habits",
        progress_percent=40,
        completed_at=None,
    )

    db.session.add_all([python_course, habits_course])
    db.session.flush()

    # --- 3) Modules for each course ---

    # For Intro to Python (all completed)
    m1 = Module(
        course_id=python_course.id,
        title="Getting Started",
        order_index=1,
        is_completed=True,
    )
    m2 = Module(
        course_id=python_course.id,
        title="Data Types & Variables",
        order_index=2,
        is_completed=True,
    )
    m3 = Module(
        course_id=python_course.id,
        title="Control Flow",
        order_index=3,
        is_completed=True,
    )

    # For Study Skills & Habits (one done, one not)
    m4 = Module(
        course_id=habits_course.id,
        title="Planning your week",
        order_index=1,
        is_completed=True,
    )
    m5 = Module(
        course_id=habits_course.id,
        title="Deep work sessions",
        order_index=2,
        is_completed=False,
    )

    db.session.add_all([m1, m2, m3, m4, m5])
    db.session.flush()

    # --- 4) One example module note (tests “Student writes module notes”) ---
    note = ModuleNote(
        user_id=student.id,
        module_id=m2.id,
        content="Remember to review list comprehensions before the quiz.",
    )
    db.session.add(note)

    # --- 5) Commit everything ---
    db.session.commit()

    print(" Seeded: 1 student, 2 courses, 5 modules, 1 note")

