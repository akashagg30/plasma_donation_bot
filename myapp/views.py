from collections import UserList
from backend.settings import BOT_URL, TELEGRAM_TOKEN
import json
import requests
from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from .models import Users, Donor, Beneficiary
from .utils import blood_groups, blood_group_match
import datetime

class MainView(View):
    wrong_option = "please choose from the given options only, thanks"
    beneficiaryState = 17

    def post(self, request, *args, **kwargs):
        response = JsonResponse({"ok": "POST request processed"})
        
        t_data = json.loads(request.body)

        # print(t_data)
        
        t_message = t_data["message"]
        self.t_chat_id = t_message["chat"]["id"]
        self.t_user = t_message['from']

        if('username' not in self.t_user):
            self.send_message('''please add your username and try again.
            thanks!''')
            return response

        try:
            if('text' in t_message):
                self.t_text = t_message["text"].strip()
            elif('location' in t_message):
                self.t_text = t_message['location']
            elif('contact' in t_message):
                self.t_text = t_message['contact']
            else:
                return response
        except Exception as e:
            return response

        print('--------------------------------------------------------------------------------')
        print("message : ", t_message)
        print()
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
            if((self.state==1 and self.t_text=='Donor') or (self.state < self.beneficiaryState and self.state!=1)):
                self.handleDonor()
            elif((self.state==1 and self.t_text=='Beneficiary') or (self.state >= self.beneficiaryState)):
                self.handleBeneficiary()
            else:
                self.send_message("Akash se pucho")

        return response




    def start_message(self):
        self.send_message("Hi! What are you?", {
            'keyboard' : [[{'text' : 'Donor'}], [{'text': 'Beneficiary'}]],
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





    def handleDonor(self):
        
        def changeState(num):
            self.state = self.user.state = num
            self.user.save()
            self.handleDonor()

        def askForAge():
            self.send_message("Are you between the age of 18 and 55?", {
                'keyboard' : [[{'text' : 'Yes'}], [{'text': 'No'}]],
                'one_time_keyboard' : True
            } )

        def handleAge():
            if(self.t_text == 'Yes'):
                changeState(self.state + 1)
            elif(self.t_text == 'No'):
                changeState(endState)
            else:
                askForAge()

        def askGender():
            self.send_message("Please select gender", {
                'keyboard' : [[{'text' : 'Male'}], [{'text': 'Female'}], [{'text': 'Prefer not to say'}]],
                'one_time_keyboard' : True
            } )

        def handleGender():
            if(self.t_text == 'Male' or self.t_text == 'Prefer not to say'):
                changeState(self.state + 2)
            elif(self.t_text == 'Female'):
                changeState(self.state + 1)
            else:
                if(self.t_text != 'Yes'):
                    self.send_message(self.wrong_option)
                askGender()
        
        def askPregnancy():
            self.send_message("Have you ever been pregnant?", {
                'keyboard' : [[{'text' : 'Yes'}], [{'text': 'No'}], [{'text': 'Prefer not to say'}]],
                'one_time_keyboard' : True
            } )

        def handlePregnancy():
            if(self.t_text == 'No' or self.t_text == 'Prefer not to say'):
                changeState(self.state + 1)
            elif(self.t_text == 'Yes'):
                changeState(endState)
            else:
                if(self.t_text != 'Female'):
                    self.send_message(self.wrong_option)
                askPregnancy()

        def askPtvDate():
            self.send_message("Please enter the date (in dd/mm/yy format) you tested corona positive")
        
        def handlePtvDate():
            try:
                temp = [int(x) for x in self.t_text.split('/')]
                inputDate = datetime.date(2000+temp[2] , temp[1], temp[0])
                today = datetime.date.today()

                first_covid_case_date = datetime.date(2019, 12, 31)
                
                if(inputDate < first_covid_case_date or inputDate > today):
                    self.send_message('please enter correct date')
                elif((today-inputDate).days <= 90 and (today-inputDate).days >= 30):
                    self.user.is_donor = True
                    self.user.save()
                    self.donor = Donor(users = self.user, corona_positive_since = inputDate)
                    self.donor.save()
                    changeState(self.state + 1)
                else:
                    changeState(endState)
            except:
                askPtvDate()

        def askBloodGroup():
            self.send_message("Please select your blood group", {
                'keyboard' : [[x] for x in [dict({'text' : x}) for x in blood_groups]],
                'one_time_keyboard' : True
            } )

        def handleBloodGroup():
            if(self.t_text in blood_groups):  
                self.donor.blood_group = self.t_text
                self.donor.save()
                changeState(self.state + 1)
            else:
                askBloodGroup()

        def askIfDonated():
            self.send_message("Have you donated plasma recently?", {
                'keyboard' : [[{'text' : 'Yes'}], [{'text': 'No'}]],
                'one_time_keyboard' : True
            } )

        def handleDonation():
            if(self.t_text == 'Yes'):
                changeState(self.state + 1)
            elif(self.t_text == 'No'):
                self.donor.last_plasma_donation = None
                self.donor.save()
                changeState(self.state + 2)
            else:
                askIfDonated()

        def askDonationDate():
            self.send_message("Please enter the date (in dd/mm/yy format) you donated plasma")

        def handleDonationDate():
            try:
                temp = [int(x) for x in self.t_text.split('/')]
                inputDate = datetime.date(2000+temp[2] , temp[1], temp[0])
                today = datetime.date.today()

                first_covid_case_date = datetime.date(2019, 12, 31)
                
                if(inputDate < first_covid_case_date or inputDate > today):
                    self.send_message('please enter correct date')
                else:
                    self.donor.last_plasma_donation = inputDate
                    self.donor.save()
                    changeState(self.state + 1)
            except:
                askDonationDate()

        def askIfVaccinated():
            self.send_message("Have you got vacciated recently (in last 30 days)?", {
                'keyboard' : [[{'text' : 'yes'}], [{'text': 'no'}]],
                'one_time_keyboard' : True
            } )
        
        def handleVaccination():
            if(self.t_text == 'yes'):
                changeState(self.state + 1)
            elif(self.t_text == 'no'):
                self.donor.vaccination_date = None
                self.donor.save()
                changeState(self.state + 2)
            else:
                askIfVaccinated()

        def askVaccinationDate():
            self.send_message("Please enter the date (in dd/mm/yy format) you got vaccinated")

        def handleVaccinationDate():
            try:
                temp = [int(x) for x in self.t_text.split('/')]
                inputDate = datetime.date(2000+temp[2] , temp[1], temp[0])
                today = datetime.date.today()

                first_covid_case_date = datetime.date(2019, 12, 31)
                
                if(inputDate < first_covid_case_date or inputDate > today):
                    self.send_message('please enter correct date')
                else:
                    self.donor.vaccination = inputDate
                    self.donor.save()
                    changeState(self.state + 1)
            except:
                askVaccinationDate()

        def askLocation():
            self.send_message("Please share your location with us, this helps us to match you with best benificiaries", {
                'keyboard' : [[{'text' : 'Send Location', 'request_location' : True}]],
                'one_time_keyboard' : True
            } )

        def handleLocation():
            try:
                self.donor.longitude = self.t_text['longitude']
                self.donor.latitude = self.t_text['latitude']
                self.donor.save()
                changeState(self.state + 1)
            except:
                askLocation()

        def askIfSharePhoneNumber():
            self.send_message("Do you allow the beneficiary to call you?", {
                'keyboard' : [[{'text' : 'Yes'}], [{'text': 'No'}]],
                'one_time_keyboard' : True
            } )

        def handleIfSarePhoneNumber():
            if(self.t_text == 'Yes'):
                changeState(self.state + 1)
            elif(self.t_text == 'No'):
                changeState(self.state + 2)
            else:
                askIfSharePhoneNumber()

        def askPhoneNumber():
            self.send_message("Please share your Phone Number with us", {
                'keyboard' : [[{'text' : 'Send PhoneNumber', 'request_contact' : True}]],
                'one_time_keyboard' : True
            } )

        def handlePhoneNumber():
            try:
                self.donor.phone_number = self.t_text['phone_number']
                self.donor.save()
                changeState(16)
            except:
                askPhoneNumber()
        
        def handleEligibility():
            today = datetime.date.today()

            if((today- self.donor.corona_positive_since).days <=28):
                self.user.can_donate = False
                self.user.save()
                self.send_message('not eligible yet')
            elif(self.donor.vaccination_date != None and (today-self.donor.vaccination_date).days <= 28):
                self.user.can_donate = False
                self.user.save()
                self.send_message('not eligible yet')
            elif(self.donor.last_plasma_donation != None and (today-self.last_plasma_donation).days <= 28):
                self.user.can_donate = False
                self.user.save()
                self.send_message('not eligible yet')
            else:
                self.user.can_donate = True
                self.user.save()
                self.send_message('''we have stored your information, and will share it with benificiaries.
                Thanks for registering''')



        # print
        endState = 0

        if(self.state > 7):
            self.donor = self.user.donor

        if(self.state == endState):
            self.send_message('tumse na ho payega')

        elif(self.state == 1):
            changeState(4)

        elif(self.state == 4):
            handleAge()

        elif(self.state == 5):
            handleGender()

        elif(self.state == 6):
            handlePregnancy()

        elif(self.state == 7):
            handlePtvDate()

        elif(self.state == 8):
            handleBloodGroup()

        elif(self.state == 9):
            handleDonation()

        elif(self.state == 10):
            handleDonationDate()

        elif(self.state == 11):
            handleVaccination()

        elif(self.state == 12):
            handleVaccinationDate()

        elif(self.state == 13):
            handleLocation()

        elif(self.state == 14):
            handleIfSarePhoneNumber()

        elif(self.state == 15):
            handlePhoneNumber()

        elif(self.state == 16):
            handleEligibility()

    



    def handleBeneficiary(self):
        
        def changeState(num):
            self.state = self.user.state = num
            self.user.save()
            self.handleBeneficiary()

        def askBloodGroup():
            self.send_message("Please select blood group you need plasma of", {
                'keyboard' : [[x] for x in [dict({'text' : x}) for x in blood_groups]],
                'one_time_keyboard' : True
            } )

        def handleBloodGroup():
            if(self.t_text in blood_groups):
                self.user.is_beneficiary = True
                self.user.save()
                self.beneficiary = Beneficiary(users = self.user, blood_group = self.t_text)
                self.beneficiary.save() 
                changeState(self.state + 1)
            else:
                askBloodGroup()

        def askLocation():
            self.send_message("Please share your location with us, this helps us to match you with best donors", {
                'keyboard' : [[{'text' : 'Send Location', 'request_location' : True}]],
                'one_time_keyboard' : True
            } )

        def handleLocation():
            try:
                self.beneficiary.longitude = self.t_text['longitude']
                self.beneficiary.latitude = self.t_text['latitude']
                self.beneficiary.save()
                changeState(self.state + 1)
            except:
                askLocation()

        def showDonors(donorList):
            for donor in donorList:
                donor.shown_time = datetime.datetime.now()
                donor.save()
                donor = donor.users

                msg = 'Donor Name : '+donor.name+'\n'
                msg += 'Donor user name : @'+donor.user_name+'\n'
                if donor.phone_number is not None:
                    msg += 'Donor phone number : @'+donor.phone_number+'\n'
                self.send_message(msg)

            if len(donorList) == 0:
                self.send_message('Sorry! No donnor available\nplease try after sometime')

        def handleDonorList():
            days28 = datetime.date.today() - datetime.timedelta(days=28)
            days120 = datetime.date.today() - datetime.timedelta(days=120)
            mins5 = datetime.datetime.now() - datetime.timedelta(minutes=1)
            userList =  Donor.objects.filter(blood_group__in = blood_group_match[self.beneficiary.blood_group])  \
                        .filter(corona_positive_since__lt = days28, corona_positive_since__gte = days120)   \
                        .filter(Q(vaccination_date__isnull = True) | Q(vaccination_date__lt = days28) ) \
                        .filter(Q(last_plasma_donation__isnull = True) | Q(last_plasma_donation__lt = days28) ) \
                        .filter(Q(shown_time__isnull = True) | Q(shown_time__lte = mins5))
                        
            showDonors(userList)



        if(self.state > self.beneficiaryState):
            self.beneficiary = self.user.beneficiary

        if(self.state == 1):
            changeState(self.beneficiaryState)

        elif(self.state == self.beneficiaryState):
            handleBloodGroup()

        elif(self.state == self.beneficiaryState+1):
            handleLocation()

        elif(self.state == self.beneficiaryState+2):
            handleDonorList()

        else:
            self.send_message("karye pragati pr hai")

    


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
