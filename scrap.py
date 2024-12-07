from flask import Flask , render_template
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import requests
from flask import request


url =f'https://masstamilan.one'

app = Flask(__name__)


@app.route('/')
def index():
    page = 1
    page = requests.get(f'{url}/movie-index?page={page}')
    soup = BeautifulSoup(page.content,'html.parser')
    # get all movie name from this 
    #  <h2 class="movie-name">
    #   <a href="/bottle-radha-songs">
    #    Bottle Radha
    #   </a>
    #  </h2>
    movies = []

    for ele in soup.find_all('div', class_='movie'):
        temp_dict ={}
        movie_name = ele.find('h2', class_='movie-name').get_text(strip=True)
        movie_image_url = ele.find('picture').find('img')['src']
        movie_url = ele.find('h2', class_='movie-name').find('a')['href']
        temp_dict['name'] = movie_name
        temp_dict['link'] = f'{movie_url}'
        temp_dict['image'] = f'{url}{movie_image_url}'
        movies.append(temp_dict)

    # for link in movie_links:
    #     song_page = requests.get(f'{url}{link}')
    #     link_soup = BeautifulSoup(song_page.content,'html.parser')
    #     for a_tag in link_soup.find_all('a', class_='downloadbutton'):
    #             download_url = a_tag['href']
    #             download_urls.append(f'{url}{download_url}')
    


    print(movies)


    return render_template('index.html' , movies=movies )

@app.route('/song/<movie_name>')
def song(movie_name):
    movie_link = request.args.get('extra_param')
    song_page = requests.get(f'{url}{movie_link}')
    return render_song(song_page.content)




@app.route('/search/<search_text>')
def search_song(search_text):
    try:
        song_page = requests.get(f'{url}/{search_text}-songs')
        if not song_page.content:
            return render_template('notfound.html')
        return render_song(song_page.content)
    except:
        return render_template('notfound.html')


def render_song(content):
    soup = BeautifulSoup(content,'html.parser')
    songs = soup.find_all('div', class_='song-list')
    all_songs = []

    image_sources = soup.find_all('source')
    image_url = image_sources[0]['srcset'] if image_sources else soup.find('img')['src']
    movie_name = soup.find('span', {'itemprop': 'name'}).text

    for song in songs:
        temp_dict = {}
        song_name = song.find('span', itemprop='name').get_text(strip=True)
        download_link = song.find('a', class_='downloadbutton')['href']
        temp_dict['name'] = song_name
        temp_dict['link'] = f'{url}{download_link}'
        all_songs.append(temp_dict)
    return render_template('songs.html' , songs=all_songs , movie_name=movie_name , image_url=f'{url}{image_url}' )
