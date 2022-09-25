from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from datetime import date,datetime


from .models import Iteminfo,Assignitem_info
from . forms import PostForm
from . form import AssignForm,MainForm,ReplaceForm,RemoveForm
from django.contrib.auth.models import User
from .models import *
from xhtml2pdf import pisa
from django.template.loader import get_template

# Create your views here.

def index(request):
    return render(request,'Furniture/index.html')

def specifications(request,spe_id):
    allproduct = Iteminfo.objects.filter(pk=spe_id)
    context = {'allproduct': allproduct}
    return render(request,'Furniture/Specifications.html',context)

def order_detail(request,ord_id):
    allproduct = Iteminfo.objects.filter(pk=ord_id)
    context = {'allproduct': allproduct}
    return render(request,'Furniture/Order_detail.html',context)

def purchase_detail(request,pur_id):
    allproduct = Iteminfo.objects.filter(pk=pur_id)
    context = {'allproduct': allproduct}
    return render(request,'Furniture/Purchase_detail.html',context)

def additem(request):
    if request.method == 'POST':
            item_id = request.POST['item_id']
            item_name = request.POST['item_name']
            company = request.POST['company']
            purchase_date = request.POST['purchase_date']
            qty = request.POST['qty']
            tot_qty=request.POST['qty']
            Pur_from = request.POST['Pur_from']
            order_ref = request.POST['order_ref']
            order_date = request.POST['order_date']
            in_no = request.POST['in_no']
            spec = request.POST['spec']
            warn = request.POST['warn']
            ind_pri = request.POST['ind_pri']
            tot_pri = request.POST['tot_pri']
            auth = request.POST['auth']
            photo = request.FILES['photo']


            if qty == 0 :
                messages.error(request, ' Item Quantity must be greater than 0 !!! ')
                return redirect('/furniture/additem')

            if not item_name.isalnum():
                messages.error(request, 'Item Name must be only Character !')
                return redirect('/furniture/additem')

            if not company.isalnum():
                messages.error(request, 'Company Name must be only Character !')
                return redirect('/furniture/additem')

            if purchase_date >= warn :
                messages.error(request, 'Warranty must be greater than Purchase date !')
                return redirect('/furniture/additem')

            # if (Item_info.objects.filter(item_id=form.cleaned_data['item_id']).exists()):
            #     messages.error(request, 'Items Id already exists  !')
            #     return redirect('/hardware/additem')
            else:
                hardware = Iteminfo(item_id=item_id, item_name=item_name, company=company, purchase_date=purchase_date,
                                     qty=qty, Pur_from = Pur_from, order_ref=order_ref, order_date=order_date,in_no=in_no,
                                     spec=spec, warn=warn, ind_pri=ind_pri, auth=auth, tot_pri=tot_pri, photo=photo, tot_qty=tot_qty)
                hardware.save()
                messages.success(request, 'Items Successfully Added to stock !')
                return redirect('/furniture/additem')
    users = User.objects.all()
    item=Iteminfo.objects.all()
    items = len(item) + 100
    context={'users': users,'items': items}
    return render(request, 'Furniture/additem.html',context )
    # item = Item_info.objects.all()
    # if request.method == 'POST':
    #    item_id = request.POST['item_id']
    #    item_name = request.POST['item_name']
    #    company= request.POST['company']
    #    purchase_date = request.POST['purchase_date']
    #    qty = request.POST['qty']
    #    Pur_from = request.POST['Pur_from']
    #    order_ref = request.POST['order_ref']
    #    order_date = request.POST['order_date']
    #    in_no = request.POST['in_no']
    #    spec = request.POST['spec']
    #    warn = request.POST['warn']
    #    ind_pri = request.POST['ind_pri']
    #    auth = request.POST['auth']
    #
    #    if len(item_id) < 3 :
    #       messages.error(request, 'Item Id must be more than 3 digit !')
    #       return redirect('/hardware/additem')
    #
    #    if item_id == item.item_id :
    #       messages.error(request, 'Item Id already exist !')
    #       return redirect('/hardware/additem')
    #
    #    if not item_name.isalnum():
    #       messages.error(request, 'Item name must be only Character !')
    #       return redirect('/hardware/additem')

    #    else:
    #       hardware = Item_info( item_id= item_id,item_name=item_name,company=company,purchase_date=purchase_date,qty=qty,
    #                             Pur_from= Pur_from, order_ref=order_ref,order_date=order_date,in_no=in_no,spec=spec,
    #                             warn=warn,ind_pri=ind_pri,auth=auth)
    #       hardware.save()




