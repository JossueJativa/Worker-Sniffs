from django.contrib import admin

# Register your models here.
from API.models import *

admin.site.register(User)
admin.site.register(Comments)
admin.site.register(Stars)
admin.site.register(Product)
admin.site.register(Problems)
admin.site.register(Problems_Tikets)
admin.site.register(Client)
admin.site.register(Tecnic)
admin.site.register(CallCenter)
admin.site.register(Manger)
admin.site.register(Certificate)