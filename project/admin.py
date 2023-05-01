from django.contrib import admin
from project.models import contact,Product,Type,seller,buyer,Rating,Report,comment,Bidding,Bidwons

# Register your models here.
admin.site.register(seller),
admin.site.register(contact),
admin.site.register(Product),
admin.site.register(buyer),
admin.site.register(Rating),
admin.site.register(Report),
admin.site.register(comment),
admin.site.register(Bidding),
admin.site.register(Bidwons),
admin.site.register(Type)
#admin.site.register()