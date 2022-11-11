
from telegram import ReplyKeyboardRemove
from info import token
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)


fld = list(range(1, 10))
x = chr(128124)
o = chr(128520)
count = 9
player = x
CHOICE = 0

def show_field(field):
    txt = ''
    for i in range(len(field)):
        if not i % 3:
            txt += f'\n{"-" * 25}\n'
        txt += f'{field[i]:^8}'
    txt += f"\n{'-' * 25}"
    return txt


def check_win(field):
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    n = [field[x[0]] for x in win_coord if field[x[0]] == field[x[1]] == field[x[2]]]
    return n[0] if n else n


def start(update, _):
    global fld, player, count
    fld = list(range(1, 10))
    count = 9
    player = x
    update.message.reply_text(f"Hi, this is a fight between Good {chr(128124)} and Evil {chr(128520)}\n\n" 
        "Press /cancel to exit")
    update.message.reply_text(show_field(fld))
    update.message.reply_text(f"Go first {chr(128124)}")
    return CHOICE


def choice(update, _):
    global player, count
    move = update.message.text
    if move == '/cancel':
        cancel(update, _)
    elif move == '/start':
        start(update, _)
    elif not move.isdigit():
        update.message.reply_text(f"Incorrect input{chr(9940)}\nEnter a number!") 
    else:
        move = int(move)
        if move not in fld:
            update.message.reply_text(f"Incorrect input{chr(9940)}\nTry again")
        else:
            fld.insert(fld.index(move), player)
            fld.remove(move)
            update.message.reply_text(show_field(fld))
            if check_win(fld):
                if player == x:
                    update.message.reply_text(f"{player} - GOOD HAS THRIUMPHED! {chr(127881)}{chr(128588)}")
                else:
                    update.message.reply_text(f"{player} - EVIL HAS WON, THE WORLD MUST BE SAVED! {chr(128562)}{chr(127384)}")
                return ConversationHandler.END
            player = o if player == x else x
            count -= 1

    if count == 0:
        update.message.reply_text(f"Good and Evil are in balance now {chr(9775)}{chr(128591)}")
        return ConversationHandler.END

    

def cancel(update, _):
    update.message.reply_text(
        f"Bye! We'll save the world next time {chr(128075)}", 
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

if __name__ == '__main__':
    updater = Updater(token)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOICE: [MessageHandler(Filters.text, choice)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    print('server start')

    updater.start_polling()
    updater.idle()