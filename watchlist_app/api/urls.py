from django.urls import path, include
# from watchlist_app.api import views #importing views from api folder
from watchlist_app.api.views import WatchListAV, WatchDetailAV, StreamPlatformAV, StreamPlatformDetailAV, ReviewList, ReviewDetail, ReviewCreate, StreamPlatformMV, UserReview, WatchListGV

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('stream', StreamPlatformMV, basename='streamplatform')
urlpatterns = [
    ##### functions based views #####
    # path('list/', views.movie_list, name='movie-list' ),
    # path('<int:pk>',  views.movie_details, name='movie-detail'),
    ####  classes based views ######
    path('list/', WatchListAV.as_view(), name='movie-list' ),
    path('<int:pk>/',  WatchDetailAV.as_view(), name='movie-detail'),
    # path('stream/', StreamPlatformAV.as_view(), name='stream'),
    # path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name='streamplatform-detail'),
    ######### Router - two path in one ########
    path('',include(router.urls)),
    #Reviews
    # path('review/', ReviewList.as_view(), name='review-list'), #all reviews from databases
    # path('review/<int:pk>/', ReviewDetail.as_view(), name='review-list'), # reveiws for every movie
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'), # all reviews for a single movie
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('reviews/', UserReview.as_view() , name='user-review'),
    #Filtering
    path('list2/', WatchListGV.as_view(), name='movie-list2' ),
]