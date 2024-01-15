from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView,DetailView
from .models import Book,Category
from account.models import Borrow,Comment
from account.forms import CommentForm
from django.views import View
from django.contrib import messages
from django.utils import timezone
from datetime import datetime

# Create your views here.

class BookDisplay(ListView):
    template_name = 'book_display.html'
    context_object_name = 'books'
    model = Book

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            return Book.objects.filter(categories__slug=category_slug)
        else:
            return Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context
    
class BookDetailView(DetailView):
    model = Book
    template_name = 'details.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if hasattr(user, 'account'):
            account = user.account
            book = self.object
            has_borrowed = Borrow.objects.filter(user=account, book=book, returned=False).exists()
            context['btn'] = has_borrowed     

            comments = Comment.objects.filter(book=self.object)
            context['comments'] = comments

        return context

# class AddCommentView(View):
#     template_name = 'comment.html'
#     form_class = CommentForm

#     def get(self, request, book_id):
#         book = Book.objects.get(pk=book_id)
#         form = self.form_class(initial={'book': book})
#         return render(request, self.template_name, {'form': form, 'book': book})

#     def post(self, request, book_id):
#         book = Book.objects.get(pk=book_id)
#         form = self.form_class(request.POST)

#         if form.is_valid():
#             user = request.user

#             if Borrow.objects.filter(user=user, book=book).exists():
#                 form.instance.user = user
#                 form.instance.book = book
#                 form.save()
#                 messages.success(request, 'Comment added successfully.')
#             else:
#                 messages.error(request, 'You can only comment on books you have borrowed.')

#             return redirect('book_detail', pk=book_id)

#         return render(request, self.template_name, {'form': form, 'book': book})
    
def borrow(request,pk):
    o_book = Book.objects.get(pk=pk)
    o_account = request.user.account
    if o_account.book.filter(id=o_book.id).exists():
        messages.warning(request, 'You already have this book. Please return to get another book')
    elif o_account.balance < o_book.price:
        messages.warning(request, 'You dont have sufficiant balance for this book.')
    else:
        o_account.book.add(o_book)
        o_account.balance -= o_book.price
        o_account.save()
        b = Borrow(user=request.user.account,book=o_book,borrowed_time=datetime.now())
        b.save()
        messages.success(request, 'Book added successfully.')
    return redirect('book_list')



    

    