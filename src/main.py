import os, random, datetime, config
from local import *
from aiogram import Bot, Dispatcher, executor, types
from mc import PhraseGenerator
from platform import system, release
from sys import version
from bs4 import BeautifulSoup
from requests import get
from loguru import logger


bot = Bot(token=config.token)
dp = Dispatcher(bot)

botver = '1.0'
bot_info = botvertitle + botver + platformtitle + system() + ' ' + release() + pythonvertitle + version

print(splash + botver + '\n')

logger.info('Initialization...')

def readff(file): # Read from file
    try:
        Ff = open(file, 'r', encoding='UTF-8')
        Contents = Ff.read()
        Ff.close()
        return Contents
    except:
        return None

path_to_base = 'Bases/botbase.txt'
path_to_log = 'Logs/log_' + str(datetime.datetime.now()).replace(' ', '_').replace(':', '-') + '.txt'

if not os.path.exists('Lists'):
    os.mkdir('Lists')

if not os.path.exists('Lists/blacklist.txt'):
    f = open('Lists/blacklist.txt', 'w', encoding='utf8')
    f.write('')
    f.close()

if not os.path.exists('Lists/whitelist.txt'):
    f = open('Lists/whitelist.txt', 'w', encoding='utf8')
    f.write('')
    f.close()

if not os.path.exists('Lists/botbasechats.txt'):
    f = open('Lists/botbasechats.txt', 'w', encoding='utf8')
    f.write('')
    f.close()

if not os.path.exists('Lists/disabledchats.txt'):
    f = open('Lists/disabledchats.txt', 'w', encoding='utf8')
    f.write('')
    f.close()

if not os.path.exists('Lists/logsdisabledchats.txt'):
    f = open('Lists/logsdisabledchats.txt', 'w', encoding='utf8')
    f.write('')
    f.close()

if not os.path.exists('Bases'):
    os.mkdir('Bases')

if not os.path.exists(path_to_base):
    f = open(path_to_base, 'w', encoding='utf8')
    f.write('Hello World!·')
    f.close()

if not os.path.exists('Logs'):
    os.mkdir('Logs')

if not os.path.exists(path_to_log):
    lf = open(path_to_log, 'w', encoding='utf8')
    lf.write('')
    lf.close()


botbasechatslist = open('Lists/botbasechats.txt', encoding='utf8').read().split('\n')
disabledchatslist = open('Lists/disabledchats.txt', encoding='utf8').read().split('\n')
logsdisabledchatslist = open('Lists/logsdisabledchats.txt', encoding='utf8').read().split('\n')

if config.blacklist == 1:
    blacklist = open('Lists/blacklist.txt', encoding='utf8').read().split('\n')
    whitelist = ['']
    notallowedmsg = blacklistedmsg
else:
    whitelist = open('Lists/whitelist.txt', encoding='utf8').read().split('\n')
    blacklist = ['']
    notallowedmsg = notwhitelistedmsg

newsbtnmenu = types.InlineKeyboardMarkup(row_width=1)
newsbtns = [types.InlineKeyboardButton(text=newsbtn1, url='https://t.me/' + config.newschannel), types.InlineKeyboardButton(text=newsbtn2, url='https://t.me/' + config.logschannel)]

newsbtnmenu.add(*newsbtns)

contactwithadminmenu = types.InlineKeyboardMarkup(row_width=1)
contactwithadminbtn = types.InlineKeyboardButton(text=contactwithadmintext, url='https://t.me/' + config.adminusername)
contactwithadminmenu.add(contactwithadminbtn)

exec(readff("dem.py"))

logger.success('Ready!')

@dp.message_handler(commands=['start', 'help'])
async def get_started(message: types.Message):
    logstr = message.from_user.first_name + ' (ID ' + str(message.from_user.id) + ') (Chat ID ' + str(message.chat.id) + '): ' + message.text 
    logger.info(logstr)
    with open(path_to_log, 'a', encoding='utf8') as lf:
        lf.write(logstr + '\n')
    if config.blacklist == 0 and str(message.chat.id) in whitelist and str(message.from_user.id) in whitelist or config.blacklist == 1 and str(message.chat.id) not in blacklist and str(message.from_user.id) not in blacklist:
        await message.reply(hellomsg)
    else:
        await message.reply(notallowedmsg, parse_mode='HTML', reply_markup=contactwithadminmenu)

