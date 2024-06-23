from rest_framework import serializers
from user_app.models import CustomUser

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'bio']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self, **kwargs):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({"error": "Passwords do not match"})
        
        if CustomUser.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({"error": "Email is already in use!"})
        
        account = CustomUser(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            bio=self.validated_data['bio'],
        )
        account.set_password(password)
        account.save()
        
        return account

class AuthorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['is_author_requested']

    def update(self, instance, validated_data):
        instance.is_author_requested = validated_data.get('is_author_requested', instance.is_author_requested)
        instance.save()
        return instance
