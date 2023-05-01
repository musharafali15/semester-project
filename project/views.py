from logging import CRITICAL

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils._os import safe_join
from django.views.generic import DetailView
from django.db.models import Avg, Max, Min, Sum

from project import views
from .forms import UserRegisterForm
from django.utils.crypto import get_random_string
import random
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import Type, seller, Product, Rating, buyer, Report, comment, Bidding, Bidwons, contact

from fpdf import FPDF, HTMLMixin
import os
from fypproject.settings import BASE_DIR, STATICFILES_DIRS, MEDIA_ROOT


# Create your views here.
def innnn(request):
    return HttpResponse("<h1>Hello To View</h1>")
def validate_seller(request):
    cnic = request.POST.get('cnic', None)
    data = {
        'is_taken': seller.objects.filter(CNIC__iexact=cnic).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this CNIC already exists.'
    return JsonResponse(data)

#Homepage
def index(request):
    #Query select * from Table
    prod = Product.objects.all()
    #prod = Product.objects.filter(prod_status='NS').order_by('prod_price')
    #Query end

    prod1 = Product.objects.filter(prod_status='S', auction_status='NF').order_by('prod_price')

    uniquee = Product.objects.order_by('prod_category').values('prod_category').distinct()
    uniq = []
    for i in uniquee:
        uniq.append(i.get('prod_category'))

    param = {'prod': prod,
             'prod1': prod1,
             'range': 4,
             'unique':uniq}
    return render(request, 'index.html', param)


def prod_list(request):
    prod = Product.objects.all()
    recent = Product.objects.latest()
    earliest = Product.objects.earliest()
    print(recent.user)
    print(earliest.user)

    return render(request, 'product-list.html', {'prod': prod, 'recent': recent, 'earliest': earliest})
def cat(request,item):
    prod = Product.objects.filter(prod_category=item)
    prod1 = Product.objects.filter(prod_status='S', auction_status='NF').order_by('prod_price')
    searchh=Product.objects.filter(prod_category=item)
    uniquee = Product.objects.order_by('prod_category').values('prod_category').distinct()
    uniq = []
    category=item
    for i in uniquee:
        uniq.append(i.get('prod_category'))
    param = {'prod1': prod1,'prod': prod,
             'unique':uniq,'range': 4,
             'category':category}

    return render(request,'web/category_search.html',param)
@login_required
def contact_admin(request):
    contactt=contact.objects.all().order_by()
    param={

        'contact':contactt
    }
    return render(request,'admin/contact_admin.html',param)
@login_required
def goprofile(request):
    user = request.user

    if user.is_superuser:
        slr=seller.objects.all()
        byr=buyer.objects.all()

        param={
            'user':user,
            'buyer':byr,
            'seller':slr
        }
        return redirect('/admin/')
    param = {user: user}
    obj = Type.objects.get(user_id=user.id)
    if (obj.con == False):
        return render(request, 'emailconfirm.html')
    elif (obj.confirmm == False):
        if (obj.type == 'S'):
            param = {'param': user.email}
            return render(request, 'Seller/profile.html', param)
        elif (obj.type == 'G'):
            param = {'param': user.email}
            return render(request, 'Buyer/profile.html', param)
        else:
            param = {'param': user.email}
            return render(request, 'Buyer/profile.html', param)
    # elif(obj.pconfirm==False):

    #  return render(request, 'adminconfirm.html')
    else:
        if (obj.type == 'S'):
            if (obj.pconfirm == False):
                obj = seller.objects.filter(user_id=user.id)
                obj.update(pconfirm="True")
            obj = seller.objects.filter(user_id=user.id)
            totalcount = Product.objects.filter(user_id=user.id, prod_status='S')
            tcount = totalcount.count()
            Successfulcount = Product.objects.filter(user_id=user.id, prod_status='S', auction_status='F')
            scount = Successfulcount.count()
            Oncount = Product.objects.filter(user_id=user.id, prod_status='S', auction_status='NF')
            oncount = Oncount.count()
            pendingcount = Product.objects.filter(user_id=user.id, prod_status='NS')
            pcount = pendingcount.count()
            avgrating = 0.0
            rattingg = Rating.objects.filter(user_id=user.id)
            for item in rattingg:
                avgrating = item.rating
            bid_slug=[]
            bidwonn=Bidwons.objects.filter(user_id=user.id)
            for i in bidwonn:
                print(i.fname)
            prod=Product.objects.filter(user_id=user.id)

            '''for i in totalcount:
                bid_slug.append(Bidwons.objects.filter(seller_id=user.id))
            for i in bid_slug:
                for j in i:
                    print(j.seller_id)'''

            param = {'param': obj,
                     'tcount': tcount,
                     'scount': scount,
                     'oncount': oncount,
                     'pcount': pcount,
                     'avgrating': avgrating,
                     'totalcount':prod,
                     }
            return render(request, 'Seller/influencer-profile.html', param)
        elif (obj.type == 'G'):
            obj = buyer.objects.filter(user_id=user.id)
            obj1 = Type.objects.filter(user_id=user.id)
            param = {'param': obj,
                     'type': obj1}
            return render(request, 'Buyer/influencer-profile.html', param)
        else:
            if (obj.pconfirm == False):
                obj = buyer.objects.filter(user_id=user.id)
                obj.update(pconfirm="True")
            obj = buyer.objects.filter(user_id=user.id)
            obj1 = Type.objects.filter(user_id=user.id)
            param = {'param': obj,
                     'type': obj1}
            return render(request, 'Buyer/influencer-profile.html', param)
    # return render(request,'profile.html')


def register(request):
    user = request.user
    obj = Type.objects.get(user_id=user.id)
    confirmcode = request.POST.get('con')
    # print(confirmcode)
    if (str(obj.emcon) == confirmcode):

        obj1 = Type.objects.filter(user_id=user.id)
        obj1.update(con="True")
        return redirect('/goprofile/')
    else:
        param = {'error': "Enter Correct Code"}
        return render(request, 'emailconfirm.html', param)


def about(request):
    return render(request, 'about.html')

#Backend
def contactt(request):

    return render(request, 'web/contact.html')#front end link


def contact_sent(request):
    id = None
    param = ""
    name = None
    email = None
    subjectt = None
    message = None
    img = None
    idd = None
    if request.method == 'POST':
        name = request.POST.get('nam')
        email = request.POST.get('email')
        subjectt = request.POST.get('subject')
        messag = request.POST.get('message')
        img = request.FILES.get('filee')
        #insertion
        obj = contact.objects.create(c_name=name, c_email=email, subject=subjectt, message=messag, file=img)
        obj.save()
        idd = obj.c_id
        send_mail(
            'Contact Message !!! ' + str(subjectt),  # subject portion
            'Hi Admin!\n Someone Trying to reach You  Mr.| Mrs.' + str(name) + 'having Responce ID' + str(
                obj.c_id) + 'and Email' + str(email),  # message portion
            'bidbeaverss@gmail.com',  # email from
            ['team.bidbeaverss@gmail.com'],  # email to
            fail_silently=False, )
    param = {
        'idd': idd,
    }
    return render(request, 'web/contact_sent.html', param)



def after(request):
    return render(request, 'after-login-index.html')


def single(request):
    return render(request, 'single.html')


def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        rad = request.POST.get('rad')
        print(rad)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            # print(username, email, password)
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
            obj = get_random_string(length=6, allowed_chars='1234567890')
            mymodel = Type.objects.create(user_id=user.id, type=rad, emcon=str(obj), con=True, confirmm=False,
                                          pconfirm=True)
            mymodel.save()
            # send_mail(
            #     'Your Account Confirmation Code ',  # subject portion
            #     'Your Account Confirmation Code is ' + str(obj),  # message portion
            #     'bidbeaverss@gmail.com',  # email from
            #     [user.email],  # email to
            #     fail_silently=False, )
            messages.success(request, f'Account created for {username}')
            return redirect('/accounts/login/')
    else:
        form = UserRegisterForm()

    return render(request, 'signup.html', {'form': form})


def Gsignup(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('pas')
        chec = User.objects.filter(username=username)
        if (chec.count() == 1):
            messages.error(request, f'{username} that Username already Exists Choose a new one..!')
            return render(request, 'Gsignup.html')
        else:
            user = User.objects.create(username=username, email="@gmail.com")
            user.set_password(password)
            user.save()
            obj = get_random_string(length=6, allowed_chars='1234567890')
            mymodel = Type.objects.create(user_id=user.id, type='G', emcon=str(obj), con=True, confirmm=False,
                                          pconfirm=True)
            mymodel.save()
            messages.success(request, f'Account created for {username}. Kindly login..!')
            return redirect('/accounts/login/')

    return render(request, 'Gsignup.html')


def seller_dashboard(request):
    return render(request, 'Seller/index.html')


@login_required
def product_up(request):
    user = request.user
    if request.method == 'POST':
        img = request.FILES.get('img')
        pname = request.POST.get('pname')
        price = request.POST.get('price')
        minbid = request.POST.get('minbid')
        tframe = request.POST.get('tframe')
        desc = request.POST.get('desc')
        loc = request.POST.get('loc')
        bstart = request.POST.get('bstart')
        bend = request.POST.get('bend')
        obj = Product.objects.create(user_id=user.id, image=img, prod_title=pname, prod_description=desc,
                                     prod_price=price, prod_loc=loc, minbid=minbid, tframe=tframe, starttime=bstart,
                                     endtime=bend)

        obj.save()
        obj1 = Product.objects.filter(user_id=user.id, image=img, prod_title=pname, prod_description=desc,
                                      prod_price=price, prod_loc=loc, minbid=minbid, tframe=tframe, starttime=bstart,
                                      endtime=bend)
        obj2=Product.objects.get(id=obj.id)

        #obj1.update(slug=obj.id)
        #obj2.update(slug=obj.id)
        obj2.slug=obj.id
        obj2.save()
        messages.success(request, "Product added Successfully..!")
        return redirect('/pages/form-validation/')

    return render(request, "Seller/pages/form-validation.html")


# for seller sale product detail
def product_sell(request):
    return render(request, "Seller/pages/data-tables.html")


def buyer_dashboard(request):
    return render(request, 'Buyer/index.html')


def product_buy(request):
    return render(request, 'Buyer/pages/data-tables.html')


'''
def seller(request):
    return render(request,'Seller/influencer-profile.html')'''


@login_required
def profile(request):
    user = request.user
    obj1 = Type.objects.get(user_id=user.id)
    if (obj1.confirmm == False):
        if request.method == 'POST':
            image = request.FILES.get('img')
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            cnic = request.POST.get('cnic')
            contact = request.POST.get('contact')
            city = request.POST.get('city')
            address = request.POST.get('address')
            postalcode = request.POST.get('postalcode')
            desc = request.POST.get('desc')
            obj = seller.objects.create(user=obj1.user, image=image, Fname=fname, Lname=lname, CNIC=cnic,
                                        phone_no=contact, city=city, address=address, postal_code=postalcode,
                                        description=desc)
            obj.save()
            obj2 = Type.objects.filter(user_id=user.id)
            obj2.update(confirmm="True")
            ratobj = Rating.objects.create(user_id=user.id, rating=5.0)
            ratobj.save()
            msg = "A new User has submiited personal information kindly Review it and confirm it " + "\n" + "By going to" + "\n" + "Admin Login=>Types=>Click on the required User=>Tick the pconfirm Button" + "\n" + "User details are as follows" + "\n" + "Username : " + str(
                user.username) + "\n" + "FName : " + str(fname) + "\n" + "LName : " + str(
                lname) + "\n" + "CNIC : " + str(cnic) + "\n" + "City : " + str(city) + "\n" + "Address : " + str(
                address)
            send_mail(
                'New User Registration',  # subject portion
                msg,
                'bidbeaverss@gmail.com',  # email from
                ['team.bidbeaverss@gmail.com'],  # email to
                fail_silently=False, )
            return redirect('/goprofile/')


@login_required
def Bprofile(request):
    user = request.user
    obj1 = Type.objects.get(user_id=user.id)
    if (obj1.confirmm == False):
        if request.method == 'POST':
            image = request.FILES.get('img')
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            cnic = request.POST.get('cnic')
            contact = request.POST.get('contact')
            city = request.POST.get('city')
            address = request.POST.get('address')
            postalcode = request.POST.get('postalcode')
            obj = buyer.objects.create(user=obj1.user, image=image, Fname=fname, Lname=lname, CNIC=cnic,
                                       phone_no=contact, city=city, address=address, postal_code=postalcode)
            obj.save()
            obj2 = Type.objects.filter(user_id=user.id)
            obj2.update(confirmm="True")

            ''' msg="A new User has submiited personal information kindly Review it and confirm it "+"\n"+"By going to"+"\n"+"Admin Login=>Types=>Click on the required User=>Tick the pconfirm Button"+"\n"+"User details are as follows"+"\n"+"Username : "+str(user.username)+"\n"+"FName : "+str(fname)+"\n"+"LName : "+str(lname)+"\n"+"CNIC : "+str(cnic)+"\n"+"City : "+str(city)+"\n"+"Address : "+str(address)
            send_mail(
                'New User Registration',  # subject portion
                msg,
                'bidbeaverss@gmail.com',  # email from
                ['team.bidbeaverss@gmail.com'],  # email to
                fail_silently=False, )'''
            return redirect('/goprofile/')


def profile_buyer(request):
    return render(request, 'Buyer/profile.html')


@login_required
def ChangePass(request):
    if request.method == 'POST':
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if (pass1 == pass2):
            user = request.user
            u = User.objects.get(username=user.username)
            u.set_password(pass1)
            u.save()
            messages.success(request, f'Password changed for {user.username} ...')
            return redirect('/changepass/')
        else:
            messages.success(request, f'Password1 and Password2 didnot matched..')
            return redirect('/changepass/')

        print(pass1, pass2)
    return render(request, "Seller/pages/change-password.html")


@login_required
def PendingAuctions(request):
    user = request.user
    if request.method == 'POST':
        print("ongoing")
    try:
        obj = Product.objects.filter(user_id=user.id, prod_status='NS')
        param = {'param': obj}
        for item in obj:
            print(item.image)
        return render(request, 'Seller/pages/PendingAuctions.html', param)
    except:
        print("error")
        messages.error(request, 'Sorry No Pending Product found..!')
        return render(request, 'Seller/pages/PendingAuctions.html')


@login_required
def ongoingAuctions(request):
    user = request.user
    try:
        obj = Product.objects.filter(user_id=user.id, prod_status='S', auction_status='NF')
        param = {'param': obj}
        return render(request, 'Seller/pages/OnGoingAuction.html', param)
    except:
        print("error")
        messages.error(request, 'Sorry No OnGoing Auctions found..!')
        return render(request, 'Seller/pages/OnGoingAuction.html')


@login_required
def BongoingAuctions(request):
    try:
        obj = Product.objects.filter(prod_status='S', auction_status='NF')
        param = {'param': obj}
        return render(request, 'Buyer/pages/OnGoingAuction.html', param)
    except:
        print("error")
        messages.error(request, 'Sorry No OnGoing found..!')
        return render(request, 'Buyer/pages/OnGoingAuction.html')


@login_required
def BPendingAuctions(request):
    try:
        obj = Product.objects.filter(prod_status='NS', auction_status='NF')
        param = {'param': obj}
        return render(request, 'Buyer/pages/PendingAuctions.html', param)
    except:
        print("error")
        messages.error(request, 'Sorry No starting Soon Auctions found..!')
        return render(request, 'Buyer/pages/PendingAuctions.html')


def startAuction(request, slug):
    user = request.user
    obj = Product.objects.filter(user_id=user.id, slug=slug)
    obj.update(prod_status='S')
    messages.success(request, 'Auction Has been started..!')
    return redirect('/pendingAuctions/')


def stopAuction(request, slug):
    user = request.user
    lbids = 0
    ltbids = 0
    sbids = 0
    stbids = 0
    maxbid = 0.0
    bw_id = 0
    sellerName = ''
    sellerPhone = ''
    sellerEmail = ''
    prodName = ''
    prodDescription = ''
    p_image = ''
    p_loc = ''
    auction_status = ''
    buyerEmail = ''
    obj = Product.objects.filter(user_id=user.id, slug=slug)
    for item in obj:
        prodName = item.prod_title
        prodDescription = item.prod_description
        p_image = item.image
        p_loc = item.prod_loc
        auction_status = item.auction_status
    sellerobj = seller.objects.filter(user_id=user.id)
    for item in sellerobj:
        sellerName = item.Fname + " " + item.Lname
        sellerPhone = item.phone_no
        sellerEmail = item.user.email
    obj.update(auction_status='F')
    bobj = Bidding.objects.filter(forproduct=slug)
    if (bobj.count != 0):
        for item in bobj:
            if maxbid <= item.bamount:
                maxbid = item.bamount
            buobj = buyer.objects.filter(user_id=item.user_id)
            for item in buobj:
                lbids = item.lbids
            ltbids = lbids + 1
            buobj.update(lbids=ltbids)
            print("bobj count ", item.user.username)
        wobj = Bidding.objects.filter(forproduct=slug, bamount=maxbid)
        for item in wobj:
            bw_id = item.user_id
        winner = buyer.objects.filter(user_id=bw_id)
        for item in winner:
            sbids = item.sbids
        winner.update(sbids=sbids + 1, lbids=ltbids - 1)
        buyerobj = User.objects.filter(id=bw_id)
        for item in buyerobj:
            buyerEmail = item.email
    print(buyerEmail)
    bidwon = Bidwons.objects.create(user_id=bw_id, pimage=p_image, p_title=prodName, p_disc=prodDescription,
                                    p_loc=p_loc, auction_status=auction_status, seller_id=user.id, slug=slug)
    bidwon.save()
    msg = "Product Details are as Follows : " + "\n" + "Product Name : " + str(
        prodName) + "\n" + "Product Description : " + str(
        prodDescription) + "\n" + "Seller Details : " + "\n" + "Seller Name : " + str(
        sellerName) + "\n" + "Seller Phone Number : " + str(sellerPhone) + "\n" + "Seller Email : " + str(sellerEmail)
    '''send_mail(
        'Congrations You have Won the Bid,Kindly contact the seller',  # subject portion
        msg,
        'bidbeaverss@gmail.com',  # email from
        [buyerEmail],  # email to
        fail_silently=False, )'''

    messages.success(request, 'Auction Has been finished ...!')
    return redirect('/finishedAuctions/' + str(slug) + '/')


def removeproduct(request, slug):
    user = request.user
    obj = Product.objects.filter(user_id=user.id, slug=slug)
    obj.delete()
    messages.success(request, 'Product Deleted Successfully..!')
    return redirect('/pendingAuctions/')


def ArticleDetailView(request, slug):
    user = request.user
    object = Product.objects.filter(user_id=user.id, slug=slug)
    param = {'param': object}
    return render(request, 'Seller/pages/productdetail.html', param)


def editProduct(request, slug):
    user = request.user
    slug1 = slug
    obj = Product.objects.filter(user_id=user.id, slug=slug)
    param = {'param': obj}
    return render(request, 'Seller/pages/editproduct.html', param)


def auctionDetails(request, slug):
    user = request.user
    maxbidamount = 0.0
    maxbid = Bidding.objects.filter(forproduct=slug)
    for item in maxbid:
        if item.bamount > maxbidamount:
            maxbidamount = item.bamount

    obj = Product.objects.filter(user_id=user.id, slug=slug)
    comments = comment.objects.filter(forproduct=slug).order_by("created_date").reverse()

    param = {'param': obj,
             'comment': comments,
             'maxbid': maxbidamount,
             }
    return render(request, 'Seller/pages/AuctionDetail.html', param)


@login_required
def bidDetails(request, slug):
    user = request.user
    obj = Product.objects.filter(slug=slug)
    userid = ''
    tsale = 0
    avgrating = 0.0
    maxbidamount = 0.0

    comments = comment.objects.filter(forproduct=slug).order_by("created_date").reverse()
    bobj = Bidding.objects.filter(user_id=user.id, forproduct=slug)
    maxbid = Bidding.objects.filter(forproduct=slug)
    for item in maxbid:
        if item.bamount > maxbidamount:
            maxbidamount = item.bamount

    for item in obj:
        userid = item.user_id

    uobj = seller.objects.filter(user_id=userid)
    uprod = Product.objects.filter(user_id=userid)
    for total in uprod:
        if (total.auction_status == 'F'):
            tsale = tsale + 1
    ratobj = Rating.objects.filter(user_id=userid)
    for rat in ratobj:
        avgrating = rat.rating
    param = {'param': obj,
             'user': uobj,
             'tsale': tsale,
             'avgrating': avgrating,
             'comment': comments,
             'bid': bobj,
             'maxbid': maxbidamount,
             'email': user.email
             }
    return render(request, 'Buyer/pages/bidDetail.html', param)


@login_required
def ssfuldetail(request, slug):
    user = request.user
    obj = Product.objects.filter(slug=slug)
    userid = ''
    tsale = 0
    avgrating = 0.0

    for item in obj:
        userid = item.user_id

    uobj = seller.objects.filter(user_id=userid)
    uprod = Product.objects.filter(user_id=userid)
    for total in uprod:
        if (total.auction_status == 'F'):
            tsale = tsale + 1
    ratobj = Rating.objects.filter(user_id=userid)
    for rat in ratobj:
        avgrating = rat.rating

    param = {'param': obj,
             'user': uobj,
             'tsale': tsale,
             'avgrating': avgrating,

             }
    return render(request, 'Buyer/pages/ssfuldetail.html', param)


def editP(request):
    user = request.user
    if request.method == 'POST':
        img = request.FILES.get('img')
        pname = request.POST.get('pname')
        price = request.POST.get('price')
        minbid = request.POST.get('minbid')
        tframe = request.POST.get('tframe')
        desc = request.POST.get('desc')
        loc = request.POST.get('loc')
        slug = request.POST.get('slug')
        bstart = request.POST.get('bstart')
        bend = request.POST.get('bend')
        print(slug, img)
        obj1 = Product.objects.filter(user_id=user.id, slug=slug)
        obj1.delete()
        object = Product.objects.create(user_id=user.id, image=img, prod_title=pname, prod_description=desc,
                                        prod_price=price, prod_loc=loc, minbid=minbid, tframe=tframe, starttime=bstart,
                                        endtime=bend, slug=slug)
        object.save()
        obj = Product.objects.filter(user_id=user.id, slug=slug)
        param = {'param': obj}
        return render(request, 'Seller/pages/editproduct.html', param)


def giverating(request):
    userid = request.POST.get('userid')
    prod_id = request.POST.get('prod_id')
    rat = request.POST.get('rat')
    rat1 = float(rat)
    avgrat = 0.0
    currentrat = 0.0
    objrat = Rating.objects.filter(user_id=userid)
    for item in objrat:
        currentrat = item.rating
    avgrat = (currentrat + rat1) / 2.0
    objrat.update(rating=avgrat)
    messages.success(request, 'Rating has been submitted successfully..!')
    return redirect('/bidDetails/' + prod_id + '/')


def reportseller(request):
    bname = request.user.username
    print(bname)
    userid = request.POST.get('userid')
    sub = request.POST.get('sub')
    desc = request.POST.get('desc')
    prod_id = request.POST.get('prod_id')
    print(sub, desc)
    obj = Report.objects.create(user_id=userid, subject=sub, description=desc)
    obj.save()
    msg = "A new Seller has been reported by " + str(
        bname) + "\n" + "Report detail are as below " + "\n" + "Subject : " + str(sub) + "\n" + "Description : " + str(
        desc)
    send_mail(
        'Seller Report',  # subject portion
        msg,
        'bidbeaverss@gmail.com',  # email from
        ['team.bidbeaverss@gmail.com'],  # email to
        fail_silently=False, )
    messages.success(request, 'Report has been submitted successfully..!')
    return redirect('/bidDetails/' + prod_id + '/')


def reportbuyer(request):
    sname = request.user.username
    userid = request.POST.get('userid')
    print(request.POST.get('usr'))
    print(userid)
    sub = request.POST.get('sub')
    desc = request.POST.get('desc')
    prod_id = request.POST.get('prod_id')
    print(sub, desc)
    obj = Report.objects.create(user_id=userid, subject=sub, description=desc)
    obj.save()
    msg = "A new Buyer has been reported by " + str(
        sname) + "\n" + "Report detail are as below " + "\n" + "Subject : " + str(sub) + "\n" + "Description : " + str(
        desc)
    send_mail(
        'Seller Report',  # subject portion
        msg,
        'bidbeaverss@gmail.com',  # email from
        ['team.bidbeaverss@gmail.com'],  # email to
        fail_silently=False, )
    messages.success(request, 'Report has been submitted successfully..!')
    return redirect('/finishedAuctions/' + prod_id + '/')


def commentt(request):
    user = request.user
    comm = request.POST.get('comment')
    prod_id = request.POST.get('prod_id')
    bobj = buyer.objects.filter(user_id=user.id)
    image = ""
    fname = ""
    lname = ""
    for item in bobj:
        image = item.image
        fname = item.Fname
        lname = item.Lname
    obj = comment.objects.create(user_id=user.id, image=image, fname=fname, lname=lname, forproduct=prod_id,
                                 message=comm)
    obj.save()
    obj1 = comment.objects.filter(user_id=user.id, image=image, fname=fname, lname=lname, forproduct=prod_id,
                                  message=comm)
    obj1.update(slug=obj.id)

    messages.success(request, 'Comment has been submitted successfully..!')
    return redirect('/bidDetails/' + prod_id + '/')


def removecomment(request, slug):
    print("haha", slug)
    url = ''
    obj = comment.objects.filter(slug=slug)
    for item in obj:
        url = item.forproduct
    obj.delete()
    messages.success(request, 'Comment deleted Successfully..!')
    return redirect('/auctionDetails/' + str(url) + '/')


def bid(request):
    user = request.user
    forprod = request.POST.get('prod_id')
    bidd = request.POST.get('bid')
    image = ""
    fname = ""
    lname = ""
    nofbidder = 0
    totalbids = 0
    obj = Bidding.objects.filter(user_id=user.id, forproduct=forprod)
    if (obj.count() == 0):
        uobj = buyer.objects.filter(user_id=user.id)
        for item in uobj:
            image = item.image
            fname = item.Fname
            lname = item.Lname
            totalbids = item.tbids
        tbids = totalbids + 1
        obj = Bidding.objects.create(user_id=user.id, image=image, fname=fname, lname=lname, bamount=bidd,
                                     forproduct=forprod)
        obj.save()
        uobj.update(tbids=tbids)
        pobj = Product.objects.filter(slug=forprod)
        if (pobj.count != 0):
            for item in pobj:
                nofbidder = item.nofbidder
            pobj.update(nofbidder=nofbidder + 1)
            messages.success(request, 'Successfully Bid..!')
        return redirect('/bidDetails/' + str(forprod) + '/')
    else:
        obj.update(bamount=bidd)
        messages.success(request, 'Successfully Bid..!')
        return redirect('/bidDetails/' + str(forprod) + '/')


def finishAuctions(request):
    user = request.user
    pobj = Product.objects.filter(user_id=user.id, prod_status='S', auction_status='F')
    param = {'param': pobj}
    return render(request, 'Seller/pages/FinishedAuction.html', param)


def finishedAuctions(request, slug):
    user = request.user
    maxbid = 0
    bwinner_id = 0
    pobj = Product.objects.filter(user_id=user.id, slug=slug)
    Bobj = Bidding.objects.filter(forproduct=slug)
    for item in Bobj:
        if item.bamount >= maxbid:
            maxbid = item.bamount
    Bobj1 = Bidding.objects.filter(bamount=maxbid)
    for item in Bobj1:
        bwinner_id = item.user_id
    bobj = buyer.objects.filter(user_id=bwinner_id)
    cmnt = comment.objects.filter(forproduct=slug)
    param = {'param': pobj,
             'user': bobj,
             'comment': cmnt,
             'bamount': maxbid,
             }
    return render(request, 'Seller/pages/Result.html', param)


def bidwons(request):
    user = request.user
    prod_id = ''
    bidwons = Bidwons.objects.filter(user_id=user.id)
    print(bidwons.count())
    if (bidwons.count != 0):
        param = {'param': bidwons,
                 }

    return render(request, 'Buyer/pages/Bidwons.html', param)


def bidwinDetails(request, slug):
    user = request.user
    seller_id = 0
    prod_id = 0
    avgrating = 0.0
    maxbidamount = 0.0
    bidwons = Bidwons.objects.filter(user_id=user.id, slug=slug)
    if (bidwons.count != 0):
        for item in bidwons:
            seller_id = item.seller_id
        print(seller_id)
        sobj = seller.objects.filter(user_id=seller_id)
        totalcount = Product.objects.filter(user_id=seller_id, prod_status='S', auction_status='F')
        rattingg = Rating.objects.filter(user_id=seller_id)
        for item in rattingg:
            avgrating = item.rating
        tcount = totalcount.count()
        cmnt = comment.objects.filter(forproduct=slug)

        bobj = Bidding.objects.filter(user_id=user.id, forproduct=slug)
        maxbid = Bidding.objects.filter(forproduct=slug)
        for item in maxbid:
            if item.bamount > maxbidamount:
                maxbidamount = item.bamount
        param = {'param': bidwons,
                 'user': sobj,
                 'tsale': tcount,
                 'avgrating': avgrating,
                 'comment': cmnt,
                 'bid': bobj,
                 'maxbid': maxbidamount,
                 }
        return render(request, 'Buyer/pages/BidwonDetail.html', param)


def delbidwin(request, slug):
    user = request.user
    bwinobj = Bidwons.objects.filter(user_id=user.id, slug=slug)
    bwinobj.delete()
    messages.success(request, 'Deleted Successfully...!')
    return redirect('/bidwons/')


def changetype(request):
    user = request.user
    if request.method == 'POST':
        uname = request.POST.get("name")
        rad = request.POST.get('rad')
        em = request.POST.get("em")
        uget = User.objects.filter(username=uname)
        for data in uget:
            print(data.id)
        print(user.id)
        code = get_random_string(length=6, allowed_chars='1234567890')
        obj = Type.objects.filter(user_id=user.id)
        obj.update(con=False, emcon=str(code), confirmm=False, type=rad)
        uget.update(email=em)
        delobj = buyer.objects.filter(user_id=user.id)
        delobj.delete()
        msg = "Your email confirmation code is : " + str(code)
        send_mail(
            'Email Confirmation Code',  # subject portion
            msg,
            'bidbeaverss@gmail.com',  # email from
            [em],  # email to
            fail_silently=False, )
        return redirect('/goprofile/')

    param = {'param': user.username}
    return render(request, "changetype.html", param)


def forgetpas(request):
    if request.method == 'POST':
        em = request.POST.get("em")
        uname = request.POST.get("uname")
        obj = User.objects.filter(email=em, username=uname)
        userid = ""
        for item in obj:
            userid = item.id
        if (obj.count() == 0):
            messages.error(request, 'Incorrect username or email,Kindly enter correct username and password...!')
            return render(request, "forget.html")
        else:
            obj1 = Type.objects.filter(user_id=userid)
            code = get_random_string(length=6, allowed_chars='1234567890')
            obj1.update(emcon=str(code))
            msg = "Your Password confirmation code is : " + str(code)
            send_mail(
                'Password Confirmation Code',  # subject portion
                msg,
                'bidbeaverss@gmail.com',  # email from
                [em],  # email to
                fail_silently=False, )
            messages.success(request, 'Confirmation code has been sent to your email...!')
            return redirect('/forgetconfirm/')

    return render(request, "forget.html")


def forgetconfirm(request):
    if request.method == 'POST':
        code = request.POST.get("code")
        obj = Type.objects.filter(emcon=code)
        if (obj.count() == 0):
            messages.error(request, 'Kindly enter correct code...!')
            return redirect('/forgetconfirm/')
        else:
            # obj.update(emcon=get_random_string(length=6, allowed_chars='1234567890'))
            userid = ""
            for item in obj:
                userid = item.user_id
            param = {'param': userid}
            return render(request, "resetpass.html", param)
    return render(request, "forgetconfirm.html")


def resetpass(request):
    if request.method == 'POST':
        uid = request.POST.get("uid")
        print(uid)
        pas = request.POST.get("pas")
        user = User.objects.get(id=uid)
        user.set_password(pas)

        user.save()
        messages.success(request, "Password has been changed,kindly login...!")
        return redirect('/accounts/login/')
    return render(request, "resetpass.html")


'''
def simple_table(request):
    class HTML2PDF(FPDF, HTMLMixin):
        pass
    spacing=1
    obj=seller.objects.all()
    print(obj.count())
    data = [['First Name', 'Last Name', 'CNIC', 'Phone NO'],

            ]

    for item in obj:
        temp=[item.Fname,item.Lname,item.CNIC,item.phone_no]
        data.append(temp)


    pdf = FPDF()
    pdf.set_font("Arial", size=12)
    pdf.add_page()

    col_width = pdf.w / 4.5
    row_height = pdf.font_size
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height * spacing,
                     txt=item, border=1)
        pdf.ln(row_height * spacing)
        code = get_random_string(length=6, allowed_chars='1234567890')
    pathh=os.path.join(MEDIA_ROOT,'simple_table'+code+'.pdf')
    pdf.output(pathh)




    fs = FileSystemStorage()
    #BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = safe_join(MEDIA_ROOT,'simple_table'+code+'.pdf')
    #filename =os.path.join(BASE_DIR,'simple_table743454.pdf')
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="simple_table'+code+'.pdf"'
            os.remove(filename)
            return response

    return HttpResponse("")


'''


# single Product
def detail_prod(request, slug):
    prod = Product.objects.all()
    print(slug)
    pd = Product.objects.filter(slug=slug)
    Min_Bid = None
    Current_Max_Bid = None
    prod_price = None
    usr = None
    for i in pd:
        usr = i.user
    person = Type.objects.get(user=usr)
    print(person.user)
    sellr = seller.objects.get(user=usr)
    print(sellr.Fname)
    uniquee=Product.objects.order_by('prod_category').values('prod_category').distinct()
    uniq=[]
    for i in uniquee:
        uniq.append(i.get('prod_category'))
    '''
    for i in pd:
        if(i.prod_status=='S' and i.auction_status=='NF'):
            bid=Bidding.objects.filter(forproduct=slug)
            print("if run 1")
            if bid.exists():
                print("True")
            else:
                print("False")
        else:
            Min_Bid=i.minbid
            
            print("else Run")'''

    return render(request, 'single.html', {'prod': pd, 'person': person, 'seller': sellr,'unique':uniq})


from django.db.models import Q


def search(request):
    if request.method == 'GET':
        query = request.GET.get('search')
        result = None
        if query:
            result = Product.objects.filter(
                Q(prod_title__icontains=query) | Q(prod_price__icontains=query) | Q(prod_category__icontains=query)
                | Q(prod_loc__icontains=query) | Q(prod_price__icontains=query) | Q(prod_description__icontains=query))
        final_outcome = None

        if result.exists():
            CRITICAL = 50
            messages.add_message(request, CRITICAL, 'Result Found ')
            final_outcome = result
        else:
            CRITICAL = 50
            messages.add_message(request, CRITICAL, 'Result Not Found | Plz try again with another keyword.')
            final_outcome = 'Retry'
        print(final_outcome)
        param = {
            'final_outcome': final_outcome,
            'result': result
        }
    return render(request, 'search.html', param)
