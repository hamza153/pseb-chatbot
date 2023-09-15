# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
import requests
import pandas as pd
import json

pseb_API_url=conversation_file_path =""
def init_config():
    global pseb_API_url, conversation_file_path
    api_config = json.load(open("C:\\Users\\ahsan\\Downloads\\FinalPSEBChatbotFolder\\PSEB_rasa_three\\actions\\Data_Config.json"))

    pseb_API_url = api_config['pseb_API_url']
    conversation_file_path = api_config['conversation_file_path']
init_config()

class ActionAskEmail(Action):
    def name(self) -> Text:
        return "action_ask_email"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        name=str(tracker.get_slot("name")).title().split()[0]
        dispatcher.utter_message(text=f"{name}, I would like to know your Email address.")

class ActionAskPhoneNumber(Action):
    def name(self) -> Text:
        return "action_ask_phone_number"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        name=str(tracker.get_slot("name")).title().split()[0]
        dispatcher.utter_message(text=f"Please {name}, can you provide your contact number too?")

class ActionRegisterGuestUser(Action):
    def name(self) -> Text:
        return "action_register_guest_user"
    async def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("name")
        email = tracker.get_slot("email")
        phone_number = tracker.get_slot("phone_number")

        url = pseb_API_url+"create_guest_contact"

        payload = {'email': email,
                   'number': phone_number}
        files = [

        ]
        headers = {}
        slots = []

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        if (response.status_code == 200):
            message=response.json().get('message')
            guest_id=response.json().get('guest_id')

            dispatcher.utter_message(text='Thanks for taking out some time to update us with your details.\nWhat '
                                          'information you would like to know about PSEB?')
            slots= [SlotSet("user_id", str(response.json().get('guest_id'))),SlotSet("user_type", 'guest'),SlotSet("guest_status", True),SlotSet("affiliation_status", True)]
        else:
            dispatcher.utter_message(text='We have network error at our server side. If you have any query related to '
                                          'PSEB, I can assist you with that.')

        return slots

class ActionVerifyRegisteredUser(Action):
    def name(self) -> Text:
        return "action_verify_registered_user"
    async def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        user_id = tracker.get_slot("user_id")

        url = pseb_API_url+"user_details"

        payload = {'reg_key': user_id}
        files = [

        ]
        headers = {

        }
        slots=[]
        company_name='Ovex Technologies'

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        if(response.status_code==200):
            status=response.json().get('status')

            if (status):
                dispatcher.utter_message(text='You have been successfully verified. \nWhat information you would like to '
                                              'know about PSEB?')
                slots= [SlotSet("user_type", 'registered'),SlotSet("registered_status", True),SlotSet("company_name", company_name),SlotSet("affiliation_status", True),SlotSet("r_status", True)]
            else:
                dispatcher.utter_message(text='We could not get your Registration ID verified. You can proceed as a '
                                              'guest user.')
                slots= [SlotSet("user_type", None),SlotSet("user_id", None),SlotSet("registered_status", False),SlotSet("affiliation_status", False),SlotSet("r_status", False)]
        else:
            dispatcher.utter_message(text='We have network error at our server side. If you have any query related to '
                                          'PSEB, I can assist you with that.')
            slots =[SlotSet("user_type", None),SlotSet("user_id", None),SlotSet("registered_status", False),SlotSet("affiliation_status", False),SlotSet("r_status", False)]
        return slots

class ActionGetAccountStatus(Action):
    def name(self) -> Text:
        return "action_get_account_status"
    async def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        user_id = tracker.get_slot("user_id")
        url = pseb_API_url+"account_status"

        payload = {'reg_key': user_id}
        files = [

        ]
        headers = {
        }
        print("Account ID: ", user_id)

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        if response.status_code == 200:
            if response.json().get('status'):
                status = response.json().get('account_status_details')
            else:
                status= None

            dispatcher.utter_message(text=f'Your user account status is: {status}.')

        else:
            dispatcher.utter_message(text='We have network error at our server side. If you have any query related to '
                                      'PSEB, I can assist you with that.')

        return []

