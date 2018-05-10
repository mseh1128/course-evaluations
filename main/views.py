from django.shortcuts import render
from main.forms import HomeForm
from django.contrib import messages
# Create your views here.
def index(request):
	if request.method == 'POST':
		form = HomeForm(request.POST)
		if form.is_valid():
			# text = form.cleaned_data['post']
			return render(request, 'main/fullpage.html', {'form':form})
		else:
			return render(request, 'main/homepage.html', {'form':form})	
	else:
		form = HomeForm() 
		return render(request, 'main/homepage.html', {'form':form})