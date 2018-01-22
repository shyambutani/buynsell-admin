from django.template.response import TemplateResponse
from django.http import HttpResponse
from .models import User_Data,Category,SubCategory,Attributes,Product_Ad,Images,Product_attribute
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
session = []
ad_list={}
def admin(request):
    if not "active_admin" in request.session:
        return login(request)
    return render(request,'admin.html')


def homepage(request):
    queryset = Category.objects.all()
    return render(request,"homepage.html",{"category_data" : queryset})


def signup(request):
    return render(request,"signup.html")


def checkEmailandPassword(request):
    email = request.POST['uemail']
    password = request.POST['upassword']
    confirmpassword = request.POST['cpassword']
    user = User_Data.objects.filter(user_email=email)
    if user.count() == 0:
        if password == confirmpassword:
            return addUser(request)
        else:
            passwordError = "Both Password should match."
            return TemplateResponse(request, "signup.html", {"Error": passwordError})
    else:
        emailError = "Email address already exists."
        return TemplateResponse(request, "signup.html", {"Error": emailError})


def onaddCategoryclick(request):
    if not "active_admin" in request.session:
        return login(request)
    cats = Category.objects.all()
    if session:
       session[:] = []
    return render(request,'onaddCategoryclick.html',{'cats':cats})


def saveCategory(request):
    if not "active_admin" in request.session:
        return login(request)
    if request.method == 'POST':
        radio = request.POST.get('optradio',None)
        if radio == 'existing':
            category = request.POST.get('cat_option',None)
            cat = Category.objects.filter(cat_name=category)
            cat_message=""
            subcategory = request.POST.get('sub_cat', None)
            subcatobj = SubCategory(subcat_name=subcategory,category_id=cat[0].cat_id)
            subcatobj.save()
            subcat_message = subcategory+" Added.."
            att_message=""
            for x in session:
                att_value = x
                attobj = Attributes(attribute_name=att_value,subcategory_id=subcatobj.subcat_id)
                attobj.save()
                att_message = att_message+" "+x+" att added"
            msg_list={cat_message,subcat_message,att_message}
            return render(request,'result.html',{'msg_list':msg_list})
        if radio == 'new':
            category = request.POST.get('new_cat',None)
            catobj = Category(cat_name=category)
            catobj.save()
            cat_message = category+" Added"
            subcategory = request.POST.get('sub_cat', None)
            subcatobj = SubCategory(subcat_name=subcategory,category_id=catobj.cat_id)
            subcatobj.save()
            subcat_message = subcategory+" Added.."
            att_message=""
            for x in session:
                att_value = x
                attobj = Attributes(attribute_name=att_value,subcategory_id=subcatobj.subcat_id)
                attobj.save()
                att_message = att_message+" "+x+" att added. "
            msg_list = {cat_message,subcat_message,att_message}
            return render(request,'result.html',{'msg_list':msg_list})


@csrf_exempt
def addtosession(request):
    att_value = request.POST['myvalue']
    if not att_value in session:
        session.append(att_value)
        request.session[att_value] = att_value
        return HttpResponse(att_value+" added..")
    else:
        return HttpResponse("Attribute already added.!")


@csrf_exempt
def deletefromsession(request):
    att_value = request.POST['myvalue']
    if att_value in session:
        session.remove(att_value)
        del request.session[att_value]
        return HttpResponse(att_value+" deleted..")
    else:
        return HttpResponse("Attribute Not found..!")


def addUser(request):
    if request.method == 'POST':
        username = request.POST['uname']
        lastname = request.POST['usurname']
        email = request.POST['uemail']
        password = request.POST['upassword']
        confirmpassword = request.POST['cpassword']
        phone_no = request.POST['uphonenumber']
        userdata = User_Data(first_name=username ,last_name=lastname,user_email=email,user_password=password,user_phone_no=phone_no)
        userdata.save()
        return TemplateResponse(request,"login.html",{})


