from bilibili_api import Credential

from ATRI.configs import Field, PluginConfig


class BilibiliConfig(PluginConfig):
    """Bilibili 登录凭据设置。"""

    sessdata = Field(
        str, "", "SESSDATA", "B站登录 Cookie；填写后启用登录请求，请勿泄露。"
    )
    bili_jct = Field(str, "", "BILI_JCT", "B站登录 Cookie，请勿泄露。")
    buvid3 = Field(str, "", "BUVID3", "B站登录 Cookie，可选。")
    buvid4 = Field(str, "", "BUVID4", "B站登录 Cookie，可选。")
    dedeuserid = Field(str, "", "DedeUserID", "B站登录 Cookie，可选。")
    ac_time_value = Field(str, "", "ac_time_value", "B站登录 Cookie，可选。")

    def create_credential(self) -> Credential | None:
        cookie_names = (
            "sessdata",
            "bili_jct",
            "buvid3",
            "buvid4",
            "dedeuserid",
            "ac_time_value",
        )
        cookies = {}
        for name in cookie_names:
            value = self.get(name, "")
            if not isinstance(value, str):
                raise TypeError(f"B站 Cookie {name} 必须是字符串")
            value = value.strip()
            if value:
                cookies[name] = value

        return Credential(**cookies) if cookies else None
