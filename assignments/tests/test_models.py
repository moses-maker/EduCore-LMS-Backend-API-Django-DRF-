"""
Comprehensive test cases for Assignment and Submission models.
Demonstrates full TDD approach with edge cases.
"""

import pytest
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.assignments.models import Assignment, Submission, AssignmentType, SubmissionStatus
from apps.users.models import User, UserRole
from apps.courses.models import Course
from apps.enrollments.models import Enrollment, EnrollmentStatus


@pytest.fixture
def lecturer():
    """Create a lecturer for testing"""
    return User.objects.create_user(
        email='lecturer@test.com',
        password='pass123',
        first_name='Jane',
        last_name='Teacher',
        role=UserRole.LECTURER
    )


@pytest.fixture
def student():
    """Create a student for testing"""
    return User.objects.create_user(
        email='student@test.com',
        password='pass123',
        first_name='John',
        last_name='Doe',
        role=UserRole.STUDENT
    )


@pytest.fixture
def course(lecturer):
    """Create a course for testing"""
    return Course.objects.create(
        code='CS101',
        title='Intro to CS',
        description='Test course',
        lecturer=lecturer,
        credits=3,
        max_students=50,
        start_date=timezone.now().date(),
        end_date=timezone.now().date() + timedelta(days=90)
    )


@pytest.fixture
def assignment(course, lecturer):
    """Create an assignment for testing"""
    return Assignment.objects.create(
        course=course,
        title='Assignment 1',
        description='First assignment',
        assignment_type=AssignmentType.HOMEWORK,
        max_points=100,
        passing_points=60,
        due_date=timezone.now() + timedelta(days=7),
        created_by=lecturer
    )


@pytest.mark.django_db
class TestAssignmentModel:
    """Test Assignment model functionality"""
    
    def test_create_assignment(self, course, lecturer):
        """Test creating an assignment"""
        due_date = timezone.now() + timedelta(days=7)
        assignment = Assignment.objects.create(
            course=course,
            title='Test Assignment',
            description='Test description',
            assignment_type=AssignmentType.HOMEWORK,
            max_points=100,
            passing_points=60,
            due_date=due_date,
            created_by=lecturer
        )
        
        assert assignment.course == course
        assert assignment.title == 'Test Assignment'
        assert assignment.assignment_type == AssignmentType.HOMEWORK
        assert assignment.max_points == 100
        assert assignment.passing_points == 60
        assert assignment.created_by == lecturer
    
    def test_assignment_string_representation(self, assignment):
        """Test assignment __str__ method"""
        expected = f"{assignment.course.code} - {assignment.title}"
        assert str(assignment) == expected
    
    def test_assignment_types(self, course, lecturer):
        """Test different assignment types"""
        types = [
            AssignmentType.HOMEWORK,
            AssignmentType.QUIZ,
            AssignmentType.PROJECT,
            AssignmentType.EXAM
        ]
        
        for atype in types:
            assignment = Assignment.objects.create(
                course=course,
                title=f'Test {atype}',
                description='Test',
                assignment_type=atype,
                max_points=100,
                passing_points=60,
                due_date=timezone.now() + timedelta(days=7),
                created_by=lecturer
            )
            assert assignment.assignment_type == atype
    
    def test_is_available_property(self, course, lecturer):
        """Test is_available property"""
        now = timezone.now()
        
        # Assignment available now
        assignment1 = Assignment.objects.create(
            course=course,
            title='Available Now',
            description='Test',
            assignment_type=AssignmentType.HOMEWORK,
            max_points=100,
            passing_points=60,
            due_date=now + timedelta(days=7),
            created_by=lecturer
        )
        assert assignment1.is_available is True
        
        # Assignment not yet available
        assignment2 = Assignment.objects.create(
            course=course,
            title='Future Assignment',
            description='Test',
            assignment_type=AssignmentType.HOMEWORK,
            max_points=100,
            passing_points=60,
            due_date=now + timedelta(days=7),
            available_from=now + timedelta(days=1),
            created_by=lecturer
        )
        assert assignment2.is_available is False
        
        # Assignment no longer available
        assignment3 = Assignment.objects.create(
            course=course,
            title='Past Assignment',
            description='Test',
            assignment_type=AssignmentType.HOMEWORK,
            max_points=100,
            passing_points=60,
            due_date=now + timedelta(days=7),
            available_until=now - timedelta(days=1),
            created_by=lecturer
        )
        assert assignment3.is_available is False
    
    def test_is_overdue_property(self, course, lecturer):
        """Test is_overdue property"""
        now = timezone.now()
        
        # Not overdue
        assignment1 = Assignment.objects.create(
            course=course,
            title='Not Overdue',
            description='Test',
            assignment_type=AssignmentType.HOMEWORK,
            max_points=100,
            passing_points=60,
            due_date=now + timedelta(days=7),
            created_by=lecturer
        )
        assert assignment1.is_overdue is False
        
        # Overdue
        assignment2 = Assignment.objects.create(
            course=course,
            title='Overdue',
            description='Test',
            assignment_type=AssignmentType.HOMEWORK,
            max_points=100,
            passing_points=60,
            due_date=now - timedelta(days=1),
            created_by=lecturer
        )
        assert assignment2.is_overdue is True
    
    def test_assignment_validation(self, course, lecturer):
        """Test assignment validation (passing_points <= max_points)"""
        assignment = Assignment(
            course=course,
            title='Invalid Assignment',
            description='Test',
            assignment_type=AssignmentType.HOMEWORK,
            max_points=100,
            passing_points=120,  # Invalid: exceeds max_points
            due_date=timezone.now() + timedelta(days=7),
            created_by=lecturer
        )
        
        with pytest.raises(ValidationError):
            assignment.clean()
    
    def test_late_submission_settings(self, course, lecturer):
        """Test late submission penalty settings"""
        assignment = Assignment.objects.create(
            course=course,
            title='Late Penalty Test',
            description='Test',
            assignment_type=AssignmentType.HOMEWORK,
            max_points=100,
            passing_points=60,
            due_date=timezone.now() + timedelta(days=7),
            allow_late_submission=True,
            late_penalty_per_day=10.0,
            created_by=lecturer
        )
        
        assert assignment.allow_late_submission is True
        assert assignment.late_penalty_per_day == 10.0


