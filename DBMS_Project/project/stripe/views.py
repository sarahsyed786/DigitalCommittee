from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib import messages
import stripe
# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY

class HomePageView(TemplateView):
    template_name = 'homepage.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

def charge(request):
    if request.method == 'POST':
        token = request.POST.get('pk_test_51ORaD1GygBCH0kbVxe8kX7RbpSTLf2KQvzVyOw22dbJJfxWnQ20n2ATIhQLfSNej4LA5UwrTcOz2URYbHroPBwI100vhjrlMZU')
        
        try:
          charge = stripe.Charge.create(
            amount = 1000,
            currency = 'pkr',  
            source = token,
            description = 'Package Charge',
        )
          return render(request, 'charge.html', {'charge': charge})
        
        except:
            
            return render(request, 'error.html')
    return render(request, 'homepage.html')