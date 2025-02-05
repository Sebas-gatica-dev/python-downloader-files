# python-downloader-files

This Python script takes a URL and performs a partial validation to check if the page uses pagination or scroll loading. If it has pagination, it goes through all the pagination content. If the loading is by scroll, it uses Selenium to simulate the user's scroll. If it cannot detect any of these types of loads, what it does is download all the images it has available.