def login(request):
    if "active_admin" in request.session:
        return admin(request)
    elif "active_user" in request.session:
        return homepage(request)
    else:
        return render(request,'login.html')


def loginValidation(request):

    email_id = request.POST['uemail']
    password = request.POST['upassword']

    user = User_Data.objects.filter(user_email=email_id)
    if user:
        correct_password = user[0].user_password
        if password == correct_password:
            if email_id == 'admin@gmail.com':
                request.session['active_admin'] = email_id
                return render(request, 'admin.html')
            else:
                request.session['active_user'] = email_id
                successMessage = "You are successfully logged in."
                return homepage(request)
        else:
            errorMessage = "Invalid credentials inserted"
            return TemplateResponse(request, "login.html", {"Success": errorMessage})
    else:
        errorMessage = "Email does not exist!"
        return TemplateResponse(request, "login.html", {"Success": errorMessage})

def logout(request):
    if "active_admin" in request.session:
        del request.session['active_admin']
    if "active_user" in request.session:
        del request.session['active_user']
    return login(request)
        

def ondeletecategoryclick(request):
    if not "active_admin" in request.session:
        return login(request)
    cat = Category.objects.all()
    sub_cat = SubCategory.objects.all()
    att = Attributes.objects.all()
    return render(request, 'deletecategory.html', {'cat' : cat, 'sub_cat' : sub_cat, 'att' : att})


@csrf_exempt
def delete_att(request):
    if not "active_admin" in request.session:
        return login(request)
    att_value = request.POST['att_value']
    subcat_value=request.POST['subcat_value']
    sub_catobj=SubCategory.objects.filter(subcat_name=subcat_value)
    sub_catobj_id=sub_catobj[0].subcat_id
    attobj = Attributes.objects.filter(attribute_name=att_value,subcategory_id=sub_catobj_id)
    attobj.delete()
    return HttpResponse(att_value+" Deleted")


@csrf_exempt
def delete_subcat(request):
    if not "active_admin" in request.session:
        return login(request)
    subcat_value = request.POST['subcat_value']
    sub_catobj=SubCategory.objects.filter(subcat_name=subcat_value)
    sub_catobj.delete()
    return HttpResponse(subcat_value+" deleted..!")


@csrf_exempt
def delete_category(request):
    if not "active_admin" in request.session:
        return login(request)
    cat_value = request.POST['cat_value']
    catobj = Category.objects.filter(cat_name=cat_value)
    catobj.delete()
    return HttpResponse(cat_value+" deleted..!")

