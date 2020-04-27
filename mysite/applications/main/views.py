from django.shortcuts import render, redirect
from .forms import ContactForm
from datetime import date
from .models import Email

# sendemail
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def main(request):
    return render(request, 'main.html')

def contact(request):
    return render(request, 'contact.html')

def emailView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            today = date.today()
            d = today.strftime('%Y-%m-%d')
            try:
                a = Email(email=from_email, subject=subject, message=message, date=d)
                a.save()
                send_mail(subject, message, from_email, ['shnam93@gmail.com', 'sangnam1101@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('sent/')

    return render(request, "contact.html", {'form': form})

def successView(request):
    return render(request, 'contact_sent.html')
