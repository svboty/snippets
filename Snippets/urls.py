from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('snippets/add', views.add_snippet_page, name='snippets-add'),
    path('snippets/list/', views.snippets_page, name='snippets-list'),
    path('snippets/<int:snippet_id>', views.snippet_detail, name='snippets-detail'),
    path('snippets/<int:snippet_id>/update', views.snippet_update, name='snippets-update'),
    path('snippets/<int:snippet_id>/delete', views.snippet_delete, name='snippets-delete'),
    path('registration/', views.registration, name='registration'),
    path('comment/add/', views.comment_add, name="comment_add"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
