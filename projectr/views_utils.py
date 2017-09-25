from django.http import HttpResponseRedirect
from models import Notification

def redirect_user_to_homepage(user_type):
    """
    Redirect a user to a particular home page based on their
    user type (i.e student, instructor, client)
    """
    if user_type == 'S':
        return HttpResponseRedirect("/student/")
    elif user_type == 'I':
        return HttpResponseRedirect("/instructor/")
    elif user_type == 'C':
        return HttpResponseRedirect("/client/")
    else:
        assert False, "Invalid user type for user"


def create_introduction_notification(user):
    """
    """
    subject = "Welcome to Groupr"
    body = "Anything is possible at Groupr. The infinite is possible at Groupr. The unattainable is unknown at Groupr. This Groupr. This is Groupr."
    new_notif = Notification(recipient=user, subject=subject, text=body)
    new_notif.save()
