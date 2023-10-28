from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home,name='home'),
    path('login',views.Login_page,name='login'),
    path('logout',views.Logout,name='logout'),
    path('category',views.category,name='category'),
    path('products/<int:id>',views.products,name='products'),
    path('productdes/<int:id>',views.productdes,name='productdes'),
    path('cart/<int:id>',views.cart,name='cart'),
    path('buy/<int:id>',views.buy,name='buy'),
    path('buyu/<int:id>',views.buyu,name='buyu'),
    path('removecart/<int:id>',views.removecart,name='removecart'),
    path('cancelorder/<int:id>',views.cancelorder,name='cancelorder'),
    path('nccancelorder/<int:id>',views.nccancelorder,name='nccancelorder'),
    path('carts',views.carts,name='carts'),
    path('register',views.register_page,name='register'),
    path('orders',views.orders,name='orders'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)