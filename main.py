from datetime import datetime
import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from Event import *


class User:
    chatId :int
    events = []
    currentEvent : AbstractEvent


    def __init__(self, chatId: int):
        self.chatId = chatId

    def addEvent(self, event: AbstractEvent):
        self.events.append(event)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

MAIN, CREATEEVENT, EVENTTYPE, MEETING, EVENT, ENTERDATE, ENTERNAME, BIRTHDAY_PERSON, MEETING_PLACE, REMINDER_NOTE = range(10)

users = {}


def getUser(update: Update):
    chatId = update.message.chat_id
    
    if chatId not in users:
        user = User(chatId)
        users[chatId] = user
        return user
    else:
        return users[chatId]    
    

logger = logging.getLogger(__name__)



def start(update: Update, context: CallbackContext) -> int:    
    user = getUser(update)
    if len(user.events) != 0:
        printEvents(update)

    user.currentEvent = None
    
    update.message.reply_text('/create чтобы создать событие.', reply_markup=ReplyKeyboardRemove())
    return CREATEEVENT

def createEvent(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Выберите тип события:',
        reply_markup=ReplyKeyboardMarkup([['Birthday'], ['Meeting'], ['Reminder']], one_time_keyboard=True),)
    return EVENTTYPE

def eventType(update: Update, context: CallbackContext) -> int:   
    
    text = update.message.text
    user = getUser(update)

    if text == 'Birthday':
        user.currentEvent = Birthday()
        update.message.reply_text('Введите дату события в формате дд/мм/гггг ч:м \nПример: 01.09.1939 7:22 ')
        return ENTERDATE    

    else:       
        if text == 'Meeting':
            update.message.reply_text('Введите название события: ')
            user.currentEvent = Meeting()
            return ENTERDATE

        elif text == 'Reminder':
            update.message.reply_text('Введите название события: ')
            user.currentEvent = Reminder()
            return ENTERDATE

        else:
            update.message.reply_text('Выберите тип события:', reply_markup=ReplyKeyboardMarkup([['Birthday'], ['Meeting'], ['Reminder']], one_time_keyboard=True),)
            return EVENTTYPE
    return MAIN

def enterEventName(update: Update, context: CallbackContext) -> int:  
    
    user = getUser(update)
    user.currentEvent.name = update.message.text
    update.message.reply_text('Введите дату события в формате дд/мм/гггг ч:м \nПример: 01.09.1939 7:22 ') 
    
    return ENTERDATE

def enterDate(update: Update, context: CallbackContext) -> int:  
    
    try:
        out = datetime.datetime.strptime(update.message.text, "%d.%m.%Y %H:%M")
    except ValueError:
        update.message.reply_text('Введите дату события в формате дд/мм/гггг ч:м \nПример: 01.09.1939 7:22 ') 
        return ENTERDATE
    user = getUser(update)
    user.currentEvent.date = out

    if isinstance(user.currentEvent, Birthday):
        update.message.reply_text("Укажите имя именинние: ")
        return BIRTHDAY_PERSON

    elif isinstance(user.currentEvent, Meeting):
        update.message.reply_text("Укажите место встречи: ")
        return MEETING_PLACE

    elif isinstance(user.currentEvent, Reminder):
        update.message.reply_text("Примечание: ")
        return REMINDER_NOTE
    
    return MAIN
   
def enterBirthdayPerson(update: Update, context: CallbackContext) -> int:

    user = getUser(update)

    if isinstance(user.currentEvent, Birthday):
        user.currentEvent.person = update.message.text
        user.events.append(user.currentEvent)
        user.currentEvent = None
        printEvents(update)

    return MAIN

def enterMeetingPlace(update: Update, context: CallbackContext) -> int:

    user = getUser(update)

    if isinstance(user.currentEvent, Meeting):
        user.currentEvent.place = update.message.text
        user.events.append(user.currentEvent)
        user.currentEvent = None
        printEvents(update)

    return MAIN

def enterReminderNote(update: Update, context: CallbackContext) -> int:

    user = getUser(update)

    if isinstance(user.currentEvent, Reminder):
        user.currentEvent.note = update.message.text
        user.events.append(user.currentEvent)
        user.currentEvent = None
        printEvents(update)

    return MAIN

def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user    
    update.message.reply_text(
        'Действие отменено.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def printEvents(update: Update):

    user = getUser(update)

    if len(user.events) == 1:
        text = 'Текущее событие:\n\n'

    else:
        text = 'Текущие события:\n\n'

    separator = '\n\n'
    text += separator.join([x.display() for x in user.events])    
    update.message.reply_text(text)

def main() -> None:
    updater = Updater("1404194101:AAGksqvOXzhRAfTMu2l3koC6fbJv1hytT2o", use_context=True)
    dispatcher = updater.dispatcher
    mainCommands = [CommandHandler('start', start), CommandHandler('create', createEvent),MessageHandler(Filters.command('cancel'), cancel)]

    conv_handler = ConversationHandler(entry_points= mainCommands,
        states={
            MAIN: mainCommands, 
            CREATEEVENT: [CommandHandler('create', createEvent)],
            EVENTTYPE: [MessageHandler(Filters.text, eventType)],            
            #ENTERDATE: [MessageHandler(Filters.regex('(\d{1,2}\.\d{1,2}\.\d{4} \d{1,2}:\d{1,2})'), enterDate)],
            ENTERDATE: [MessageHandler(Filters.text, enterDate)],
            ENTERNAME: [MessageHandler(Filters.text, enterEventName)],
            BIRTHDAY_PERSON: [MessageHandler(Filters.text, enterBirthdayPerson)],
            MEETING_PLACE: [MessageHandler(Filters.text, enterMeetingPlace)],
            REMINDER_NOTE: [MessageHandler(Filters.text, enterReminderNote)],
        },
        fallbacks=[MessageHandler(Filters.command('cancel'), cancel)], 
        allow_reentry = True)

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()    


if __name__ == '__main__':
    main()
