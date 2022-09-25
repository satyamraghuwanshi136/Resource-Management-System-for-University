from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import permission_required
from .models import *
from . forms import PostForm
from . forms import ManForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import  Q

#pdf file download imports
from django.http import FileResponse

from django.http import HttpResponse

from django.template.loader import get_template

from xhtml2pdf import pisa

# Create your views here.


def index(request):
    return render(request,'Software/Index.html')


def manage(request):
    if request.method == 'POST':
        SName = request.POST['SName']
        LabI = request.POST['LabI']
        softwareA= Software_manage(SName=SName,LabI=LabI)
        softwareA.save()

    return render(request,'Software/Manage.html')


def delete(request):
    allproduct = Software_info.objects.all()
    if 'q' in request.GET:
        q=request.GET['q']
        allproduct = Software_info.objects.filter(Q(SName__icontains=q) | Q(PurForSub__icontains=q) | Q(Keys__icontains=q) | Q(id__icontains=q))

    return render(request,'Software/Delete.html',{'allproduct':allproduct})


def delete_man(request):
    items = Software_manage.objects.all()
    if 'q' in request.GET:
        q=request.GET['q']
        items = Software_manage.objects.filter(Q(SName__icontains=q) | Q(LabI__icontains=q))

    return render(request, 'Software/Delete_man.html', {'items': items})


def del_event(request,prod_id):
    if request.method == 'GET':
        Software_info.objects.filter(pk=prod_id).delete()
        return redirect('/software/delete')

def del_man(request,main_id):
    if request.method == 'GET':
        Software_manage.objects.filter(pk = main_id).delete()
        return redirect('/software/delete_man')


def update(request,prod_id):
    product = Software_info.objects.get(pk=prod_id)
    form = PostForm
    if request.method == 'POST':
        form = PostForm(request.POST, instance=product)
        if form.is_valid():
            Soft_id = request.POST['Soft_id']
            SName = request.POST['SName']
            Users = request.POST['Users']
            Tot_users = request.POST['Users']
            PurD = request.POST['PurD']
            ExpD = request.POST['ExpD']
            # Keys = request.POST['Keys']
            PurForSub = request.POST['PurForSub']
            ind_pri = request.POST['ind_pri']
            # date = request.POST['date']
            auth = request.POST['auth']

            if Users == 0:
                messages.error(request, ' No. of Users must be greater than 0 !!! ')
                return redirect('/software/total')

            if not SName.isalnum():
                messages.error(request, 'Software Name must be only Character !')
                return redirect('/software/total')

            if PurD >= ExpD:
                messages.error(request, 'Expire Date must be greater than Purchase date !')
                return redirect('/software/total')

            else:
              form.save()
              messages.success(request, 'Software Informations Successfully Updated  !')
              return redirect('/software/total')
    return render(request,'Software/Update.html',{'product':product})

def update_man(request,main_id):
    items = Software_manage.objects.get(pk = main_id)
    form = ManForm
    if request.method == 'POST':
        form = ManForm(request.POST, instance=items)
        if form.is_valid():
            form.save()
        return redirect('/software/delete_man')
    return render(request,'Software/Update_man.html',{'items' :items})


def add(request):
    users = User.objects.all()
    all = Software_info.objects.all()
    allproduct = len(all) + 100
    context={'users': users,'allproduct':allproduct}
    # form = PostForm
    # if request.method == 'POST':
    #     form = PostForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    # context = {'form':form}
    # return render(request, 'Software/Add.html', context)
    if request.method == 'POST':
       Soft_id = request.POST['Soft_id']
       SName = request.POST['SName']
       Users = request.POST['Users']
       Tot_users = request.POST['Users']
       PurD = request.POST['PurD']
       ExpD = request.POST['ExpD']
       # Keys = request.POST['Keys']
       PurForSub = request.POST['PurForSub']
       ind_pri = request.POST['ind_pri']
       # date = request.POST['date']
       auth = request.POST['auth']


       if Users == 0:
           messages.error(request, ' No. of Users must be greater than 0 !!! ')
           return redirect('/software/add')

       if not SName.isalnum():
           messages.error(request, 'Software Name must be only Character !')
           return redirect('/software/add')

       if PurD >= ExpD:
           messages.error(request, 'Expire Date must be greater than Purchase date !')
           return redirect('/software/add')

       else:
          software_Add = Software_info(Soft_id=Soft_id,SName=SName,Users=Users,PurD=PurD,ExpD=ExpD,PurForSub=PurForSub,ind_pri=ind_pri,auth=auth,Tot_users=Tot_users)
          software_Add.save()
          messages.success(request, 'Software Successfully Added  !')

    return render(request, 'Software/Add.html', context )

