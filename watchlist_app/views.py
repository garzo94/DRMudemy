# from django.shortcuts import render, HttpResponse
# from django.http import JsonResponse
# from .models import Movie

# # Create your views here.


# def movie_list(request):
#     movies = Movie.objects.all()
#     print(movies.values())
#     return JsonResponse(movies.values())

# def movie_details(request, pk):
#     movie =  Movie.objects.get(pk=pk)
#     data = {
#         'name': movie.name
#     }
#     return JsonResponse(data)
