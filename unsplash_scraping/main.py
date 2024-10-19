import json
import requests as req
from bs4 import BeautifulSoup
import os

class Unsplash:
    def __init__(self, search:str, page:int=1, per_page:int=20, quality:str='regular', dir_name:str = 'unsplash'):
        """
        You can change the default values to git you needs.
        search: you can search any type of pics you want
            page: the page number
            per_page: number of images you want on that page
            quality: is pictures quality, there's: raw, full, regular, small and thumb (default: regular)
        """
        self.search = search
        self.page = page
        self.per_page = per_page
        self.headers = {
            "authority": "unsplash.com",
            "method": "GET",
            "path": "/napi/search/photos?page=1&per_page=20&query=tesla&xp=search-region-awareness%3Aexperiment",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            "cache-control": "no-cache",
            "client-geo-region": "us",
            "cookie": "ugid=fdae82134fcf17eb235653de6cdd38425751511; require_cookie_consent=false; xp-simplified-plus-page=experiment; xp-search-disable-synonyms-2=experiment; xp-search-region-awareness=experiment; xp-reduced-affiliates=half; uuid=491fa020-6abc-11ef-9fbd-93bbfd9a28f7; azk=491fa020-6abc-11ef-9fbd-93bbfd9a28f7; azk-ss=true; xp-search-disable-curation=experiment; xp-enable-join-modal=control; xp-unlock-link-upgrade=control; xp-affiliate-collections=essentials; _sp_ses.0295=*; un_sesh=Um5tVVZxVVVmbjl4U3NTTW40bk54akUvOG94d2U2VTlmTlpIckQyV2xoVTdaY2tuY1NCNXRWTEM2YzFjTkgrSXRvbmpXOVo2Sk40eXVmbmtDTTBmSUtJdjFaRlR6Q0xUakxOMXdkVk14bjhZV2RIOURWblUzUWErZ1F3a0g2S2prbTN6UmdoK1lFWmdjYnh6MlFweEt3N3JPM3ZlQnR2Tm1ydW9MUUFHc21qYXFySTI2SVRKaDRHeExnN0JWODJ6M2xrb21KMHArWElSV1FsVFFWT2UxS0ppT0RDR3lRc1ZEMkQ0a3NvbU44TTdiR3FMZFI4MzdFcU5PYXpka29LQmJnVWtuK2pIUFZDaXNUd0VSYitCV01hS1lhbVdCR3ZPMHQrSVk3V1I1UHc9LS0wcEp2MzdHdEsydnc5Yks4dDYzdzlnPT0%3D--9a5e3d4130803c45156cf3b443e16618977eb94e; _dd_s=logs=1&id=87353d90-0bbc-411e-958c-b260b4132d84&created=1729230763818&expire=1729231670744; _sp_id.0295=5d2828fc-bdc8-40d7-8fe6-6cf0ad9c5ad0.1725454238.7.1729230771.1729143961.17a2ed0d-3dc6-4cc1-a67f-96bf7ee83ab2.fd94eb9e-c9c1-4861-a434-e7c4da2f33c8.b1c5803c-ed76-447c-b8d4-cccf74539b5b.1729229781093.52",
            "dnt": "1",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        }
        self.quality = quality
        self.dir_name = dir_name
    
    def make_requests(self) -> 'json':
        """Returns json data from the api request """
        url = f"https://unsplash.com/napi/search/photos?page={self.page}&per_page={self.per_page}&plus=none&query={self.search}&xp=search-region-awareness%3Aexperiment"
        res = req.get(url)
        res.raise_for_status()
        data = res.json()
        return data["results"]

    def get_picture(self) -> dict:
        """This method returns a dictionary of id and urls """

        dict_of_pics_and_ids = {}
        all_results = self.make_requests()
        for item in range(0, len(all_results)):
            name = all_results[item]['id']
            url = all_results[item]['urls'][self.quality]
            dict_of_pics_and_ids[name] = url
        return dict_of_pics_and_ids

    def save_pictures(self):
        """This method gets the image and save it to a folder called unsplash"""
        try:
            os.mkdir(f"./{self.dir_name}")
        except FileExistsError:
            pass

        num = 1
        for url in self.get_picture().values():
            with open(f"./{self.dir_name}/pic{num}.jpg", 'wb') as file:
                file.write(req.get(url).content)
                num += 1


downloader = Unsplash(search="alaska")
downloader.save_pictures()