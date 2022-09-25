from urllib import response
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import permission_required, login_required

import Resources
from . import views, forms, models
from Resources import models as ResourcesModels
from datetime import datetime,timedelta,date

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.core.mail import send_mail



# Create your views here.
@login_required
def manage(request):
    userEmail = request.user.email
    student = ResourcesModels.Student.objects.filter(Email=userEmail)
    isAdmin = True if student.count() == 0 else False
    
    context = {
        'isAdmin': isAdmin
    }

    return render(request, 'library/manage.html', context)


@login_required
def addbook_view(request):
    #now it is empty book form for sending to html
    form=forms.BookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.BookForm(request.POST)
        if form.is_valid():
            if(models.Book.objects.filter(isbn = form.cleaned_data['isbn']).exists()):
              messages.warning(request, 'Alert! Book Already Exits.')
              return HttpResponseRedirect(request.path_info)
            else:
              user=form.save()
              # return render(request,'library/bookadded.html')
              messages.success(request, 'Success! Book Added Successfully.')
              return HttpResponseRedirect(request.path_info)

    return render(request,'library/addbook.html',{'form':form})

@login_required
def viewbooks_view(request):
    book_list =  models.Book.objects.all()
    userEmail = request.user.email

    student = ResourcesModels.Student.objects.filter(Email=userEmail)

    isAdmin = True if student.count() == 0 else False

    if request.method == "POST":
        query_name = request.POST.get('name', None)
        query_category = request.POST.get('category', None)
        query_author = request.POST.get('author', None)

        if query_name:
            results = models.Book.objects.filter(name__contains=query_name)
            book_list = results

        if query_category:
            results = models.Book.objects.filter(category__contains=query_category)
            book_list = results
        
        if query_author:
            results = models.Book.objects.filter(author__contains=query_author)
            book_list = results

    page = request.GET.get('page', 1)

    paginator = Paginator(book_list, 7)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {
      'books' : books,
      'isAdmin': isAdmin
    }

    return render(request, 'library/viewbooks.html', context)


@login_required
def editbook_view(request, pk):
  book = models.Book.objects.get(id=pk)
  form = forms.BookForm(instance=book)

  if request.method=='POST':
    #now this form have data from html
    form=forms.BookForm(request.POST, instance=book)
    if form.is_valid():
        user=form.save()
        messages.info(request, 'Success! Book Edited Successfully.')
        return HttpResponseRedirect(request.path_info)

  context = {'form': form}
  return render(request,'library/addbook.html',context)

@login_required
def deletebook_view(request, pk):
  book = models.Book.objects.get(id=pk)
  book.delete()

  book_list =  models.Book.objects.all()
  
  page = request.GET.get('page', 1)

  paginator = Paginator(book_list, 7)
  try:
      books = paginator.page(page)
  except PageNotAnInteger:
      books = paginator.page(1)
  except EmptyPage:
      books = paginator.page(paginator.num_pages)

  context = {
    'books' : books
  }

  messages.warning(request, 'Success! Book Deleted Successfully.')

  return render(request, 'library/viewbooks.html', context)


@login_required
def delete_issued_book_view(request, pk):
  book = models.IssuedBook.objects.get(id=pk)
  book.delete()
  
  # Quantity Update
  quantityUpdate = models.Book.objects.get(isbn=book.isbn)
  quantityUpdate.quantity += 1
  quantityUpdate.save()

  return issuedbook_view(request)


@login_required
def issuebook_view(request, pk):
    book = models.Book.objects.get(id=pk)
    context = {
        'book': book,
        'student' : ''
    }

    if request.method == "POST":
        query_name = request.POST.get('name', None)
        query_studentname = request.POST.get('studentname', None)
        
        if query_name:
            student=ResourcesModels.Student.objects.filter(Enrollment__contains=query_name)
            if student:
                context['student'] = student[0]
            else: 
                context['student'] = 'not found'
            
            if(student.exists()):
                request.session['studentdata'] = student[0].Enrollment
            else:
                messages.error(request, 'No Student Found. Firstly Add Student. Or Enter Correct Enrollment.')
                return HttpResponseRedirect(request.path_info)
        
        else:
            obj=models.IssuedBook()

            obj.enrollment=request.session['studentdata']
            obj.isbn=book.isbn
            # Quantity Update
            quantityUpdate = models.Book.objects.get(isbn=book.isbn)
            quantityUpdate.quantity -= 1
            quantityUpdate.save()

            obj.save()
            messages.info(request, 'Success! Book Issued Successfully.')
            return HttpResponseRedirect(request.path_info)
            # return render(request,'library/bookissued.html')

    return render(request,'library/issuebook.html', context)


@login_required
def issuedbook_view(request):
    issuedbooks=models.IssuedBook.objects.all()

    if request.method == "POST":
      query_name = request.POST.get('name', None)
      if query_name:
          results = models.IssuedBook.objects.filter(enrollment__contains=query_name)
          issuedbooks = results
    
    li=[]
    for ib in issuedbooks:
        # print(getattr(ib,'issuedate'))
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-getattr(ib,'issuedate'))
        d=getattr(days,'days')
        fine=0
        
        if d>30:
            students= ResourcesModels.Student.objects.filter(Enrollment=ib.enrollment)
            day=d-30
            fine=day*10


        books=list(models.Book.objects.filter(isbn=ib.isbn))
        students=list(ResourcesModels.Student.objects.filter(Enrollment=ib.enrollment))
        i=0
        for l in books:
            t=(students[i].First,students[i].Enrollment,books[i].name,books[i].author,issdate,expdate,fine,ib.id)
            i=i+1
            li.append(t)
      
    page = request.GET.get('page', 1)

    paginator = Paginator(li, 10)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)


    return render(request,'library/viewissuedbook.html',{'li':books})
  

