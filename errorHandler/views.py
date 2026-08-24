from django.shortcuts import render

def error400(request, exception):
    return render(request, 'errorHandler/error400.html', status=400)
def error403(request, exception):
    return render(request, 'errorHandler/error403.html', status=403)
def error404(request, exception):
    return render(request, 'errorHandler/error404.html', status=404)
def error500(request):
    return render(request, 'errorHandler/error500.html', status=500)