# Projectr

Projectr is a web application allowing for client-based group project courses to run more smoothly.
Potential clients can submit projects, students can bid on them, and instructors can award bids to students.

# Release Notes

### Features

#### General Features
* Students, instructors, and clients can register and passwords are stored with the Django-provided hashing mechanism.

#### Student Features
* Students can select a section to join, which will make their bids show up on their instructors dashboard.
* Students can view submitted projects and browse for interesting projects to submit bids on.
* Students can submit questions on a project that show up for the client to respond to on their dashboard, in case it is not clear
  what the student would be signing up to do if they bid on the project.
* Students can send messages to other users, in particular their instructors.
* Students will receive notifications if their bids are accepted or rejected by their instructors.

#### Instructor Features
* Instructors can send and receive messages to other users
* Instructors can see bids that have been submitted (bids include team member names and a description of why they should be awarded the project) and opt to accept or reject them.
* Instructors can view projects submitted by clients and either accept them or reject them.

#### Client Features
* Clients can submit new projects, which will appear for students to bid on after an instructor approves it.
* Clients can check the status of projects they have submitted (whether they have been approved, and if so, if there are any bids on them).
* Clients can respond to questions submitted on their projects by students.
* Clients will receive notifications if their projects are rejected.



### Bug Fixes
This is release 1.0 and there have been no previous releases.



### Bugs and Defects
* The application aims to streamline the bidding and project submission process, and does not attempt to manage the lifetime of the project.
* Email notifications are not sent, only in-app notifications are displayed for important events.
* The server does not dump any logs about requests made to the server


# Install Guide

### Prerequisites
* The system has been tested being deployed on Linux (Ubuntu 15, Arch-Linux), Windows, and OS X.
  Operating System compatabilities should not be expected.
* A [python](https://www.python.org) 2 interpreter
* [pip](https://pip.pypa.io/en/stable/installing/) the Python package manager
* [MySQL](http://www.mysql.com/) database engine.  Alternative implementations such as [MariaDB](https://mariadb.com) have been tested as well.
* git for retrieving the source code.

These can be installed easily from your system package manager.  The following example works on Pacman-based Linux machines.
Refer to your package manager's documentation for the names of these packages.

```$ pacman -S python2 pip2 mariadb git```


### Dependent Libraries
The only library requirement is to install Django from pip.

```$ pip install Django```


### Download Instructions
Users will not need to download / install the application themselves, since they will access it from a web browser.
Only one instance of the application needs to be deployed on the server, so there is no binary release.
The source code can be obtained from this repo with the following command:

```$ git clone https://github.com/rguthrie3/Projectr```


### Installation
There is no installation step, as a binary image does not need to reside in user's filesystems.
The application only needs to be deployed.
Refer to the deployment section below.


### Deployment
Deployment involves running the application on a server that other users can send requests to.
Typically, this is done by renting space on a cloud server.
Examples of services that allow for easy deployment are [Heroku](https://heroku.com) and [DigitalOcean](https://digitalocean.com).
Refer to your respective hosting service's guide for getting access to a cloud instance.
Once you can access a terminal to input commands to your cloud instance, follow the above steps to acquire the necessary software and
retrieve a copy of the source code.
There are a few extra steps after this to finish deployment:

#### Preparing the Database
Django has support for database migrations, which means it generates SQL code based on your Python objects to create and update your database schema.
Django needs to be told to do this.
First create the database.

1. Log into MySQL

```$ mysql -u <username> -p <password>```

2. Create the "projectr" database

```> create database projectr; exit```

3. Generate the migrations from Django (assuming your current directory is the root of the project)

```$ python manage.py makemigrations```

```(if you are running it dfor the first time use : $ python manage.py makemigrations projectr)```

```$ python manage.py migrate```

#### Running the Server
Once the database is generated, the application can be ran with the following command

```$ python manage.py runserver```

### Troubleshooting
* During development, if Django database migrations are causing problems (error messages, etc.), the easiest fix is to just force it to re-create the entire development database
  (do not do this in production!).  Delete the database in MySQL then delete the migrations, then follow the steps from Preparing the Database above to recreate it.

```$ mysql -u <username> -p <root>```

```> drop database projectr; exit```

```$ rm projectr/migrations/00*```
