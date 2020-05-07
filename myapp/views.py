from django.shortcuts import render

def post_list(request):
    return render(request, 'myapp/post_list.html', {})
