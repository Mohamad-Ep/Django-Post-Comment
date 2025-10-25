from rest_framework import serializers
from ...models import Article,Category
from rest_framework.reverse import reverse
from apps.accounts.models import Profile
import os
# _______________________________________________________

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['created_date']
# _______________________________________________________

class PostSerializer(serializers.ModelSerializer):
    relative_url = serializers.SerializerMethodField(method_name='get_absolute_url',read_only=True)
    
    class Meta:
        model = Article
        exclude = ['created_date','updated_date']
        read_only_fields = ['published_date','author']
        
    def get_absolute_url(self,obj):
        request = self.context.get('request')
        return reverse('blog:api-v1:post_details', kwargs={'slug': obj.slug},request=request)
    
    def validate_image_name(self, value):
        valid_formats = ['.jpg', '.jpeg', '.png', '.webp']
        file,exe = os.path.splitext(value.name.lower())
        
        if exe not in valid_formats:
            raise serializers.ValidationError("The image file format is not valid.")
        return value
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')
        if request.parser_context.get("kwargs").get("slug"):
            rep.pop('relative_url')
            
        rep['category']=CategorySerializer(instance.category).data
        return rep
    
    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(user=self.context.get('request').user)
        return super().create(validated_data)
# _______________________________________________________