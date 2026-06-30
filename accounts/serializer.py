from rest_framework import serializers
from .models import CustomUser, VIA_EMAIL, VIA_PHONE, CODE_VERIFY, NEW, DONE, PHOTO_DONE
from shared.utils import check_email_or_phone
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.db.models import Q
from django.contrib.auth import authenticate

class SignUpSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields['email_or_phone_number'] = serializers.CharField(required=True, write_only=True)
        
    
    class Meta:
        model = CustomUser
        fields = ['id', 'auth_status', 'auth_type']
        read_only_fields = ['id', 'auth_status', 'auth_type']
        
    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        if user.auth_type == VIA_EMAIL:
            code = user.generate_code(VIA_EMAIL)
            print(f'---------------EMAIL CODE: {code} ------------------------')
        elif user.auth_type == VIA_PHONE:
            code = user.generate_code(VIA_PHONE)
            print(f'---------------SMS CODE: {code} ------------------------')
        else:
            raise ValidationError(
                { 'msg': 'Siz xato email yoki telefon raqam kiritdingiz',
                'status': status.HTTP_400_BAD_REQUEST}
                )
        user.save()
        return user        
        
            
        
    
    def validate(self, data):
        data = self.auth_validate(data)
        return data
        
    @staticmethod
    def auth_validate(data):
        user_input = str(data.get('email_or_phone_number')).lower()
        user_auth_type = check_email_or_phone(user_input)
        if user_auth_type == 'email':
            data = {
                'email':user_input,
                'auth_type':VIA_EMAIL
            }
        elif user_auth_type == 'phone':
            data = {
                'phone_number':user_input,
                'auth_type':VIA_PHONE
            }
        else:
            raise ValidationError(
                { 'msg': 'Siz xato email yoki telefon raqam kiritdingiz',
                'status': status.HTTP_400_BAD_REQUEST}
                )
        return data
    
    def validate_email_or_phone_number(self, value):
        value = str(value).lower()
        user = CustomUser.objects.filter(Q(email=value) | Q(phone_number=value)).first()
        if user and user.auth_status not in [NEW, CODE_VERIFY]:
            raise ValidationError(
                { 'msg': 'Bu email yoki telefon raqamdan oldin royxatdan otilgan',
                'status': status.HTTP_400_BAD_REQUEST}
                )
            
        if user and user.auth_status in [NEW, CODE_VERIFY]:
            user.delete()          
        return value
    
    def to_representation(self, instance):
        data =  super(SignUpSerializer, self).to_representation(instance)
        data.update(instance.token())
        return data
        
    


class ChangeInfoSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=False, write_only=True)
    phone_number = serializers.CharField(required=False, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    conf_password = serializers.CharField(required=True, write_only=True)
    
    
    def validate(self, data):
        password = data.get('password')
        conf_password = data.get('conf_password')
        if password and conf_password and password != conf_password:
            raise ValidationError(
                { 'msg': 'parollar mos emas',
                'status': status.HTTP_400_BAD_REQUEST}
                )
            
        return data
    
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.username = validated_data.get('username')
        if validated_data.get('email'):
            instance.email = validated_data.get('email')
        if validated_data.get('phone_number'):
            instance.phone_number = validated_data.get('phone_number')
        instance.set_password(validated_data.get('password'))
        
        
        if instance.auth_status == NEW:
            raise ValidationError(
                { 'msg': 'Siz hali ozingizni tasdiqlamagansiz',
                'status': status.HTTP_400_BAD_REQUEST}
                )
        
        instance.auth_status = DONE
        
        instance.save()
        
        return instance
    
    
    def to_representation(self, instance):
        return {
            "msg": 'Malumotlar yangilandi',
            'status': status.HTTP_200_OK,
            'token': instance.token()
        }
    
    
    
class ChangePhotoSerializer(serializers.Serializer):
    photo = serializers.ImageField()
    
    
    
    def update(self, instance, validated_data):
        photo = validated_data.get('photo', None)
        if photo:
            instance.photo = validated_data.get('photo')
       
    
        instance.auth_status = PHOTO_DONE
        
        instance.save()
        
        return instance
    
    
    def to_representation(self, instance):
        return {
            "msg": 'Rasm yangilandi',
            'status': status.HTTP_200_OK,
            'token': instance.token()
        }
    
    
    
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError


class LoginSerializer(serializers.Serializer):
    user_input = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user_input = attrs.get("user_input")
        password = attrs.get("password")

        user = CustomUser.objects.filter(
            Q(username=user_input) |
            Q(email=user_input) |
            Q(phone_number=user_input)
        ).first()

        if not user:
            raise ValidationError({
                "msg": "Login yoki parol xato",
                "status": status.HTTP_400_BAD_REQUEST
            })

        if user.auth_status in [NEW, CODE_VERIFY]:
            raise ValidationError({
                "msg": "Siz hali to'liq ro'yxatdan o'tmagansiz",
                "status": status.HTTP_400_BAD_REQUEST
            })

        authenticated_user = authenticate(
            username=user.username,
            password=password
        )

        if not authenticated_user:
            raise ValidationError({
                "msg": "Login yoki parol xato",
                "status": status.HTTP_400_BAD_REQUEST
            })

        attrs["user"] = authenticated_user
        return attrs
    

