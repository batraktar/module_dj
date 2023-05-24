from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app.views import Login, Registration, Logout, ProductListView, ProductDetailView, ProductCreateView, ProdUpdateView, PurchaseCreate

urlpatterns = [
    path('', ProductListView.as_view(), name='base'),
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Registration.as_view(), name='registration'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_item'),
    path('create_product/', ProductCreateView.as_view(), name='create'),
    path('update_product/<slug:slug>/', ProdUpdateView.as_view(), name='update'),
    path('buy/<slug:slug>/', PurchaseCreate.as_view(), name='buy_product'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
