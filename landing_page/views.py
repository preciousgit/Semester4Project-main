from django.shortcuts import render


# Create your views here.
def open_landing_page(request):
    return render(request, "landing_page.html")