def totalstock(request):
    allproduct= Iteminfo.objects.all()
    if request.method == "POST":
        item_id = request.POST.get('item_id', None)
        item_name = request.POST.get('item_name', None)

        if item_id:
            results = Iteminfo.objects.filter(item_id__contains=item_id)
            allproduct = results

        if item_name:
            results = Iteminfo.objects.filter(item_name__contains=item_name)
            allproduct = results

    context = {'allproduct': allproduct}
    return render(request, 'Furniture/totalstock.html', context)


    # if request.method == 'POST':
    #     item_id = request.POST.get('item_id')
    #     item_name = request.POST.get('item_name')
    #
    #     allproduct = Item_info.objects.filter(Q(item_id__contains=item_id) & Q(item_name__contains=item_name))
    #     context = {'allproduct': allproduct}
    #     return render(request, 'hardware/totalstock.html', context)
    # else:
    #     allproduct = Item_info.objects.all()
    #
    #     context = {'allproduct': allproduct}
    #     return render(request, 'hardware/totalstock.html', context)


def update(request,prod_id):
    # if request.method == 'GET':
    #     Item_info.objects.filter(pk = prod_id).delete()
    #     return redirect('/hardware/totalstock')
    product = Iteminfo.objects.get(pk=prod_id)
    forms = PostForm
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            item_id = request.POST['item_id']
            item_name = request.POST['item_name']
            company = request.POST['company']
            purchase_date = request.POST['purchase_date']
            qty = request.POST['qty']
            tot_qty = request.POST['qty']
            Pur_from = request.POST['Pur_from']
            order_ref = request.POST['order_ref']
            order_date = request.POST['order_date']
            in_no = request.POST['in_no']
            spec = request.POST['spec']
            warn = request.POST['warn']
            ind_pri = request.POST['ind_pri']
            tot_pri = request.POST['tot_pri']
            auth = request.POST['auth']

            if qty == 0:
                messages.error(request, ' Item Quantity must be greater than 0 !!! ')
                return redirect('/furniture/totalstock')

            if not item_name.isalnum():
                messages.error(request, 'Item Name must be only Character !')
                return redirect('/furniture/totalstock')

            if not company.isalnum():
                messages.error(request, 'Company Name must be only Character !')
                return redirect('/furniture/totalstock')

            if purchase_date >= warn:
                messages.error(request, 'Warranty must be greater than Purchase date !')
                return redirect('/furniture/totalstock')
            else:
             form.save()
             messages.success(request, 'Items Informations Successfully Updated  !')
             return redirect('/furniture/totalstock')
    return render(request,'Furniture/update.html',{'product':product})


def assignItem(request):
    form = AssignForm
    if request.method == 'POST':
        form = AssignForm(request.POST)
        if form.is_valid():
            item_id = request.POST.get('item_id')
            quantity = request.POST.get('quantity')

            item = Iteminfo.objects.get(pk=item_id)

            if (int(quantity) > int(item.qty)):
                messages.error(request, 'Quantity entered cannot be greater than the stock !!! ')
                return redirect('/furniture/totalstock')

            if (int(quantity) == 0):
                messages.error(request, ' Item Quantity must be greater than 0 !!! ')
                return redirect('/furniture/totalstock')

            if (int(quantity) <= int(item.qty)):
                item.qty -= int(quantity)
            else:
                item.qty = 0
                Iteminfo.objects.filter(id=item_id).delete()

            item.save()
            form.save()
            context = {'form': form}
            messages.success(request, 'Items Successfully Assign  !')
            return redirect('/furniture/totalstock',context)

    users = User.objects.all()
    items = Iteminfo.objects.all()
    faculty = Faculty.objects.all()
    context = {'users': users, 'items': items , 'faculty': faculty}
    return render(request, 'Furniture/assign_item.html', context)

