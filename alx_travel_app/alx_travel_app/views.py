from django.http import JsonResponse

def api_home(request):
    return JsonResponse({"message": "Welcome to the API!" , 
                         "visite the Django admin : " : "http://127.0.0.1:8000/admin/", 
                         "visite the Swagger docs : " : "http://127.0.0.1:8000/swagger/",
                         "visite the JSON response API  : " : "http://127.0.0.1:8000/api/"})
