from rest_framework.views import APIView, View
from rest_framework.response import Response
from .permissions import HasAPIKey
from .tasks import prove_singleton


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


class SingletonView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        x = int(kwargs['value'])
        result = prove_singleton.delay(x)
        result = result.get()
        msg = f"The result is {result}"
        return Response({'message': msg})