def viewAssign(request):
    items = Assignitem_info.objects.all()
    if request.method == "POST":
        item_id = request.POST.get('item_id', None)
        item_name = request.POST.get('item_name', None)
        lab_name=request.POST.get('lab_name', None)

        if item_id:
            results = Assignitem_info.objects.filter(item_id=item_id)
            items = results

        if item_name:
            results = Assignitem_info.objects.filter(item_id__item_name__contains=item_name)
            items = results

        if lab_name:
            results = Assignitem_info.objects.filter(lab_name__contains=lab_name)
            items = results

    context = {'items': items}
    return render(request, 'Furniture/view_assign.html', context)

    # items = Assign_item_info.objects.all()
    # if 'q' in request.GET:
    #     q = request.GET['q']
    #     items = Assign_item_info.objects.filter(Q(lab_name__icontains = q) | Q(faculty__icontains = q) | Q(item_id__item_id = q))
    # return render(request, 'hardware/view_assign.html', {'items': items})

    # if request.method == 'POST':
    #     company_name = request.POST.get('company_name')
    #     item_name = request.POST.get('item_name')
    #     company = request.POST.get('company')
    #     lab_name = request.POST.get('lab_name')
    #     items = Assign_item_info.objects.filter(Q(item_id__company__contains=company_name) &
    #                                 Q(item_id__item_name__contains=item_name) & Q(lab_name__contains=lab_name))
    #     context = {'items': items}
    #     return render(request, 'hardware/view_assign.html', context)
    # else:
    #     items = Assign_item_info.objects.all()
    #     prod = Item_info.objects.all()
    #     context = {'items':items ,'prod':prod}
    #     return render (request,'hardware/view_assign.html', context)


def assign_ret(request,return_id):
    items = Assignitem_info.objects.get(pk=return_id)
    forms = AssignForm
    if request.method == 'POST':
        form = AssignForm(request.POST, instance=items)
        if form.is_valid():
            form.save()
            return redirect('/furniture/viewassign')
    return render(request, 'Furniture/assign_return.html' ,{'items':items})


def replace_ret(request,ret_id):
    items = Replaceitem.objects.get(pk=ret_id)
    forms = ReplaceForm
    if request.method == 'POST':
        form = ReplaceForm(request.POST, instance=items)
        if form.is_valid():
            form.save()
            return redirect('/furniture/replace_items')
    return render(request, 'Furniture/replace_return.html' ,{'items':items})


def add_return(request):
    if request.method == 'POST':
            Item_id=request.POST.get('item_id')
            quantity = request.POST.get('quantity')
            id=request.POST.get('id')
            assign = Assignitem_info.objects.get(id=id)
            item = Iteminfo.objects.get(pk=Item_id)


            if (int(quantity) > int(assign.quantity)):
                messages.error(request, 'Quantity entered cannot be greater than the stock !!! ')
                return redirect('/furniture/viewassign')

            if (int(quantity) == 0):
                messages.error(request, ' Item Quantity must be greater than 0 !!! ')
                return redirect('/furniture/viewassign')

            if (int(quantity) <= int(assign.quantity)):
                item.qty += int(quantity)
                assign.quantity -= int(quantity)
            else:
                assign.quantity = 0
                assign.delete()

            item.save()
            assign.save()
            messages.success(request, 'Items Successfully Added to stock !')
            if (assign.quantity == 0):
                Assignitem_info.objects.filter(id=assign.id).delete()
            return redirect('/furniture/viewassign')
    return render(request, 'Furniture/view_assign.html')


def addmain(request):
    form = MainForm
    if request.method == 'POST':
        form = MainForm(request.POST)
        if form.is_valid():
            item_id = request.POST.get('item_id')
            quantity = request.POST.get('qty')

            item = Iteminfo.objects.get(pk=item_id)

            if (int(quantity) > int(item.qty)):
                messages.error(request, 'Quantity entered cannot be greater than the stock !!! ')
                return redirect('/furniture/totalstock')

            if (int(quantity) == 0):
                messages.error(request, ' Item Quantity must be greater than 0 !!! ')
                return redirect('/furniture/totalstock')

            if (int(quantity) <= int(item.qty)):
                item.qty -= int(quantity)
            else:
                item.qty = 0
                Iteminfo.objects.filter(id=item_id).delete()

            item.save()
            form.save()
            context = {'form': form}
            messages.success(request, 'Items Successfully Added to Repair  !')
            return redirect('/furniture/totalstock',context)

    users = User.objects.all()
    produt = Iteminfo.objects.all()
    context = {'users': users, 'items': produt}
    return render(request, 'hardware/totalstock.html', context)


