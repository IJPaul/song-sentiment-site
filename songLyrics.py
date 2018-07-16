import basic_scraping
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

"""
Returns the frequency of lyrics by word in a song

Parameter songURL: The Genius url
Precondition: A valid song url on Genius.com
"""
def getLyricsFreq(songURL):
    lyricsFreq = {}
    badChars = ['!','?',',','.','(',')', '"']
    lyrics = basic_scraping.getPageElement(songURL, 'div', 'lyrics').getText()
    
    for c in badChars:
        lyrics = lyrics.replace(c, "")
    for subtext in lyrics.split(" "):
        for word in subtext.split('\n'):
            if len(word) >= 1 and (word[0] == '[' or word[len(word)-1] == ']'):
                pass
            else:
                word = word.lower()
                if word in lyricsFreq:
                    lyricsFreq[word] += 1
                else:
                    lyricsFreq[word] = 1
    return lyricsFreq

"""
Returns an array containing lyrics of a song line by line

Parameter songURL: The Genius url
Precondition: A valid song url on Genius.com
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

Parameter billboardURL: The billboard url
Precondition: A valid billboard url from billboardtop100of.com
"""
def getTopSongs(billboardURL):
    songs = []
    rows = basic_scraping.getPageElements(billboardURL, 'td')
    i = 0
    while i < len(rows)-2:
        artist = rows[i+1].getText()
        artist = re.sub('\n', '', artist)
        song = getPrimarySongName(rows[i+2].getText())
        song = re.sub('\n', '', song)
        song = song.replace("LYRICS", "")
        if artist == 'Weeknd':
            artist = 'The Weeknd'
        artistAndSong = (artist, song)
        songs.append(artistAndSong)
        i += 3
    return songs
"""
Returns the song's primary name i.e. if the song is
'Habits (Stay High)', then just 'Habits' is returned
"""
def getPrimarySongName(song):
    parenthesis = song.find('(')
    if parenthesis == -1:
        return song
    else:
        newTitle = song[:parenthesis]
        return newTitle.strip()

"""
Returns a billboardtop100of url for the given year
"""
def getBillboardURL(year):
    url = "http://billboardtop100of.com/%s-2/" % year
    return url

"""
Returns a VADER sentiment dictionary for a sentence
Inaccurate results for larger pieces of text (text >= 5 sentences)
"""
def getSentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(text)
    return vs

"""
Returns a VADER sentiment dictionary for an entire song
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
        sentiment[key] = '{0:.3g}'.format(sentiment[key] / count)
    return sentiment

"""
Returns whether song is postive, neutral, or negative
based on the songs compound VADER score
"""
def getSongMood(songURL):
    overallSentiment = float(getSongSentiment(songURL)['compound'])
    print(overallSentiment)
    if overallSentiment >= 0.05:
        return 'positve'
    elif overallSentiment > - 0.05:
        return 'neutral'
    else:
        return 'negative'
                    
"""
Returns the Genius URL of a song from the artist name and song name

def getGeniusURL(artist, song):
    baseURL = "https://Genius.com/"
    badChars = ['!','?',',','.','(',')', '"', '$']
    artistName = artist.replace(' ', '-')
    songTitle = song.replace(' ', '-')
    songTitle = songTitle.replace("'", "")
    print(songTitle)
    for bc in badChars:
        artistName = artistName.replace(bc, "")
        songTitle = songTitle.replace(bc, "")
    geniusURL = baseURL + artistName + '-' + songTitle + '-lyrics'
    return geniusURL
"""
def getGeniusURL(artist, song):
    baseURL = "https://Genius.com/"
    badChars = ['!','?',',','.','(',')', '"', '$']
    artistName = artist.replace(' ', '-')
    songTitle = song.replace(' ', '-')

    artistName = re.sub("[!?,'.()\"$]", "", artistName)
    songTitle = re.sub('[!?,\'.()"$]', "", songTitle)
        
    geniusURL = baseURL + artistName + '-' + songTitle + '-lyrics'
    return geniusURL

def getYearSentiment(year):
    billboardURL = getBillboardURL(year)
    # a tuple in the form (artist, song)
    topHundred = getTopSongs(billboardURL)
    moodDict = {'neg' : 0, 'pos' : 0, 'neu' : 0}
    for artistSong in topHundred:
        
        artist = artistSong[0].split('feat.')[0].strip()
        song = artistSong[1]
        
        geniusURL = getGeniusURL(artist, song)
        print(geniusURL)
        mood = getSongMood(geniusURL)
        
        if mood == 'negative':
            moodDict['neg'] += 1
        elif mood == 'positive':
            moodDict['pos'] += 1
        else:
            moodDict['neu'] += 1
    return moodDict
            
            
    
    
        
        
   
        

