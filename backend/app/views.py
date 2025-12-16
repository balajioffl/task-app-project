from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

@api_view(["GET"])
def check(request):
    return Response({"msg":"backend is working !"})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def test_api(request):
    return Response(
        {
            "msg" : "JWT is working !",
            "user" : request.user.username
        }
    )