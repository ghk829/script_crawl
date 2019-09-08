import scrapy
import os

class MainSpider(scrapy.Spider):

    name = "example"

    base_url = "https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show="

    series = ["how-i-met-your-mother",
              "disenchantment-2018"
              ]
    start_urls = []

    for e in series:
        start_urls.append(base_url+e);

    def parse(self,response):

        for url in response.css(".season-episodes > "
                                ".season-episode-title"
                                "::attr('href')").extract():
            yield scrapy.Request(response.urljoin(url),self.parse_script)


    def parse_script(self,response):

        series_name = response.url.split("tv-show=")[1].split("&")[0]

        if not os.path.exists(series_name):
            os.mkdir(series_name)
        filename = response.url.split("&")[1]

        result = "\n".join(response.css("#content_container > div.main-content > "
                                        "div.main-content-left > div.episode_script > "
                                        "div.scrolling-script-container::text").getall())
        self.write_to_file(f"{series_name}/{filename}.txt",result)

    def write_to_file(self,filename,result):
        with open(filename,"w") as f:
            f.write(result)