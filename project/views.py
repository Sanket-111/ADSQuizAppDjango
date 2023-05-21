
from django.contrib import messages
from django.shortcuts import redirect, render
import mysql.connector as sql
import json
from django.http import JsonResponse
# Create your views here.
std_id=0
quiz_id=0
def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('password')
        
        if username=="" or pass1=="":
             messages.warning(request,"Fields Can't Be Empty !!")
             return redirect('login')
        if username=="Patil" and pass1=="Patil":
             return redirect('home')
        if username=="Patil" and pass1!="Patil":
             messages.warning(request,"No Such Teacher Record Found ! Incorrect Username Or Password !!!")
             return redirect('login')
        else:
            m=sql.connect(host="localhost",user="root",passwd="system",database="ads3")
            cursor=m.cursor()
            st1="select * from student where id= '{}' and password='{}'".format(username,pass1)
            cursor.execute(st1)
            t=tuple(cursor.fetchall())
            if t==():
             messages.warning(request,"No Such Student Record Found ! Check Username And Password Again !")
             return redirect('login')
            else:
                global std_id 
                std_id = username
                return redirect('studenthome')


    return render (request,'login.html')
def HomePage(request):
   return render (request,'home.html')
def AddStudentPage(request):
   
    if request.method=='POST':
        m=sql.connect(host="localhost",user="root",passwd="system",database="ads3")
        if m.is_connected():
            print("Successfully Connected to MySQL database.")
        else:
            print("Check yo inputs, they really correct?")
        name=request.POST.get('name')
        roll=request.POST.get('id')
        dept_name=request.POST.get('dept_name')
        password=request.POST.get('password')
        toal_credit=request.POST.get('total_credit')
        if name=="" or roll=="" or dept_name=="" or password=="" or toal_credit=="":
              messages.warning(request,"All  Fields are menadetory ")
              return redirect('addstudent')
        cursor=m.cursor()
        st1="select * from department where dept_name= '{}'".format(dept_name)
        cursor.execute(st1)
        t=tuple(cursor.fetchall())
        if t==():
             messages.warning(request,"Invalid Department Name !!")
             return redirect('addstudent')
        st1="select * from student where ID= '{}'".format(roll)
        cursor.execute(st1)
        t=tuple(cursor.fetchall())
        if t!=():
             messages.warning(request,"Studnet With This ID is already Registered !!!")
             return redirect('addstudent')
        cd="insert into student values ('{}','{}','{}','{}','{}')".format(roll,name,dept_name,toal_credit,password)
        cursor.execute(cd)
        m.commit()
        messages.success(request,"Registration  Succesful!! , Student Can Now LogIn with The Credentials !")
        return redirect('addstudent')

    return render (request,'addstudent.html')

def AddQuestionPage(request):
    if request.method == 'POST':
        
        question_text = request.POST['question']
        option_a = request.POST['optionA']
        option_b = request.POST['optionB']
        option_c = request.POST['optionC']
        option_d = request.POST['optionD']
        answer = request.POST['answer']

        if question_text=="" or option_a=="" or option_b=="" or option_c=="" or option_d=="" or answer=="":
            messages.warning(request,"All Fields Are Mandetory")
            return redirect('addquestion')
        m=sql.connect(host="localhost",user="root",passwd="system",database="ads3")
        cursor=m.cursor()
        cd="INSERT INTO questions (question, optionA, optionB, optionC, optionD, answer) VALUES ('{}','{}', '{}', '{}', '{}', '{}')".format(question_text, option_a, option_b, option_c, option_d, answer)
        cursor.execute(cd)
        m.commit()
        messages.success(request,"Question Added !!")
        return redirect('addquestion')
    return render (request,'addquestion.html')

def ViewQuestionsPage(request):
    m=sql.connect(host="localhost",user="root",passwd="system",database="ads3")
    cursor=m.cursor()
    st1="select * from questions "
    cursor.execute(st1)
    questions = cursor.fetchall()
    return render (request,'viewquestions.html',{'questions': questions})

def CreateQuizPage(request):
    if request.method=='POST':
       arraystring=request.POST.get('count')
       my_list = arraystring.split(",")
       print(my_list)
       m=sql.connect(host="localhost",user="root",passwd="system",database="ads3")
       cursor=m.cursor()
       title = request.POST['quizname']
       for i in my_list:
           st="INSERT INTO quiz values ('{}','{}')".format(title,i)
           cursor.execute(st)
           m.commit()
       messages.success(request,"Quiz Created !")
       st1="select * from questions "
       cursor.execute(st1)
       questions = cursor.fetchall()
       return render (request,'createquiz.html',{'questions': questions})
    else:
      m=sql.connect(host="localhost",user="root",passwd="system",database="ads3")
      cursor=m.cursor()
      st1="select * from questions "
      cursor.execute(st1)
      questions = cursor.fetchall()
      return render (request,'createquiz.html',{'questions': questions})


def CheckResultPage(request):
    m=sql.connect(host="localhost",user="root",passwd="system",database="ads3")
    cursor=m.cursor()
    st1="SELECT * FROM marks"
    cursor.execute(st1)
    records = cursor.fetchall()
    return render (request,'checkresults.html',{'records': records})

def StudentHomePage(request):
     if request.method=="POST":
       m=sql.connect(host="localhost",user="root",passwd="system",database="ads3")
       cursor=m.cursor()
       global quiz_id
       quiz_id=request.POST.get('name')
     
       
       return redirect ('quiz') 
     else:
      
        m=sql.connect(host="localhost",user="root",passwd="system",database="ads3")
        cursor=m.cursor()
        st1="SELECT DISTINCT q.title, IFNULL(m.marks, 0) AS marks FROM quiz q LEFT JOIN marks m ON q.title = m.quiz_title AND m.student_id = '{}'".format(std_id)
        cursor.execute(st1)
        records = cursor.fetchall()
        return render (request,'studenthome.html',{'records': records})

     
def QuizPage(request):
   if request.method=="POST":
     marks=request.POST.get('score')
     title=request.POST.get('title')
     print(std_id,title,marks)
     m=sql.connect(host="localhost",user="root",passwd="system",database="ads3")
     cursor=m.cursor()
     if(marks!=0):
        st1="INSERT INTO marks values ('{}','{}','{}')".format(title,std_id,marks)
        cursor.execute(st1)
        m.commit()
     
     return redirect ('studenthome')
   else:
     m=sql.connect(host="localhost",user="root",passwd="system",database="ads3")
     cursor=m.cursor()
     st1="SELECT questions.ID, questions.question, questions.optionA, questions.optionB, questions.optionC, questions.optionD, questions.answer FROM quiz JOIN questions ON quiz.q_id = questions.ID WHERE quiz.title = '{}'".format(quiz_id)
     cursor.execute(st1)
     questions = cursor.fetchall()
     return render (request,'quiz.html',{'questions': questions,'quiz_name':quiz_id})  