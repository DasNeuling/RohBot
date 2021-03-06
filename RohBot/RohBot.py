import telegram
import time

from BotConnector import BotConnector
from intents.IntentDelegator import IntentDelegator

global delegator


def lookupLastMessage(bot):
    global lastOffset
    updates = []
    try:
        updates = bot.getUpdates(offset=lastOffset + 1, timeout=3)
    except telegram.error.TimedOut as e:
        print e
    if len(updates) == 0:
        return
    lastMessage = updates[-1]
    chat_id = lastMessage.message.chat_id

    if lastMessage.message.text == None:
        return

    lastText = lastMessage.message.text.encode('utf-8')
    lastOffset = lastMessage.update_id

    print("Received message from {} with id {} and text \"{}\"".format(lastMessage.message.chat.first_name,
                                                                       lastMessage.update_id, lastText))

    # bot.send_message(chat_id, "You wrote: " + lastText)

    delegator.handleRequest(chat_id, lastText)


if __name__ == "__main__":
    lastOffset = 0
    bot = BotConnector.getInstance()
    delegator = IntentDelegator()

    while True:
        try:
            lookupLastMessage(bot)
        except (UnicodeEncodeError, TypeError) as e:
            print(e)
        time.sleep(1)
