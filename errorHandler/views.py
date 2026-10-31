from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template

def error400(request, exception):
    template = get_template("errorHandler/error400.html")
    html = template.render()
    return HttpResponse(html, status=400)
def error403(request, exception):
    return render(request, 'errorHandler/error403.html', status=403)
def error404(request, exception):
    return render(request, 'errorHandler/error404.html', status=404)
def error500(request):
    template = get_template("errorHandler/error500.html")
    html = template.render()
    return HttpResponse(html, status=500)
