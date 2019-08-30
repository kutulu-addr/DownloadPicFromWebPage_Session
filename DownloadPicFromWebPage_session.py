import requests
import re
import os.path
from PIL import Image
import shutil
##from lxml import etree
try:
    import cookielib
except:
    import http.cookiejar as cookielib


class GetPicAfterLogin(object):

    def __init__(self):
        self.headers = {  ##Init target website and local information
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept-Encoding': 'gzip, deflate',
            'Host': '', ##target website main page url
            'DNT': '1'
        }
        self.login_url ='' ##Login page url
        self.post_url = '' ##Login link string 
        ##self.logined_url = 'https://github.com/settings/profile'
        
        ##Get session and save in same directory
        self.session = requests.session() 
        self.session.cookies = cookielib.LWPCookieJar(filename='cookies')

##    def load_cookie(self):
##        try:
##            self.session.cookies.load(ignore_discard=True)
##        except:
##            print('cookie 不成功')
##
##    def get_param(self):
##        response = self.session.get(self.login_url, headers=self.headers)
##        selector = etree.HTML(response.text)
##        field_one = selector.xpath('//div/input[2]/@value')
##        print(field_one)
##        return field_one
        
    def login_post(self, username, password):  ##Combine and post login message, return link status
        post_data = {
            'username': username,
            'password': password,
            'loginsubmit': 'true',
            'formhash': 'd0fb1c81'
        }
        res = self.session.post(self.post_url, data=post_data, headers=self.headers)
        if(res.status_code == 200):
            self.session.cookies.save()
            return True
        else:
            return False

    def get_imageurl(self, pageurl):  ##Get images url from webpage source
        pageres = self.session.get(pageurl, headers = self.headers)
        if(pageres.status_code == 200):
            patter = re.compile(r'<img src="http.*?"', re.S)
            urls = re.findall(patter, pageres.text)

            imageurls = []

            for url in urls:
                imageurl = re.findall(r'http.*jpg', url)
                if(imageurl):
                    imageurls.extend(imageurl)
                else:
                    continue
                
            return imageurls
        else:
            return False

    def get_image(self, filepath, imagefilename, imageurl = ''): ##Download images by image url
        if(imageurl==''):
            return
        else:
            filename = filepath + imagefilename
            res = requests.get(imageurl)
            cont = res.content
            with open(filename, "wb") as pic:
                pic.write(cont)

if __name__ == "__main__":
    GPAL = GetPicAfterLogin()
    res = GPAL.login_post(username = '', password = '') ##Type user name and password
    if(res==True):
        print('Successful login')
        print('Paste the page URL you want:')
        pageurl = input()
        
        imageurls = GPAL.get_imageurl(pageurl)
        
        print('Please give full direction, default same as python script:')
        filepath = input() ##Type the path images will be saved
        
        if not os.path.isdir(filepath): ##Estimate standard system directory
            filepath = '.\\downloaded_image\\'
            print('As default direction, files will be saved in .\\downloaded_image\\')
        
        if not os.path.exists('.\\downloaded_image\\'): ##Estimate accessable path
            os.mkdir('.\\downloaded_image\\')
        else:
            shutil.rmtree('.\\downloaded_image\\')

        imageNum = 0
        
        for imageurl in imageurls:
             imagefilename = '0' + str(imageNum) + '.jpg' ##Set every image file name
             GPAL.get_image(filepath, imagefilename, imageurl)
             imageNum = imageNum + 1
             print(imagefilename + ' saved!')
        print('Finished!')
    else:
        print('Failure to login, please check login process by manual on web browser')
        exit()
