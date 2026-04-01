
# """
# URL configuration for pro project.
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/4.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.ind),
    path('l',views.log),
    path('forgot', views.forgot_password, name="forgot"),
    path('reset/<token>', views.reset_password, name='reset_password'),
    path('r',views.reg),
    path('al',views.logouta),
    path('ul',views.logoutu),
    path('b',views.bk),
    path('d',views.ds),
    path('ad',views.adash),
    path('p',views.pro),
    path('up',views.upd),
    path('ap',views.apro),
    path('aup',views.aupd),
    path('ai',views.adi),
    path('ui', views.upi),
    path('di/<int:id>/', views.deli,name="deli"),
    path('ei/<int:id>', views.edi,name="edi"),
    path('iu/<int:id>/', views.itup,name="itup"),
    path('aor', views.aordtl),
    # path('crt/',views.cart1),
    path('cart/', views.ditm),
    path('ac/<int:id>', views.addcart),
    path('cart/in/<int:id>/', views.inqty, name='inqty'),
    path('cart/dc/<int:id>/', views.dcqty, name='dcqty'),
    path('rm/<int:id>', views.rmcart),
    path('ord', views.ordr),
    path('abs', views.abst),
    path('dig', views.digi),
    path('pen', views.pencl),
    path('so/<int:id>', views.sorder),
    path('min/<int:id>', views.minusitm),
    path('plu/<int:id>', views.plusitm),
    path('sb/<int:id>', views.sby),
    path('rz', views.razor),
    path('ordt', views.ordtls),
    path('mr', views.mlor),
    path('pay/<int:id>', views.paymnt),
    path('by', views.buy),
    path('mb',views.mby),
    # path('can/<int:id>',views.cancel),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

