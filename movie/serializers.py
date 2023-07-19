from rest_framework import serializers
from .models import *

# class MovieSerializer(serializers.ModelSerializer):
#     # id = serializers.CharField(read_only=True)
#     # created_at = serializers.CharField(read_only=True)
#     # updated_at = serializers.CharField(read_only=True)
#     comments = serializers.SerializerMethodField(read_only=True)  
#     # def 뭐시기랑얘는 세트!! 포린키 다대다 일대다 다 얘 써줘야대요 나머지는 그냥 클래스메타필드에넣으면돼요
#     tag = serializers.SerializerMethodField()
    
#     def get_comments(self,instance):
#         serializer = CommentSerializer(instance.comments, many=True)
#         return serializer.data
    
#     def get_tag(self,instance):
#         tags = instance.tag.all()
#         return [tag.name for tag in tags] 
#     #tags만큼 반복하며 tagname을리스트?
    
#     class Meta:
#         model= Movie
#         fields = '__all__'
#         # fields = ['id','name','content','created_at','updated_at','comments', 'tag']
#         # fields = ('id, 'name, 'content', 'created_at', 'updated_at')
        
#     image = serializers.ImageField(use_url=True, required=False)
    
    
class MovieSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField()
    image = serializers.ImageField(use_url=True, required=False)
    # writer = serializers.TextField(read_only = True)
    def get_comments(self, instance):
        serializer = CommentSerializer(instance.comments, many=True)
        return serializer.data
    
    def get_tag(self, instance):
        tags = instance.tag.all()
        return [tag.name for tag in tags]
    
    class Meta:
        model = Movie
        fields = "__all__"
        read_only_fields = ['id', 'created_at' , 'updated_at', 'comments', 'num']
    

class MovieListSerializer(serializers.ModelSerializer):
    comments_cnt = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()
    
    def get_comments_cnt(self, instance):
        return instance.comments.count()
    
    def get_tag(self,instance):
        tags = instance.tag.all()
        return [tag.name for tag in tags]
        
    class Meta:
        model = Movie
        fields = ['id', 'name', 'created_at', 'updated_at', 'image', 'comments_cnt', 'tag']
        read_only_fields = ['id', 'created_at' , 'updated_at', 'comments_cnt']


class CommentSerializer(serializers.ModelSerializer):
    
    movie = serializers.SerializerMethodField()
    
    def get_movie(self, instance):
        return instance.movie.name
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['movie']
        
        
class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        field = '__all__'
        