@dp.message_handler(commands='basemode')
async def toggle_global_and_local_base(message: types.Message):
    logstr = message.from_user.first_name + ' (ID ' + str(message.from_user.id) + ') (Chat ID ' + str(message.chat.id) + '): ' + message.text 
    logger.info(logstr)
    if config.blacklist == 0 and str(message.chat.id) in whitelist and str(message.from_user.id) in whitelist or config.blacklist == 1 and str(message.chat.id) not in blacklist and str(message.from_user.id) not in blacklist:
        memberinfo = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if memberinfo.status != "member" or message.chat.id == message.from_user.id:
            if str(message.chat.id) in botbasechatslist:
                if not os.path.exists('Bases/' + str(message.chat.id) + '.txt'):
                    bf = open('Bases/' + str(message.chat.id) + '.txt', 'w', encoding='utf8')
                    bf.write('Hello World!·')
                botbasechatslist.remove(str(message.chat.id))
                bbclist = open('Lists/botbasechats.txt', 'w', encoding='utf8')
                for ids in botbasechatslist:
                    bbclist.write('%s\n' %ids)
                await message.reply(basemsg2, parse_mode='HTML')
            else:
                botbasechatslist.append(str(message.chat.id))
                bbclist = open('Lists/botbasechats.txt', 'w', encoding='utf8')
                for ids in botbasechatslist:
                    bbclist.write('%s\n' %ids)
                await message.reply(basemsg1, parse_mode='HTML')
        else:
            await message.reply(onlyadmin)
    else:
        await message.reply(notallowedmsg, parse_mode='HTML', reply_markup=contactwithadminmenu)



@dp.message_handler(commands='botonoff')
async def toggle_bot_for_chat(message: types.Message):
    logstr = message.from_user.first_name + ' (ID ' + str(message.from_user.id) + ') (Chat ID ' + str(message.chat.id) + '): ' + message.text
    logger.info(logstr)
    if config.blacklist == 0 and str(message.chat.id) in whitelist and str(message.from_user.id) in whitelist or config.blacklist == 1 and str(message.chat.id) not in blacklist and str(message.from_user.id) not in blacklist:
        memberinfo = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if memberinfo.status != "member" or message.chat.id == message.from_user.id:
            if str(message.chat.id) in disabledchatslist:
                disabledchatslist.remove(str(message.chat.id))
                dclist = open('Lists/disabledchats.txt', 'w', encoding='utf8')
                for ids in disabledchatslist:
                    dclist.write('%s\n' %ids)
                await message.reply(togglemsg2, parse_mode='HTML')
            else:
                disabledchatslist.append(str(message.chat.id))
                dclist = open('Lists/disabledchats.txt', 'w', encoding='utf8')
                for ids in disabledchatslist:
                    dclist.write('%s\n' %ids)
                await message.reply(togglemsg1, parse_mode='HTML')
        else:
            await message.reply(onlyadmin)
    else:
        await message.reply(notallowedmsg, parse_mode='HTML', reply_markup=contactwithadminmenu)

@dp.message_handler(commands='logsmode')
async def toggle_logs(message: types.Message):
    logstr = message.from_user.first_name + ' (ID ' + str(message.from_user.id) + ') (Chat ID ' + str(message.chat.id) + '): ' + message.text 
    logger.info(logstr)
    if config.blacklist == 0 and str(message.chat.id) in whitelist and str(message.from_user.id) in whitelist or config.blacklist == 1 and str(message.chat.id) not in blacklist and str(message.from_user.id) not in blacklist:
        memberinfo = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if memberinfo.status != "member" or message.chat.id == message.from_user.id:
            if str(message.chat.id) in logsdisabledchatslist:
                logsdisabledchatslist.remove(str(message.chat.id))
                ldclist = open('Lists/logsdisabledchats.txt', 'w', encoding='utf8')
                for ids in logsdisabledchatslist:
                    ldclist.write('%s\n' %ids)
                await message.reply(logstogglemsg2, parse_mode='HTML')
            else:
                logsdisabledchatslist.append(str(message.chat.id))
                ldclist = open('Lists/logsdisabledchats.txt', 'w', encoding='utf8')
                for ids in logsdisabledchatslist:
                    ldclist.write('%s\n' %ids)
                await message.reply(logstogglemsg1, parse_mode='HTML')
        else:
            await message.reply(onlyadmin)
    else:
        await message.reply(notallowedmsg, parse_mode='HTML', reply_markup=contactwithadminmenu)

