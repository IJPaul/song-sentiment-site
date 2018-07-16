import basic_scraping
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import googlesearch

"""
Returns an array containing lyrics of a song line by line

Parameter songURL: The Genius URL
Precondition: A valid song lyrics URL (string)
"""
def getLyrics(songURL):
    lyricsArr = []
    lyrics = basic_scraping.getPageElement(songURL, 'div', 'lyrics').getText()
    for line in lyrics.split('\n'):
        if len(line) >= 1 and not (line[0] == '[' and line[len(line)-1] == ']'):
            lyricsArr.append(line)
    return lyricsArr
        

"""
Returns an array of the top 100 artists and songs of the given year

Parameter billboardURL: The billboard URL
Precondition: A valid billboard URL from billboardtop100of.com (string)
"""
def getTopSongs(billboardURL):
    songs = []
    rows = basic_scraping.getPageElements(billboardURL, 'td')
    i = 0
    while i < len(rows)-2:
        artist = getPrimaryArtist(rows[i+1].getText())
        artist = re.sub('\n', '', artist)
        song = getPrimarySongName(rows[i+2].getText())
        song = re.sub('\n', '', song)
        song = song.replace("LYRICS", "")
        
        artistAndSong = (artist, song)
        songs.append(artistAndSong)
        i += 3
    return songs

"""
Returns true if the generated Genius URL is in fact a valid Genius. Returns false otherwise

Parameter songURL: The URL
Precondition: songURL is a string
"""
def isValidGeniusUrl(songURL):
    try:
        lyrics = basic_scraping.getPageElement(songURL, 'div', 'lyrics').getText()
        return True
    except:
        return False
    
"""
Returns the song's primary artist(s) by removing features
ex: 'Rihanna feat. Drake' becomes 'Rihanna'
ex: 'Major Lazer and DJ Snake feat. MO' becomes 'Major Lazer and DJ Snake'

Parameter artist: The name of the artist(s)
Preconditon: artist is a string
"""
def getPrimaryArtist(artist):
    feature = artist.find('feat.')
    if feature == -1:
        return artist
    else:
        newArtist = artist[:feature].strip()
        return newArtist
"""
Returns the song's primary name i.e. if the song is
ex: 'Habits (Stay High)' becomes 'Habits'

Parameter song: The name of the song
Preconditon: song is a string
"""
def getPrimarySongName(song):
    parenthesis = song.find('(')
    if parenthesis == -1:
        return song
    else:
        newTitle = song[:parenthesis].strip()
        return newTitle

"""
Returns a billboardtop100of URL for the given year

Parameter year: The year
Precondition: year is an int 1940 <= year <= current year
"""
def getBillboardUrl(year):
    url = "http://billboardtop100of.com/%s-2/" % year
    return url

"""
Returns a VADER sentiment dictionary for a sentence

Parameter text: The text to be analyzed for sentiment
Precondition: text is a string of roughly sentence length
"""
def getSentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(text)
    return vs

"""
Returns a VADER sentiment dictionary for an entire song if the song has lyrics
otherwise, returns None

Parameter songURL: The Genius URL
Precondition: A valid song lyrics URL (string)
"""
def getSongSentiment(songURL):
    lyricsArr = getLyrics(songURL)
   
    sentiment = {'neg': 0, 'neu': 0, 'pos': 0, 'compound' : 0}
    count = 0
    for line in lyricsArr:
        vs = getSentiment(line)
        sentiment['neg'] += vs['neg']
        sentiment['neu'] += vs['neu']
        sentiment['pos'] += vs['pos']
        sentiment['compound'] += vs['compound']
        count += 1
    for key in sentiment:
        if count != 0:
            sentiment[key] = '{0:.3g}'.format(sentiment[key] / count)
        else:
            sentiment[key] = 0
    return sentiment

"""
Returns whether song is 'postive', 'neutral', or 'negative'
based on the songs compound VADER score

Parameter songURL: The Genius URL
Precondition: A valid song lyrics URL (string)
"""
def getSongMood(songURL):
    overallSentiment = float(getSongSentiment(songURL)['compound'])
    print(overallSentiment)
    if overallSentiment >= 0.05:
        return 'positive'
    elif overallSentiment > -0.05:
        return 'neutral'
    else:
        return 'negative'
                    
"""
Returns the Genius URL of a song from the artist name and song name if one exists
otherwise, returns None

Parameters artist, song: Name of artist(s), name of song
Preconditions: artist and song are both strings
"""
def getGeniusUrl(artist, song):
    # Attempt to get the url by doing regex expression replacement
    baseUrl = "https://Genius.com/"
    artistName = artist.replace(' ', '-')
    songTitle = song.replace(' ', '-')
    artistName = re.sub('[\$"\'()!%#?]', "", artistName)
    songTitle = re.sub('[\$"\'()!%#,?]', "", songTitle)
    
    geniusUrl = (baseUrl + artistName + '-' + songTitle + '-lyrics').replace(chr(8217), '')
    print(geniusUrl)
    
    if not isValidGeniusUrl(geniusUrl):
        geniusUrl = getGeniusUrlFromGoogle(artist, song)
    return geniusUrl

"""
Returns the top Genius URLs from a Google Search of the invalid Genius URL.

This function is used when artists and songs have names such that performing regular expression operations
on the artist name and song name and inserting them into the base Genius URL is not enough
to generate the valid Genius song lyrics URL.

Since the URL is close to the valid one, a google search of the invalid one will return the correct one within
the first few results.

Parameters artist, song: Name of artist(s), name of song
Preconditions: artist and song are both strings
"""
def getGeniusUrlFromGoogle(artist, song):
    searchTerms = 'genius lyrics ' + artist + ' ' + song
    urls = googlesearch.scrapeGoogle(searchTerms, 10)
    geniusUrl = None
    for url in urls:
        if isValidGeniusUrl(url):
            geniusUrl = url
            break
    return geniusUrl

"""
Parameters artist, song: Name of artist(s), name of song
Preconditions: artist and song are both strings
"""
def getYearSentiment(year):
    billboardUrl = getBillboardUrl(year)
    # a tuple in the form (artist, song)
    topHundred = getTopSongs(billboardUrl)
    moodDict = {'neg' : 0, 'pos' : 0, 'neu' : 0}
    for artistSong in topHundred:
        artist = artistSong[0].split('feat.')[0].strip()
        song = artistSong[1]
        url = getGeniusUrl(artist, song)
        mood = getSongMood(url)
        
        if mood == 'negative':
            moodDict['neg'] += 1
        elif mood == 'positive':
            moodDict['pos'] += 1
        else:
            moodDict['neu'] += 1
    return moodDict
            
            
    
    
        
        
   
        