def get_delete_ad(request):
    if not "active_admin" in request.session:
        return login(request)
    category_list = Category.objects.all()
    subcategory_list = SubCategory.objects.all()
    global ad_list
    # if request.session['selected_state']:
    #     del request.session['selected_state']
    # if not request.session['selected_city'] == {}:
    #     request.session.modified = True
    #     del request.session['selected_city']
    if request.method == 'POST':
        state = request.POST['listBox']
        city = request.POST['secondlist']
        category = request.POST['category']
        sub_category = request.POST['sub_category']
        search_text = request.POST['search_text']

        if search_text is not None:
            ad_list = Product_Ad.objects.filter(product_description__icontains=search_text)
            request.session['search_text'] = search_text
            if state == 'SELECT STATE':
                if "selected_city" in request.session:
                    del request.session['selected_city']
                if "selected_state" in request.session:
                    del request.session['selected_state']
                if category == 'Category':
                    if "selected_subcategory" in request.session:
                        del request.session['selected_subcategory']
                    if "selected_category" in request.session:
                        del request.session['selected_category']
                    ad_list = ad_list.all()
                else:
                    request.session['selected_category'] = category
                    if sub_category == 'Sub Category':
                        if "selected_subcategory" in request.session:
                            del request.session['selected_subcategory']
                        ad_list = ad_list.filter(product_category=category)
                    else:
                        request.session['selected_subcategory'] = sub_category
                        ad_list = ad_list.filter(product_category=category, product_subcategory=sub_category)
            else:
                request.session['selected_state'] = state
                if city == 'Select city':
                    if "selected_city" in request.session:
                        del request.session['selected_city']
                    if category == 'Category':
                        if "selected_category" in request.session:
                            del request.session['selected_category']
                        if "selected_subcategory" in request.session:
                            del request.session['selected_subcategory']
                        ad_list = ad_list.filter(state=state)
                    else:
                        request.session['selected_category'] = category
                        if sub_category == 'Sub Category':
                            if "selected_subcategory" in request.session:
                                del request.session['selected_subcategory']
                            ad_list = ad_list.filter(state=state, product_category=category)
                        else:
                            request.session['selected_subcategory'] = sub_category
                            ad_list = ad_list.filter(state=state, product_category=category, product_subcategory=sub_category)
                else:
                    request.session['selected_city'] = city
                    if category == 'Category':
                        if "selected_category" in request.session:
                            del request.session['selected_category']
                        if "selected_subcategory" in request.session:
                            del request.session['selected_subcategory']
                        ad_list = ad_list.filter(state=state, city=city)
                    else:
                        request.session['selected_category'] = category
                        if sub_category == 'Sub Category':
                            if "selected_subcategory" in request.session:
                                del request.session['selected_subcategory']
                            ad_list = ad_list.filter(state=state, city=city, product_category=category)
                        else:
                            request.session['selected_subcategory'] = sub_category
                            ad_list = ad_list.filter(state=state, city=city, product_category=category, product_subcategory=sub_category)
        else:
            if "search_text" in request.session:
                del request.session['search_text']
            ad_list = Product_Ad.objects.all()
            if state == 'SELECT STATE':
                if "selected_city" in request.session:
                    del request.session['selected_city']
                if "selected_state" in request.session:
                    del request.session['selected_state']
                if category == 'Category':
                    if "selected_subcategory" in request.session:
                        del request.session['selected_subcategory']
                    if "selected_category" in request.session:
                        del request.session['selected_category']
                    ad_list = ad_list.all()
                else:
                    request.session['selected_category'] = category
                    if sub_category == 'Sub Category':
                        if "selected_subcategory" in request.session:
                            del request.session['selected_subcategory']
                        ad_list = ad_list.filter(product_category=category)
                    else:
                        request.session['selected_subcategory'] = sub_category
                        ad_list = ad_list.filter(product_category=category, product_subcategory=sub_category)
            else:
                request.session['selected_state'] = state
                if city == 'Select city':
                    if "selected_city" in request.session:
                        del request.session['selected_city']
                    if category == 'Category':
                        if "selected_subcategory" in request.session:
                            del request.session['selected_subcategory']
                        if "selected_category" in request.session:
                            del request.session['selected_category']
                        ad_list = ad_list.filter(state=state)
                    else:
                        request.session['selected_category'] = category
                        if sub_category == 'Sub Category':
                            if "selected_subcategory" in request.session:
                                del request.session['selected_subcategory']
                            ad_list = ad_list.filter(state=state, product_category=category)
                        else:
                            request.session['selected_subcategory'] = sub_category
                            ad_list = ad_list.filter(state=state, product_category=category, product_subcategory=sub_category)
                else:
                    request.session['selected_city'] = city
                    if category == 'Category':
                        if "selected_subcategory" in request.session:
                            del request.session['selected_subcategory']
                        if "selected_category" in request.session:
                            del request.session['selected_category']
                        ad_list = ad_list.filter(state=state, city=city)
                    else:
                        request.session['selected_category'] = category
                        if sub_category == 'Sub Category':
                            if "selected_subcategoy" in request.session:
                                del request.session['selected_subcategory']
                            ad_list = ad_list.filter(state=state, city=city, product_category=category)
                        else:
                            request.session['selected_subcategory'] = sub_category
                            ad_list = ad_list.filter(state=state, city=city, product_category=category, product_subcategory=sub_category)
        # print(ad_list.values())

        page = request.GET.get('page', 1)
        paginator = Paginator(ad_list, 5)
        # try:
        #     paginator = Paginator(ad_list, 5)
        # except :
        #     print("hello")
        try:
            adobj = paginator.page(page)
        except PageNotAnInteger:
            adobj = paginator.page(1)
        except EmptyPage:
            adobj = paginator.page(paginator.num_pages)
        # request.session['ad_list'] = ad_list
        return render(request, 'deletead.html', {'ads': adobj, 'cat_list': category_list, 'subcat_list': subcategory_list})
    elif request.method == 'GET' and 'page' in request.GET:
        # if "ad_list" in request.session:
        #     ad_list=request.session['ad_list']
        # ad_list=Product_Ad.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(ad_list, 5)
        try:
            adobj = paginator.page(page)
        except PageNotAnInteger:
            adobj = paginator.page(1)
        except EmptyPage:
            adobj = paginator.page(paginator.num_pages)

        return render(request, 'deletead.html', {'ads': adobj, 'cat_list': category_list, 'subcat_list': subcategory_list})
    else:
        if "selected_state" in request.session:
            del request.session['selected_state']
        if "selected_city" in request.session:
            del request.session['selected_city']
        if "selected_category" in request.session:
            del request.session['selected_category']
        if "selected_subcategory" in request.session:
            del request.session['selected_subcategory']
        if "search_text" in request.session:
            del request.session['search_text']
        ad_list = Product_Ad.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(ad_list, 5)
        try:
            adobj = paginator.page(page)
        except PageNotAnInteger:
            adobj = paginator.page(1)
        except EmptyPage:
            adobj = paginator.page(paginator.num_pages)

        return render(request, 'deletead.html', {'ads': adobj, 'cat_list': category_list, 'subcat_list': subcategory_list})

