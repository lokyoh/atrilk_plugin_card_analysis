# atrilk_plugin_card_analysis

ATRI-LK 插件:解析QQ小程序卡片。

### 功能:
  - 解析B站小程序视频
  - 解析B站链接

### 配置B站登录

在 ATRI-LK 的插件设置中打开“小程序解析”，填写自己账号的 B站 Cookie：

- `SESSDATA`：登录请求建议填写。
- `BILI_JCT`、`BUVID3`、`BUVID4`、`DedeUserID`、`ac_time_value`：可选，按浏览器 Cookie 中的同名值填写。

Cookie 可在已登录 B站的浏览器开发者工具的站点存储中查看。请仅使用自己的 Cookie，并妥善保管；不要提交配置文件或把 Cookie 发给他人。所有字段留空时，插件仍会以未登录方式请求。