def viewmain(request):
    items = Maintainitem.objects.all()
    for li in items:
        days = (date.today()-getattr(li, 'add_date'))
        d = getattr(days, 'days')
        if d > 15:
            id = getattr(li, 'item_id')
            messages.error(request,  'Alert !' "\t" "\t" + "( Item Id - "+str(id)+")" + "\n" 'Item given for repair more than 15 days  !!! ' )

    if request.method == "POST":
        item_id = request.POST.get('item_id', None)
        item_name = request.POST.get('item_name', None)

        if item_id:
            results = Maintainitem.objects.filter(item_id=item_id)
            items = results

        if item_name:
            results = Maintainitem.objects.filter(item_id__item_name__contains=item_name)
            items = results

    context = {'items':items }
    return render (request,'Furniture/viewmain.html', context)



def main_ret(request,ret_id):
    items = Maintainitem.objects.get(pk=ret_id)
    forms = MainForm
    if request.method == 'POST':
        form = MainForm(request.POST, instance=items)
        if form.is_valid():
            form.save()
            return redirect('/furniture/viewmain')
    return render(request, 'Furniture/main_return.html' ,{'items':items})



def return_main(request):
    if request.method == 'POST':
            Item_id=request.POST.get('item_id')
            quantity = request.POST.get('qty')
            id=request.POST.get('id')
            assign = Maintainitem.objects.get(id=id)
            item = Iteminfo.objects.get(pk=Item_id)


            if (int(quantity) > int(assign.qty)):
                messages.error(request, 'Quantity entered cannot be greater than the stock !!! ')
                return redirect('/furniture/viewmain')

            if (int(quantity) == 0):
                messages.error(request, ' Item Quantity must be greater than 0 !!! ')
                return redirect('/furniture/viewmain')

            if (int(quantity) <= int(assign.qty)):
                item.qty += int(quantity)
                assign.qty -= int(quantity)
            else:
                assign.qty = 0
                assign.delete()

            item.save()
            assign.save()
            messages.success(request, 'Items Successfully Added to stock !')
            if (assign.qty == 0):
                Maintainitem.objects.filter(id=assign.id).delete()
            return redirect('/furniture/viewmain')
    return render(request, 'Furniture/viewmain.html')


def return_replace(request):
    if request.method == 'POST':
            Item_id = request.POST.get('item_id')
            quantity = request.POST.get('qty')
            id=request.POST.get('id')
            assign = Replaceitem.objects.get(id=id)
            item = Iteminfo.objects.get(pk=Item_id)


            if (int(quantity) > int(assign.qty)):
                messages.error(request, 'Quantity entered cannot be greater than the stock !!! ')
                return redirect('/furniture/replace_items')

            if (int(quantity) == 0):
                messages.error(request, ' Item Quantity must be greater than 0 !!! ')
                return redirect('/furniture/replace_items')

            if (int(quantity) <= int(assign.qty)):
                item.qty += int(quantity)
                assign.qty -= int(quantity)
            else:
                assign.qty = 0
                assign.delete()

            item.save()
            assign.save()
            messages.success(request, 'Items Successfully Added to stock !')
            if (assign.qty == 0):
                Replaceitem.objects.filter(id=assign.id).delete()
            return redirect('/furniture/replace_items')
    return render(request, 'Furniture/replace_items.html')

def main_remove(request,rem_id):
    items = Maintainitem.objects.get(pk=rem_id)
    users = User.objects.all()
    context = {'items': items, 'users': users}
    forms = MainForm
    if request.method == 'POST':
        form = MainForm(request.POST, instance=items)
        if form.is_valid():
            form.save()
            return redirect('/furniture/viewmain')
    return render(request, 'Furniture/main_remove.html' ,context)


def main_replace(request,rep_id):
    items = Iteminfo.objects.get(pk=rep_id)
    users = User.objects.all()
    context = {'items': items, 'users': users}
    forms = PostForm
    if request.method == 'POST':
        form = PostForm(request.POST, instance=items)
        if form.is_valid():
            form.save()
            return redirect('/furniture/totalstock')
    return render(request, 'Furniture/main_replace.html' ,context)


def add_main(request,man_id):
    items = Iteminfo.objects.get(pk=man_id)
    users = User.objects.all()
    context={'items': items,'users': users}
    forms = PostForm
    if request.method == 'POST':
        form = PostForm(request.POST, instance=items)
        if form.is_valid():
            form.save()
            return redirect('/furniture/totalstock')
    return render(request, 'Furniture/maintenance.html', context)


