from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient



from watchlist_app.api import serializers
from watchlist_app import models

class StreamPlatformCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password='1234')
        # self.token = Token.objects.get(user__username=self.user)
        client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")

        self.stream = models.StreamPlatform.objects.create(name='Netflix', about='good', website='www.net.com')
        

    def test_streamplatform_create(self):
        data = {
            'name':'Netfilx',
            'about': 'mywebsite',
            'website': 'net.com',

        }
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class WatchListTestCase(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(username="example", password='1234')
        # self.token = Token.objects.get(user__username=self.user)
        client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")

        self.stream = models.StreamPlatform.objects.create(name='Netflix', about='good', website='www.net.com')
        
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title='my title', storyline='my story', active=True)
        
        self.review = models.Reviews.objects.create(review_user=self.user, description='great',rating=5,watchlist=self.watchlist, active=True)

    def test_watch_create(self): 
        data = {
            'platform':self.stream,
            "title":"Exampl movie",
            "storyline": "Example",
            "active":True
        }

        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # If iam not a admin I get 403 forbidden

    def test_watchlist(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist(self):
        response = self.client.get(reverse('movie-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.get().title, 'my title')
        self.assertEqual(models.WatchList.objects.count(), 1)

class ReviewTestCase(APITestCase):
    def setUp(self): #to create a review I need a movie and a movie needs a platform
        self.user = User.objects.create_user(username="example", password='1234')
        # self.token = Token.objects.get(user__username=self.user)
        client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")

        self.stream = models.StreamPlatform.objects.create(name='Netflix', about='good', website='www.net.com')
        
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title='my title', storyline='my story', active=True)
        self.watchlist2 = models.WatchList.objects.create(platform=self.stream, title='my title', storyline='my story', active=True)

        self.review = models.Reviews.objects.create(review_user=self.user, description='great',rating=5, watchlist = self.watchlist2, active=True)

    def test_review_create(self):
        data ={
             'review_user':self.user,
             "rating":5,
             "description":'great',
             "watchlist": self.watchlist,
             "active":True
         }

        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_review_create_unauth(self):

        data ={
             'review_user':self.user,
             "rating":5,
             "description":'great',
             "watchlist": self.watchlist,
             "active":True
         }

        self.client.force_authenticate(user=None)#log out
        response = self.client.post(reverse('review-create', args=(self.watchlist2.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):

          data ={
             'review_user':self.user,
             "rating":4,
             "description":'great - updated',
             "watchlist": self.watchlist,
             "active":True
         }
        

          response = self.client.put(reverse('review-create', args=(self.watchlist.id,)),data)
          self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_review_list(self):

        response = self.client.get(reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_ind(self):

        response = self.client.get(reverse('review-list', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_user(self):
        response = self.client.get(reverse('/watch/reviews/?username'+self.username))
        self.assertEqual(response.status_code, status.HTTP_200_OK)



