"""
This file contains Django forms for each form that users of the application might want to submit
(e.g the form for registering as a user).
"""
from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

class RegisterForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    user_type = forms.ChoiceField(widget=forms.RadioSelect, label="User Type",
                    choices=[("S", "Student"), ("I", "Instructor"), ("C", "Client")])
    key = forms.CharField(widget=forms.TextInput, label="Instructor Key", required=False) # The magic key that allows you to register as an instructor

class ProjectSubmissionForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput, label="Project Name")
    requirements = forms.CharField(widget=forms.TextInput, label="Project Requirements")
    keywords = forms.CharField(widget=forms.TextInput, label="Keywords")
    description = forms.CharField(widget=forms.TextInput, label="Description")

class MessageForm(forms.Form):
    recipient = forms.CharField(widget=forms.TextInput, label="To")
    subject = forms.CharField(widget=forms.TextInput, label="Subject")
    text = forms.CharField(widget=forms.Textarea, label="Message Text")

class BidSubmissionForm(forms.Form):
    team_members = forms.CharField(widget=forms.TextInput, label="Team Members")
    description = forms.CharField(widget=forms.Textarea, label="Note to Instructors/Client")

class NewSectionForm(forms.Form):
    """
    For instructors registering a new class section
    """
    name = forms.CharField(widget=forms.TextInput, label="Section Name")

class QuestionForm(forms.Form):
    """
    For students submitting a question on a project
    """
    question = forms.CharField(widget=forms.Textarea, label="Question Text")

class ReplyForm(forms.Form):
    """
    This form is for a client replying to a student's question on their project.
    """
    text = forms.CharField(widget=forms.Textarea, label="Reply Text")

class ProfileForm(forms.Form):
    tags = forms.CharField(widget=forms.TextInput, label="Tags")