def itemassign(request,ass_id):
    items = Iteminfo.objects.get(pk=ass_id)
    users = User.objects.all()
    faculty = Faculty.objects.all()
    context = {'users': users, 'items': items, 'faculty': faculty}
    forms = PostForm
    if request.method == 'POST':
        form = PostForm(request.POST, instance=items)
        if form.is_valid():
            form.save()
            return redirect('/furniture/totalstock')
    return render(request, 'Furniture/assign_item.html', context)


def replace_main(request):
    form = ReplaceForm
    if request.method == 'POST':
        form = ReplaceForm(request.POST)
        if form.is_valid():
            item_id = request.POST.get('item_id')
            quantity = request.POST.get('qty')

            item = Iteminfo.objects.get(pk=item_id)

            if (int(quantity) > int(item.qty)):
                messages.error(request, 'Quantity entered cannot be greater than the stock !!! ')
                return redirect('/furniture/totalstock')

            if (int(quantity) == 0):
                messages.error(request, ' Item Quantity must be greater than 0 !!! ')
                return redirect('/furniture/totalstock')

            if (int(quantity) <= int(item.qty)):
                item.qty -= int(quantity)

            else:
                item.qty = 0
                item.delete()

            item.save()
            form.save()
            context = {'form': form}
            messages.success(request, 'Items Successfully Added to Replace  !')
            return redirect('/furniture/totalstock',context)


    users = User.objects.all()
    produt = Iteminfo.objects.all()
    context = {'users': users, 'items': produt}
    return render(request, 'furniture/totalstock.html', context)



def replace_items(request):
        items = Replaceitem.objects.all()
        if request.method == "POST":
            item_id = request.POST.get('item_id', None)
            item_name = request.POST.get('item_name', None)

            if item_id:
                results = Replaceitem.objects.filter(item_id=item_id)
                items = results

            if item_name:
                results = Replaceitem.objects.filter(item_id__item_name__contains=item_name)
                items = results

        context = {'items': items}
        return render(request, 'Furniture/replace_items.html', context)


def remove_main(request):
    form = RemoveForm
    if request.method == 'POST':
        form = RemoveForm(request.POST)
        if form.is_valid():
            quantity = request.POST.get('qty')
            id=request.POST.get('id')
            assign = Maintainitem.objects.get(id=id)


            if (int(quantity) > int(assign.qty)):
                messages.error(request, 'Quantity entered cannot be greater than the stock !!! ')
                return redirect('/furniture/viewmain')

            if (int(quantity) == 0):
                messages.error(request, ' Item Quantity must be greater than 0 !!! ')
                return redirect('/furniture/viewmain')

            if (int(quantity) <= int(assign.qty)):
                assign.qty -= int(quantity)

            else:
                assign.qty = 0
                assign.delete()


            assign.save()
            form.save()
            context = {'form': form}
            messages.success(request, 'Items Successfully Added to Discard  !')
            if (assign.qty == 0):
                Maintainitem.objects.filter(id=assign.id).delete()
            return redirect('/furniture/viewmain')
    return render(request, 'Furniture/viewmain.html')


def remove_items(request):
    items = Removeitem.objects.all()
    if request.method == "POST":
        item_id = request.POST.get('item_id', None)
        item_name = request.POST.get('item_name', None)

        if item_id:
            results = Removeitem.objects.filter(item_id=item_id)
            items = results

        if item_name:
            results = Removeitem.objects.filter(item_id__item_name__contains=item_name)
            items = results

    context = {'items': items}
    return render(request, 'Furniture/remove_items.html', context)


def report_totalstock(request):
    allproduct = Iteminfo.objects.all()

    template_path = 'Furniture/report_totalstock.html'

    context = {'allproduct': allproduct}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="Furniture_Totalstock_report.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def report_assign(request):
    items= Assignitem_info.objects.all()

    template_path = 'Furniture/report_assignitems.html'

    context = {'items': items}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="Furniture_Assignitems_report.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def report_maintenance(request):
    items = Maintainitem.objects.all()

    template_path = 'Furniture/report_maintenance.html'

    context = {'items': items}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="Furniture_Maintenance_report.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def report_replace(request):
    items = Replaceitem.objects.all()

    template_path = 'Furniture/report_replaceitems.html'

    context = {'items': items}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="Furniture_Replaceitems_report.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def report_remove(request):
    items = Removeitem.objects.all()

    template_path = 'Furniture/report_removeitems.html'

    context = {'items': items}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="Furniture_Discarditems_report.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response