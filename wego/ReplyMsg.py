# -*- coding: utf-8 -*-
'''
被动回复消息

'''

class BaseMsg(object):
    #dict data 传入解析后的request.body
    reply_data={}
    def __init__(self,data):
        self.reply_data = {'FromUserName':data['ToUserName'],'ToUserName':data['FromUserName'],'CreateTime':int(time.time())}

    def make_xml(self):
        return self.wechat._make_xml(self.reply_data)
    
class TextMsg(BaseMsg):
    def __init__(self,data,content):
        super(TextMsg,self).__init__(data)
        self.reply_data['MsgType'] = 'text'
        self.reply_data['content'] = content

class ImageMsg(BaseMsg):
    def __init__(self,data,media_id):
        super(ImageMsg,self).__init__(data)
        self.reply_data['MsgType'] = 'image'
        self.reply_data['Image'] = {'MediaId':media_id}

class VoiceMsg(BaseMsg):
    def __init__(self,data,media_id):
        super(VoiceMsg,self).__init__(data)
        self.reply_data['MsgType'] = 'voice'
        self.reply_data['Voice'] = {'MediaId':media_id}

class VideoMsg(BaseMsg):
    def __init__(self,data,media_id,**kwargs):
        super(VideoMsg,self).__init__(data)
        self.reply_data['MsgType'] = 'video'
        self.reply_data['Video'] = {'MediaId':media_id}
        if title:
            self.reply_data['Video']['Title'] = title
        if description:
            self.reply_data['Video']['Description'] = description

class MusicMsg(BaseMsg):
    def __init__(self,data,**kwargs):
        super(MusicMsg,self).__init__(data)
        self.reply_data['MsgType'] = 'music'
        self.reply_data['Music'] = kwargs


class NewsMsg(BaseMsg):
    def __init__(self,data,news_list=[]):
        super(NewsMsg,self).__init__(data)
        self.reply_data['MsgType'] = 'news'
        count = len(news_list)
        if count:
            self.reply_data['ArticleCount'] = count
            self.reply_data['Articles'] = news_list 


def msg_or_event_type(data):
    '''
    data 是request.body穿过来的xml
    '''
    msg_type=('text','voice','video','location','link','shortvideo','image')
    #转dict
    if data.MsgType in msg_type:
        data['type'] = data.MsgType
    elif data.MsgType == 'event' :
        if data.Event == 'subscribe' and data.has_key('EventKey') :
            data['type'] = 'scan_subcribe_event'
        else:
            data['type'] = data.Event.lower() + '_event'
   
    return data
    
