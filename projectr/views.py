from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import LoginForm, RegisterForm, ProjectSubmissionForm, MessageForm, \
        BidSubmissionForm, NewSectionForm, QuestionForm, ReplyForm, ProfileForm
from models import Project, Message, Bid, Section, Notification, Question, InstructorKey
from views_utils import redirect_user_to_homepage, create_introduction_notification
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    """
    Authenticated users will be sent to their home pages,
    unauthenticated users will be sent to the Login / Register home screen
    """
    if request.user.is_authenticated():
        if request.user.is_superuser:
            return HttpResponseRedirect("/admin/")
        return redirect_user_to_homepage(request.user.profile.user_type)
    else:
        return render(request, "index.html")


def login_view(request):
    """
    Endpoint for logins.
    Logged in users will be redirected to their homepage.
    If login fails, they will be redirected to /login to try again.
    Successful login will authenticate them and send them to their homepage
    """
    if request.user.is_authenticated():
        return redirect_user_to_homepage(request.user.profile.user_type)

    if request.method == "POST": # User attempting to log in
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(username=email, password=password)
            if user is not None:
                # User was successfully authenticated, redirect them to their home page
                login(request, user)
                return redirect_user_to_homepage(user.profile.user_type)

        # Reject the login and notify that the email / password was wrong
        blank_form = LoginForm()
        return render(request, "login.html", { "invalid": True, "form": blank_form })
    else: # GET request
        form = LoginForm()
        return render(request, "login.html", { "form": form })


def logout_view(request):
    """
    Log the user out and return them to the Login/Register splash screen
    """
    logout(request) # doesn't throw if user not logged in, just silently does nothing
    return HttpResponseRedirect("/")


def register(request):
    """
    Endpoint for new users registering.
    Authenticated users will just be redirected to their homepage.
    If registration fails, the user is redirected to /register and an error appears
    """
    if request.user.is_authenticated():
        return redirect_user_to_homepage(request.user.profile.user_type)

    blank_form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user_type = form.cleaned_data["user_type"]

            currKey = InstructorKey.objects.filter(key = form.cleaned_data["key"]).first()

            if user_type == "I" and currKey is None:
                messages.add_message(request, messages.INFO, 'The Instructor key was incorrect')
                return render(request, "register.html", { "form": form })

            try: # Try and create the new user object
                new_user = User.objects.create_user(email,
                                                    email=email,
                                                    password=password)
                new_user.profile.user_type = user_type
                if user_type == 'I':
                    currKey.delete()

                new_user.save() # save the new user to the database
            except IntegrityError:
                # Duplicate email: notify the user and bail on registering
                return render(request, "register.html", { "duplicate_email": True, "form": blank_form })


            user = authenticate(username=email, password=password)
            login(request, user)

            # Create an introduction notification to display to the new user
            create_introduction_notification(user)

            if user_type == 'S':
                # Allow instructors to join/create a section, students to join a section
                return HttpResponseRedirect("/joinsection/")
            else:
                return redirect_user_to_homepage(user_type)
        else:
            # The form data was bad, display an error
            return render(request, "register.html", { "invalid": True, "form": blank_form })
    else:
        # The user did not try and register, and just needs to see the register form
        return render(request, "register.html", { "form": blank_form })


@login_required
def instructor(request):
    """
    Get all the information from the database to display an instructor's homepage (messages, notifications, bids etc.)
    and then render the page
    """
    personalMessages = Message.objects.filter(recipient__id=request.user.id)
    bids = Bid.objects.filter(instructors__id=request.user.id)
    notifications = Notification.objects.filter(recipient__id=request.user.id)
    projs_to_approve = Project.objects.filter(is_approved=False)
    sections = Section.objects.all()

    context = {
        "notifications": notifications,
        "inbox": personalMessages,
        "bids": bids,
        "projects_to_approve": projs_to_approve
    }

    return render(request, "instructor.html", context)


@login_required
def client(request):
    """
    Render the client homepage.
    Grabs what is needed for the client: their projects / bids, notifications, and any questions
    on their projects
    """
    if request.method == "POST":
        # User submitted a project, add this project to the database
        form = ProjectSubmissionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            requirements = form.cleaned_data["requirements"]
            keywords = form.cleaned_data["keywords"]
            description = form.cleaned_data["description"]

            new_project = Project(name=name,
                                  requirements=requirements,
                                  keywords=keywords,
                                  description=description,
                                  client=request.user,
                                  is_approved=False)

            new_project.save()
        else:
            blank_form = LoginForm()
            return render(request, "client.html", { "invalid": True, "form": blank_form })
    form = ProjectSubmissionForm()
    reply_form = ReplyForm()
    bids = Bid.objects.filter(project__client__id=request.user.id)
    projects = Project.objects.filter(client_id=request.user.id)
    questions = Question.objects.filter(project__client__id=request.user.id)
    notifications = Notification.objects.filter(recipient__id=request.user.id)
    context = {
            "bids": bids,
            "form": form,
            "projects": projects,
            "questions": questions,
            "reply_form": reply_form,
            "notifications": notifications
    }
    return render(request, "client.html", context)


