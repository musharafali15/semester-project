from django.conf.urls.static import static
from django.urls import path,include

from fypproject import settings
from . import views
from .views import ArticleDetailView

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contactt,name='contact'),
    path('contact_sent/', views.contact_sent, name='contact_sent'),

    path('after/', views.after, name='after'),
    path('single/', views.single, name='single'),
#Seller Dashboard and operations
    #path('seller/',views.seller,name="seller_profile"),
    path('dashboard/seller/', views.seller_dashboard, name='seller_dashboard'),
    path('new/product/', views.product_up, name='new_product'),
#seller sale Products
    path('seller/table/',views.product_sell,name='sell_detail'),
    path('profile/', views.profile, name='profile'),
    path('Bprofile/', views.Bprofile, name='Bprofile'),

    #Buyer Dashboard and its Operation
    path('dashboard/buyer/',views.buyer_dashboard,name='buyer_dashboard'),
#buyer bid products
    path('buyer/table/',views.product_buy,name='buyer_products'),
    path('buyer/',views.profile_buyer,name='buyer'),
    path('signup/',views.signup, name='signup.html'),
    path('Gsignup/',views.Gsignup, name='signup.html'),
    path('goprofile/',views.goprofile,name="dds"),
    path('register/',views.register, name='signup.html'),
    path('changepass/',views.ChangePass,name="changepass"),
    path('pages/form-validation/',views.product_up,name="addproduct"),
    path('pendingAuctions/',views.PendingAuctions,name="PendingAuctions"),
    path('BpendingAuctions/',views.BPendingAuctions,name="BPendingAuctions"),
    path('ongoingAuctions/',views.ongoingAuctions,name="ongoingAuctions"),
    path('BongoingAuctions/',views.BongoingAuctions,name="ongoingAuctions"),
    path('startAuction/<slug>/',views.startAuction,name="startAuction"),
    path('stopAuction/<slug>/',views.stopAuction,name="stopAuction"),
    path('finishedAuctions/<slug>/',views.finishedAuctions,name="finishedAuctions"),
    path('removeproduct/<slug>/',views.removeproduct,name="removeproduct"),
    path('removecomment/<slug>/',views.removecomment,name="removecomment"),
    path('delbidwin/<slug>/',views.delbidwin,name="delbidwin"),
    path('editProduct/<slug>/',views.editProduct,name="editProduct"),
    path('auctionDetails/<slug>/',views.auctionDetails,name="auctionDetails"),
    path('bidDetails/<slug>/',views.bidDetails,name="bidDetails"),
    path('bidwinDetails/<slug>/',views.bidwinDetails,name="bidwinDetails"),
    path('ssfuldetail/<slug>/',views.ssfuldetail,name="ssfuldetail"),
    path('edit',views.editP,name="editP"),
    path('<slug:slug>', views.ArticleDetailView, name='showproduct'),

    path('giverating/',views.giverating,name="giveratring"),
    path('reportseller/',views.reportseller,name="reportseller"),
    path('reportbuyer/',views.reportbuyer,name="reportbuyer"),
    path('comment/',views.commentt,name="comment"),
    path('bid/',views.bid,name="bid"),
    path('finishedAuctions/',views.finishAuctions,name="bid"),
    path('bidwons/',views.bidwons,name="bidwons"),
    path('changetype/',views.changetype,name="changetype"),
    path('forget/',views.forgetpas,name="forget"),
    path('forgetconfirm/',views.forgetconfirm,name="forgetconfirm"),
    path('resetpass/',views.resetpass,name="resetpass"),
    path('product_list/',views.prod_list,name='Product Detail'),
    path('detail_prod/<slug>/',views.detail_prod,name='Detail'),

    #For Searching
    path('search/',views.search,name="Search"),
    #path('simple_table/',views.simple_table,name="simple_table"),
    path('in/',views.innnn,name="innn"),
    path('cat/<str:item>/',views.cat,name="category"),
    path('admin_contact/',views.contact_admin,name="AdminContact"),
    path('ajax/validate_seller/',views.validate_seller,name="validate_seller"),


]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
