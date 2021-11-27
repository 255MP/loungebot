from discord.ext import commands


class LoungeBot(commands.Bot):
    async def process_commands(self, message):
        """|coro|

        This function processes the commands that have been registered
        to the bot and other groups. Without this coroutine, none of the
        commands will be triggered.

        By default, this coroutine is called inside the :func:`.on_message`
        event. If you choose to override the :func:`.on_message` event, then
        you should invoke this coroutine as well.

        This is built using other low level tools, and is equivalent to a
        call to :meth:`~.Bot.get_context` followed by a call to :meth:`~.Bot.invoke`.

        Parameters
        -----------
        message: :class:`discord.Message`
            The message to process commands for.
        """
        ctx = await self.get_context(message)
        await self.invoke(ctx)
