from __future__ import print_function
import receiveVoiceNotification from receiveVoiceNotification

# importing intent response building functions

"""
This function for callPayLambda :: The following are the functionalities,
1. Validates each of the slot values
2. Makes all required followup intents
    :: The following are the intents flow :: upiFlow = (upiRequirements => ConfirmIntent => Acknowledgment)
        payToFounder => upiFlow
        recharge => upiFlow
        payToPhoneNumber =< upiFlow
"""


# --------------- Helpers that build all of the responses ---------------------#

# --------------- Function after intent fullfillment  -------------------------#
def getWelcomeResponse(lexRequest):
    """ An example of a custom lex response i.e Welcome.
    """
    lexSampleResponse = {
        "sessionAttributes": {},
        "recentIntentSummaryView": [
            {
                "intentName": "welcomeTocallPay",
                "checkpointLabel": "Label",
                "slots": {},
                "confirmationStatus": None,
                "dialogActionType": "ElicitIntent",
                "fulfillmentState": "Fulfilled",
                "slotToElicit": None
            }
        ],
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "PlainText",
              "content": "Welcome to callPay! Here you can send money to any one."
            }
        }
    }
    print("Lex response ::",lexSampleResponse)
    # try adding user phone number:
    if "phone number" in lexRequest["sessionAttributes"]:
        lexSampleResponse["sessionAttributes"] = {
            "phone number": lexRequest["sessionAttributes"]["phone number"] 
        }
        phoneNumber = lexRequest["sessionAttributes"]["phone number"]
        phoneNumber_ = ""
        for n in str(phoneNumber):
            phoneNumber_ += n + " "
        text = "Hi user! your phone number is {}. Here you can send money".format(phoneNumber_)
        lexSampleResponse["dialogAction"]["message"]["content"] = text
        
    return lexSampleResponse

def buildLexResponse(lexRequest):
    """
    Takes the required values from the params object 
    builds the response in required format and returns
    """
    response  = buildLexResponseForupiRequirements(lexRequest)
    return response

def buildLexResponseForupiRequirements(lexRequest):
    """
    Builds lex response for upiRequirements gathering
    """
    lexResponse = {
        "sessionAttributes": {},
        "recentIntentSummaryView": [
            {
                "intentName": "Name",
                "checkpointLabel": "Label",
                "slots": {},
                "confirmationStatus": None,
                "dialogActionType": "ElicitIntent, ElicitSlot, ConfirmIntent, Delegate, or Close",
                "fulfillmentState": "Fulfilled",
                "slotToElicit": None
            }
        ],
        "dialogAction": {}
    }
    
    # extracting required fields from lexRequest
    intentName = lexRequest['currentIntent']['name']
    slots = lexRequest['currentIntent']['slots']
    
    # check whether all slots are gathered for upi payment or not
    otherRequiredParams = {
        "amount"
    }
    requiredParams = [
        "amount",
        "pinNumber"
        ]
        # other details to be added ]
    
    for p in requiredParams:
        if p not in slots:
            # make lex response to elicit the slot p
             # ConfirmIntent
            # adding the values to the response
            # adding intent
            lexResponse["recentIntentSummaryView"][-1]["intentName"] = intentName
            lexResponse["recentIntentSummaryView"][-1]["slots"] = slots
            lexResponse["recentIntentSummaryView"][-1]["dialogActionType"] = "ElicitSlot"
            lexResponse["recentIntentSummaryView"][-1]["fulfillmentState"] = "Fulfilled"
            lexResponse["recentIntentSummaryView"][-1]["slotToElicit"] = None
            
            # adding slots to  dialog action
            lexResponse["dialogAction"] =  {
                "type": "ElicitSlot",
                "message": {
                  "contentType": "PlainText",
                  "content": "Please enter your pin for upi payment"
                },
               "intentName": "upiRequirements",
               "slots": slots,
               "slotToElicit" : p,
            }
            return lexResponse

            
    # all params are gathered :
    # make the payment
    # give the acknowledgement
    lexResponse = makeUpiPayment(lexRequest)
    
    # session has to be refreshed
    return lexResponse
    
