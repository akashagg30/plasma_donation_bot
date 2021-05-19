from django.db.models.query_utils import select_related_descend
from backend.settings import BOT_URL, TELEGRAM_TOKEN
import json
import os

import requests
from django.http import JsonResponse, response
from django.views import View
from .models import Users, Donner
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

class MainView(View):
    wrong_option = "please choose from the given options only, thanks"

    def post(self, request, *args, **kwargs):
        response = JsonResponse({"ok": "POST request processed"})
        
        t_data = json.loads(request.body)
        
        # if('callback_query' in t_data):
        #     self.handleCalander(t_data['callback_query'])
        #     return response

        t_message = t_data["message"]
        self.t_chat_id = t_message["chat"]["id"]
        self.t_user = t_message['from']


        try:
            self.t_text = t_message["text"].strip()
        except Exception as e:
            return response

        print('--------------------------------------------------------------------------------')
        # print("message : ", t_message)
        # print()
        print("text : ", self.t_text)
        print('--------------------------------------------------------------------------------')

        if(self.t_text == '/start'):
            self.isUserExists()
            self.user.state = 1
            self.user.save()
            self.start_message()
            return response

        else:
            if(not self.isUserExists()):
                self.start_message()
                return response
            
            self.state = self.user.state
            print(self.state)
            if((self.state==1 and self.t_text=='Donner') or (self.state < 21 and self.state!=1)):
                self.handleDonner()
            elif((self.state==1 and self.t_text=='Beneficiary')):
                self.handleBeneficiary()
            else:
                self.send_message("Server Error")

        return response




    def start_message(self):
        self.send_message("Hi! What are you?", {
            'keyboard' : [[{'text' : 'Donner'}], [{'text': 'Beneficiary'}]],
            'one_time_keyboard' : True
        } )

    def isUserExists(self):
        try:
            self.user = Users.objects.get(pk=self.t_user['id'])
            return True
        except:
            self.user = Users(id = self.t_user['id'], name = self.t_user['first_name'], user_name = self.t_user['username'])
            self.user.save()
            return False





    def handleDonner(self):
        def changeState(num):
            self.state = self.user.state = num
            self.user.save()
            self.handleDonner()

        def askGender():
            self.send_message("Please select gender", {
                'keyboard' : [[{'text' : 'Male'}], [{'text': 'Female'}], [{'text': 'Prefer not to say'}]],
                'one_time_keyboard' : True
            } )

        def handleGender():
            if(self.t_text == 'Male' or self.t_text == 'Prefer not to say'):
                changeState(6)
            elif(self.t_text == 'Female'):
                changeState(5)
            else:
                self.send_message(self.wrong_option)
                askGender()
        
        def checkPregnancy():
            self.send_message("Have you ever been pregnant?", {
                'keyboard' : [[{'text' : 'Yes'}], [{'text': 'No'}], [{'text': 'Prefer not to say'}]],
                'one_time_keyboard' : True
            } )

        def handlePregnancy():
            if(self.t_text == 'No' or self.t_text == 'Prefer not to say'):
                changeState(6)
            elif(self.t_text == 'Yes'):
                changeState(0)
            else:
                self.send_message(self.wrong_option)
                askGender()

        if(self.state == 1):
            changeState(4)

        elif(self.state == 4):
            if(self.t_text == 'Donner'):
                askGender()
            else:
                handleGender()

        elif(self.state == 5):
            if(self.t_text == 'Female'):
                checkPregnancy()
            else:
                handlePregnancy()

        # elif(self.state == 6):
        #     calendar, step = DetailedTelegramCalendar().build()
        #     self.send_message(f"Select {LSTEP[step]}", calendar)

        else :
            self.send_message("working on it")


    
    def handleBeneficiary(self):
        self.send_message("hi beneficiary")
    

    def handleCalander(self, c):
        import pprint
        pprint.PrettyPrinter(indent=4).pprint(c)
        print(c)
        result, key, step = DetailedTelegramCalendar().process(c['data'])
        if not result and key:
            self.edit_message_text(f"Select {LSTEP[step]}",
                                c['message']['chat']['id'],
                                c['message']['message_id'],
                                reply_markup=key)
        elif result:
            self.edit_message_text(f"You selected {result}",
                                c['message']['chat']['id'],
                                c['message']['message_id'])


    def edit_message_text(self, message, chat_id, message_id, reply_markup=''):
        data = {
            "chat_id": chat_id,
            "text": message,
            "message_id" : message_id,
            "parse_mode": "Markdown",
            'reply_markup': reply_markup
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            f"{BOT_URL}/sendMessage", data=json.dumps(data), headers=headers
        )

    def send_message(self, message, markup = ""):
        data = {
            "chat_id": self.t_chat_id,
            "text": message,
            "parse_mode": "Markdown",
            "reply_markup" : markup,
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            f"{BOT_URL}/sendMessage", data=json.dumps(data), headers=headers
        )
