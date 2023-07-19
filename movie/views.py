from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view


from .models import Movie,Comment, Tag
from .serializers import MovieSerializer, CommentSerializer, TagSerializer, MovieListSerializer

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    # serializer_class = MovieSerializer

    def get_serializer_class(self):
        
        if self.action == "list" : 
            return (MovieListSerializer)
        return (MovieSerializer)
        
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        #createmodelmixin에내장 
        movie = serializer.instance
        self.handle_tags(movie)
        #영화객체생성및변수에저장
        return Response(serializer.data)
        
    def handle_tags(self, movie):
        words = movie.content.split(' ')
        tag_list = []
        for w in words :
            if w[0] == "#":
                tag_list.append(w[1:])
                
        for t in tag_list:
            tag, created = Tag.objects.get_or_create(name=t)
            movie.tag.add(tag) 
            
        movie.save()
        
    
    def perform_update(self, serializer):
        movie = serializer.save()
        movie.tag.clear()
        self.handle_tags(movie)
        
    


    


# @api_view(['GET','POST'])
# def comment_read_create(request, movie_id):
#     movie = get_object_or_404(Movie, id=movie_id)
    
#     if request.method == 'GET':
#         comments = Comment.objects.filter(movie=movie)
#         serializer = CommentSerializer(comments, many=True)
#         return Response(data=serializer.data)
    
#     elif request.method == 'POST':
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(movie=movie)
#         return Response(serializer.data)
    
    
class CommentViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer



class MovieCommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        movie = self.kwargs.get("movie_id")
        queryset = Comment.objects.filter(movie_id=movie)
        # serializer = self.get_serializer(queryset, many=True)
        return queryset
    
    
    
    def create(self, request,movie_id=None):
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(movie=movie)
        return Response(serializer.data)
        

# @api_view(['GET'])
# def find_tag(request, tag_name):
#     f_tag = get_object_or_404(Tag, name=tag_name)
#     if request.method == 'GET':
#         movie = Movie.objects.filter(tag__in = [f_tag]) 
#         serializer = MovieSerializer(movie, many=True)
#         return Response(data=serializer.data)


class TagViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "name"
    lookup_url_kwarg = "tag_name" #알려주는거지변수설정아님
    
    def retrieve(self, request, *args, **kwargs):
        tag_name = kwargs.get("tag_name")
        tag = get_object_or_404(Tag, id=tag_name)
        movies = Movie.objects.filter(tag=tag)
        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data)