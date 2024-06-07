from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import HasAPIKey


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class ByeView(APIView):
    permission_classes = (HasAPIKey,)

    def get(self, request):
        content = {'message': 'Bye, World!'}
        return Response(content)

    def post(self, request):
        text = request.data['text']
        return Response({'message': text})
