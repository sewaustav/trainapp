from django.shortcuts import render

def mainpage(request):
    # здесь другие разрабы будут вставлять код
    return render(request, 'fitapp/main.html')


