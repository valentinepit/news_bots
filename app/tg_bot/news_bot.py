import requests
import telebot

bot_token = "5034223897:AAGj1NPq3LrSrng4kyUIuC1gQk_0OWDu1S4"
channel_id = "@warp_news"

bot = telebot.TeleBot(bot_token)


# @bot.message_handler(content_types=["text"])
# def commands(message):
#     bot.send_message(channel_id, message.text)


def telegram_bot_send_text(bot_message):
    url = "https://api.telegram.org/bot"
    send_text = url + bot_token + "/sendMessage?chat_id=" + channel_id + "&parse_mode=HTML&text=" + bot_message
    # send_text = url + bot_token + '/sendMessage?chat_id=' + channel_id + '&parse_mode=MarkdownV2&text=' + bot_message
    try:
        response = requests.get(send_text)
    except Exception as e:
        return e
    return response.json()


# bot.polling()