@csrf_exempt
def deletead(request):
    if not "active_admin" in request.session:
        return login(request)
    ad_id = request.POST['ad_id']
    adobj = Product_Ad.objects.filter(ad_id=ad_id)
    adobj.delete()
    return HttpResponse("Ad with id= "+ad_id+" deleted")


def product_details(request):
    adid = request.GET.get('ad_id')
    ad = Product_Ad.objects.filter(ad_id=adid)
    product_images = Images.objects.filter(product_ad_id=adid)
    images = []
    for image in product_images:
        images.append(image.image_path)
    product_atts = Product_attribute.objects.filter(product_id=adid)

    return render(request, 'product_details.html', {'ad_details': ad, 'product_images': images, 'product_attributes': product_atts})


def updateadmin(request):
    if not "active_admin" in request.session:
        return login(request)
    # request.session['admin']="admin@gmail.com"
    if request.method == 'POST':
        f_name=request.POST['uname']
        l_name=request.POST['usurname']
        u_email=request.POST['uemail']
        old_pass=request.POST['oldpassword']
        new_pass=request.POST['upassword']
        re_pass=request.POST['cpassword']
        phone_no=request.POST['uphonenumber']
        old_email=request.session['active_admin']
        old_admin_data=User_Data.objects.filter(user_email=old_email)
        if not old_pass == old_admin_data[0].user_password:
            return TemplateResponse(request,"edit_admin.html",{'Error':"Old Password did not matched",'admin_data':old_admin_data})
        else:
            if not new_pass == re_pass:
                return TemplateResponse(request,"edit_admin.html",{'Error':"Password not matched",'admin_data':old_admin_data})
            else:
                old_admin_data[0].first_name=f_name
                old_admin_data[0].last_name=l_name
                old_admin_data[0].user_password=new_pass
                old_admin_data[0].user_phone_no=phone_no
                old_admin_data[0].save()
                return TemplateResponse(request,"edit_admin.html",{'Success':"Updated",'admin_data':old_admin_data})

            
    else:
        admin_email=request.session['active_admin']
        adminobj=User_Data.objects.filter(user_email=admin_email)
        return render(request, 'edit_admin.html',{'admin_data':adminobj})