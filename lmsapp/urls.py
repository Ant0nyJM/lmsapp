from django.urls import path
from . import views

urlpatterns =[
    path('',views.book_search),
    path('signup/',views.signup,name='signup'),
    path('login/',views.userlogin,name='login'),
    path('logout/',views.userlogout,name='logout'),
    path('user/<int:user_id>/home/',views.user_home,name='user_home'),

    path('usersearch/',views.user_search,name='user_search'),
    path('user/<str:username>/',views.get_user,name='getuser'),
    path('user/<int:user_id>/passwchange/',views.passw_change,name='passwchange'),
    path('booksearch/',views.book_search,name='book_search'),


    path('book/<int:book_id>/',views.get_book,name='getbook'),
    
    path('dashboard/bookissue/',views.dash_book_issue,name='dash_book_issue'),
    path('dashboard/bookreturn/',views.book_return,name='book_return'),
    path('dashboard/bookadd/',views.book_add,name='book_add'),
    path('dashboard/bookedit/',views.book_edit,name='book_edit'),
    path('dashboard/bookdelete/',views.book_delete,name='book_delete'),


    ]
