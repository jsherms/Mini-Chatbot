from rest_framework import viewsets, status
from .models import User, Conversation, FAQ
from .serializers import UserSerializer, ConversationSerializer, FAQSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for creating new users in Database
    """
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
    """
    A ViewSet for Conversations. Can create new conversation or engage with existing conversation
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    http_method_names = ['post']

    @action(detail=False, methods=['post'], name="Start Conversation")
    def createConversation(self, request):
        """
        An endpoint for creating a new conversation
        """
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        conversation = Conversation.objects.create(user=user)
        serializer = ConversationSerializer(conversation)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], name="Send Message")
    def askQuestion(self, request):
        """
        Endpoint for sending a conversation message. Will return answer or default if answer unknown
        """
        conversation_id = request.data.get('conversation_id')
        question_text = request.data.get('question')

        # Validate parameters
        if not conversation_id or not question_text:
            return Response({"error": "conversation_id and question are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the conversation by id
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)

        # Search for the FAQ matching the question
        try:
            faq = FAQ.objects.get(question__iexact=question_text)
        except FAQ.DoesNotExist:
            return Response({
            "conversation_id": conversation.id,
            "question": faq.question,
            "answer": "I'm not so sure about that. Please contact customer support"
        }, status=status.HTTP_200_OK)

        # Return the answer from the FAQ
        return Response({
            "conversation_id": conversation.id,
            "question": faq.question,
            "answer": faq.answer
        }, status=status.HTTP_200_OK)



class FAQViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing all FAQs
    """
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    http_method_names = ['get']