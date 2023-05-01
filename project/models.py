from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils import timezone
# Create your models here.

CHOICES = (
    ('S', 'Seller'),
    ('B', 'Buyer'),
    ('G','Guest')
)

AuctionStatus = (
    ('F', 'Finished'),
    ('NF', 'Not Finished'),
)

prod_status= (
    ('S', 'Started'),
    ('NS', 'Not Started'),
)



class Type(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    type = models.CharField(choices=CHOICES,max_length=1,blank=True)
    con=models.BooleanField(default=False)
    emcon=models.CharField(max_length=15,blank=False)
    confirmm=models.BooleanField(default=False)
    pconfirm=models.BooleanField(default=False)
    created_date = models.DateTimeField('date created', default=timezone.now)
    def __str__(self):
        return self.user.username

class seller(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField()
    Fname=models.CharField(max_length=20,blank=False)
    Lname=models.CharField(max_length=20,blank=True)
    CNIC=models.CharField(max_length=20,blank=False,unique=True)
    phone_no=models.CharField(max_length=20)
    city=models.CharField(max_length=15,default='N/A')
    address=models.CharField(max_length=75,blank=False)
    postal_code=models.CharField(max_length=7,blank=True)
    description=models.TextField(max_length=500,default="")
    created_date = models.DateTimeField('date created', default=timezone.now)

    def __str__(self):
        return self.user.username


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(null=True, blank=True, default=0.0)
    created_date = models.DateTimeField('date created', default=timezone.now)
    def __str__(self):
        return self.user.username

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject=models.CharField(max_length=100)
    description=models.TextField(max_length=1000)
    created_date = models.DateTimeField('date created', default=timezone.now)
    def __str__(self):
        return self.user.username


class buyer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image=models.ImageField()
    Fname=models.CharField(max_length=20,blank=False)
    Lname=models.CharField(max_length=20,blank=True)
    CNIC=models.CharField(max_length=20,blank=False,unique=True)
    phone_no=models.CharField(max_length=20,blank=False)
    buyer_email = models.EmailField()
    city = models.CharField(max_length=15, default='N/A')
    address = models.CharField(max_length=75, blank=False)
    postal_code = models.CharField(max_length=7, blank=True)
    tbids=models.IntegerField(default=0)
    sbids=models.IntegerField(default=0)
    lbids=models.IntegerField(default=0)
    created_date = models.DateTimeField('date created', default=timezone.now)


    def __str__(self):
        return self.user.username

class comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image=models.ImageField()
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    forproduct=models.IntegerField()
    message=models.CharField(max_length=100)
    created_date = models.DateTimeField('date created', default=timezone.now)
    slug = models.SlugField(null=True, blank=True,default="")
    def __str__(self):
        return self.user.username
    def get_remove_comment_url(self):
        return reverse("removecomment", kwargs={
            'slug': self.slug
        })


class Bidding(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField()
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    bamount=models.FloatField()
    forproduct = models.IntegerField()
    created_date = models.DateTimeField('date created', default=timezone.now)
    def __str__(self):
        return self.user.username


class contact(models.Model):
    c_id=models.AutoField(primary_key=True)
    c_name=models.TextField()
    c_email=models.EmailField()
    subject=models.TextField()
    phone=models.TextField()
    message=models.TextField()
    file=models.FileField(upload_to='media/ContactUS',blank=True)
    created_date = models.DateTimeField('date created', default=timezone.now)

    def __str__(self):
        return self.subject

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)#Null False nahi krna
    prod_title=models.TextField()
    prod_description=models.TextField()
    prod_price=models.FloatField(default=0.0)
    minbid=models.FloatField(default=0.0)
    prod_category=models.CharField(max_length=15,default='House')
    #prod_files=models.FileField(upload_to='media/products')
    tframe=models.IntegerField(default=24)
    prod_loc=models.TextField()
    prod_status=models.CharField(choices=prod_status,max_length=2,default="NS")
    prod_date=models.DateTimeField().auto_now
    auction_status=models.CharField(choices=AuctionStatus,max_length=2,default="NF")
    starttime=models.CharField(max_length=50,default="")
    endtime=models.CharField(max_length=50,default="")
    nofbidder=models.IntegerField(default=0)
    slug = models.SlugField(null=True, blank=True)  # new
    created_date = models.DateTimeField('date created', default=timezone.now)

    class Meta:
        get_latest_by = ['created_date']

    def get_absolute_urls(self):
        return reverse('showproduct', kwargs={'slug': self.slug})
    def __str__(self):
        return self.prod_title
    def get_remove_product_url(self):
        return reverse("removeproduct", kwargs={
            'slug': self.slug
        })

    def get_start_auction_url(self):
        return reverse("startAuction", kwargs={
            'slug': self.slug
        })
    def get_stop_auction_url(self):
        return reverse("stopAuction", kwargs={
            'slug': self.slug
        })
    def get_finish_auction_url(self):
        return reverse("finishedAuctions", kwargs={
            'slug': self.slug
        })

    def get_edit_product_url(self):
        return reverse("editProduct", kwargs={
            'slug': self.slug
        })
    def get_auction_details_product_url(self):
        return reverse("auctionDetails", kwargs={
            'slug': self.slug
        })


    def get_details_bid_product_url(self):
        return reverse("bidDetails", kwargs={
            'slug': self.slug
        })



    def get_ssfuldetail_url(self):
        return reverse("ssfuldetail", kwargs={
            'slug': self.slug
        })

    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url



class Bidwons(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pimage=models.ImageField(default='')
    p_title=models.CharField(max_length=20,default='')
    p_disc=models.TextField(max_length=500,default='')
    p_loc=models.CharField(max_length=50,default='')
    auction_status=models.CharField(max_length=10,default='F')
    seller_id=models.IntegerField()

    slug=models.SlugField(default=0)
    created_date = models.DateTimeField('date created', default=timezone.now)

    def __str__(self):
        return self.user.username


    def get_bidwin_details_url(self):
        return reverse("bidwinDetails", kwargs={
            'slug': self.slug
        })

    def get_delete_bidwin_url(self):
        return reverse("delbidwin", kwargs={
            'slug': self.slug
        })





