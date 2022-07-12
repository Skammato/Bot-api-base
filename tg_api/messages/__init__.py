from typing import Optional

class Messages:
    async def sendMessage(self, *args, **kwargs):
        default = ["chat_id", "text", "parse_mode", "entities", "disable_web_page_preview", "disable_notification", "reply_to_message_id", "reply_markup"]
        params = await self.build(default, *args, **kwargs)
        return (await self.send("sendMessage", params, "Message"))
    async def sendPhoto(self, *args, **kwargs):
        default = ["chat_id", "photo", "caption", "parse_mode", "caption_entities", "disable_web_page_preview", "disable_notification", "reply_to_message_id", "reply_markup"]
        params = await self.build(default, *args, **kwargs)
        return (await self.send("sendPhoto", params, "Message"))

class message_buonds:
    def __init__(self, msg):
        self.msg = msg
    async def reply_text(self, *args, **kwargs):
        if "reply" in list(kwargs):
            if kwargs["reply"]:
                kwargs["reply_to_message_id"] = self.msg.message_id
            del kwargs["reply"]
        return (await self.msg.client.sendMessage(self.msg.chat.id, *args, **kwargs))
    async def download(self, *args, **kwargs):
        if self.msg.photo:
            file_id = self.msg.photo[0]['file_id']
        elif self.msg.video:
            file_id = self.msg.video.file_id
        elif self.msg.audio:
            file_id = self.msg.audio.file_id
        elif self.msg.voice:
            file_id = self.msg.voice.file_id
        if file_id:
            return (await self.msg.client.download_media(file_id, *args, **kwargs))
        else:
            raise Exception("[400] Message doesn't have any media")