@login_required
def student(request):
    """
    Render the student homepage.
    Gets a few projects to display as a sample, and any messages / notifications for the student
    """
    try:
        Section.objects.get(students__id=request.user.id)
    except ObjectDoesNotExist:
        return HttpResponseRedirect("/joinsection/")

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            try:
                sender = request.user
                recipient = User.objects.get(email=form.cleaned_data["recipient"])
                subject = form.cleaned_data["subject"]
                text = form.cleaned_data["text"]

                new_message = Message(sender=sender,
                                      recipient=recipient,
                                      subject=subject,
                                      text=text)

                new_message.save()
            except KeyError:  #TODO Is this the right error?
                # TODO indicate that recipient does not exist
                pass
        else:
            # TODO indicate some kind of failure
            pass

    projects = Project.objects.filter(is_approved=True)[:5] # This is efficient according to docs, although it doesn't look that way
    personalMessages = Message.objects.filter(recipient__id=request.user.id)
    notifications = reversed(Notification.objects.filter(recipient__id=request.user.id))
    form = MessageForm()
    context = {
            "projects": projects,
            "inbox": personalMessages,
            "form": form,
            "notifications": notifications
    }
    return render(request, "student.html", context)


def projects(request):
    """
    Renders the view of the projects page (where users can browse a list of all projects in the system
    """
    # Read in all projects from the database
    projects = Project.objects.filter(is_approved=True) # only get projects instructors have approved
    return render(request, "projects.html", { "projects": projects })


@login_required
def project_view(request, project_id):
    """
    Renders an individual project page, where users can ask questions, look at asked questions/responses,
    and submit a bid.
    """
    proj = Project.objects.get(id=int(project_id))
    bid_success = False
    if request.method == "POST":
        # User submitted a bid on this project
        form = BidSubmissionForm(request.POST)
        if form.is_valid():
            team_members = form.cleaned_data["team_members"]
            description = form.cleaned_data["description"]
            section = Section.objects.get(students__id=request.user.id)

            new_bid = Bid(team_members=team_members, description=description, project=proj, is_approved=False, student=request.user)
            new_bid.save()
            new_bid.instructors.set(section.instructors.all())

            bid_success = True # TODO notify the user on the UI that the bid was submitted

            new_notification = Notification(recipient=request.user, subject="Bid on \"{}\" submitted.".format(proj.name),
                                            text="You submitted a bid with team members {}.  \
                                                  If the bid is awarded, you will receive \
                                                  another notification here.".format(team_members))
            new_notification.save()
    form = BidSubmissionForm()
    questions = Question.objects.filter(project__id=proj.id)
    question_form = QuestionForm()
    context = {
            "project": proj,
            "form": form,
            "bid_success": bid_success, # For showing a message that the bid was successfully saved
            "question_form": question_form,
            "questions": questions
    }
    return render(request, "project.html", context)


@login_required
def messages_internal(request):
    """
    Render the inbox of the user sending the request
    """
    messages_internal = Message.objects.filter(recipient__id=request.user.id)
    return render(request, "messages.html", { "messages": messages_internal })


@login_required
def join_a_section(request, section_id):
    """
    Render the page where instructors can go to make a new section and
    students can go to join a section
    """
    # If User already belongs to a section, remove them from the original
    if request.user.profile.section_id != None:
        old_section = Section.objects.get(id=int(request.user.profile.section_id))
        if request.user.profile.user_type == 'S':
            old_section.students.remove(request.user.id)
        else:
            assert False, "Invalid user type"
    # Add section
    if section_id != "":
        section = Section.objects.get(id=int(section_id))
        if request.user.profile.user_type == 'S':
            section.students.add(request.user)
            request.user.profile.section_id = section_id
            request.user.profile.save()
        else:
            assert False, "Invalid user type"
        return redirect_user_to_homepage(request.user.profile.user_type)

    sections = Section.objects.all()

    context = {
            "sections": sections
    }
    return render(request, "joinsection.html", context)

@login_required
def manage_sections(request):
    """
    Render the page where instructors can go to make a new section or
    edit existing ones.
    """

    if request.method == "POST":
        # Class is being submitted
        form = NewSectionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            new_section = Section(name=name)
            new_section.save()
            return redirect_user_to_homepage(request.user.profile.user_type)

    form = NewSectionForm()
    sections = Section.objects.all()
    context = {
            "form": form,
            "sections": sections,
            "listSize": sections.count()
    }
    return render(request, "managesection.html", context)

@login_required
def edit_a_section(request, section_id):
    """
    Render the page where instructors can go to make a new section and
    students can go to join a section
    """
    if section_id != "":
        # User is choosing to edit the section's name
        form = NewSectionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            section = Section.objects.get(id=int(section_id))
            setattr(section, "name", name)
            section.save()
            return redirect_user_to_homepage(request.user.profile.user_type)

    form = NewSectionForm()
    sections = Section.objects.all()
    context = {
            "form": form,
            "section_id": section_id
    }
    return render(request, "editsection.html", context)

@login_required
def send_message(request):
    """
    Render page where students / instructors can go to send a message to other users
    """
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            try:
                sender = request.user
                recipient = User.objects.get(email=form.cleaned_data["recipient"])
                subject = form.cleaned_data["subject"]
                text = form.cleaned_data["text"]

                new_message = Message(sender=sender,
                                      recipient=recipient,
                                      subject=subject,
                                      text=text)

                new_message.save()
            except KeyError:  #TODO Is this the right error?
                # TODO indicate that recipient does not exist
                pass
        else:
            # TODO indicate some kind of failure
            pass
    form = MessageForm()
    context = {
            "form": form,
    }
    return render(request, "sendmessage.html", context)

@login_required
def profile(request):
    """
    Endpoint for new users registering.
    Authenticated users will just be redirected to their homepage.
    If registration fails, the user is redirected to /register and an error appears
    """
    blank_form = ProfileForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data["tags"]
        else:
            # The form data was bad, display an error
            return render(request, "profile.html", { "invalid": True, "form": blank_form })
    else:
        # The user did not try and register, and just needs to see the register form
        return render(request, "profile.html", { "form": blank_form })
