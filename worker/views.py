from django.shortcuts import render,HttpResponse,redirect
from . models import Farmer,Worker,Crop
from django.db.models import Count, Sum
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.db.models import F, ExpressionWrapper, DecimalField

# Create your views here.
def farmer(request):
    if request.method=="GET":
        return render(request,'former.html')

    if request.method == "POST":
        aadhar = request.POST.get('aadhar')
        phone_number = request.POST.get('phone_number')
        name = request.POST.get('name')
        date_of_start = request.POST.get('date_of_start')
        crop_type = request.POST.get('crop_type')
        image = request.FILES.get('image')  # Get uploaded image file

        # Save to the database
        Farmer.objects.create(
            aadhar=aadhar,
            phone_number=phone_number,
            name=name,
            date_of_start=date_of_start,
            crop_type=crop_type,
            image=image,
        )

        return HttpResponse('success stored')  # Redirect to a success page

     # Render the form on GET
def farmerlist(request):
    farmers = Farmer.objects.all()  # Fetch all farmers from the database
    return render(request, 'flist.html', {'farmers': farmers})
def crop(request):
    if request.method=="GET":
        return render(request,'crop.html')
def worker(request):
    if request.method=="GET":
        return render(request,'worker.html')
def worker(request):
    if request.method == "POST":
        # Get data from the POST request
        aadhar = request.POST.get('aadhar')
        phone_number = request.POST.get('phone_number')
        name=request.POST.get('name')
        father_name = request.POST.get('father_name')  # Changed from 'name' to 'father_name'
        job_type = request.POST.get('job_type')  # Assuming you have this field
        image = request.FILES.get('image')  # Get the uploaded image file

        # Save the data into the Worker model
        Worker.objects.create(
            aadhar=aadhar,
            phone_number=phone_number,
            name=name,
            father_name=father_name,
            job_type=job_type,
            image=image,
        )

        return render(request,'worker.html')  # You can change this to redirect to another page or show a success message

    return render(request, 'worker.html') 

def workerlist(request):
    if request.method == "GET":
        workers_list = Worker.objects.all()  # Fetch all workers from the database
        return render(request, 'workerslist.html', {'workers': workers_list})

def crop(request):
    if request.method == 'POST':
        farmer_aadhar = request.POST.get('farmer_aadhar')
        worker_aadhar = request.POST.get('worker_aadhar')
        crop_name = request.POST.get('crop_name')
        working_date = request.POST.get('working_date')
        per_day_price = request.POST.get('per_day_price')

        try:
            # Ensure the farmer and worker exist
            farmer = Farmer.objects.get(aadhar=farmer_aadhar)
            worker = Worker.objects.get(aadhar=worker_aadhar)

            # Check if the worker is already assigned to the same farmer on the same date
            if Crop.objects.filter(farmer_aadhar=farmer, worker_aadhar=worker, working_date=working_date).exists():
                return render(request, 'crop.html', {'error': 'Worker is already assigned to this farmer on the same date!'})

            # Create and save the new crop entry
            Crop.objects.create(
                farmer_aadhar=farmer,
                worker_aadhar=worker,
                crop_name=crop_name,
                working_date=working_date,
                per_day_price=per_day_price
            )

            return render(request, 'crop.html', {'error': 'Worker added successfully!'})  # Success message

        except Farmer.DoesNotExist:
            return render(request, 'crop.html', {'error': 'Farmer not found!'})
        except Worker.DoesNotExist:
            return render(request, 'crop.html', {'error': 'Worker not found!'})

    return render(request, 'crop.html')
    
def croplist(request):
    if request.method == "GET":
        # Fetch all crop records
        crops = Crop.objects.all()

        # Pass the crops to the template to display
        return render(request, 'croplist.html', {'crops': crops})
from django.shortcuts import render
from django.db.models import Count, Sum
from .models import Crop  # Ensure Crop model is correctly imported