class ActionGetRegistrationStatus(Action):
    def name(self) -> Text:
        return "action_get_registration_status"
    async def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        user_id = tracker.get_slot("user_id")
        url =pseb_API_url+"registration_status"

        payload = {'reg_key': user_id}
        files = [

        ]
        headers = {
        }
        print("Reg ID: ",user_id)

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        if (response.status_code == 200):
            if response.json().get('status'):
                status = response.json().get('registration_status_details')
            else:
                status= None

            dispatcher.utter_message(
                text=f'Your registration status is: {status}.')

        else:
            dispatcher.utter_message(text='We have network error at our server side. If you have any query related to '
                                      'PSEB, I can assist you with that.')
        return []

class ActionEscalationNoTicket(Action):
    def name(self) -> Text:
        return "action_escalate_no_ticket"
    async def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:


        sender_id=str(tracker.sender_id)
        file=sender_id+'.csv'
        file = conversation_file_path+file

        # df = pd.read_csv(file)
        # df = df.iloc[::-1]
        # df = df.loc[df.col1 != 'user_id']
        # list = []
        #
        # for index, row in df.iterrows():
        #     print(index)
        #     if (index != 0):
        #         list.append({row['col1']: row['col2']})
        list=[{"bot": "hi"}, {"user":"hello"}]

        contact_id=tracker.get_slot("user_id")
        contact_type=tracker.get_slot("user_type")
        problem_statement='Testing'
        message_thread=list

        url =pseb_API_url+"create_interaction"

        payload = {'contact_id': contact_id,
                   'contact_type': contact_type,
                   'problem_statement': problem_statement,
                   'message_thread': message_thread}

        files = [

        ]
        headers = {

        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        dispatcher.utter_message(text='Okay. Do you want to know anything else?')
        return []

class ActionGenerateTicket(Action):
    def name(self) -> Text:
        return "action_generate_ticket"
    async def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:

        sender_id=str(tracker.sender_id)
        file=sender_id+'.csv'
        file = conversation_file_path+file

        # df = pd.read_csv(file)
        # df = df.iloc[::-1]
        # df = df.loc[df.col1 != 'user_id']
        # list = []
        #
        # for index, row in df.iterrows():
        #     print(index)
        #     if (index != 0):
        #         list.append({row['col1']: row['col2']})
        # print(list)
        list = [{"bot": "hi"}, {"user": "hello"}]



        contact_id=tracker.get_slot("user_id")
        contact_type=tracker.get_slot("user_type")
        problem_statement='Testing'
        message_thread=list

        url = pseb_API_url+"generate_ticket"

        payload = {'contact_id': contact_id,
                   'contact_type': contact_type,
                   'problem_statement': problem_statement,
                   'message_thread': message_thread}

        files = [

        ]
        headers = {

        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        if (response.status_code == 200):

            ticket=response.json().get('ticket_reference_key')

            dispatcher.utter_message(text=f'We have successfully generated a Ticket for you.\nYour Ticket ID is: {ticket}.')

        else:
            dispatcher.utter_message(text='We have network error at our server side. If you have any query related to '
                                          'PSEB, I can assist you with that.')
        return []




class ActionEscalationNoSupportEmail(Action):
    def name(self) -> Text:
        return "action_escalate_no_support_email"
    async def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:


        sender_id=str(tracker.sender_id)
        file=sender_id+'.csv'
        file = conversation_file_path+file

        # df = pd.read_csv(file)
        # df = df.iloc[::-1]
        # df = df.loc[df.col1 != 'user_id']
        # list = []
        #
        # for index, row in df.iterrows():
        #     print(index)
        #     if (index != 0):
        #         list.append({row['col1']: row['col2']})
        list=[{"bot": "hi"}, {"user":"hello"}]


        contact_id=tracker.get_slot("user_id")
        contact_type=tracker.get_slot("user_type")
        problem_statement='Testing'
        message_thread=list

        url =pseb_API_url+"create_interaction"

        payload = {'contact_id': contact_id,
                   'contact_type': contact_type,
                   'problem_statement': problem_statement,
                   'message_thread': message_thread}

        files = [

        ]
        headers = {

        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        dispatcher.utter_message(text='Okay. Do you want to know anything else?')
        return []

class ActionSupportEmail(Action):
    def name(self) -> Text:
        return "action_support_email"
    async def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:

        sender_id=str(tracker.sender_id)
        file=sender_id+'.csv'
        file = conversation_file_path+file

        # df = pd.read_csv(file)
        # df = df.iloc[::-1]
        # df = df.loc[df.col1 != 'user_id']
        # list = []
        #
        # for index, row in df.iterrows():
        #     print(index)
        #     if (index != 0):
        #         list.append({row['col1']: row['col2']})
        # print(list)
        list=[{"bot": "hi"}, {"user":"hello"}]



        contact_id=tracker.get_slot("user_id")
        contact_type=tracker.get_slot("user_type")
        problem_statement='Testing'
        message_thread=list

        url = pseb_API_url+"generate_ticket"

        payload = {'contact_id': contact_id,
                   'contact_type': contact_type,
                   'problem_statement': problem_statement,
                   'message_thread': message_thread}

        files = [

        ]
        headers = {

        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        if (response.status_code == 200):

            ticket=response.json().get('ticket_reference_key')

            dispatcher.utter_message(text=f'We have successfully sent an email to support team.\nYour Email Reference '
                                          f'ID is: {ticket}.')
        else:
            dispatcher.utter_message(text='We have network error at our server side. If you have any query related to '
                                          'PSEB, I can assist you with that.')
        return []



class ActionConversationStoring(Action):
    def name(self) -> Text:
        return "action_conversation_storing"

    async def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        conversation = tracker.events
        print("----------------------------------\nTracker ID :",tracker.sender_id)
        print(conversation)
        import os
        if not os.path.isfile('chats.csv'):
            with open('chats.csv', 'w') as file:
                file.write("intent,user_input,entity_name,entity_value,action,bot_reply\n")
        chat_data = ''
        col1, col2 = [],[]
        col1.append('Sender ID')
        col2.append(tracker.sender_id)
        for i in conversation:
            if i['event'] == 'user':
                col1.append('user')
                col2.append(i['text'])
                chat_data += i['parse_data']['intent']['name'] + ',' + i['text'] + ','
                print('user: {}'.format(i['text']))
                if len(i['parse_data']['entities']) > 0:
                    chat_data += i['parse_data']['entities'][0]['entity'] + ',' + i['parse_data']['entities'][0][
                        'value'] + ','
                    print('extra data:', i['parse_data']['entities'][0]['entity'], '=',
                          i['parse_data']['entities'][0]['value'])
                    col1.append('entity_'+i['parse_data']['entities'][0]['entity'])
                    col2.append(i['parse_data']['entities'][0]['value'])
                else:
                    chat_data += ",,"
            elif i['event'] == 'bot':
                col1.append('bot')
                col2.append(i['text'])
                print('Bot: {}'.format(i['text']))
                try:
                    chat_data += i['metadata']['utter_action'] + ',' + i['text'] + '\n'
                except KeyError:
                    pass
        else:
            with open('chats.csv', 'a') as file:
                file.write(chat_data)

        df=pd.DataFrame({'col1':col1, 'col2': col2})
        fname = 'convo.csv'
        # print(df_results_suggestions_Elastic)
        if os.path.isfile(fname):
            df = df.append(pd.read_csv(fname))
        df.to_csv(fname, index=False)

        # dispatcher.utter_message(text="All Chats saved.")
        return []



# class ActionDefaultFallback(Action):
#     def name(self) -> Text:
#         return "action_default_fallback"
#
#     def run(
#             self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#         # tell the user they are being passed to a customer service agent
#         intent = tracker.latest_message['intent'].get('name')
#         dispatcher.utter_message(text=f"For intent: {intent}, fallback action.")
#         return []

# class ActionTwoStageFallback(Action):
#     def name(self) -> Text:
#         return "action_two_stage_fallback"
#
#     def run(
#             self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#         # tell the user they are being passed to a customer service agent
#         if tracker.get_slot("affiliation_status"):
#             dispatcher.utter_message(text="Sorry, I have not understood what you are trying to say. Please! come up "
#                                           "again by rephrasing.")
#             if tracker.get_slot("affiliation_status"):
#                 pass
#             else:
#                 pass
#         else:
#             dispatcher.utter_message(text="Sorry, I have not understood what you are trying to say. Please! come up "
#                                           "again by rephrasing.")
#
#         return []
