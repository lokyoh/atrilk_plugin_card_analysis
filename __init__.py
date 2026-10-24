import json
import re

from nonebot.adapters.onebot.v11 import GroupMessageEvent

from ATRI.exceptions import str_traceback
from ATRI.log import log
from ATRI.service import Service

from .bilibili import get_bilibili_card_info
from .config import BilibiliConfig

plugin = Service(
    "小程序解析", "解析QQ小程序卡片。", "0.0.4", Service.ServiceType.FUNCTION, "l_o_o_k"
)
config = plugin.add_plugin_config(BilibiliConfig)

analysis = plugin.on_message("卡片解析", "helloworld", block=False)


@analysis.handle()
async def _(event: GroupMessageEvent):
    message = event.message
    for segment in message:
        if segment.type == "json":
            now_type = "json"
            try:
                json_data = json.loads(segment.data["data"])
                if "detail_1" in json_data["meta"]:
                    json_meta = json_data["meta"]["detail_1"]
                    if json_meta["title"] == "哔哩哔哩":
                        now_type = "哔哩哔哩"
                        sender = json_meta.get("host", {}).get("nick", "")
                        short_url = json_meta["qqdocurl"].split("?")[0]
                        msg = await get_bilibili_card_info(
                            short_url, sender, config.create_credential()
                        )
                        await analysis.send(msg)
            except Exception as e:
                log.warning(f":解析{now_type}时发生以下错误\n{str_traceback(e)}")
        if segment.type == "text":
            text = segment.data["text"]
            pattern = re.compile(
                r"https?://(?:www\.)?(?:bilibili\.com/video/|b23\.tv/)[a-zA-Z0-9]+(?=[/?]|\s|$)",
                re.IGNORECASE,
            )
            match = pattern.search(text)
            if match:
                url = match.group(0)
                try:
                    msg = await get_bilibili_card_info(
                        url, credential=config.create_credential()
                    )
                    await analysis.send(msg)
                except Exception as e:
                    log.warning(f":解析bilibili链接时发生以下错误\n{str_traceback(e)}")
