from django.urls import path
from . import views



urlpatterns = [
    path('mainpage/',views.mainpage,name='mainpageurl'),
    path('',views.farmer,name='farmerrigistationurl'),
    path('farmerlist/',views.farmerlist, name='farmerlisturl'),
    path('crop/',views.crop,name='cropurl'),
    path('croplist/',views.croplist,name='croplisturl'),
    path('worker/',views.worker,name='workerregistationurl'),
    path('workerlist/',views.workerlist,name='workerlisturl'),
    path('workingdetails/',views.workingdetails,name='workingdetails'),
    path('login/',views.login,name='loginpageurl'),
    path('logout/',views.logout,name='logouturl'),
    path('countofworker/',views.countofworker,name='countofworker'),
    path('farmer-worker-report/',views.farmerworkerreport,name='farmer-worker-report'),
     path('farmer-worker-report2/',views.totalfarmerworkerreport,name='farmer-worker-report2'),
   
]