@pytest.mark.django_db
class TestSubmissionModel:
    """Test Submission model functionality"""
    
    def test_create_submission(self, assignment, student):
        """Test creating a submission"""
        submission = Submission.objects.create(
            assignment=assignment,
            student=student,
            content='This is my submission',
            status=SubmissionStatus.DRAFT
        )
        
        assert submission.assignment == assignment
        assert submission.student == student
        assert submission.content == 'This is my submission'
        assert submission.status == SubmissionStatus.DRAFT
        assert submission.points_earned is None
    
    def test_submission_string_representation(self, assignment, student):
        """Test submission __str__ method"""
        submission = Submission.objects.create(
            assignment=assignment,
            student=student
        )
        
        expected = f"{student.get_full_name()} - {assignment.title}"
        assert str(submission) == expected
    
    def test_unique_submission_per_student(self, assignment, student):
        """Test student can only have one submission per assignment"""
        Submission.objects.create(
            assignment=assignment,
            student=student,
            content='First submission'
        )
        
        with pytest.raises(Exception):  # IntegrityError
            Submission.objects.create(
                assignment=assignment,
                student=student,
                content='Second submission'
            )
    
    def test_submission_status_workflow(self, assignment, student):
        """Test submission status transitions"""
        submission = Submission.objects.create(
            assignment=assignment,
            student=student,
            content='Test submission',
            status=SubmissionStatus.DRAFT
        )
        
        assert submission.status == SubmissionStatus.DRAFT
        assert submission.submitted_at is None
        
        # Submit
        submission.status = SubmissionStatus.SUBMITTED
        submission.save()
        submission.refresh_from_db()
        
        assert submission.status == SubmissionStatus.SUBMITTED
        assert submission.submitted_at is not None
        
        # Grade
        submission.status = SubmissionStatus.GRADED
        submission.points_earned = 85
        submission.save()
        submission.refresh_from_db()
        
        assert submission.status == SubmissionStatus.GRADED
        assert submission.graded_at is not None
    
    def test_is_late_property(self, course, lecturer, student):
        """Test is_late property"""
        now = timezone.now()
        
        # Create assignment due in the past
        assignment = Assignment.objects.create(
            course=course,
            title='Late Test',
            description='Test',
            assignment_type=AssignmentType.HOMEWORK,
            max_points=100,
            passing_points=60,
            due_date=now - timedelta(days=2),
            created_by=lecturer
        )
        
        # On-time submission
        submission1 = Submission.objects.create(
            assignment=assignment,
            student=student
        )
        submission1.submitted_at = now - timedelta(days=3)
        submission1.save()
        assert submission1.is_late is False
        
        # Late submission
        student2 = User.objects.create_user(
            email='student2@test.com',
            password='pass123',
            first_name='Jane',
            last_name='Smith'
        )
        submission2 = Submission.objects.create(
            assignment=assignment,
            student=student2
        )
        submission2.submitted_at = now - timedelta(days=1)
        submission2.save()
        assert submission2.is_late is True
    
    def test_days_late_calculation(self, course, lecturer, student):
        """Test days_late property calculation"""
        now = timezone.now()
        
        assignment = Assignment.objects.create(
            course=course,
            title='Late Test',
            description='Test',
            assignment_type=AssignmentType.HOMEWORK,
            max_points=100,
            passing_points=60,
            due_date=now - timedelta(days=5),
            created_by=lecturer
        )
        
        submission = Submission.objects.create(
            assignment=assignment,
            student=student
        )
        submission.submitted_at = now - timedelta(days=2)
        submission.save()
        
        assert submission.days_late == 3
    
    def test_percentage_score_calculation(self, assignment, student):
        """Test percentage_score property"""
        submission = Submission.objects.create(
            assignment=assignment,
            student=student,
            points_earned=85
        )
        
        assert submission.percentage_score == 85.0
        
        # Test with different points
        submission.points_earned = 75
        submission.save()
        assert submission.percentage_score == 75.0
    
    def test_is_passing_property(self, assignment, student):
        """Test is_passing property"""
        # Passing submission
        submission1 = Submission.objects.create(
            assignment=assignment,
            student=student,
            points_earned=85
        )
        assert submission1.is_passing is True
        
        # Failing submission
        student2 = User.objects.create_user(
            email='student2@test.com',
            password='pass123',
            first_name='Jane',
            last_name='Smith'
        )
        submission2 = Submission.objects.create(
            assignment=assignment,
            student=student2,
            points_earned=45
        )
        assert submission2.is_passing is False
        
        # Edge case: exactly passing points
        student3 = User.objects.create_user(
            email='student3@test.com',
            password='pass123',
            first_name='Bob',
            last_name='Jones'
        )
        submission3 = Submission.objects.create(
            assignment=assignment,
            student=student3,
            points_earned=60
        )
        assert submission3.is_passing is True
    
    def test_grading_workflow(self, assignment, student, lecturer):
        """Test complete grading workflow"""
        # Student submits
        submission = Submission.objects.create(
            assignment=assignment,
            student=student,
            content='My complete solution',
            status=SubmissionStatus.SUBMITTED
        )
        submission.submitted_at = timezone.now()
        submission.save()
        
        assert submission.status == SubmissionStatus.SUBMITTED
        assert submission.points_earned is None
        assert submission.graded_by is None
        
        # Lecturer grades
        submission.status = SubmissionStatus.GRADED
        submission.points_earned = 92
        submission.feedback = 'Excellent work!'
        submission.graded_by = lecturer
        submission.save()
        
        submission.refresh_from_db()
        
        assert submission.status == SubmissionStatus.GRADED
        assert submission.points_earned == 92
        assert submission.percentage_score == 92.0
        assert submission.is_passing is True
        assert submission.feedback == 'Excellent work!'
        assert submission.graded_by == lecturer
        assert submission.graded_at is not None


