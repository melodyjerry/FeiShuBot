# !/usr/bin/env python3
# coding:utf-8

# larkbot.py

import base64
import hashlib
import hmac
import json
import socket
import time
from datetime import datetime
import re
import subprocess
import requests

# ========================================================
# 机器人推送的参数配置
# ========================================================
WEBHOOK_CONFIG = {
    # 机器人推送路径
    "WEBHOOK_URL": "your-webhook-url",
    # 安全校验,需要在机器人=>安全设置=>签名校验 详见 https://getfeishu.cn/hc/zh-cn/articles/360024984973-%E5%9C%A8%E7%BE%A4%E8%81%8A%E4%B8%AD%E4%BD%BF%E7%94%A8%E6%9C%BA%E5%99%A8%E4%BA%BA
    "WEBHOOK_SECRET": "your-webhook-secret"
}

# ========================================================
# 消息主体的参数配置
# 全部json可前往 jsont.run 进行校验、压缩、格式化
# ========================================================
# 消息类型,可选:text(普通文本)、post(富文本)、interactive(消息卡片)等等
# 详见 https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/im-v1/message/create_json
msg_type = "interactive"

# ========================================================
# text普通文本的参数配置
# 详见 https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/im-v1/message/create_json#c9e08671
# ========================================================
content_text = "⌚时间进度条👻"

# ========================================================
# post富文本的参数配置
# 详见 https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/im-v1/message/create_json#45e0953e
# ========================================================
# 富文本的标题
content_post_title = "⌚时间进度条👻"
# 内容格式可选:text、a（at、image、media、emotion等在这代码里暂时不可用，原因未知）
content_post_line_1_1_tag = "text"
content_post_line_1_1_text = "第1行前半部分"
content_post_line_1_2_tag = "a"
content_post_line_1_2_text = "http://"
content_post_line_1_2_href = "后半部分是超链接"
content_post_line_2_1_tag = "text"
content_post_line_2_1_text = "第2行前半部分"
content_post_line_2_2_tag = "a"
content_post_line_2_2_text = "www."
content_post_line_2_2_href = "后半部分是超链接"
content_post_line_3_1_tag = "text"
content_post_line_3_1_text = "第3行前半部分"
content_post_line_3_2_tag = "a"
content_post_line_3_2_text = "feishu."
content_post_line_3_2_href = "后半部分是超链接"
content_post_line_4_1_tag = "text"
content_post_line_4_1_text = "第4行前半部分"
content_post_line_4_2_tag = "a"
content_post_line_4_2_text = "cn"
content_post_line_4_2_href = "后半部分是超链接"
# 可根据需要增删内容，对应的set_content_post()方法也需要进行修改

# ========================================================
# interactive消息卡片的参数配置
# 详见 https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SM2ATN
# 温馨提示：消息卡片的开发是更加复杂的，因为形式多样，json写起来也容易出错
#       故在这不在进行多参数配置
#       只对 card 的结构字段进行配置
#       可将消息卡片搭建工具中生成的代码，压缩后，粘贴在此
#
# 飞书消息卡片搭建工具：https://open.feishu.cn/tool/cardbuilder?from=cotentmodule
# json可前往 jsont.run 进行校验、压缩、格式化
#
# 完整的参考json：{"msg_type":"interactive","card":{"header":{"template":"blue","title":{"content":"这是标题","tag":"plain_text"}},"elements":[{"tag":"div","text":{"content":"**快速进入求助通道、快速查询救援电话、医疗信息、危险路段，关注灾情进展，获取自救指南**\n把这份资料转给有需要的人，河南加油，我们同在！","tag":"lark_md"}},{"tag":"hr"},{"tag":"div","text":{"content":"点击下方文字直接进入相关信息页\n🔺 [救援电话与紧急救助](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#SIQuxo)\n🔺 [医疗信息](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#9dwe7G)\n🔺 [危险路段](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#dTMAfK)\n🔺 [紧急避险](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#au2CLp)\n🔺 [自救指南](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#PpihPw)\n🔺 [持续进展](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#kcVAoi)\n🔺 [红十字捐款通道](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#UP5HvB)","tag":"lark_md"}},{"tag":"hr"},{"actions":[{"tag":"button","text":{"content":"查看全文","tag":"plain_text"},"type":"primary","url":"https://open.feishu.cn/"}],"tag":"action"}]}}
# card 结构字段主要是 config 与 header 和 elements 三个部分
# ========================================================
# 卡片基础参数配置, 详见 https://open.feishu.cn/document/ukTMukTMukTM/uAjNwUjLwYDM14CM2ATN
# 是否允许卡片被转发(默认 true)
# 转发后，卡片上的“回传交互”组件将自动置为禁用态。用户不能在转发后的卡片操作提交数据
# card_config_enable_forward = "true"
# 是否为共享卡片(默认为false)
# true：是共享卡片，更新卡片的内容对所有收到这张卡片的人员可见。
# false：是独享卡片，即仅操作用户可见卡片的更新内容。
# card_config_update_multi = "false"

