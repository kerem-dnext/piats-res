# Creating app/models/resume.py - ORM models
from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class Applicant(db.Model):
    """Applicant model based on the provided ERD"""
    __tablename__ = 'applicant'
    
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    professional_summary = db.Column(db.Text)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    linked_in_url = db.Column(db.String(255))
    portfolio_url = db.Column(db.String(255))
    job_title = db.Column(db.String(100))
    
    # Relationships
    skills = db.relationship('ApplicantSkills', backref='applicant', lazy=True, cascade='all, delete-orphan')
    experience = db.relationship('ApplicantExperience', backref='applicant', lazy=True, cascade='all, delete-orphan')
    education = db.relationship('ApplicantEducation', backref='applicant', lazy=True, cascade='all, delete-orphan')
    languages = db.relationship('ApplicantLanguages', backref='applicant', lazy=True, cascade='all, delete-orphan')
    projects = db.relationship('ApplicantProjects', backref='applicant', lazy=True, cascade='all, delete-orphan')
    certifications = db.relationship('ApplicantCertifications', backref='applicant', lazy=True, cascade='all, delete-orphan')

class ApplicantSkills(db.Model):
    """Applicant skills model"""
    __tablename__ = 'applicant_skills'
    
    id = db.Column(db.BigInteger, primary_key=True)
    applicant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('applicant.user_id'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    proficiency_level = db.Column(db.String(50))
    years_of_experience = db.Column(db.Integer)

class ApplicantExperience(db.Model):
    """Applicant experience model"""
    __tablename__ = 'applicant_experience'
    
    id = db.Column(db.BigInteger, primary_key=True)
    applicant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('applicant.user_id'), nullable=False)
    job_title = db.Column(db.String(100))
    company_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

class ApplicantEducation(db.Model):
    """Applicant education model"""
    __tablename__ = 'applicant_education'
    
    id = db.Column(db.BigInteger, primary_key=True)
    applicant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('applicant.user_id'), nullable=False)
    degree = db.Column(db.String(100))
    institution = db.Column(db.String(100))
    field_of_study = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    grade = db.Column(db.String(20))

class ApplicantLanguages(db.Model):
    """Applicant languages model"""
    __tablename__ = 'applicant_languages'
    
    id = db.Column(db.BigInteger, primary_key=True)
    applicant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('applicant.user_id'), nullable=False)
    language = db.Column(db.String(50))
    proficiency_level = db.Column(db.String(50))

class ApplicantProjects(db.Model):
    """Applicant projects model"""
    __tablename__ = 'applicant_projects'
    
    id = db.Column(db.BigInteger, primary_key=True)
    applicant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('applicant.user_id'), nullable=False)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    role = db.Column(db.String(100))
    technologies = db.Column(db.String(255))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    url = db.Column(db.String(255))

class ApplicantCertifications(db.Model):
    """Applicant certifications model"""
    __tablename__ = 'applicant_certifications'
    
    id = db.Column(db.BigInteger, primary_key=True)
    applicant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('applicant.user_id'), nullable=False)
    name = db.Column(db.String(100))
    issuer = db.Column(db.String(100))
    issue_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)
    credential_id = db.Column(db.String(100))
    credential_url = db.Column(db.String(255))
