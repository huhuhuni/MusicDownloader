[English Readme](https://github.com/huhuhuni/MusicDownloader/blob/master/README.md)

# MusicDownloader

MusicDownloader是一款基于Python3的MP3资源下载程序，目前可以根据163音乐网站发布的歌曲ID下载相应的歌曲，功能简单，使用方便。

# Build&Install

下载此项目然后运行 `pip install `.

# How To Use

你需要查一下网易云网站上的歌曲ID.比如:https://music.163.com/#/song?id=571854148. 然后需要编写一个简单的Python脚本。

比如：

```python
from MusicDownloader import music163
m = music163.music163_()
m.download("571854148")
```