@dp.message_handler(commands='info')
async def get_bot_info(message: types.Message):
    logstr = message.from_user.first_name + ' (ID ' + str(message.from_user.id) + ') (Chat ID ' + str(message.chat.id) + '): ' + message.text 
    logger.info(logstr)
    with open(path_to_log, 'a', encoding='utf8') as lf:
        lf.write(logstr + '\n')
    if config.blacklist == 0 and str(message.chat.id) in whitelist and str(message.from_user.id) in whitelist or config.blacklist == 1 and str(message.chat.id) not in blacklist and str(message.from_user.id) not in blacklist:
        await message.reply(bot_info)
    else:
        await message.reply(notallowedmsg, parse_mode='HTML', reply_markup=contactwithadminmenu)

@dp.message_handler(commands='stats')
async def get_statistics(message: types.Message):
    await message.reply(okaymsg)

@dp.message_handler(commands='getchatbase')
async def get_local_base(message: types.Message):
    logstr = message.from_user.first_name + ' (ID ' + str(message.from_user.id) + ') (Chat ID ' + str(message.chat.id) + '): ' + message.text
    logger.info(logstr)
    with open(path_to_log, 'a', encoding='utf8') as lf:
        lf.write(logstr + '\n')
    if config.blacklist == 0 and str(message.chat.id) in whitelist and str(message.from_user.id) in whitelist or config.blacklist == 1 and str(message.chat.id) not in blacklist and str(message.from_user.id) not in blacklist:
        try:
            basefile = open('Bases/' + str(message.chat.id) + '.txt', 'r', encoding='utf8')
            await message.reply_document(basefile, caption=baseinstdesc1)
            basefile.close()
        except:
            bf = open('Bases/' + str(message.chat.id) + '.txt', 'w', encoding='utf8')
            bf.write('Hello World!·')
            bf.close()
            basefile = open('Bases/' + str(message.chat.id) + '.txt', 'r', encoding='utf8')
            await message.reply_document(basefile, caption=baseinstdesc1)
            basefile.close()
    else:
        await message.reply(notallowedmsg, parse_mode='HTML', reply_markup=contactwithadminmenu)

@dp.message_handler(commands='getbotbase')
async def get_global_base(message: types.Message):
    logstr = message.from_user.first_name + ' (ID ' + str(message.from_user.id) + ') (Chat ID ' + str(message.chat.id) + '): ' + message.text
    logger.info(logstr)
    with open(path_to_log, 'a', encoding='utf8') as lf:
        lf.write(logstr + '\n')
    if config.blacklist == 0 and str(message.chat.id) in whitelist and str(message.from_user.id) in whitelist or config.blacklist == 1 and str(message.chat.id) not in blacklist and str(message.from_user.id) not in blacklist:
        basefile = open(path_to_base, 'r', encoding='utf8')
        await message.reply_document(basefile, caption=baseinstdesc2)
        basefile.close()
    else:
        await message.reply(notallowedmsg, parse_mode='HTML', reply_markup=contactwithadminmenu)

@dp.message_handler(commands=['getlogs', 'news'])
async def get_news(message: types.Message):
    logstr = message.from_user.first_name + ' (ID ' + str(message.from_user.id) + ') (Chat ID ' + str(message.chat.id) + '): ' + message.text
    logger.info(logstr)
    with open(path_to_log, 'a', encoding='utf8') as lf:
        lf.write(logstr + '\n')
    if config.blacklist == 0 and str(message.chat.id) in whitelist and str(message.from_user.id) in whitelist or config.blacklist == 1 and str(message.chat.id) not in blacklist and str(message.from_user.id) not in blacklist:
        await message.reply(newsmsg, reply_markup=newsbtnmenu)
    else:
        await message.reply(notallowedmsg, parse_mode='HTML', reply_markup=contactwithadminmenu)

