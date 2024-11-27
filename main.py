from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
from pkg.platform.types import *
import re
from plugins.AIDrawing.get_image import download_image


# 注册插件
@register(name="AIDrawing", description="使用function calling函数实现AI画图的功能，并自带图像发送", version="0.1", author="Hanschase")
class Fct(BasePlugin):
    def __init__(self, host: APIHost):
        pass

    @llm_func(name="Drawer")
    async def _(self,query, keywords: str)->str:
        """Call this function to draw something before you answer any questions.
        - Expand the user's description into a more elaborate and detailed English prompt suitable for AI image generation, including adding details like camera aperture and specific scene descriptions, and then input the enhanced description.
        - You will be will become reticent.
        - Use the English keywords.
        - Try to use short keywords as much as possible

        Args:
            keywords: The enhanced description.

        Returns:
            img: The generated image.
        """
        self.ap.logger.info(f"优化后关键词,{keywords}")
        img = "https://image.pollinations.ai/prompt/" + keywords
        return img

    #发送图片
    @handler(NormalMessageResponded)
    async def convert_message(self, ctx: EventContext):
        message = ctx.event.response_text
        image_pattern = re.compile(r'(https://image[^\s)]+)')
        #如果匹配到了image_pattern
        if image_pattern.search(message):
            url = image_pattern.search(message).group(1)
            try:
                #去除url末尾的句号或者括号
                if url.endswith('.') or url.endswith(')'):
                    url = url[:-1]
                self.ap.logger.info(f"正在发送图片图片...{url}")
                ctx.add_return('reply', MessageChain([Image(url=url)]))
            except Exception as e:
                await ctx.send_message(ctx.event.launcher_type, str(ctx.event.launcher_id),MessageChain([f"发生了一个错误：{e}"]))
        else:
            return ctx.add_return('reply', message)

    def __del__(self):
        pass
