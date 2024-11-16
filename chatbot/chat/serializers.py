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
    user_name = serializers.CharField(write_only=True)
    user = serializers.IntegerField(read_only=True, source='user.id')

    class Meta:
        model = Conversation
        fields = ['id', 'user', 'user_name', 'created_at']

    def create(self, validated_data):
        user_name = validated_data.pop('user_name')
        try: 
            user = User.objects.get(name=user_name)
        except User.DoesNotExist:
             raise serializers.ValidationError({"user": f"User '{user_name}' does not exist"})
        conversation = Conversation.objects.create(user=user, **validated_data)
        return conversation
    
    def validate(self, data):
        user = data.get('user')
        if isinstance(user, str):
            try:
                user = User.objects.get(name=user)  # Look up the user by name
            except User.DoesNotExist:
                raise serializers.ValidationError({"user": f"User '{user}' does not exist in the database"})
            
            # Replace 'user' with the user's primary key (ID)
            data['user'] = user.id
        return data

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'conversationid', 'question', 'answer', 'category']
    def validate(self, data):
        """
        Check that FAQ's question and answer are not longer than 150 characters
        """
        if len(data['question']) > 150:
            raise serializers.ValidationError("Question cannot be longer than 150 characters")
        if len(data['answer']) > 150:
            raise serializers.ValidationError("Answer cannot be longer than 150 characters")
        return data