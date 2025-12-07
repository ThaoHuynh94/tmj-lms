# seed.py - create demo data for TMJ (5 courses version)

from datetime import date, timedelta
from app import create_app, db
from app.models import User, Course, Module, ModuleNote, ModuleProgress

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # -------------------------------------------------
    # 1) Demo user
    # -------------------------------------------------
    student = User(username="student1", email="student1@example.com")
    student.set_password("password123")
    student.streak_days = 3
    student.last_active_date = date.today() - timedelta(days=4)

    db.session.add(student)
    db.session.flush()

    # -------------------------------------------------
    # 2) Define 5 demo courses
    # -------------------------------------------------
    course_titles = [
        "Intro to Python",
        "Study Skills & Habits",
        "Time Management Essentials",
        "Effective Note-Taking",
        "Mindfulness for Students"
    ]

    courses = []
    for title in course_titles:
        c = Course(
            user_id=student.id,
            title=title,
            progress_percent=0,
            completed_at=None,
        )
        db.session.add(c)
        courses.append(c)

    db.session.flush()

    # -------------------------------------------------
    # 3) Add modules + module progress for each course
    # -------------------------------------------------

    # A helper function to create modules + progress rows
    def add_course_modules(course, module_info):
        progress_rows = []
        for index, (module_name, percent) in enumerate(module_info, start=1):

            # Module (structural, for course_detail / note system)
            m = Module(
                course_id=course.id,
                title=module_name,
                order_index=index,
                is_completed=(percent == 100),
            )
            db.session.add(m)

            # ModuleProgress (actual progress data used in UI)
            mp = ModuleProgress(
                user_id=student.id,
                course_id=course.id,
                module_name=module_name,
                percent_complete=percent,
            )
            progress_rows.append(mp)

        db.session.add_all(progress_rows)


    # Define unique module sets for each course
    add_course_modules(courses[0], [
        ("Getting Started", 100),
        ("Data Types & Variables", 100),
        ("Control Flow", 100),
    ])

    add_course_modules(courses[1], [
        ("Planning your week", 100),
        ("Deep work sessions", 20),
    ])

    add_course_modules(courses[2], [
        ("Time Blocking Basics", 50),
        ("Managing Distractions", 10),
        ("Weekly Planning", 0),
    ])

    add_course_modules(courses[3], [
        ("Cornell Notes Method", 100),
        ("Mind Maps", 60),
    ])

    add_course_modules(courses[4], [
        ("Breathing Techniques", 80),
        ("Study Meditation", 40),
        ("Focus Reset Exercises", 10),
    ])

    # -------------------------------------------------
    # 4) One example module note (on first module of Python)
    # -------------------------------------------------
    first_python_module = Module.query.filter_by(course_id=courses[0].id).first()
    note = ModuleNote(
        user_id=student.id,
        module_id=first_python_module.id,
        content="Remember to review list comprehensions before the quiz.",
    )
    db.session.add(note)

    # -------------------------------------------------
    # 5) Commit everything
    # -------------------------------------------------
    db.session.commit()
    print("Seeded: 1 user, 5 courses, multi-module progress, 1 note, streak demo")