@dp.message_handler(commands='ping')
async def bot_ping(message: types.Message):
    logstr = message.from_user.first_name + ' (ID ' + str(message.from_user.id) + ') (Chat ID ' + str(message.chat.id) + '): ' + message.text 
    logger.info(logstr)
    with open(path_to_log, 'a', encoding='utf8') as lf:
        lf.write(logstr + '\n')
    if config.blacklist == 0 and str(message.chat.id) in whitelist and str(message.from_user.id) in whitelist or config.blacklist == 1 and str(message.chat.id) not in blacklist and str(message.from_user.id) not in blacklist:
        logreqlog = message.from_user.first_name + ' (ID ' + str(message.from_user.id) + ') pinged the bot ' + '[' + str(datetime.datetime.now()) + ']'
        logger.info(logreqlog)
        with open(path_to_log, 'a', encoding='utf8') as lf:
            lf.write(logreqlog + '\n')
        await message.reply(pongmsg)
    else:
        await message.reply(notallowedmsg, parse_mode='HTML', reply_markup=contactwithadminmenu)

@dp.message_handler(commands='justsay')
async def just_say(message: types.Message):
    logstr = message.from_user.first_name + ' (ID ' + str(message.from_user.id) + ') (Chat ID ' + str(message.chat.id) + '): ' + message.text 
    logger.info(logstr)
    with open(path_to_log, 'a', encoding='utf8') as lf:
        lf.write(logstr + '\n')
    if config.blacklist == 0 and str(message.chat.id) in whitelist and str(message.from_user.id) in whitelist or config.blacklist == 1 and str(message.chat.id) not in blacklist and str(message.from_user.id) not in blacklist:
        if str(message.chat.id) in botbasechatslist:
            with open(path_to_base, encoding='utf8') as bfile:
                txt = bfile.read().split('·')
        else:
            if not os.path.exists('Bases/' + str(message.chat.id) + '.txt'):
                bf = open('Bases/' + str(message.chat.id) + '.txt', 'w', encoding='utf8')
                bf.write('Hello World!·')
            with open('Bases/' + str(message.chat.id) + '.txt', encoding='utf8') as bfile:
                txt = bfile.read().split('·')
        generatedtext = PhraseGenerator(samples=txt).generate_phrase()
        await message.reply(generatedtext)
        logstr = 'Bot just said: ' + generatedtext 
        logger.info(logstr)
        with open(path_to_log, 'a', encoding='utf8') as lf:
            lf.write(logstr + '\n')
            if str(message.chat.id) not in logsdisabledchatslist:
                await bot.send_message(config.logschannelid, ijustsaidtitle + generatedtext)
    else:
        await message.reply(notallowedmsg, parse_mode='HTML', reply_markup=contactwithadminmenu)

@dp.message_handler(commands='saymuch')
async def say_much(message: types.Message):
    logstr = message.from_user.first_name + ' (ID ' + str(message.from_user.id) + ') (Chat ID ' + str(message.chat.id) + '): ' + message.text 
    logger.info(logstr)
    with open(path_to_log, 'a', encoding='utf8') as lf:
        lf.write(logstr + '\n')
    if config.blacklist == 0 and str(message.chat.id) in whitelist and str(message.from_user.id) in whitelist or config.blacklist == 1 and str(message.chat.id) not in blacklist and str(message.from_user.id) not in blacklist:
        if str(message.chat.id) in botbasechatslist:
            with open(path_to_base, encoding='utf8') as bfile:
                txt = bfile.read().split('·')
        else:
            if not os.path.exists('Bases/' + str(message.chat.id) + '.txt'):
                bf = open('Bases/' + str(message.chat.id) + '.txt', 'w', encoding='utf8')
                bf.write('Hello World!·')
            with open('Bases/' + str(message.chat.id) + '.txt', encoding='utf8') as bfile:
                txt = bfile.read().split('·')
        generatedtext = ''
        for mgt in range(config.saymuchcycles):
            generatednowtext = PhraseGenerator(samples=txt).generate_phrase()
            generatedtext += ' ' + generatednowtext
        await message.reply(generatedtext)
        logstr = 'Bot said much: ' + generatedtext 
        logger.info(logstr)
        with open(path_to_log, 'a', encoding='utf8') as lf:
            lf.write(logstr + '\n')
        if str(message.chat.id) not in logsdisabledchatslist:
            await bot.send_message(config.logschannelid, isaidmuchtitle + generatedtext)
    else:
        await message.reply(notallowedmsg, parse_mode='HTML', reply_markup=contactwithadminmenu)


