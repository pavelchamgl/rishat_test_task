from django.urls import path
from .views import get_session_id, item_detail, create_order, process_order

urlpatterns = [
    path('buy/<int:id>/', get_session_id, name='get_session_id'),
    path('item/<int:id>/', item_detail, name='item_detail'),
    path('create_order/', create_order, name='create_order'),
    path('process_order/', process_order, name='process_order'),
]
