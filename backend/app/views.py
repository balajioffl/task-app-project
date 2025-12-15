from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def check(request):
    return Response({"msg":"backend is working !"})