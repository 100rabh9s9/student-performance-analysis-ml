from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student_reg
from django.contrib.auth import logout


# Create your views here.
def index(request):
    return render(request, "index.html")


def studentReg(request):
    if request.POST:
        username1=request.POST['name']
        email1=request.POST['email']
        phonenumber1=request.POST['phone']
        password1=request.POST['password']
        dept1=request.POST['department']
        year1=request.POST['year']
        image1=request.FILES['image']
        address1=request.POST['address']
        if Student_reg.objects.filter(Email=email1).exists():
            messages.info(request,"Already Have Registered")
        else:
            user=Login.objects.create_user(
            username=email1,password=password1,usertype='student',viewPassword=password1)
            user.save()
            register=Student_reg.objects.create(
            Username=username1,Email=email1,Phonenumber=phonenumber1,Password=password1,Image=image1,Address=address1,Dept=dept1,Year=year1,logid=user)
            register.save()
            messages.info(request,"Registered Successfully")
            return redirect("/login")
    return render(request, "studentRegister.html")


def login(request):
    if request.POST:
        Email2=request.POST['email']
        Password2=request.POST['password']
        user=authenticate(username=Email2,password=Password2)
        if user is not None:
            if user.usertype=="admin":
                messages.info(request,"Login As Admin")
                return redirect("/adminHome")
            elif user.usertype=="student":
                request.session['uid']=user.id
                messages.info(request,"Login As Student")
                return redirect("/studentHome")
            elif user.usertype=="guide":
                request.session['uid']=user.id
                messages.info(request,"Login As Guide")
                return redirect("/guideHome")    
            else:
                messages.info(request,"Invalid Username Or Password")
                return redirect("/login")
        else:
            messages.info(request,"Invalid Username Or Password")
            return redirect("/login")
    return render(request, "login.html")

def log_out(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('/') 

# ==================================    COORDINATOR(ADMIN)    ==================================
def adminHome(request):
    users = Student_reg.objects.all().order_by('id')  # Forces DB reload
    return render(request, "STUDENT/adminHome.html", {'users': users})  


# from django.shortcuts import render, get_object_or_404, redirect
# from app.models import Student_reg

def updatestudent(request, student_id):
    print("Received POST Data:", request.POST)
    student = get_object_or_404(Student_reg, id=student_id)  # Fetch student by ID
    
    if request.method == "POST":
        student.Username = request.POST.get('username')
        student.Email = request.POST.get('email')
        student.Phonenumber = request.POST.get('phone') or student.Phonenumber
        student.Password = request.POST.get('password')  # Ideally, hash passwords
        student.Dept = request.POST.get('department')
        student.Year = request.POST.get('Year')  # 🔹 FIX: Match model field name
        student.Address = request.POST.get('address')

        # Handle image update
        if 'image' in request.FILES:
            student.Image = request.FILES['image']

        print(f"🔹 Before Save - Username: {student.Username} | Year: {student.Year}")  # Debugging
        student.save()
        print(f"🔹 After Save - Username: {student.Username} | Year: {student.Year}")  # Debugging

        return redirect("adminHome")  # Redirect to the admin home page

    return render(request, "STUDENT/updatestudent.html", {"student": student})


def deletestudent(request, student_id):
    student = get_object_or_404(Student_reg, id=student_id)

    # First delete the Login object if exists
    if student.logid:
        student.logid.delete()

    # Then delete the student record
    student.delete()

    return redirect('adminHome')


# ========================================    STUDENT    =======================================

def studentHome(request):
    return render(request, "STUDENT/studentHome.html")


def addProjectAbstract(request):
    uid = request.session['uid']
    student = Student_reg.objects.get(logid=uid)
    # id = request.GET.get('id')
    # guide = Guide.objects.get(id=id)
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        abstract_file = request.FILES.get('abstract_file')
        pro=ProjectAbstract.objects.create(
            title=title,
            description=description,
            abstract_file=abstract_file,
            uid=student
        )
        pro.save()
        messages.success(request, "Project abstract submitted successfully!")
        # return redirect('viewProjectAbstracts')
    return render(request, "STUDENT/addAbstract.html")

def blogdetail(request):
    return render(request, "STUDENT/blog-detail.html")



# ======================================================
from django.shortcuts import render
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression

def performance_prediction(request):
    student_performance = None

    if request.method == "POST":
        # Collect input from the student
        try:
            math_score = float(request.POST['math_score'])
            reading_score = float(request.POST['reading_score'])
            writing_score = float(request.POST['writing_score'])
        except ValueError:
            return render(request, 'your_template.html', {'error': 'Invalid score input.'})

        # Load the dataset
        df = pd.read_csv('./StudentsPerformance.csv')
        # df = pd.read_csv('../../studentsPerformance.csv')

        # Calculate average score for each student
        df['average_score'] = (df['math score'] + df['reading score'] + df['writing score']) / 3

        # Encode categorical variables
        for column in ['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course']:
            df[column] = LabelEncoder().fit_transform(df[column])

        # Features and Target
        X = df[['math score', 'reading score', 'writing score']]
        y = (df['average_score'] >= 75).astype(int)

        # Split the dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Standardize the data
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        # Train Logistic Regression model
        model = LogisticRegression()
        model.fit(X_train, y_train)  

        # Predict with student input
        student_input = scaler.transform([[math_score, reading_score, writing_score]])
        student_prediction = model.predict(student_input)
        student_performance = "High Performer" if student_prediction[0] == 1 else "Needs Improvement"


    return render(request, 'STUDENT/addAbstract.html', {'student_performance': student_performance})
