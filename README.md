# MusicDownloader

MusicDownloader is a MP3 resource downloader based on Python 3.At present, it can download the corresponding songs according to the ID of the songs published in 163 music website.It is simple and single in function and easy to use.

# Build&Install

Download this project and run `pip install `.

# How To Use

You need to check the song ID on 163cloud's website.Like this:https://music.163.com/#/song?id=571854148. Then you need to write a simple Python script.

Like this:

```python
from MusicDownloader import music163
m = music163.music163_()
m.download("571854148")
```

