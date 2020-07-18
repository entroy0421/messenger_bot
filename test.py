import json

input_file = open('questions.json')
questions = json.load(input_file)

print(questions[0]['question'])