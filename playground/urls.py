from django.urls  import path
from . import views

# URLConf, Django looks for this
urlpatterns = [
    path('celery_task', views.celery_task),
    path('templated_emails', views.templated_emails),
    path('attach_file', views.attach_file),
    path('mail_admin', views.mail_admin),
    path('hello/', views.say_hello),
    path('last_five/', views.last_five),
    path('products_count/', views.aggregate),
    path('annotate/', views.annotate),
    path('annotate_product/', views.annotate_product),
    path('annotate_practice/', views.annotate_practice),
    path('contenttype/', views.contenttype),
    path('taggeditem_custom_manager/', views.taggeditem_custom_manager),
    path('create_collection/', views.create_collection),
    path('update_collection/', views.update_collection),
    path('delete_collection/', views.delete_collection),
    path('cart_create/', views.cart_create),
    path('cart_update/', views.cart_update),
    path('cart_delete/', views.cart_delete),
    path('order_transaction/', views.order_transaction),
    path('raw_sql/', views.raw_sql),
]