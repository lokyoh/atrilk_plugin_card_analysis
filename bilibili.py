from bilibili_api import parse_link
from bilibili_api.video import Video

from ATRI.message import MessageBuilder

from .utils import trans_time


class VideoStat:
    def __init__(self, state):
        self.view = state["view"]
        self.like = state["like"]
        self.coin = state["coin"]
        self.favorite = state["favorite"]
        self.share = state["share"]
        self.reply = state["reply"]
        self.danmaku = state["danmaku"]


class VideoInfo:
    def __init__(self, info):
        self.bvid = info["bvid"]
        self.pic = info["pic"]
        self.title = info["title"]
        self.desc = info["desc"]
        self.owner = info["owner"]["name"]
        self.duration = info["duration"]
        self.stat = VideoStat(info["stat"])


async def get_bilibili_card_info(url, sender: str = "") -> MessageBuilder:
    obj, resource_type = await parse_link(url)
    if isinstance(obj, Video):
        info = await obj.get_info()
        info = VideoInfo(info)
        message = MessageBuilder()
        message.text(f"""{sender}分享了B站视频:
标题:{info.title}
UP:{info.owner} | {info.bvid} | 时长:{trans_time(info.duration)}
数据：播放:{info.stat.view} 点赞:{info.stat.like} 投币:{info.stat.coin} 收藏:{info.stat.favorite} 转发:{info.stat.share} 评论:{info.stat.reply} 弹幕:{info.stat.danmaku}
简介:{info.desc}
视频链接:https://www.bilibili.com/video/{info.bvid}""")
        message.image(info.pic)
        return message
    else:
        raise ValueError("不是视频")