@login_required
def issuedbookbystudent_view(request):
    # issuedbooks=models.IssuedBook.objects.all()
    student=ResourcesModels.Student.objects.filter(Email=request.user.email)
    # print(student[0].Enrollment)
    issuedbooks=models.IssuedBook.objects.filter(enrollment=student[0].Enrollment)

    
    li=[]
    for ib in issuedbooks:
        # print(getattr(ib,'issuedate'))
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-getattr(ib,'issuedate'))
        d=getattr(days,'days')
        fine=0

        if d>30:
            day=d-30
            fine=day*10


        books=list(models.Book.objects.filter(isbn=ib.isbn))
        students=list(ResourcesModels.Student.objects.filter(Enrollment=ib.enrollment))
        i=0
        for l in books:
            t=(students[i].First,students[i].Enrollment,books[i].name,books[i].author,issdate,expdate,fine)
            i=i+1
            li.append(t)
      
    page = request.GET.get('page', 1)

    paginator = Paginator(li, 10)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)


    return render(request,'library/viewissuedbookbystudent.html',{'li':books})
  
@login_required
def generatereports_view(request):
    return render(request,'library/reporthome.html',{})

@login_required
def render_all_books_report_view(request):
    template_path = 'library/all_books_report.html'
    book_list =  models.Book.objects.all()
    
    avl_book_list = []
    ntavl_book_list = []
    for book in book_list:
        if book.quantity != 0:
            avl_book_list.append(book)
    
    for book in book_list:
        if book.quantity == 0:
            ntavl_book_list.append(book)

    issuedbooks=models.IssuedBook.objects.all()
    li=[]
    for ib in issuedbooks:
        # print(getattr(ib,'issuedate'))
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-getattr(ib,'issuedate'))
        d=getattr(days,'days')
        fine=0
        if d>30:
            day=d-30
            fine=day*10


        books=list(models.Book.objects.filter(isbn=ib.isbn))
        students=list(ResourcesModels.Student.objects.filter(Enrollment=ib.enrollment))
        i=0
        for l in books:
            t=(students[i].First +' '+ students[i].Last, " / ".join([str(students[i].Course_id),str(students[i].Semester_id)]),students[i].Enrollment,books[i].name,books[i].author,issdate,expdate,fine,ib.id)
            i=i+1
            li.append(t)

    avlbooksquantity = 0

    for book in avl_book_list:
        avlbooksquantity += book.quantity

    totalbooks = avlbooksquantity + li.__len__()

    context = {
        'avlbooks': avl_book_list,
        'ntavlbooks': ntavl_book_list,
        'issuedbooks': li,
        'totalbooks': totalbooks,
        'avlbooksquantity': avlbooksquantity,
        'ntavlbooksquantity': ntavl_book_list.__len__(),
        'issuedbooksquantity': li.__len__(),
    }
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def render_all_available_books_report_view(request):
    template_path = 'library/all_available_books_report.html'
    book_list =  models.Book.objects.all()
    updated_book_list = []
    for book in book_list:
        if book.quantity != 0:
            updated_book_list.append(book)

    context = {'books': updated_book_list,'sno': 0}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def render_all_issued_books_report_view(request):
    template_path = 'library/all_issued_books_report.html'
    issuedbooks=models.IssuedBook.objects.all()

    
    li=[]
    for ib in issuedbooks:
        # print(getattr(ib,'issuedate'))
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-getattr(ib,'issuedate'))
        d=getattr(days,'days')
        fine=0
        if d>30:
            day=d-30
            fine=day*10


        books=list(models.Book.objects.filter(isbn=ib.isbn))
        students=list(ResourcesModels.Student.objects.filter(Enrollment=ib.enrollment))
        i=0
        for l in books:
            t=(students[i].First +' '+ students[i].Last, " / ".join([str(students[i].Course_id),str(students[i].Semester_id)]),students[i].Enrollment,books[i].name,books[i].author,issdate,expdate,fine,ib.id)
            i=i+1
            li.append(t)

    context = {'books': li}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def render_all_not_available_books_report_view(request):
    template_path = 'library/all_not_available_books_report.html'
    book_list =  models.Book.objects.all()
    updated_book_list = []
    for book in book_list:
        if book.quantity == 0:
            updated_book_list.append(book)

    context = {'books': updated_book_list,}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def generate_report_view(request):
       if request.method == "POST":
        query_name = request.POST.get('report-dropdown', None)
        
        if(query_name == "GenerateAllBooksReport"):
            return redirect('/library/generate-all-books-report')
        
        if(query_name == "GenerateAvailableAllBooksReport"):
            return redirect('/library/generate-all-available-books-report')
        
        if(query_name == "GenerateAllNotAvailableBooksReport"):
            return redirect('/library/generate-all-not-available-books-report')
        
        if(query_name == "GenerateAllIssuedBooksReport"):
            return redirect('/library/generate-all-issued-books-report')
        
