import basic_scraping
from openpyxl import Workbook
from openpyxl import load_workbook

"""
Returns the top 100 songs of the year along with the artist
Parameter: the year to collect data on
Precondition: year is an int 2006 <= year <= 2017
"""
def getArtistsAndSongs(year):
    BILLBOARD_URL = 'https://www.billboard.com/charts/year-end/%s/hot-100-songs'
    url = BILLBOARD_URL % year
    topArtistSong = []
    yeChartSongItems = basic_scraping.getPageElements(url, 'div', {'class' : 'ye-chart-item__title'})
    yeChartArtistItems = basic_scraping.getPageElements(url, 'div', {'class' : 'ye-chart-item__artist'})
    for itemIndex in range(100):
        song = yeChartSongItems[itemIndex].getText().strip()
        artist = yeChartArtistItems[itemIndex].getText().strip()
        topArtistSong.append((artist, song))
    return topArtistSong

