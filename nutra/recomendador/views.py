from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
@csrf_exempt
def recomendacion(request):
    print("controladooo alvaro",request.POST)
    retorno = {"s1":request.POST["cat1"],"s2":request.POST["cat2"],"s3":request.POST["cat3"],"s4":request.POST["cat4"]}
    return HttpResponse (
		json.dumps(retorno),
		content_type = "application/json"
	)	