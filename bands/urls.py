from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^savecategory', views.saveCategory, name='saveCategory'),
    url(r'^onaddCategoryclick', views.onaddCategoryclick, name='onaddCategoryclick'),
    url(r'^signup/', views.signup,name="signup"),
    url(r'^addUser/$', views.addUser,name="addUser"),
    url(r'^login/$', views.login,name="login"),
    url(r'^loginValidation', views.loginValidation,name="loginValidation"),
    url(r'^checkEmailandPassword/$', views.checkEmailandPassword,name="checkEmailandPassword"),
    url(r'^homepage/$', views.homepage,name="homepage"),
    url(r'^admin/$', views.admin,name='admin'),
    url(r'^addtosession/$', views.addtosession,name='addtosession'),
    url(r'^deletefromsession/$', views.deletefromsession,name='deletefromsession'),
    url(r'^deletecategory/$', views.ondeletecategoryclick,name='ondeletecategoryclick'),
    url(r'^delete_att/$', views.delete_att,name='delete_att'),
    url(r'^delete_subcat/$', views.delete_subcat,name='delete_subcat'),
    url(r'^delete_category/$', views.delete_category,name='delete_category'),
    url(r'get_delete_ad/$', views.get_delete_ad,name='get_delete_ad'),
    url(r'deletead/$', views.deletead,name='deletead'),
    url(r'product_details/$', views.product_details, name='product_details'),
    url(r'updateadmin/$',views.updateadmin,name='updateadmin'),
    url(r'logout/$',views.logout,name='logout')
]
