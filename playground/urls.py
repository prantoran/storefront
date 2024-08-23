from django.urls  import path
from . import views

# URLConf, Django looks for this
urlpatterns = [
    path('hello/', views.say_hello),
    path('last_five/', views.last_five),
    path('products_count/', views.aggregate),
    path('annotate/', views.annotate),
    path('annotate_product/', views.annotate_product),
    path('annotate_practice/', views.annotate_practice)
]