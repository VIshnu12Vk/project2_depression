from django.urls import path
from .import views
from .import utils
urlpatterns = [
    path('firstpage/',views.first_page),
    path('secondpage/',views.secondpage, name='secondpage'),
    path('about/',views.about, name='about'),
    path('game/',views.game, name='game'),
    path('my-view/', views.my_view, name='my-view'),
    path('questions/', views.question_page, name='question_page'),
    path('emotion-detection/', views.live_emotion_detection, name='live_emotion_detection'),
    path('emotion-detection-page/', views.emotion_detection_page, name='emotion_detection_page'),
    path('update_session_variable/', views.update_session_variable, name='update_session_variable'),
    path('result/', views.result_view, name='result_view'),
   
    
    

]