from django.urls import path
from .views import BookDisplay,BookDetailView,borrow
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', BookDisplay.as_view(), name='book_list'),
    path('category/<slug:category_slug>/', BookDisplay.as_view(), name='book_list_by_category'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('borrow/<int:pk>/', borrow, name='borrow_book'),
]
