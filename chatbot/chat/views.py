from rest_framework import viewsets, status
from .models import User, Conversation, FAQ
from .serializers import UserSerializer, ConversationSerializer, FAQSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filters import FAQFilter

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    http_method_names = ['post']
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    http_method_names = ['post']

    @action(detail=False, methods=['post'], name="Start Conversation")
    def createConversation(self, request):
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FAQViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing all FAQs
    """
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    http_method_names = ['get']