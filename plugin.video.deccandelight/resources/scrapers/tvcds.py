'''
thiruttuvcds deccandelight plugin
Copyright (C) 2016 Gujal

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
from main import Scraper
from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib, re, requests
import HTMLParser

class tvcds(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://thiruttuvcds.com/thiruttuvcd/category/'
        self.icon = self.ipath + 'tvcds.png'
        self.list = {'01Tamil Movies': self.bu + 'new-tamil-movies/',
                     '02Telugu Movies': self.bu + 'telugu/',
                     '03Hindi Movies': self.bu + 'hindi/',
                     '04Tamil Dubbed Movies': self.bu + 'tamil-dubbed/',
                     '05English Movies': self.bu + 'english/',
                     '06[COLOR cyan]Adult Movies[/COLOR]': self.bu[:-21] + 'private/',
                     '07[COLOR yellow]** Search **[/COLOR]': self.bu[:-9] + '?s='}
                     
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Thiruttu VCDs')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'postcont'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer('div', {'class':'wp-pagenavi'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('div', {'class':'postbox'})
        
        for item in items:
            title = h.unescape(item.h2.text)
            title = self.clean_title(title)
            url = item.find('a')['href']
            try:
                thumb = item.find('img')['src']
            except:
                thumb = self.icon
            movies.append((title, thumb, url))
        
        if 'next' in str(Paginator):
            nextli = Paginator.find('a', {'class':'nextpostslink'})
            purl = nextli.get('href')
            pgtxt = Paginator.find('span', {'class':'pages'}).text
            title = 'Next Page.. (Currently in %s)' % pgtxt
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,url):
        videos = []
            
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'videosection'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)
        links = videoclass.findAll('iframe')

        for link in links:
            try:
                vidurl = link.get('src')
                self.resolve_media(vidurl,videos)
            except:
                pass
      
        return videos