def workingdetails(request):
    if request.method == "GET":
        return render(request, 'worker_work.html')

    if request.method == "POST":
        farmer_aadhar = request.POST.get('farmer_aadhar')  # Use POST instead of GET
        worker_aadhar = request.POST.get('worker_aadhar')

        if not (farmer_aadhar and worker_aadhar):
            return render(request, 'worker_work.html', {'error': 'Invalid request'})

        # Fetch worker's records for a specific farmer
        worker_work = Crop.objects.filter(farmer_aadhar_id=farmer_aadhar, worker_aadhar_id=worker_aadhar) \
                                  .values('working_date', 'per_day_price') \
                                  .annotate(total_days=Count('working_date'))

        # Calculate total sum of earnings
        total_earning = Crop.objects.filter(farmer_aadhar_id=farmer_aadhar, worker_aadhar_id=worker_aadhar) \
                                    .aggregate(total_sum=Sum('per_day_price'))['total_sum'] or 0

        return render(request, 'worker_work.html', {
            'worker_work': worker_work,
            'total_earning': total_earning,
            'total_days': len(worker_work)  # Count unique working days
        })
def mainpage(request):
    if request.method=="GET":
        return render(request,'mainpage.html')
from django.contrib.auth import login as auth_login, authenticate

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Using auth_login to avoid conflict with the view name
            return redirect('mainpageurl')  # Redirect after successful login
        else:
            # Handle invalid login attempt
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')


def signup(request):
    if request.method=="GET":
        emptyform=UserCreationForm()
        return render(request,'signup.html',{'form':emptyform})
    if request.method=="POST":
        dataform=UserCreationForm(request.POST)
        if dataform.is_valid()==True:
            dataform.save()
            return redirect('loginpageurl')
        else:
            return render(request,'signup.html',{'form':dataform})
def logout(request):
    auth_logout(request)  
    return redirect('mainpageurl')
def countofworker(request):
    if request.method == "GET":
        return render(request, 'worker_work_summary.html')

    if request.method == "POST":
        farmer_aadhar = request.POST.get('farmer_aadhar')
        worker_aadhar = request.POST.get('worker_aadhar')

        if not (farmer_aadhar and worker_aadhar):
            return render(request, 'worker_work_summary.html', {'error': 'Invalid request'})

        # Count working days and total earnings for each worker-farmer pair
        worker_summary = (
            Crop.objects.filter(farmer_aadhar_id=farmer_aadhar, worker_aadhar_id=worker_aadhar)
            .values('farmer_aadhar_id', 'worker_aadhar_id')
            .annotate(total_days=Count('working_date', distinct=True), total_earning=Sum('per_day_price'))
        )

        return render(request, 'worker_work_summary.html', {'worker_summary': worker_summary})
    
def farmerworkerreport(request):
    workers_per_day = None
    farmer_aadhar = None

    if request.method == "POST":
        farmer_aadhar = request.POST.get('farmer_aadhar')

        if farmer_aadhar:
            # Count workers per day for the given farmer
            workers_per_day = (
                Crop.objects.filter(farmer_aadhar_id=farmer_aadhar)
                .values('working_date')
                .annotate(worker_count=Count('worker_aadhar_id', distinct=True))
                .order_by('working_date')
            )

    return render(request, 'farmer_worker_report.html', {
        'workers_per_day': workers_per_day,
        'farmer_aadhar': farmer_aadhar
    })
from django.db.models import Count, Sum, F

from django.db.models import Count, F, Sum

from django.shortcuts import render
from django.db.models import Count, Sum
from .models import Crop

def totalfarmerworkerreport(request):
    workers_per_day = None
    farmer_aadhar = None
    total_worker_count = 0
    total_earning = 0

    if request.method == "POST":
        farmer_aadhar = request.POST.get('farmer_aadhar')

        if farmer_aadhar:
            # Get workers per day along with their total per-day price
            workers_per_day = (
                Crop.objects.filter(farmer_aadhar_id=farmer_aadhar)
                .values('working_date')
                .annotate(
                    worker_count=Count('worker_aadhar_id'), 
                    per_day_total=Sum('per_day_price')
                )
                .order_by('working_date')
            )

            # Calculate total workers in all days
            total_worker_count = sum(entry['worker_count'] for entry in workers_per_day)
            # Calculate total earning for all days
            total_earning = sum(entry['per_day_total'] for entry in workers_per_day)

    return render(request, 'farmer_worker_report2.html', {
        'workers_per_day': workers_per_day,
        'farmer_aadhar': farmer_aadhar,
        'total_worker_count': total_worker_count,  
        'total_earning': total_earning  
    })
