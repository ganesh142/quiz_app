from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('hostreg',views.hostreg,name='hostreg'),
    path('hostdel',views.hostdel,name='hostdel'),
    path('home',views.home,name='home'),
    path('hostlgn',views.hostlgn,name='hostlgn'),
    path('userlgn',views.userlgn,name='userlgn'),
    path('data',views.data,name='data'),
    path('addqn',views.addqn,name='addqn'),
    path('delqn',views.delqn,name='delqn'),
    path('addusr',views.addusr,name='addusr'),
    path('delusr',views.delusr,name='delusr'),
    path('start',views.start,name='start'),
    path('exam',views.exam,name='exam'),
    path('logout',views.logout,name='logout'),
    path('getscore',views.getscore,name='getscore'),
    path('ulst',views.ulst,name='ulst'),
    path('qlst',views.qlst,name='qlst'),
    path('updtq',views.updtq,name='updtq'),
    path('upusr',views.upusr,name='upusr'),
    path('chnm',views.chnm,name='chnm'),
    path('chml',views.chml,name='chml'),
    path('chpw',views.chpw,name='chpw'),
]