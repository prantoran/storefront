from django.urls  import path
from . import views

# URLConf, Django looks for this
urlpatterns = [
    path('hello/', views.say_hello)
]