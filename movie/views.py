from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64


def home(request):
    #return HttpResponse("<h1>Welcome to Home Page</h1>")
    #return render(request, 'home.html', {'name':'Agustín Figueroa'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'movies': movies, 'searchTerm': searchTerm, 'name': 'Agustín Figueroa'})   

def about(request):
    return render(request, 'about.html')

def statistics_view(request):
    matplotlib.use('Agg')
    all_movies = Movie.objects.all()

    # Movies per year
    movie_counts_by_year = {}
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        movie_counts_by_year[year] = movie_counts_by_year.get(year, 0) + 1

    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    graphic = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Movies per genre (only first genre)
    genre_counts = {}
    for movie in all_movies:
        first_genre = str(movie.genre).split(',')[0].strip() if movie.genre else "None"
        genre_counts[first_genre] = genre_counts.get(first_genre, 0) + 1

    bar_positions_genre = range(len(genre_counts))
    plt.bar(bar_positions_genre, genre_counts.values(), width=bar_width, align='center', color='orange')
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_genre, genre_counts.keys(), rotation=45)
    plt.subplots_adjust(bottom=0.3)
    buffer_genre = io.BytesIO()
    plt.savefig(buffer_genre, format='png')
    buffer_genre.seek(0)
    plt.close()
    genre_graphic = base64.b64encode(buffer_genre.getvalue()).decode('utf-8')
    buffer_genre.close()

    return render(request, 'statistics.html', {'graphic': graphic, 'genre_graphic': genre_graphic})

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})
