import json

from bilibili_api import parse_link
from bilibili_api.video import Video
from nonebot.adapters.onebot.v11 import GroupMessageEvent

from ATRI.exceptions import str_traceback
from ATRI.log import log
from ATRI.message import MessageBuilder
from ATRI.service import Service

plugin = Service(
    "小程序解析", "解析QQ小程序卡片。", "0.0.1", Service.ServiceType.FUNCTION, "l_o_o_k"
)

analysis = plugin.on_message("卡片解析", "helloworld")


@analysis.handle()
async def _(event: GroupMessageEvent):
    message = event.message
    for segment in message:
        if segment.type == "json":
            now_type = "json"
            try:
                json_data = json.loads(segment.data["data"])
                json_meta = json_data["meta"]["detail_1"]
                if json_meta["title"] == "哔哩哔哩":
                    now_type = "哔哩哔哩"
                    sender = json_meta.get("host", {}).get("nick", "")
                    short_url = json_meta["qqdocurl"].split("?")[0]
                    info = await get_video_info(short_url)
                    message = MessageBuilder()
                    message.text(f"""{sender}分享了B站视频:
标题:{info.title}
UP:{info.owner} | {info.bvid} | 时长:{trans_time(info.duration)}
数据：播放:{info.stat.view} 点赞:{info.stat.like} 投币:{info.stat.coin} 收藏:{info.stat.favorite} 转发:{info.stat.share} 评论:{info.stat.reply} 弹幕:{info.stat.danmaku}
简介:{info.desc}
视频链接:https://www.bilibili.com/video/{info.bvid}""")
                    message.image(info.pic)
                    await analysis.send(message)
            except Exception as e:
                log.warning(f":解析{now_type}时发生以下错误\n{str_traceback(e)}")


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


async def get_video_info(url) -> VideoInfo:
    obj, resource_type = await parse_link(url)
    if isinstance(obj, Video):
        info = await obj.get_info()
        return VideoInfo(info)
    else:
        raise ValueError("不是视频")


def trans_time(duration: int):
    hour = int(duration // 3600)
    minute = int(duration // 60 % 60)
    second = int(duration % 60)
    raise f"{f'{hour}:' if hour else ''}{minute}:{second}"
