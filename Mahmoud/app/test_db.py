from database import SessionLocal
from models import User, Exam, Question, StudentAnswer, Result

db = SessionLocal()

#  لو عايزين نمسح الداتا القديمة
db.query(Result).delete()
db.query(StudentAnswer).delete()
db.query(Question).delete()
db.query(Exam).delete()
db.query(User).delete()
db.commit()

# Users
admin = User(
    username="admin",
    email="admin@test.com",
    hashed_password="123",
    role="admin"
)

student = User(
    username="student",
    email="student@test.com",
    hashed_password="123",
    role="student"
)

db.add_all([admin, student])
db.commit()

# Exam
exam = Exam(
    title="Python Basics Exam",
    description="Simple exam for testing",
    duration_minutes=30,
    created_by=admin.id
)

db.add(exam)
db.commit()

# Questions
q1 = Question(
    exam_id=exam.id,
    question_text="What is Python?",
    question_type="mcq",
    choices=["Programming Language", "Database", "Operating System", "Browser"],
    correct_answer="Programming Language",
    score=1
)

q2 = Question(
    exam_id=exam.id,
    question_text="Which keyword is used to define a function in Python?",
    question_type="mcq",
    choices=["func", "def", "function", "define"],
    correct_answer="def",
    score=1
)

db.add_all([q1, q2])
db.commit()

# Student Answers
answer1 = StudentAnswer(
    student_id=student.id,
    exam_id=exam.id,
    question_id=q1.id,
    answer="Programming Language",
    is_correct=True
)

answer2 = StudentAnswer(
    student_id=student.id,
    exam_id=exam.id,
    question_id=q2.id,
    answer="def",
    is_correct=True
)

db.add_all([answer1, answer2])
db.commit()

# Result
total_score = 2
max_score = 2
percentage = (total_score / max_score) * 100

result = Result(
    student_id=student.id,
    exam_id=exam.id,
    total_score=total_score,
    max_score=max_score,
    percentage=percentage
)

db.add(result)
db.commit()

print("Test data inserted successfully!")
print("Admin:", admin.email)
print("Student:", student.email)
print("Exam:", exam.title)
print("Score:", total_score, "/", max_score)
print("Percentage:", percentage)