# --------------- Functions for upi payment -----------------------------------#
def buildLexResponseAfterPayment(lexRequest, upiResponse):
    """
    Makes acknowledgment response after payment
    i.e success or failue
    """
    
    lexResponse = {
        "sessionAttributes": {},
        "recentIntentSummaryView": [
            {
                "intentName": "upiRequirements",
                "checkpointLabel": "Label",
                "slots": {},
                "confirmationStatus": "Confirmed",
                "dialogActionType": "Close",
                "fulfillmentState": "Fulfilled",
                "slotToElicit": None
            }
        ],
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "PlainText",
              "content": "Your money sent"
            }
          }
    }
    slots = lexRequest["currentIntent"]["slots"]
    if "amount" in slots:
        amount = slots['amount']
        if slots['phoneNumber'] != None:
            phoneNumber = slots['phoneNumber']
            message = "Your money rupees {} sent to phone number {}".format(amount,phoneNumber)
        else:
            message = "Your money rupees {} sent to founder that is Yeshwanth".format(amount)
            
    lexResponse["dialogAction"]["message"]["content"] = message
    return lexResponse

def callToUpiGateway(params):
    """
    Actual call to Upi gateway
    """
    return {}

def makeUpiPayment(lexRequest):
    """
    makes a upi pament
    """
    params = {} # required params from lexRequest
    # validating params:
    for key,val in params.items():
        bool, reason = getSlotValidated(val,slotType)
        if not bool:
            return buildLexResponseForSlotValidation(lexRequest)
            
    upiResponse = callToUpiGateway(params)
    upiResponse['success'] = True
    return buildLexResponseAfterPayment(lexRequest,upiResponse)

# --------------- Some other helper funtions ----------------------------------#
def getSlotValidated(slotValue,slotType):
    """
    validates whether the given slot matches with the slotType
    params:
        slotValue :: the value of the slot given by the user
        slotType :: the type of the slot whether phoneNumber or money
    """
    if slotType == 'money':
        # condition :: slotValue > 0 and slotValue < 100 
        lowerLimit = 0
        upperLimit = 100
        if slotType <lowerLimit:
            return False , ' {} is less than lower limit {}'.format(slotValue,lowerLimit) 
        if slotType >upperLimit:
            return False, ' {} is greater than upper limit {}'.format(slotValue,upperLimit)
        return True, ' {} is in between {} and {}'.format(slotValue,lowerLimit,upperLimit)
    if slotType == 'phoneNumber':
        # checks data type of not str
        if type(slotValue) == str:
            return False, 'phone number :: {} is in string format'.format(slotValue)
        else:
            # check number of digits == 10
            tempSlotValue = str(slotValue)
            if len(tempSlotValue) != 10:
                return False, 'phone number :: {} not having 10 digits'.format(slotValue)
            else:
                return True, 'phone number :: {} having 10 digits'.format(slotValue)

def buildLexResponseForSlotValidation(lexRequest):
    """
    Build lex response if any of the slot validation fails
    """
    pass
# --------------- Events ------------------

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    response = getWelcomeResponse()
    return response


def on_intent(lexRequest):
    """ Called when the user specifies an intent for this skill """
    intentName = lexRequest["currentIntent"]['name']
    
    if intentName == 'welcomeTocallPay':
        return getWelcomeResponse(lexRequest)
    
    if 'AMAZON' in intentName:
        if intentName == "AMAZON.HelpIntent":
            return getWelcomeResponse()
        elif intentName == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
            return handle_session_end_request()
        else:
            raise ValueError("Invalid intent")
    
    
    if intentName == "upiRequirements":
        # case when intentName is upiRequirements i.e fullfilled by user
        return buildLexResponseForupiRequirements(lexRequest)
        
    if intentName == "receiveVoiceNotification":
        return receiveVoiceNotification(lexRequest) 
    # for all other intent fullfillment    
    return buildLexResponse(lexRequest)
        

# --------------- Main handler ------------------

def lambda_handler(request, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    # Uncomment below if you need print whole lex request
    print("Incoming request...")
    print("Request :: ",request)

    return on_intent(request)
    