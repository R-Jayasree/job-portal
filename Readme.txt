Problem Statement :
-------------------
To create a mediating platform through which
Job seekers:
       can explore open positions matching their profiles.
Job recruiters:
       can search for deserving applicants who meet their job requirements

Design :
-------------------

Language used (Backend) :  Python 
Web Framework           :  Django
Frontend                :  HTML, CSS
Database                :  SQLite3


Modules :
-------------------

1. Login and Sign up:
     a) authenticate_user() :  Users are authenticated by their username and password from database
     b) login_view()        :  Allows users to login to the portal
     c) signup_view()       :  Allows users to SignUp on their first use of portal


2. Profile management:
     a) create_profile()   :  To create user's profile by collecting the necessary information. 
     b) update_profile()   :  User can update his/her profile anytime
     c) delete_profile()   :  User can permanently logoff from the portal
	
           
3. Matching:
     a) The job_list()      : pairs job seekers with relevant openings based on criterias like 
                              skills, qualifications, experience,location, salary,etc.
     b) The seekers_list()  : pairs job recruiters with relevant seekers based on their specifications 
                              
4. Search:
     a) search_jobs()       : Job seekers can search for open jobs by applying various search filters.
     b) search_seekers()    : Job recruiters can search for employees 

5. Notification:
     a) apply_job()             : Job seekers can apply for any job
        view_applied_seekers()  : Job recruiters can view the list of seekers who have applied for their job

     b) select_employee()       : Job recruiters can hire employees
        view_selected_jobs()    : Job seekers can view the list of jobs for which they have got selected
    
     c) view_queries()         : Job recruiters can view the queries they have got from seekers related to their job

6. FAQ:
     a) faq_view()   :  Job seekers can view the frequently asked questions of a job and can also ask questions



Project Structure :
-----------------------

myproject/
├── .dist/
│   
├── include/
│   
├── job/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py    
│   │   ( contains all the website urls )
│   ├── wsgi.py
│   ├── media/
│   │   ├── faq_documents/
│   │   └── profile_pictures/
│   │   
│   ├── TalenTrack/
│   │   ├── migrations/
│   │   ├── templates/
│   │   │    ( contains all the html templates )
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── views.py
│   │   │    ( complete backend code )
│   │   ├── urls.py
│   │   │    ( contains all the app urls )
│   │   ├── tests.py
│   │   └── models.py
│   │        ( contains the models JobSeeker and JobRecruiter )
│   ├── dbsqlite3
│   └── manage.py
│
├── Lib/
│   
├── Scripts/
│  
└── pyvenv



