#DJANGO
from django.shortcuts import get_object_or_404
#restframework
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAuthenticatedOrReadOnly
# functions based views
from rest_framework.decorators import api_view
# clases based viewse
from rest_framework.views import APIView
#Mixings
from rest_framework import generics
from rest_framework import mixins
#viewsets
from rest_framework import viewsets
#permissions
from watchlist_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly
#throtlling
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle 
#Filtering or Searching
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
#pagination
from watchlist_app.api.pagination import WatchListPagination, WatchListOPagination, WatchListCPagination
#models and model serializer
from watchlist_app.models import WatchList, StreamPlatform, Reviews
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
##################### Concret View Classes #######################
class UserReview(generics.ListAPIView):
      # queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    #No permission this means anyone can make a get request
    permission_classes = [IsAuthenticated] #restriction, only authenticated user can see all reviews for a movie
     #{isAutenticatedorReadOnly} if I am authenticaed I can put and update otherwise just reading data
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    # throttle_classes = [ReviewListThrottle]

    def get_queryset(self): #overwirting queryset
        # username = self.kwargs['username'] #I am receivign this from url /watch/reviews/alex/ (<str:username>)
        username = self.request.query_params.get('username', None) #using /?paramas:value/
        
        return Reviews.objects.filter(review_user__username=username)

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    
    def perform_create(self,serializer):
        
        pk = self.kwargs.get('pk')

        movie = WatchList.objects.get(pk=pk)
        user = self.request.user
        review_queryset = Reviews.objects.filter(watchlist=movie, review_user=user)
        

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this shit!")
            

        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
            print('$$$', serializer.validated_data['rating'])
            print('$$$', movie.avg_rating) 
        else:
            print('###', serializer.validated_data['rating'])
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating'] ) / 2
            
        movie.number_rating =  movie.number_rating + 1
        movie.save()
        # print('$$$$', self.request.data )
        serializer.save(watchlist=movie, review_user=user) #which movie we have selected and who user is
    def get_queryset(self): # add this beacuse of error
        return Reviews.objects.all()


class ReviewList(generics.ListAPIView):
    # queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    #No permission this means anyone can make a get request
    permission_classes = [IsAuthenticated] #restriction, only authenticated user can see all reviews for a movie
     #{isAutenticatedorReadOnly} if I am authenticaed I can put and update otherwise just reading data
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    throttle_classes = [ReviewListThrottle]
    #filtering
    filter_backend = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active'] #/?review_user__username=value&active=true


    def get_queryset(self): #overwirting queryset
        pk = self.kwargs['pk'] #I am receivign this from url
        return Reviews.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
     queryset = Reviews.objects.all()
     serializer_class = ReviewSerializer
     permission_classes = [ScopedRateThrottle]
     throttle_scope = 'review-detail'
##################### Mixings class from classes based views #######################
# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView ):
#     queryset=Reviews.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#       return self.retrieve(request, *args, **kwargs)

# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#   queryset=Reviews.objects.all()
#   serializer_class = ReviewSerializer

#   def get(self, request, *args, **kwargs):
#       return self.list(request, *args, **kwargs)

#   def post(self, request, *args, **kwargs):
#       return self.create(request, *args, **kwargs)
######################## Model Viewset ########################### this is better
class StreamPlatformMV(viewsets.ModelViewSet): #this provide get update create delete
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer 
    permission_classes = [AdminOrReadOnly]

# class StreamPlatformMV(viewsets.ReadOnlyModelViewSet): #. ReadOnbly provides only get method for a list and a single element
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer


######################## VIEWSETS ###########################
# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True,context={'request': request}) #context here is because of hyperlink
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist,context={'request': request})
#         return Response(serializer.data)
#     # I can add creat and delete all in one url thi is perfect for huge projects

#     def create(self, request):
#         serializer =  StreamPlatformSerializer(data=request.data,context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

#####################using serializer or Modelserializer class and CLASS based views#######################
class StreamPlatformAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True,context={'request': request}) #context is to read hyperlink in serializer.py
       
        return Response(serializer.data)
    
    def post(self, request):
        serializer =  StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamPlatformDetailAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request, pk):
        try:
            platform =  StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Movie no found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform,context={'request': request}) #to show linkt sitead of id and could click the link
        return Response(serializer.data)

    def put(self, request, pk):
        platform =  StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform =  StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    #No permission this means anyone can make a get request
    # permission_classes = [IsAuthenticated] #restriction, only authenticated user can see all reviews for a movie
     #{isAutenticatedorReadOnly} if I am authenticaed I can put and update otherwise just reading data
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    #######filtering#######
    # filter_backends = [DjangoFilterBackend]
    # filter_backends = [filters.SearchFilter]
    # filter_backends = [filters.OrderingFilter]
   
    #filterset_fields = ['title', 'platform__name'] #/?review_user__username=value&active=tru
    # #####'^' start with --- '=' extac matches  --- '@' full-text only support Postgresql backend  -- '$' regex search
    # filterset_fields = ['=title', 'platform__name'] #/?serch=whateverworkd
    # #### ordering #####
    # ordering_fields = ['avg_rating']#/?-ordering=avg_rating
    pagination_class = WatchListCPagination



class WatchListAV(APIView): #AV = API VIEW
    permission_classes = [AdminOrReadOnly]
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True) #many = true when I am fetching more than 1 item
        return Response(serializer.data)

    def post(self, request):
        serializer =  WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchDetailAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request, pk):
        try:
            movie =  WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Movie no found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie =  WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie =  WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




#####################using serializer class and functions base views#######################
# @api_view(['GET', 'POST']) #whit post I can creater an instance from DRf INTERFACE
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True) #many = true when I am fetching more than 1 item
#         return Response(serializer.data)


#     if request.method == 'POST':
#         print(request.data)
#         serializer =  MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)



# @api_view(['GET','PUT','DELETE'])
# def movie_details(request, pk):

#     if request.method == 'GET':
#         try:
#             movie =  Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'Error': 'Movie no found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)


#     if request.method == 'PUT':
#         movie =  Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.error, status= status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         movie =  Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        