@pytest.mark.django_db
class TestAssignmentSubmissionIntegration:
    """Test integration between assignments and submissions"""
    
    def test_assignment_with_multiple_submissions(self, assignment, course):
        """Test assignment can have multiple submissions from different students"""
        # Create students
        students = []
        for i in range(5):
            student = User.objects.create_user(
                email=f'student{i}@test.com',
                password='pass123',
                first_name=f'Student{i}',
                last_name='Test'
            )
            students.append(student)
            
            # Enroll in course
            Enrollment.objects.create(
                student=student,
                course=course,
                status=EnrollmentStatus.ACTIVE
            )
        
        # Create submissions
        for student in students:
            Submission.objects.create(
                assignment=assignment,
                student=student,
                content=f'Submission by {student.get_full_name()}',
                status=SubmissionStatus.SUBMITTED
            )
        
        assert assignment.submissions.count() == 5
    
    def test_student_can_update_draft_submission(self, assignment, student):
        """Test student can update draft submission"""
        submission = Submission.objects.create(
            assignment=assignment,
            student=student,
            content='Initial draft',
            status=SubmissionStatus.DRAFT
        )
        
        # Update content
        submission.content = 'Updated draft'
        submission.save()
        
        submission.refresh_from_db()
        assert submission.content == 'Updated draft'
        assert submission.status == SubmissionStatus.DRAFT
    
    def test_submission_timestamps(self, assignment, student):
        """Test submission timestamp tracking"""
        submission = Submission.objects.create(
            assignment=assignment,
            student=student,
            status=SubmissionStatus.DRAFT
        )
        
        created_at = submission.created_at
        assert created_at is not None
        
        # Submit
        submission.status = SubmissionStatus.SUBMITTED
        submission.save()
        submission.refresh_from_db()
        
        assert submission.submitted_at is not None
        assert submission.submitted_at >= created_at
        
        # Grade
        submission.status = SubmissionStatus.GRADED
        submission.points_earned = 85
        submission.save()
        submission.refresh_from_db()
        
        assert submission.graded_at is not None
        assert submission.graded_at >= submission.submitted_at
