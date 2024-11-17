from rest_framework import viewsets, status
from .models import User, Conversation, FAQ, Message
from .serializers import UserSerializer, ConversationSerializer, FAQSerializer, MessageSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class UserViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for creating new users in Database
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    http_method_names = ['post', 'get']
    def list(self, request):
        return Response({
            "message": "Please enter your name and email",
            "instructions": {
                "POST": {
                    "description": "Payload to register new user",
                    "parameters": {
                        "Name": "string",
                        "Email": "string"
                    }
                }
            }
        }, status=status.HTTP_200_OK)
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        try:
            user = User.objects.get(name=request.data.get('name'))
            if (user):
                return Response("User already exists, please use another name", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    def list(self, request):
        return Response({
            "message": "Ask your question using your unique conversationId",
            "instructions": {
                "POST": {
                    "description": "Payload to send a message",
                    "parameters": {
                        "conversation_id": "int",
                        "question": "string"
                    }
                }
            }
        }, status=status.HTTP_200_OK)
    def create(self, request):
        """
        Endpoint for sending a conversation message. Will return answer or default if answer unknown
        """
        # Validate the request data
        serializer = MessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract validated data
        conversation_id = serializer.validated_data["conversation_id"]
        question = serializer.validated_data["question"]

        # Validate that the conversation exists
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)

        # Find the matching FAQ
        try:
            faq = FAQ.objects.get(question__iexact=question)
        except FAQ.DoesNotExist:
            return Response({
            "conversation_id": conversation_id,
            "question": question,
            "answer": "I'm not so sure about that. Please contact customer support"
        }, status=status.HTTP_200_OK)

        # Respond with the answer
        return Response({
            "conversation_id": conversation_id,
            "question": question,
            "answer": faq.answer
        }, status=status.HTTP_200_OK)

class ConversationViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for Conversations. Create a new Conversation using your UserId
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    http_method_names = ['get', 'post']
    def list(self, request):
        return Response({
            "message": "Create a new conversation",
            "instructions": {
                "POST": {
                    "description": "Payload to create a new conversation",
                    "parameters": {
                        "user": "int"
                    }
                }
            }
        }, status=status.HTTP_200_OK)

    def create(self, request):
        """
        An endpoint for creating a new conversation
        """
        user_id = request.data.get('user')
        if not user_id:
            return Response({"error": "user is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        conversation = Conversation.objects.create(user=user)
        serializer = ConversationSerializer(conversation)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FAQViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing all FAQs
    """
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["category",]
    http_method_names = ['get', 'list', 'options']

    def get(self, request, *args, **kwargs):
        request.GET["category"]
        try:
            data = FAQ.objects.filter(category__iexact=request.query_params.get('category'))
            serializer = FAQSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FAQ.DoesNotExist:
            return Response("Category does not contain any FAQs")