# Joke
@dp.message_handler(commands='stupidjoke')
async def get_joke(message: types.Message):
    logstr = message.from_user.first_name + ' (ID ' + str(message.from_user.id) + ') (Chat ID ' + str(message.chat.id) + '): ' + message.text 
    logger.info(logstr)
    with open(path_to_log, 'a', encoding='utf8') as lf:
        lf.write(logstr + '\n')
    if config.blacklist == 0 and str(message.chat.id) in whitelist and str(message.from_user.id) in whitelist or config.blacklist == 1 and str(message.chat.id) not in blacklist and str(message.from_user.id) not in blacklist:
        jokesresponse = get(config.jokesaddress)
        joke = BeautifulSoup(jokesresponse.text, 'lxml').find('blockquote').text
        await message.reply(joke)
        if str(message.chat.id) not in logsdisabledchatslist:
            await bot.send_message(config.logschannelid, ijustjokedtitle + joke)
    else:
        await message.reply(notallowedmsg, parse_mode='HTML', reply_markup=contactwithadminmenu)

# Bash
@dp.message_handler(commands='bash')
async def get_joke(message: types.Message):
    logstr = message.from_user.first_name + ' (ID ' + str(message.from_user.id) + ') (Chat ID ' + str(message.chat.id) + '): ' + message.text 
    logger.info(logstr)
    with open(path_to_log, 'a', encoding='utf8') as lf:
        lf.write(logstr + '\n')
    if config.blacklist == 0 and str(message.chat.id) in whitelist and str(message.from_user.id) in whitelist or config.blacklist == 1 and str(message.chat.id) not in blacklist and str(message.from_user.id) not in blacklist:
        quotesresponse = get(config.quotesaddress)
        quote = BeautifulSoup(quotesresponse.text, 'lxml').find('p', class_='qt')
        await message.reply(quote.text)
        if str(message.chat.id) not in logsdisabledchatslist:
            await bot.send_message(config.logschannelid, ijustbashedtitle + quote.text)
    else:
        await message.reply(notallowedmsg, parse_mode='HTML', reply_markup=contactwithadminmenu)


@dp.message_handler()
async def get_text_messages(message):
    myinfo = await bot.get_me()
    if config.blacklist == 0 and str(message.chat.id) in whitelist and str(message.from_user.id) in whitelist or config.blacklist == 1 and str(message.chat.id) not in blacklist and str(message.from_user.id) not in blacklist and str(message.chat.id) not in disabledchatslist:
        if '·' in message.text:
                logstr = message.from_user.first_name + ' was tried to spam a base.' 
                with open(path_to_log, 'a', encoding='utf8') as lf:
                    lf.write(logstr + '\n')
        if str(message.chat.id) in botbasechatslist:
            with open(path_to_base, 'a', encoding='utf8') as bfile:
                bfile.write((str(message.text).replace('·', '*')) + '·')
            with open(path_to_base, encoding='utf8') as file:
                txt = file.read().split('·')
        else:
            if not os.path.exists('Bases/' + str(message.chat.id) + '.txt'):
                bf = open('Bases/' + str(message.chat.id) + '.txt', 'w', encoding='utf8')
                bf.write('Hello World!·')
                bf.close()
            with open('Bases/' + str(message.chat.id) + '.txt', 'a', encoding='utf8') as bfile:
                bfile.write((str(message.text).replace('·', '*')) + '·')
            with open('Bases/' + str(message.chat.id) + '.txt', encoding='utf8') as file:
                txt = file.read().split('·')
        try:
            if len(txt) >= 2 and random.randint(config.minrandom, config.maxrandom) == config.randomresult or message.reply_to_message.from_user.id == myinfo.id:
                generatedtext = PhraseGenerator(samples=txt).generate_phrase()
                await message.reply(generatedtext)
                logstr = message.from_user.first_name + ' (ID ' + str(message.from_user.id) + ') (Chat ID ' + str(message.chat.id) + '): ' + message.text + ' | Bot answer: ' + generatedtext 
                logger.info(logstr)
                with open(path_to_log, 'a', encoding='utf8') as lf:
                    lf.write(logstr + '\n')
                if str(message.chat.id) not in logsdisabledchatslist:
                    await bot.send_message(config.logschannelid, usermsgtitle + message.text + '\n---\n\n' + botanswertitle + generatedtext + '\n---')
        except:
            pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
