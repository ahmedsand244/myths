# from django.shortcuts import render
# from .models import TeamMember, Partner

# def home_view(request):
#     return render(request, 'pages/home.html')

# def contact_view(request):
#     return render(request, 'pages/contact.html')

# def about_view(request):
#     team_members = TeamMember.objects.all()
#     partners = Partner.objects.all()
#     return render(request, 'pages/about.html', {
#         'team_members': team_members,
#         'partners': partners,
#     })





from django.shortcuts import redirect, render
from .models import TeamMember, Partner

def home_view(request):
    return redirect('/services/')

def contact_view(request):
    return render(request, 'pages/contact.html')

def about_view(request):
    team_members = TeamMember.objects.all()
    partners = Partner.objects.all()
    return render(request, 'pages/about.html', {
        'team_members': team_members,
        'partners': partners,
    })



