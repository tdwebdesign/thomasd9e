from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def process_question(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        response = question[::-1]  # Reverse the question
        return HttpResponse(response)

def cfb_assistant(request):
    return render(request, 'cfb_assistant.html')

