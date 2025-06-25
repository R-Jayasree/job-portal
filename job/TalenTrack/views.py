from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from .models import JobSeeker, JobRecruiter
from django.contrib import messages
from .models import JobSeeker, JobRecruiter
import re
import os
from django.conf import settings

def firstpage(request):
    return render(request, 'firstpage.html')

def authenticate_job_seeker(username, password):
    users = JobSeeker.objects.filter(username=username)
    if not users.exists() :
        return None,False
    for user in users:
        if user.password == password:
            return user,True
    return user,False

def authenticate_job_recruiter(username, password):
    users = JobRecruiter.objects.filter(username=username)
    if not users.exists() :
        return None,False
    for user in users:
        if user.password == password:
            return user,True
    return user,False

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        if user_type == 'job_seeker':
            user,valid = authenticate_job_seeker(username, password)
        elif user_type == 'job_recruiter':
            user,valid = authenticate_job_recruiter(username, password)

        if user is None:
            messages.error(request, 'Username does not exist')
            return redirect('login')
        elif valid == False:
            messages.error(request, 'Incorrect password')
            return redirect('login')
        else :
            request.session['user_type'] = user_type
            request.session['user_id'] = user.id
            return redirect('home')
    return render(request,'login.html')    

def signup_view(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        # Password validation
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('signup')

        if not re.search(r"[A-Z]", password):
            messages.error(request, "Password must contain at least one uppercase letter.")
            return redirect('signup')

        if not re.search(r"[!@#\$%\^&\*]", password):
            messages.error(request, "Password must contain at least one special symbol.")
            return redirect('signup')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
        
        request.session['user_type'] = user_type
        request.session['username'] = username
        request.session['email'] = email
        request.session['password'] = password
        
        if user_type == 'job_seeker':
            return redirect('createjs')  
        elif user_type == 'job_recruiter':
            return redirect('createjr')
        else :
            return redirect('welcome')
    return render(request, 'signup.html')

def profile_view(request):
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    
    if user_type == 'job_seeker':
        user = JobSeeker.objects.get(id = user_id)
        return render(request, 'seeker_profile.html', {'user': user})
    
    elif user_type == 'job_recruiter':
        print("hiii")
        user = JobRecruiter.objects.get(id = user_id)
        return render(request, 'recruiter_profile.html', {'user': user})

def create_job_seeker(request):
    if request.method == 'POST':
        # Retrieve fields from request.POST
        username = request.session.get('username')
        email = request.session.get('email')
        password = request.session.get('password')
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        description = request.POST.get('description')
        job_post = request.POST.get('job_post')
        qualifications = request.POST.get('qualifications')
        skills = request.POST.get('skills')
        experience = request.POST.get('experience')
        work_history = request.POST.get('work_history')
        min_salary_expected = request.POST.get('min_salary_expected')
        max_salary_expected = request.POST.get('max_salary_expected')
        salary_constraint = request.POST.get('salary_constraint')
        certifications = request.POST.get('certifications')
        location = request.POST.get('location')
        location_constraint = request.POST.get('location_constraint')
        work_shift = request.POST.get('work_shift')
        work_shift_constraint = request.POST.get('work_shift_constraint')
        profile_picture = request.FILES.get('profile_picture')
        # Create a new JobSeeker instance
        job_seeker = JobSeeker(
            username=username,
            email=email,
            password=password,
            name=name,
            profile_picture = profile_picture,
            age = age,
            gender = gender,
            description=description,
            job_post=job_post,
            qualifications=qualifications,
            skills=skills,
            experience=experience,
            work_history=work_history,
            min_salary_expected=min_salary_expected,
            salary_constraint=salary_constraint,
            certifications=certifications,
            location=location,
            location_constraint=location_constraint,
            work_shift=work_shift,
            work_shift_constraint=work_shift_constraint
        )

        # Save the job seeker instance
        job_seeker.save()
        request.session['user_id']= job_seeker.id
        return redirect('home') 
    return render(request, 'create_seeker_profile.html')

def create_job_recruiter(request):
    if request.method == 'POST':
        # Retrieve fields from request.POST
        username = request.session.get('username')
        email = request.session.get('email')
        password = request.session.get('password')
        name = request.POST.get('name')
        description = request.POST.get('description')
        job_post = request.POST.get('job_post')
        qualifications_reqd = request.POST.get('qualifications_reqd')
        qualifications_constraint = request.POST.get('qualifications_constraint')
        skills_reqd = request.POST.get('skills_reqd')
        skills_constraint = request.POST.get('skills_constraint')
        experience_reqd = request.POST.get('experience_reqd')
        experience_constraint = request.POST.get('experience_constraint')
        salary_provided = request.POST.get('salary_provided')
        certifications = request.POST.get('certifications')
        certificates_constraint = request.POST.get('certificates_constraint')
        location = request.POST.get('location')
        work_shift = request.POST.get('work_shift')
        profile_picture = request.FILES.get('profile_picture')
        faq_document = request.FILES.get('faq_document')

        fs = FileSystemStorage()
        if faq_document :
            filename = fs.save(faq_document.name, faq_document)
        else :
            filename = None
        # Create a new JobRecruiter instance
        job_recruiter = JobRecruiter(
            username=username,
            email=email,
            password=password,
            name=name,
            profile_picture = profile_picture,
            description=description,
            job_post=job_post,
            qualifications_reqd=qualifications_reqd,
            qualifications_constraint=qualifications_constraint,
            skills_reqd=skills_reqd,
            skills_constraint=skills_constraint,
            experience_reqd=experience_reqd,
            experience_constraint=experience_constraint,
            salary_provided=salary_provided,
            certifications=certifications,
            certificates_constraint=certificates_constraint,
            location=location,
            work_shift=work_shift,
            faq_document=filename
        )
        # Save the job recruiter instance
        job_recruiter.save()
        request.session['user_id']= job_recruiter.id
        return redirect('home') 
    return render(request, 'create_recruiter_profile.html')

def home_view(request):
    return render(request, 'home.html')   

def update_profile_recruiter(request):
    user_id = request.session.get('user_id')
    user_profile = JobRecruiter.objects.get(id = user_id)
    if request.method == 'POST' :
        user_profile.company_name = request.POST['company_name']
        user_profile.description = request.POST['description']
        user_profile.job_post = request.POST['job_post']
        user_profile.qualifications_reqd = request.POST['qualifications_reqd']
        user_profile.qualifications_constraint = request.POST['qualifications_constraint']
        user_profile.skills_reqd = request.POST['skills_reqd']
        user_profile.skills_constraint = request.POST['skills_constraint']
        user_profile.experience_reqd = request.POST['experience_reqd']
        user_profile.experience_constraint = request.POST['experience_constraint']
        user_profile.salary_provided = request.POST['salary_provided']
        user_profile.certifications = request.POST['certifications']
        user_profile.certificates_constraint = request.POST['certificates_constraint']
        user_profile.location = request.POST['location']
        user_profile.work_shift = request.POST['work_shift']
        
        faq_document = request.FILES.get('faq_document')
        fs = FileSystemStorage()
        if faq_document :
            filename = fs.save(faq_document.name, faq_document)
        else :
            filename = None
        user_profile.faq_document = filename
        user_profile.save()
        return redirect('profile')
    return render(request, 'update_profile_recruiter.html', {'user_profile': user_profile})

def update_profile_seeker(request):
    user_id = request.session.get('user_id')
    user_profile = JobSeeker.objects.get(id = user_id)
    if request.method == 'POST':
        # Update the profile with the new data
        user_profile.name = request.POST['name']
        user_profile.age = request.POST['age']
        user_profile.description = request.POST['description']
        user_profile.job_post = request.POST['job_post']
        user_profile.qualifications = request.POST['qualifications']
        user_profile.skills = request.POST['skills']
        user_profile.experience = request.POST['experience']
        user_profile.min_salary_expected = request.POST['min_salary_expected']
        user_profile.salary_constraint = request.POST['salary_constraint']
        user_profile.certifications = request.POST['certifications']
        user_profile.location = request.POST['location']
        user_profile.location_constraint = request.POST['location_constraint']
        user_profile.work_shift = request.POST['work_shift']
        user_profile.work_shift_constraint = request.POST['work_shift_constraint']
        user_profile.save()
        return redirect('profile')
    
    return render(request, 'update_profile_seeker.html', {'user_profile': user_profile})

def update_profile(request):
    user_type = request.session.get('user_type')
    if user_type == 'job_seeker' :
        return redirect('updatejs')
    elif user_type == 'job_recruiter' :
        return redirect('updatejr')
    
def delete_profile(request):
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    if user_type == 'job_seeker':
        template = 'seeker_profile.html'
        user_profile = JobSeeker.objects.get(id=user_id)
    elif user_type == 'job_recruiter':
        template = 'recruiter_profile.html'
        user_profile = JobRecruiter.objects.get(id=user_id)
    confirmation_message = None

    if request.method == 'POST':
        if 'delete_profile' in request.POST:
            confirmation_message = "Are you sure you want to delete your profile?"

        elif 'confirm_delete' in request.POST:
            if request.POST['confirm_delete'] == 'yes':
                user_profile.delete()
                return redirect('welcome')  # Redirect to success page or homepage after deletion
            elif request.POST['confirm_delete'] == 'no':
                return redirect('profile')  # Redirect back to profile if deletion is canceled

    context = {
        'confirmation_message': confirmation_message,
        'user' : user_profile,
    }
    return render(request, template, context)

def job_list(request):
    # Retrieve all job posts
    all_jobs = JobRecruiter.objects.all()

    # Initialize a list to store matched jobs
    matched_jobs = []
    id = request.session.get('user_id')
    seeker = JobSeeker.objects.get(id = id)
    removed_jobs = []
    if seeker.removed_jobs is not None :
        removed_jobs = seeker.removed_jobs.split(',')
    weights = {'skills' : 20 , 'qualifications': 20, 'certifications' : 20, 'experience' : 10, 'salary' : 10, 'location' : 10, 'work_shift' : 10 }
    for job in all_jobs:
        # Check if the job post matches the job seeker's profile attributes
        job_ok = True
        if job.job_post == seeker.job_post:
            # First : Compare skills 
            job_skills = [i.strip().lower() for i in job.skills_reqd.split(',')]
            seeker_skills = [i.strip().lower() for i in seeker.skills.split(',')]
            matched_skills = []
            for i in job_skills :
                if i in seeker_skills :
                    matched_skills.append(i)
                # if required skill is not present in seeker's skill and skills required for the job is mandatory
                # then, the job is not matched
                elif job.skills_constraint == 'Mandatory' : 
                    job_ok = False
                    break
            if job_ok == False : 
                continue          # move to next job
            skills_weightage = len(matched_skills)/len(job_skills) * weights['skills']
            
            # Second : Compare qualifications
            job_qualifications = [i.strip().lower() for i in job.qualifications_reqd.split(',')]
            seeker_qualifications = [i.strip().lower() for i in seeker.qualifications.split(',')]
            matched_qualifications = []
            for i in job_qualifications :
                if i in seeker_qualifications :
                    matched_qualifications.append(i)

                elif job.qualifications_constraint == 'Mandatory' : 
                    job_ok = False
                    break
            if job_ok == False : 
                continue          # move to next job
            qualification_weightage = len(matched_qualifications)/len(job_qualifications) * weights['qualifications']

            # Third : Compare certifications 
            job_certifications = [i.strip().lower() for i in job.certifications.split(',')]
            seeker_certifications = [i.strip().lower() for i in seeker.certifications.split(',')]
            matched_certifications = []
            for i in job_certifications :
                if i in seeker_certifications :
                    matched_certifications.append(i)
                elif job.qualifications_constraint == 'Mandatory' : 
                    job_ok = False
                    break
            if job_ok == False : 
                continue          # move to next job
            certification_weightage = len(matched_certifications)/len(job_certifications) * weights['certifications']

            # Fourth : Compare salary requirement 
            if job.salary_provided < seeker.min_salary_expected :
                if seeker.salary_constraint == 'Mandatory':
                    job_ok = False
                else :
                    salary_weightage = job.salary_provided/seeker.min_salary_expected * weights['salary']
            else :
                salary_weightage = weights['salary']
            if job_ok == False :
                continue

            # Fifth : Compare experience requirement
            if (int(job.experience_reqd) <= int(seeker.experience)):
                experience_weightage = weights['experience']
            else :
                if job.experience_constraint == 'Mandatory':
                    job_ok = False
                else : 
                    experience_weightage = int(seeker.experience)/int(job.experience_reqd) * weights['experience']
            if job_ok == False :
                continue

            # Sixth : Compare location constraint 
            if job.location.lower() != seeker.location.lower() :
                if seeker.location_constraint == 'Mandatory' :
                    job_ok = False
                else :
                    location_weightage = 0
            else :
                location_weightage = weights['location']
            if job_ok == False :
                continue

            # Seventh : Compare work shift constraints  
            if (seeker.work_shift == 'Flexible Shift') or (seeker.work_shift == job.work_shift) :
                work_shift_weightage = weights['work_shift']
            else :
                if seeker.work_shift_constraint == 'Mandatory':
                    job_ok = False
                else :
                    work_shift_weightage = 0
            if job_ok == False :
                continue

            recommendation_percentage = skills_weightage + qualification_weightage + certification_weightage + experience_weightage + location_weightage + work_shift_weightage + salary_weightage
            if (str(job.id) not in removed_jobs) :
                matched_jobs.append([job,round(recommendation_percentage,2)])
    if matched_jobs == [] :
        print("no matched jobs")
    else :
        print(matched_jobs)
    # Pass the matched jobs to the template for rendering
    matched_jobs.sort(key=lambda x: x[1],reverse= True)
    return render(request, 'job_list.html', {'jobs': matched_jobs})

def seekers_list(request):
    # Retrieve all seekers from database
    all_seekers = JobSeeker.objects.all()

    # Initialize a list to store matched seekers
    matched_seekers = []
    id = request.session.get('user_id')
    job = JobRecruiter.objects.get(id = id)
    removed_seekers = []
    if job.removed_seekers is not None :
        removed_seekers = job.removed_seekers.split(',')
    weights = {'skills' : 25 , 'qualifications': 25, 'certifications' : 25, 'experience' : 25 }
    for seeker in all_seekers:
        # Check if the seekers' profile matches the job requirements
        seeker_ok = True
        if job.job_post == seeker.job_post:
            # First : Compare skills 
            job_skills = [i.strip().lower() for i in job.skills_reqd.split(',')]
            seeker_skills = [i.strip().lower() for i in seeker.skills.split(',')]
            matched_skills = []
            for i in job_skills :
                if i in seeker_skills :
                    matched_skills.append(i)
                # if required skill is not present in seeker's skill and skills required for the job is mandatory
                # then, the seeker is not matched
                elif job.skills_constraint == 'Mandatory' : 
                    seeker_ok = False
                    break
            if seeker_ok == False : 
                print(seeker,"not matched")
                continue          # move to next seeker
            skills_weightage = len(matched_skills)/len(job_skills) * weights['skills']
            
            # Second : Compare qualifications
            job_qualifications = [i.strip().lower() for i in job.qualifications_reqd.split(',')]
            seeker_qualifications = [i.strip().lower() for i in seeker.qualifications.split(',')]
            matched_qualifications = []
            for i in job_qualifications :
                if i in seeker_qualifications :
                    matched_qualifications.append(i)

                elif job.qualifications_constraint == 'Mandatory' : 
                    seeker_ok = False
                    break
            if seeker_ok == False : 
                print("seeker 2", seeker.name)
                continue          # move to next job
            qualification_weightage = len(matched_qualifications)/len(job_qualifications) * weights['qualifications']

            # Third : Compare certifications 
            job_certifications = [i.strip().lower() for i in job.certifications.split(',')]
            seeker_certifications = [i.strip().lower() for i in seeker.certifications.split(',')]
            matched_certifications = []

            for i in job_certifications :
                if i in seeker_certifications :
                    matched_certifications.append(i)
                elif job.certificates_constraint == 'Mandatory' : 
                    seeker_ok = False
                    break
            
            if seeker_ok == False : 
                print(job_certifications,seeker_certifications,matched_certifications)
                print("seeker 3", seeker.name)
                continue          # move to next job

            certification_weightage = len(matched_certifications)/len(job_certifications) * weights['certifications']
            
            # Fourth : Compare experience requirement
            if (int(job.experience_reqd) <= int(seeker.experience))  :
                experience_weightage = weights['experience']
            else :
                if job.experience_constraint == 'Mandatory':
                    seeker_ok = False
                else :
                    experience_weightage = int(seeker.experience)/int(job.experience_reqd) * weights['experience']
                     
            if seeker_ok == False :
                print("seeker 4", seeker.name)
                continue
            

            # Fifth : Compare salary requirement 
            if job.salary_provided < seeker.min_salary_expected :
                if seeker.salary_constraint == 'Mandatory':
                    seeker_ok = False
            if seeker_ok == False : 
                print("seeker 5", seeker.name)
                continue

            # Sixth : Compare location constraint 
            if job.location.lower() != seeker.location.lower() :
                if seeker.location_constraint == 'Mandatory' :
                    seeker_ok = False
            if seeker_ok == False :
                print("seeker 6", seeker.name)
                continue

            # Seventh : Compare work shift constraints  
            if (seeker.work_shift != 'Flexible Shift') and (seeker.work_shift != job.work_shift) and (seeker.work_shift_constraint == 'Mandatory') :
                seeker_ok = False
                print("seeker 7", seeker.name)
                continue
            recommendation_percentage = skills_weightage + qualification_weightage + certification_weightage + experience_weightage 
            if str(seeker.id) not in removed_seekers :
                matched_seekers.append([seeker,round(recommendation_percentage,2)])
    if matched_seekers == [] :
        print("no matched seekers")
    else :
        matched_seekers.sort(key=lambda x: x[1],reverse= True)
        print(matched_seekers)
    # Pass the matched seekers to the template for rendering
    return render(request, 'seekers_list.html', {'seekers': matched_seekers})

def recommendations(request):
    user_type = request.session.get('user_type')  # Adjust this according to how you store user type
    if user_type == 'job_seeker':
        return redirect('job_list')
    elif user_type == 'job_recruiter':
        return redirect('seekers_list')
    else:
        return redirect('home')  # Or some other default page

def view_details(request):
    if request.method == 'POST' :
        id = str(request.POST.get('id'))
        user_type = request.session.get('user_type')
        user_id = request.session.get('user_id')
        from_search = request.GET.get('from_search', False)
        request.session['from_search'] = from_search
        if user_type == 'job_seeker' :
            job = JobRecruiter.objects.get(id = id)
            seeker = JobSeeker.objects.get(id = user_id)
            applied_job_ids = []
            if seeker.applied_jobs is not None :
                applied_job_ids = seeker.applied_jobs.split(',')
            is_applied = False     # check if the seeker applied for the job, if so we need to hide the apply button
            if id in applied_job_ids :
                is_applied = True
            context = {
                'user': job,
                'from_search': from_search,
                'is_applied' : is_applied
            }
            return render(request,'job_details.html',context)
        elif user_type == 'job_recruiter' :
            seeker = JobSeeker.objects.get(id = id)
            job = JobRecruiter.objects.get(id = user_id)
            selected_seeker_ids = []
            if job.selected_seekers is not None :
                selected_seeker_ids = job.selected_seekers.split(',')
            is_selected = False     # check if the seeker applied for the job, if so we need to hide the apply button
            if id in selected_seeker_ids :
                is_selected = True
            context = {
                'user': seeker,
                'from_search': from_search,
                'is_selected' : is_selected
            }

            return render(request,'seeker_details.html',context)
        
def remove_from_recommendations(request):
    if request.method == 'POST' :
        user_type = request.session.get('user_type')
        user_id = request.session.get('user_id')
        id = request.POST.get('remove_id')
        if user_type == 'job_seeker' :
            user = JobSeeker.objects.get(id=user_id)
            remove_id = id + ','
            if user.removed_jobs is None :
                user.removed_jobs = remove_id
            else :
                user.removed_jobs += remove_id
            print(user.removed_jobs)
            user.save()
        elif user_type == 'job_recruiter' :
            user = JobRecruiter.objects.get(id=user_id)
            remove_id = id + ','
            if user.removed_seekers is None :
                user.removed_seekers = remove_id
            else :
                user.removed_seekers += remove_id
            user.save()
        return redirect('recommendations')
        
def search_jobs(request):
    if request.method == "POST":
        company_name = request.POST.get('company_name')
        job_post = request.POST.get('job_post')
        qualification = request.POST.get('qualification')
        salary_gt = request.POST.get('salary')
        location = request.POST.get('location')
        work_shift = request.POST.get('work_shift')
    else:
        company_name = job_post = qualification = salary_gt = location = work_shift = None
        return render(request,'search_jobs.html')
    
    jobs = JobRecruiter.objects.all()
    searched_jobs = []
    for job in jobs :
        if company_name:
            if job.name.lower() != company_name.lower():
                continue    # move to next job
        if job_post:
            if job.job_post.lower() != job_post.lower():
                continue
        if qualification :
            qualifications = [i.strip().lower() for i in qualification.split(',')]
            job_qualifications =  [i.strip().lower() for i in job.qualifications_reqd.split(',')]
            matched_qualifications = [i for i in qualifications if i in job_qualifications ]
            if len(matched_qualifications) != len(qualifications) :
                continue
        if salary_gt:
            if job.salary_provided < int(salary_gt):
                continue
        if location:
            if job.location.lower() != location.lower():
                continue
        if work_shift:
            if job.work_shift.lower() != work_shift.lower():
                continue
        searched_jobs.append(job)
    return render(request, 'search_jobs_results.html', {'jobs': searched_jobs})   

def search_seekers(request):
    if request.method == 'POST' :
        job_post = request.POST.get('job_post')
        qualification = request.POST.get('qualification')
        skills = request.POST.get('skills')
        experience_min = request.POST.get('experience_min')
        experience_max = request.POST.get('experience_max')
        certifications = request.POST.get('certifications')
        gender = request.POST.get('gender')
    else :
        job_post = qualification = skills = experience_max = experience_min = certifications = None
        return render(request,'search_seekers.html')
    print(job_post,qualification,skills,experience_max,experience_min,certifications)
    seekers = JobSeeker.objects.all()
    searched_seekers = []

    for seeker in seekers:
        if job_post :
            if job_post.lower() != seeker.job_post.lower():
                continue

        if qualification :
            job_qualifications = [i.strip().lower() for i in qualification.split(',')]
            seeker_qualifications = [i.strip().lower() for i in seeker.qualifications.split(',')]
            matched_qualifications = [i for i in job_qualifications if i in seeker_qualifications]
            print(job_qualifications,seeker_qualifications,matched_qualifications)
            if len(matched_qualifications) != len(job_qualifications) :
                continue

        if skills :
            job_skills = [i.strip().lower() for i in skills.split(',')]
            seeker_skills = [i.strip().lower() for i in seeker.skills.split(',')]
            matched_skills = [i for i in job_skills if i in seeker_skills]
            if len(matched_skills) != len(job_skills) :
                continue

        if experience_min :
            if (int(seeker.experience) < int(experience_min)):
                continue

        if experience_max :
            if (int(seeker.experience) > int(experience_max)):
                continue

        if certifications :
            job_certifications = [i.strip().lower() for i in certifications.split(',')]
            seeker_certifications = [i.strip().lower() for i in seeker.certifications.split(',')]
            matched_certifications = [i for i in job_certifications if i in seeker_certifications]
            if len(matched_certifications) != len(job_certifications) :
                continue
        if gender :
            if seeker.gender != gender :
                continue
        searched_seekers.append(seeker)

    return render(request, 'search_seekers_results.html', {'seekers': searched_seekers})    

def search_view(request):
    user_type = request.session.get('user_type')  # Adjust this according to how you store user type
    if user_type == 'job_seeker':
        return redirect('search_jobs')
    elif user_type == 'job_recruiter':
        return redirect('search_seekers')
    else:
        return redirect('home')  # Or some other default page

def select_seeker(request):
    if request.method == 'POST' :
        seekerid = str(request.POST.get('seeker_id'))
        seeker = JobSeeker.objects.get(id = int(seekerid))
        user_id = request.session.get('user_id')
        job = JobRecruiter.objects.get(id=user_id)
        id = seekerid + ','
        if job.selected_seekers is None :
            job.selected_seekers = seekerid + ','
        else :
            selected_seekers = job.selected_seekers.split(',')
            if str(seekerid) not in selected_seekers :
                job.selected_seekers += seekerid + ','
        job.save()
        context = {
                'user': seeker,
                'from_search': request.session.get('from_search'),
                'is_selected' : True
            }
        return render(request,'seeker_details.html',context)
    else :
        return render(request,'seekers_list.html')

def applied_seekers(request):
    user_id = request.session.get('user_id')
    recruiter = JobRecruiter.objects.get(id=user_id)
    seekers = JobSeeker.objects.all()
    applied_seekers = []
    for seeker in seekers :
        if seeker.applied_jobs is not None :
            applied = seeker.applied_jobs.split(',')
            if str(recruiter.id) in applied :
                applied_seekers.append(seeker)
    return applied_seekers

def selected_seekers(request) :
    user_id = request.session.get('user_id')
    job = JobRecruiter.objects.get(id = user_id)
    seekers = JobSeeker.objects.all()
    selected_seekers = []
    if job.selected_seekers is not None :
        selected_seekers_ids = job.selected_seekers.split(',')
        for seeker in seekers :
            if str(seeker.id) in selected_seekers_ids :
                selected_seekers.append(seeker)
    return selected_seekers

def apply_job(request):
    if request.method == 'POST' :
        jobid = str(request.POST.get('job_id'))
        job = JobRecruiter.objects.get(id = jobid)
        user_id = request.session.get('user_id')
        seeker = JobSeeker.objects.get(id=user_id)
        id = jobid + ','
        if seeker.applied_jobs is None :
            seeker.applied_jobs = jobid + ','
        else :
            applied = seeker.applied_jobs.split(',')
            if str(jobid) not in applied :
                seeker.applied_jobs += id
        seeker.save()
        print(seeker.applied_jobs)
        context = {
                'user': job,
                'from_search': request.session.get('from_search'),
                'is_applied' : True
            }
        return render(request,'job_details.html',context)
    else :
        return render(request,'job_list.html')
    
def selected_jobs(request):
    user_id = request.session.get('user_id')
    seeker = JobSeeker.objects.get(id=user_id)
    jobs = JobRecruiter.objects.all()
    selected_jobs = []
    for job in jobs :
        if job.selected_seekers is not None :
            selected = job.selected_seekers.split(',')
            if str(seeker.id) in selected :
                selected_jobs.append(job)
    return selected_jobs

def applied_jobs(request) :
    user_id = request.session.get('user_id')
    seeker = JobSeeker.objects.get(id = user_id)
    jobs = JobRecruiter.objects.all()
    applied_jobs = []
    if seeker.applied_jobs is not None :
        applied_job_ids = seeker.applied_jobs.split(',')
        for job in jobs :
            if str(job.id) in applied_job_ids :
                applied_jobs.append(job)
    return applied_jobs

def notification_view(request) :
    active_tab = request.GET.get('tab', 'received')  # Default to 'received'
    user_type = request.session.get('user_type')
    if user_type == 'job_seeker' :
        if active_tab == 'received' :
            jobs = selected_jobs(request)
        elif active_tab == 'sent' :
            jobs = applied_jobs(request)
        
        context = {'active_tab': active_tab,
                'jobs' : jobs}
        print(context)
        return render(request, 'notification_seekers.html', context)
    
    elif user_type == 'job_recruiter' :
        if active_tab == 'received' :
            seekers = applied_seekers(request)
            context = {'active_tab': active_tab,
                'seekers' : seekers}
        elif active_tab == 'sent' :
            seekers = selected_seekers(request)
            context = {'active_tab': active_tab,
                'seekers' : seekers}
        elif active_tab == 'queries' :
            job_id = request.session.get('user_id')
            job = JobRecruiter.objects.get(id=job_id)
            faqs = []
            if job.faq_document:
                file_path = os.path.join(settings.MEDIA_ROOT, job.faq_document.name)
                faqs = parse_faq_file(file_path)
            if request.method == 'POST' :
                for i in range(len(faqs)):
                    qs = faqs[i][0]
                    user_answer = request.POST.get(f'answer_{qs}')
                    print("user gave ::", user_answer)
                    if user_answer:
                        faqs[i] = [qs,user_answer]
                        ans = user_answer
                
                with open(file_path,'w') as file :
                    for qs,ans in faqs :
                        file.write(qs + '\n')
                        file.write(ans + '\n')
                        print(qs,ans)
                job.faq_document.name = file_path 
                job.save()
                print(faqs)
            context = {'active_tab': active_tab,
                'faqs' : faqs}
    
        return render(request, 'notification_recruiter.html', context)

def parse_faq_file(file_path):
    questions = []
    answers = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if lines[i].strip().endswith('?'):
                question = lines[i].strip()
                answer = lines[i+1].strip()
                questions.append(question)
                answers.append(answer)
                i += 2  # Move to the next set of question-answer pair
            else:
                ans = answers[-1]
                ans = ans + '\n' + lines[i]
                answers[-1] = ans
                i+=1 # Skip lines that are not questions (assuming all questions end with '?')
    faqs = [[questions[i],answers[i]] for i in range(len(questions))]
    return faqs


def faq_view(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        job = JobRecruiter.objects.get(id=job_id)
        faqs = []

        # Parse FAQs from the document (if available)
        if job.faq_document:
            file_path = os.path.join(settings.MEDIA_ROOT, job.faq_document.name)
            faqs = parse_faq_file(file_path)
        # Get the user's question
        user_question = request.POST.get('question')
        user_answer = False
        if user_question:
            user_answer = "We will let you know, please check back after some time."
            for i in faqs :
                if i[0].lower() == user_question.lower() :
                    user_answer = i[1]
            if user_answer == "We will let you know, please check back after some time." :
                faqs.append([user_question, user_answer])

            with open(file_path,'w') as file :
                    for qs,ans in faqs :
                        file.write(qs + '\n')
                        file.write(ans + '\n')
                        print(qs,ans)
            job.faq_document.name = file_path 
            job.save()  

        return render(request, 'faq.html', {'faqs': faqs, 'job_id': job_id,'user_question' : user_question, 'user_answer' : user_answer})

    