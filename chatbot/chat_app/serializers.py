from rest_framework import serializers
from .models import User, Conversation, FAQ

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

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'category']
    def validate(self, data):
        """
        Check that FAQ's question and answer are not longer than 150 characters
        """
        if len(data['question']) > 150:
            raise serializers.ValidationError("Question cannot be longer than 150 characters")
        if len(data['answer']) > 150:
            raise serializers.ValidationError("Answer cannot be longer than 150 characters")
        return data