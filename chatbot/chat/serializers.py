from rest_framework import serializers
from .models import User, Conversation, FAQ, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']
    def validate(self, data):
        """
        Check that User's name and email are not longer than 40 characters
        """
        if len(data['name']) > 40:
            raise serializers.ValidationError("Name cannot be longer than 40 characters")
        if len(data['email']) > 40:
            raise serializers.ValidationError("Email cannot be longer than 40 characters")
        return data

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'user', 'created_at']
    
    def validate(self, data):
        """
        Validate user is in database before creating a conversation
        """
        user = data.get('user')
        if isinstance(user, str):
            try:
                user = User.objects.get(name=user)
            except User.DoesNotExist:
                raise serializers.ValidationError({"user": f"User '{user}' does not exist in the database"})

            data['user'] = user.id
        return data

class MessageSerializer(serializers.Serializer):
    class Meta:
        model = Message
        fields = ['conversation_id', 'question', 'response']

    conversation_id = serializers.IntegerField(required=True, help_text="The unique ID of the conversation")
    question = serializers.CharField(required=True, help_text="The question to ask")


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'category']
    question = serializers.CharField(read_only=True)
    answer = serializers.CharField(read_only=True)