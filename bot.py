from discord.ext import commands
import discord
import datetime
import sys
import config
import aiohttp
import asyncio
#import asyncpg
import logging  # logging
import logging.handlers
import traceback


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    if bot.user.id == config.dev_bot_id:
        prefixes = ['??']
    else:
        prefixes = ['?']
    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


def set_logger():
    global logger
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(
        filename='discord.log', encoding='utf-8', mode='a')
    handler.setFormatter(logging.Formatter(
        '\n%(asctime)s %(levelname)s Discord: %(funcName)s (Line %(lineno)d): '
        '%(message)s',
        datefmt="[%d.%m.%Y %H:%M]"))
    logger.addHandler(handler)

    logger = logging.getLogger("bot")
    logger.setLevel(logging.INFO)

    format = logging.Formatter(
        '%(asctime)s %(levelname)s Code: %(funcName)s (Line %(lineno)d): '
        '%(message)s',
        datefmt="[%d.%m.%Y %H:%M]")

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(format)
    stdout_handler.setLevel(logging.INFO)

    fhandler = logging.handlers.RotatingFileHandler(
        filename='bot.log', encoding='utf-8', mode='a',
        maxBytes=10**7, backupCount=5)
    fhandler.setFormatter(format)
    logger.addHandler(fhandler)
    logger.addHandler(stdout_handler)


bot = commands.Bot(command_prefix=get_prefix, help_command=commands.DefaultHelpCommand(dm_help=True))
session = aiohttp.ClientSession(loop=bot.loop)

game = discord.Game("Pythonized!")

initial_extensions = (
    'commands.meta',
    'commands.watch',
    'commands.dice',
    'commands.rps',
)


@bot.event
async def on_ready():
    global logger
    logger.info('Discord ready. Loading extensions...')
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            logger.info("loaded {}".format(extension))
        except Exception as e:
            logger.exception('Failed to load extension {}\n{}: {}'.format(
                extension, type(e).__name__, e))
    if not hasattr(bot, "uptime"):
        bot.uptime = datetime.datetime.utcnow()
    users = len(set(bot.get_all_members()))
    guilds = len(bot.guilds)
    channels = len([c for c in bot.get_all_channels()])

    await bot.change_presence(status=discord.Status.online, activity=game)
    logger.info('Logged in as {}'.format(str(bot.user)))
    logger.info("Connected to:")
    logger.info("{} servers".format(guilds))
    logger.info("{} channels".format(channels))
    logger.info("{} users\n".format(users))


async def main():
    set_logger()
    try:
        logger.info('Logging in...')
        await bot.login(config.dev_token)
        logger.info('Logged in')
        logger.info('Connecting to gateway...')
        await bot.connect()
        logger.info('Connected to gateway')
    except TypeError as e:
        logger.warning(e)
        msg = ("\nYou are using an outdated discord.py.\n"
               "update your discord.py with by running this in your cmd "
               "prompt/terminal.\npip3 install --upgrade git+https://github.com/Rapptz/discord.py@rewrite")
        sys.exit(msg)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except discord.LoginFailure:
        logger.error(traceback.format_exc())
    except KeyboardInterrupt:
        loop.run_until_complete(bot.logout())
    except:
        logger.error(traceback.format_exc())
        loop.run_until_complete(bot.logout())
    finally:
        logger.info("Shutdown")
        loop.close()
