
from django.contrib import admin

from .models import user
from .models import item
from .models import cart
from .models import order
from .models import PasswordReset

admin.site.register(user)
admin.site.register(item)
admin.site.register(cart)
admin.site.register(order)
admin.site.register(PasswordReset)



