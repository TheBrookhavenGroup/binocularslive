from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import HasAPIKey


class PermissionTestView(APIView):
    permission_classes = (HasAPIKey,)

    def post(self, request):
        return Response({'message': request.data['text']})


class SplitView(APIView):
    permission_classes = (HasAPIKey,)

    def get(self, request):
        content = {'message': 'Use a post request.'}
        return Response(content)

    def post(self, request):
        text = request.data['text']
        return Response({'message': text})
