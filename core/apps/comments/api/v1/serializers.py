from rest_framework import serializers
from ...models import BlogComment
from django.shortcuts import get_object_or_404
from apps.accounts.models import Profile
# _______________________________________________________

class CommentBlogSerializer(serializers.ModelSerializer):
    commenting_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = BlogComment
        fields = ['fullname','comment_text','is_active','published_date','commenting_user','article']
        read_only_fields = ['is_active','published_date']
        
    def create(self, validated_data):
        profile = get_object_or_404(Profile,user=self.context.get('request').user)
        validated_data['commenting_user'] = profile
        return super().create(validated_data)
        
# _______________________________________________________