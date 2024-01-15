from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import FormView,ListView
from .forms import UserAccountForm,DepositForm,CommentForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .models import Borrow,Transaction,Comment
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from books.models import Book
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.

def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

class UserRegistrationView(FormView):
    template_name = 'register.html'
    form_class = UserAccountForm
    success_url = reverse_lazy('home')
    
    def form_valid(self,form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name = 'user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
class UserLogoutView(LogoutView):
    def get_success_url(self):
        messages.success(self.request, 'Logged Out Successfully.')
        return reverse_lazy('home')
    
class BorrowedBooksListView(LoginRequiredMixin,ListView):
    template_name = 'profile.html'
    context_object_name = 'borrowed_books'

    def get_queryset(self):
        user = self.request.user.account
        return Borrow.objects.filter(user=user)
    

@login_required
def user_profile(request):
    user_borrowed_books = Borrow.objects.filter(user=request.user.account)
    return render(request, 'profile.html', {'user_borrowed_books': user_borrowed_books})

@login_required
def returnbook(request,id):
    b = Borrow.objects.get(pk=id)
    b.returned = True
    b.save()
    request.user.account.book.remove(b.book)
    account = request.user.account
    account.balance += b.book.price
    account.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def deposit_view(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount >= 200:
                Transaction.objects.create(user=request.user, amount=amount)
                account = request.user.account
                account.balance += amount
                account.save()
                messages.success(request,"Deposit Money Successful")
                send_transaction_email(request.user, amount, "Deposit Message", "deposit_email.html")
                return redirect('home')
            else:
                messages.warning(request,"Minimum deposit amount is 200")
                return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = DepositForm()

    return render(request, 'deposit.html', {'form': form})


def user_comment(request,id):
    book = get_object_or_404(Book, id=id)
    comments = Comment.objects.filter(book=book)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.book = book
            comment.save()
            return redirect('book_detail', pk=id)
    else:
        form = CommentForm()

    return render(request, 'comment.html', {'book': book, 'comments': comments, 'form': form})