# 卡片标题文案内容
card_header_title = "⌚时间进度条👻"
# 卡片标题的主题色,详见 https://open.feishu.cn/document/ukTMukTMukTM/ukTNwUjL5UDM14SO1ATN
# 可选: blue、wathet、turquoise、green、yellow、orange、red、carmine、violet、purple、indigo、grey
card_header_template = "wathet"

# 除了标题相关的放在 header 外，其他都在 elements 里
# 将相应节点的代码(可选压缩)粘贴到对应位置
# json可前往 jsont.run 进行校验、压缩、格式化
# elements参考json：[{"tag":"div","text":{"content":"**快速进入求助通道、快速查询救援电话、医疗信息、危险路段，关注灾情进展，获取自救指南**\n把这份资料转给有需要的人，河南加油，我们同在！","tag":"lark_md"}},{"tag":"hr"},{"tag":"div","text":{"content":"点击下方文字直接进入相关信息页\n🔺 [救援电话与紧急救助](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#SIQuxo)\n🔺 [医疗信息](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#9dwe7G)\n🔺 [危险路段](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#dTMAfK)\n🔺 [紧急避险](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#au2CLp)\n🔺 [自救指南](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#PpihPw)\n🔺 [持续进展](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#kcVAoi)\n🔺 [红十字捐款通道](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#UP5HvB)","tag":"lark_md"}},{"tag":"hr"},{"actions":[{"tag":"button","text":{"content":"查看全文","tag":"plain_text"},"type":"primary","url":"https://open.feishu.cn/"}],"tag":"action"}]
# card_elements = [{"tag":"div","text":{"content":"**快速进入求助通道、快速查询救援电话、医疗信息、危险路段，关注灾情进展，获取自救指南**\n把这份资料转给有需要的人，河南加油，我们同在！","tag":"lark_md"}},{"tag":"hr"},{"tag":"div","text":{"content":"点击下方文字直接进入相关信息页\n🔺 [救援电话与紧急救助](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#SIQuxo)\n🔺 [医疗信息](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#9dwe7G)\n🔺 [危险路段](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#dTMAfK)\n🔺 [紧急避险](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#au2CLp)\n🔺 [自救指南](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#PpihPw)\n🔺 [持续进展](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#kcVAoi)\n🔺 [红十字捐款通道](https://bytedance.feishu.cn/docs/doccnPjehU7ixPV61zR05TYiC5P#UP5HvB)","tag":"lark_md"}},{"tag":"hr"},{"actions":[{"tag":"button","text":{"content":"查看全文","tag":"plain_text"},"type":"primary","url":"https://open.feishu.cn/"}],"tag":"action"}]
card_elements = [{"tag":"div","text":{"content":"**Joy 小姐姐精心推出了 3 场活动，赶快选择你心水的报名吧！**","tag":"lark_md"}},{"tag":"hr"},{"extra":{"tag":"button","text":{"content":"🙋 立即报名","tag":"plain_text"},"type":"primary","url":"https://open.feishu.cn"},"tag":"div","text":{"content":"**HR 服务 | 4月亲子家庭日互动活动** \n📍 地点：13号楼1楼大厅\n🕙 时间：4月15日 10:00-12:00","tag":"lark_md"}},{"tag":"hr"},{"extra":{"tag":"button","text":{"content":"🙋 立即报名","tag":"plain_text"},"type":"primary","url":"https://open.feishu.cn"},"tag":"div","text":{"content":"**JOY 活动 | 不负春光在一起交友大会** \n📍 地点：13号楼1楼大厅\n🕑 时间：4月17日 14:00-18:00","tag":"lark_md"}},{"tag":"hr"},{"extra":{"tag":"button","text":{"content":"🙋 立即报名","tag":"plain_text"},"type":"primary","url":"https://open.feishu.cn"},"tag":"div","text":{"content":"**志愿服务 |个人孤岛 · 连接世界活动现场志愿者** \n📍 地点：江心屿博览中心 \n🕖 时间：4月18日 8:00-18:00","tag":"lark_md"}}]