def add_man(request):
    allproduct = Software_info.objects.all()
    users = User.objects.all()
    context = {'users': users, 'allproduct': allproduct}
    forms = ManForm
    if request.method == 'POST':
        form = ManForm(request.POST)
        if form.is_valid():
            item_id = request.POST.get('Soft_id')
            quantity = request.POST.get('Users')

            item = Software_info.objects.get(pk=item_id)

            if (int(quantity) > int(item.Users)):
                messages.error(request, 'Users entered cannot be greater than Available Users !!! ')
                return redirect('/software/total')

            if (int(quantity) == 0):
                messages.error(request, ' No. of Users must be greater than 0 !!! ')
                return redirect('/software/total')

            if (int(quantity) <= int(item.Users)):
                item.Users -= int(quantity)
            else:
                item.Users = 0
                Software_info.objects.filter(id=item_id).delete()

            item.save()
            form.save()
            context = {'form': form}
            messages.success(request, 'Software Successfully Assigned  !')
            return redirect('/software/total', context)

    return render(request, 'Software/Total.html',context)


def add_mant(request,maint_id):
    allproduct = Software_info.objects.get(pk=maint_id)
    users = User.objects.all()
    context = {'users': users, 'allproduct': allproduct}
    forms = PostForm
    if request.method == 'POST':
        form = PostForm(request.POST, instance=allproduct)
        if form.is_valid():
            form.save()
            return redirect('/hardware/total')
    return render(request, 'Software/Add_man.html', context)




def total(request):
    allproduct = Software_info.objects.all()
    if request.method == "POST":
        Soft_id = request.POST.get('Soft_id', None)
        SName = request.POST.get('SName', None)

        if Soft_id:
            results = Software_info.objects.filter(Soft_id__contains=Soft_id)
            allproduct = results

        if SName:
            results = Software_info.objects.filter(SName__contains=SName)
            allproduct = results

    context = {'allproduct': allproduct}
    return render(request,'Software/Total.html',context)

def valid(request):
    allproduct = Software_info.objects.all()
    if request.method == "POST":
        Soft_id = request.POST.get('Soft_id', None)
        SName = request.POST.get('SName', None)

        if Soft_id:
            results = Software_info.objects.filter(Soft_id__contains=Soft_id)
            allproduct = results

        if SName:
            results = Software_info.objects.filter(SName__contains=SName)
            allproduct = results

    return render(request, 'Software/Valid.html', {'allproduct': allproduct})


def expire(request):
    allproduct = Software_info.objects.all()
    if request.method == "POST":
        Soft_id = request.POST.get('Soft_id', None)
        SName = request.POST.get('SName', None)

        if Soft_id:
            results = Software_info.objects.filter(Soft_id__contains=Soft_id)
            allproduct = results

        if SName:
            results = Software_info.objects.filter(SName__contains=SName)
            allproduct = results

    return render(request, 'Software/Expire.html', {'allproduct': allproduct})


def view_man(request):
    items = Software_manage.objects.all()

    if request.method == "POST":
        Soft_id = request.POST.get('Soft_id', None)
        SName = request.POST.get('SName', None)

        if Soft_id:
            results = Software_manage.objects.filter(Soft_id=Soft_id)
            items = results

        if SName:
            results = Software_manage.objects.filter(Soft_id__SName__contains=SName)
            items = results

    return render (request,'Software/View_man.html', {'items':items })



def report_info(request):
    allproduct = Software_info.objects.all()

    template_path = 'Software/Report_Info.html'

    context = {'allproduct': allproduct}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="Purchase_Softwares_report.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def report_manage(request):
    items = Software_manage.objects.all()

    template_path = 'Software/Report_Manage.html'

    context = {'items': items}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="Software_Manage_report.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def report_valid(request):
    allproduct = Software_info.objects.all()

    template_path = 'Software/Report_Valid.html'

    context = {'allproduct': allproduct}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="Valid_Softwares_report.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def report_expire(request):
    allproduct = Software_info.objects.all()

    template_path = 'Software/Report_Expire.html'

    context = {'allproduct': allproduct}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="Expire_Software_report.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response