from django.urls  import path
from . import views

# URLConf, Django looks for this
urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:id>/', views.product_detail),
]