# song-sentiment-site
Website with data visualizations of song sentiment through time. 

# Introduction

The motivation for this project came from me listening to my saved songs playlist on shuffle. One moment I was listening to "Theme From New York, New York" by Frank Sinatra, and the next I was listening to "Butterfly Effect" by Travis Scott. This sharp contrast made realize how much mainstream music has changed in just the past 50 years. I thought it would be fun to quantify and visualize some of these changes.

# Visualizations

The visualizations can be found [here](https://github.com/IJPaul/song-sentiment-site).

# Tools and Packages Used

* VADER (Valence Aware Dictionary and sEntiment Reasoner) Sentiment Analysis
  * Used to get sentiment line by line of song lyrics as displayed on Genius.com
* Beautiful Soup
  * Used to scrap [Genius.com](https://genius.com/) for song lyrics and the Billboard top 100 for the top 100 songs of each year
* Chart.js
  * Used to visualize data collected
* Openpyxl
  * Used to write collected data to Excel sheets

# Notes About Scoring 
###### Taken From the https://github.com/cjhutto/vaderSentiment README.rst 

* The VADER sentiment lexicon is sensitive both the polarity and the intensity of sentiments expressed in social media contexts, **and** is also generally applicable to sentiment analysis in other domains
* The compound score is computed by summing the valence scores of each word in the lexicon, adjusted according to the rules, and then normalized to be between -1 (most extreme negative) and +1 (most extreme positive). This is the most useful metric if you want a single unidimensional measure of sentiment for a given sentence. Calling it a 'normalized, weighted composite score' is accurate.

  * **positive sentiment**: ``compound`` score >=  0.05
  * **neutral  sentiment**: (``compound`` score > -0.05) and (``compound`` score < 0.05)
  * **negative sentiment**: ``compound`` score <= -0.05
 
# Citation

Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
