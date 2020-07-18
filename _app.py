import random
from flask import Flask, request
from pymessenger.bot import Bot
import os
import json

app = Flask(__name__)
ACCESS_TOKEN = 'EAAKfV7i7OW0BALFC7wa9KCCZCUpGeJaPtBZAAyAMgAGUJFj4kp2tM7jSgnkjtIqTiH4KiSgPqcYLKBXMvAztBF5ZCVvUirFDiMjZBeNMWBTwZAdOG2ZBXbSXqMf2HL0usk7LR33VazpwV2Hk666SavnoFZBZBNY0IxurRoHI7R1N0QZDZD'
VERIFY_TOKEN = 'EAAKfV7i7OW0BALFC7wa9KCCZCUpGeJaPtBZAAyAMgAGUJFj4kp2tM7jSgnkjtIqTiH4KiSgPqcYLKBXMvAztBF5ZCVvUirFDiMjZBeNMWBTwZAdOG2ZBXbSXqMf2HL0usk7LR33VazpwV2Hk666SavnoFZBZBNY0IxurRoHI7R1N0QZDZD'
bot = Bot(ACCESS_TOKEN)
port = int(os.environ.get('PORT', 5000))

input_file = open('questions.json')
questions = json.load(input_file)

class players():
    def __init__(self, id):
        self.id = id
        self.score = 0
        self.first_to_game = 0
        self.question = 0
        self.question_answered_list = []
        self.current_question = 0
        self.correct = 0
        self.player_in_game = False
    def check_first_to_game(self):
        if self.first_to_game == 0:
            return True
        else :
            return False
    def return_question_number(self):
        self.question += 1
        return self.question

list_of_players = []

@app.route('/messengerbot', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get('hub.verify_token')
        return verify_fb_token(token_sent)
    else:
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        for player in list_of_players:
                            if recipient_id == player.id:
                                start_game(player, message['message'].get('text'))
                                return 'message processed'
                        if message['message'].get('text') == 'entroy':
                            list_of_players.append(players(recipient_id))
                            start_game(players(recipient_id), message['message'].get('text'))
                            return 'message processed'
    send_message(recipient_id, 'I am messenger bot')
    return 'message processed'

def check_answer(message):
    if message >= '1' and message <= '4':
        return True
    else:
        return False

def start_game(player, message):
    if message == 'entroy' and player.check_first_to_game() == False:
        send_message(player.id, 'do not input entroy while you are in game you mother fucker')
        return 'again'
    if player.check_first_to_game() == True:
        send_message(player.id, 'lets start the game')
        send_message(player.id, 'first i have to tell you something')
        send_message(player.id, 'there starts the game')
        player.first_to_game = 1
    if message != 'entroy':
        if check_answer(message) == False:
            send_message(player.id, 'please input 1 to 4')
            return 'again'
        if message != questions[player.current_question]['answer']:
            send_message(player.id, 'False')
        else:
            send_message(player.id, 'True')
            player.correct += 1
    if player.question == 5:
        send_message(player.id, 'you got {} answers right!!!'.format(player.correct)
        send_message(player.id, 'the game is end')
        list_of_players.remove(player)
        return 'success'
    send_message(player.id, 'question {} : '.format(player.return_question_number()))
    question_number = random.randint(0, 19)
    while question_number in player.question_answered_list:
        question_number = random.randint(0, 19)
    player.question_answered_list.append(question_number)
    send_message(player.id, questions[question_number]['question'])
    player.current_question = question_number
    return 'success'

def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return 'invalid verification token'

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return 'success'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)