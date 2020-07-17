import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAAKfV7i7OW0BACHkqLElpSJu2tXZBKmdzpJgYxULZAUmZCFrQlUHyOgVo9ifif9ODFVP2ZBP7Cq9XV9cNWN9FoVmGSP1eQC8yF1KVNEHqZBJDZAk2G1Hb3P38ZBtKl6GTrtGao8FXyW9yqHZA0phVWyY7NE2KVGM7ZCf3Y67WVGbhZCQZDZD'
VERIFY_TOKEN = 'EAAKfV7i7OW0BACHkqLElpSJu2tXZBKmdzpJgYxULZAUmZCFrQlUHyOgVo9ifif9ODFVP2ZBP7Cq9XV9cNWN9FoVmGSP1eQC8yF1KVNEHqZBJDZAk2G1Hb3P38ZBtKl6GTrtGao8FXyW9yqHZA0phVWyY7NE2KVGM7ZCf3Y67WVGbhZCQZDZD'
bot = Bot(ACCESS_TOKEN)

class players():
    def __init__(self, id):
        self.id = id
        self.score = 0
        self.first_to_game = 0
        self.question = 0
        self.question_answered_list = []
        self.current_question = 0
        self.correct = 0
    def return_player_id(self):
        return self.id
    def check_first_to_game(self):
        if self.first_to_game == 0:
            self.first_to_game = 1
            return True
        else :
            return False
    def return_question_number(self):
        self.question += 1
        return self.question
    def check_current_question_number(self):
        return self.current_question
    def change_current_question_number(self, question_number):
        self.current_question = question_number
    def change_correct(self):
        self.correct += 1
    def return_correct(self):
        return self.correct

class questions():
    def __init__(self):
        self.question_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        self.answer_list = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
    def return_answer(self, question_number):
        return self.answer_list[question_number]

list_of_players = []
list_of_questions = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    if message['message'].get('text') == 'entroy':
                        # start_game(players(recipient_id), message['message'].get('text'))
                        list_of_players.append(players(recipient_id))
                    # if player in list 
                    for player in list_of_players:
                        if recipient_id == player.return_player_id():
                            send_message(player.id, 'in list')
                            start_game(player, message['message'].get('text'))
                            return "Message Processed"
                    response_sent_text = get_message()
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

def check_answer(message):
    if message >= '1' and message <= '4':
        return True
    else:
        return False

def start_game(player, message):
    if player.check_first_to_game() == True:
        send_message(player.id, 'lets start the game')
        send_message(player.id, 'first i have to tell you some information')
        send_message(player.id, 'there starts the game')
    if message != 'entroy':
        if check_answer(message) is False:
            send_message(player.id, 'please input the numbers!!!')
            return 'success'
        if message != questions().return_answer(player.check_current_question_number()):
            send_message(player.id, 'False')
        else :
            send_message(player.id, 'True')
            player.change_correct()
    if player.question is 5:
        send_message(player.id, 'you got {} answers right!!!'.format(player.return_correct()))
        send_message(player.id, 'the game is end')
        list_of_players.remove(player)
        return 'success'
    send_message(player.id, 'question {} : '.format(player.return_question_number()))
    question_number = random.randint(0, 19)
    while question_number in player.question_answered_list:
        question_number = random.randint(0, 19)
    player.question_answered_list.append(question_number)
    print(question_number)
    send_message(player.id, questions().question_list[question_number])
    player.change_current_question_number(question_number)
    return 'success'

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

#chooses a random message to send to the user
def get_message():
    # sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return 'I am messenger bot'

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()