# ========================================================
# 群机器人推送服务封装
# ========================================================
class FsBot:
    def __init__(self,webhook_url: str, webhook_secret: str) -> None:
        if not webhook_url:
            raise ValueError("WEBHOOK_URL异常")
        if not webhook_secret:
            raise ValueError("WEBHOOK_SECRET密钥异常")
        self.webhook_url = webhook_url
        # print(webhook_url)
        # print(webhook_secret)
        self.webhook_secret = webhook_secret
        self.get_host()

    # ========================================================
    # 安全密钥签名校验
    # 1.将当前时间戳和签名校验码通过换行符\n拼接在一起作为密钥字符串签名
    # 2.使用HMAC-SHA256算法,对该字符串签名进行加密
    # 3.使用Base64编码对加密后的字符串签名进行编码，便于作为参数传递
    # ========================================================
    def gen_sign(self) -> str:
        """
        # print(str(round(time.time())))
        # print(int(datetime.now().timestamp()))
        timestamp = int(datetime.now().timestamp())

        # str_to_sign = '{}\n{}'.format(timestamp, self.webhook_secret)
        # hmac_code = hmac.new(
        #     str_to_sign.encode("utf-8"), digestmod=hashlib.sha256
        # ).digest()
        # sign = base64.b64encode(hmac_code).decode('utf-8')

        key = f'{timestamp}\n{self.webhook_secret}'
        key_enc = key.encode('utf-8')
        msg = ""
        msg_enc = msg.encode('utf-8')
        hmac_code = hmac.new(key_enc, msg_enc, digestmod=hashlib.sha256).digest()
        sign = base64.b64encode(hmac_code).decode('utf-8')

        # print(timestamp)
        # print(sign)
        """

        # 拼接timestamp和secret
        timestamp = str(round(time.time()))
        string_to_sign = '{}\n{}'.format(timestamp, self.webhook_secret)
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
        # 对结果进行base64处理
        sign = base64.b64encode(hmac_code).decode('utf-8')
        # print("timestamp=", timestamp)
        # print("sign=", sign)

        return sign

    # ========================================================
    # 根据不同的msg_type来填充内容
    # ========================================================
    """
    普通文本的内容主体填充
    """
    def set_content_text(self, content_text):
        params = {
            "sign": self.gen_sign(),  # 安全密钥签名校验
            "msg_type": "text",
            "content": {
                "text": content_text
            }
        }
        return params

    """
    富文本的内容主体填充
    """
    def set_content_post(self):
        params = {
            "sign": self.gen_sign(), # 安全密钥签名校验
            "msg_type": "post",
            "content": {
                "post": {
                    "zh-CN": {
                        "title": content_post_title,
                        "content": [
                            [
                                {
                                    "tag": content_post_line_1_1_tag,
                                    "text": content_post_line_1_1_text
                                },
                                {
                                    "tag": content_post_line_1_2_tag,
                                    "text": content_post_line_1_2_text,
                                    "href": content_post_line_1_2_href
                                }
                            ],
                            [
                                {
                                    "tag": content_post_line_2_1_tag,
                                    "text": content_post_line_2_1_text
                                },
                                {
                                    "tag": content_post_line_2_2_tag,
                                    "text": content_post_line_2_2_text
                                }
                            ],
                            [
                                {
                                    "tag": content_post_line_3_1_tag,
                                    "text": content_post_line_3_1_text
                                },
                                {
                                    "tag": content_post_line_3_2_tag,
                                    "text": content_post_line_3_2_text
                                }
                            ],
                            [
                                {
                                    "tag": content_post_line_4_1_tag,
                                    "text": content_post_line_4_1_text
                                },
                                {
                                    "tag": content_post_line_4_2_tag,
                                    "text": content_post_line_4_2_text,
                                    "a": content_post_line_4_2_href
                                }
                            ]
                        ]
                    }
                }
            }
        }
        return params

    """
    消息卡片的内容主体填充
    """
    def set_content_interactivet(self):
        params = {
            "sign": self.gen_sign(), # 安全密钥签名校验
            "msg_type": "interactive",
            "card": {
                # "config": {
                #     "enable_forward": card_config_enable_forward,
                #     "update_multi": card_config_update_multi
                # },
                "header": {
                    "template": card_header_template,
                    "title": {
                        "content": card_header_title,
                        "tag": "plain_text"
                    }
                },
                "elements": card_elements
            }
        }
        return params

    # ========================================================
    # 判断msg_type,根据不同的msg_type来填充内容
    # ========================================================
    def set_content(self, msg_type: str):
        if msg_type == "text":
            return self.set_content_text(content_text)
        elif msg_type == "post":
            return self.set_content_post()
        elif msg_type == "interactive":
            return self.set_content_interactivet()
        else:
            raise ValueError("msg_type异常,请检查~\n")

    # ========================================================
    # 发送的入口，需要传入content
    # ========================================================
    """
    通用的 推送方法
    """
    def send(self) -> None:
        if not self.webhook_url:
            # print("飞书 服务的 FSKEY 未设置!!\n取消推送")
            return
        # print("飞书 服务启动")

        params = self.set_content(msg_type)
        resp = requests.post(url=self.webhook_url, json=params)
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") and result["code"] != 0:
            # print("飞书 推送失败！错误信息如下：\n" + result["msg"])
            return
        # print("飞书 推送成功！")

    """
    普通文本 的推送方法
    为了简化其他模块使用
    """
    def send_text(self, title: str, content: str) -> None:
        if not self.webhook_url:
            # print("飞书 服务的 FSKEY 未设置!!\n取消推送")
            return
        # print("飞书 服务启动")

        # content_text = f"{title}\n\n{content}"
        # self.set_content_text(content_text)
        # params = self.set_content_text(content_text)
        # params = self.set_content("text")
        params = {"msg_type": "text", "content": {"text": f"{title}\n\n{content}"}}

        response = requests.post(url=self.webhook_url, json=params) # [0]是为了避免因为url返回的是元组，而报错raise InvalidSchema(f"No connection adapters were found for {url!r}")
        response.raise_for_status()
        result = response.json()
        if result.get("code") and result["code"] != 0:
            # print("飞书 推送失败！错误信息如下：\n" + str(result)) # 可只打输出错误信息result["msg"]
            return
        # print("飞书 推送成功！")

    # ========================================================
    # 获取ip地址、主机名称
    # ========================================================
    def get_host(self):
        # 利用正则表达式获取 IP 字符串
        # IPV4_PATTERN = r"IPv4.*: (?P.*)\n"
        # ipconfig = subprocess.run(
        #   "ipconfig", capture_output=True, text=True).stdout
        # ip = re.search(IPV4_PATTERN, ipconfig).group("ip")

        # 获取主机名
        host_name = socket.gethostname()
        # 获取IP地址
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        # host_name = FsBot.get_host()[0]
        # ip = FsBot.get_host()[1]
        # print(f"当前工位电脑的主机名是:{host_name}, IP是:{ip}\n")
        return host_name,ip

def main():
    bot = FsBot(webhook_url=WEBHOOK_CONFIG.get("WEBHOOK_URL"),webhook_secret=WEBHOOK_CONFIG.get("WEBHOOK_SECRET"))
    bot.send()

if __name__ == '__main__':
    main()

# todo: 安全密钥签名校验gen_sign()方法有问题，会报sign match fail or timestamp is not within one hour from current time
# todo: 更新详细的requirements.txt，删除不必要的依赖