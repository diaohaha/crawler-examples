where_i_begin
=============


1.2013.6.6 baidutieba.py
  实现功能：
    python 简单爬虫,从百度贴吧爬取峨眉山的所有的帖子以及回复，包括标题，姓名，id，回复时间，回复内容。并存入数据库。
  包含：
    使用python自带的SGMLParser进行网页解析。数据库用mongodb。
  问题：
    不能更新，单线程，id回复对应不一致。未保存图片。
