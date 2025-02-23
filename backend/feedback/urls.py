from django.urls import path
from feedback import views

urlpatterns = [
    # FEEDBACK URL'S
    path('add_feedback/', views.add_feedback_view, name='add_feedback'),
    path('toggle_publish_feedback/', views.toggle_publish_feedback_view, name='toggle_publish_feedback'),
    path('get_user_feedbacks/', views.get_feedbacks_view, name='get_user_feedbacks'),
    path('get_feedbacks/', views.get_all_feedbacks_view, name='get_all_feedbacks_view'),
]
