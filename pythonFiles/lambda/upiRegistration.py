"""
This file is build response for registration only for initialization stage. 
"""
import upiGateway

def case1(slots):
    # case 1 :
    case = True
    for k,v in slots.items:
        if k == 'phoneNumber':
            if v == None:
                case1 = False
        else:
            if v != None:
                case1 = False
    return case

    
def buildLexResponseForRegistrationResponse(request):
    """
    for upiRegistration intent ::
        if phoneNumber exists and bank details doesn't exists =>
            getBankDetails call i.e a upi api to get upi registered bank details
            i.e {
                bankName :
                branchName:
                ifsc
            }
            These details are updated in the response slots
    """
    # sample response template ::
    lexSampleResponse = {
        "sessionAttributes": {},
        "recentIntentSummaryView": [],
        "dialogAction": {}
    }
    lexResponse = dict(lexSampleResponse)
    slots = request['currentIntent']['slots']
    phoneNumber = slots['phoneNumber']
    # edge case ::
    # when not even phone number is alos present. 
    if phoneNumber == None:
        lexResponse["dialogAction"] = {
            "type": "ElicitSlot",
            "message": {
                "contentType": "PlainText",
                "content": "Please enter your phone number!"
            },
            "intentName": "upiRegistration",
            "slots": {},
            "slotToElicit" : "phoneNumber"
            }
        return lexResponse
    # logic 1:
    # customer calling for the first time and first turn
    # i.e only we get phone number no other slots are filled. 
    if case1(slots):
        # inside i.e only phoneNumber not none rest none
        print('Users phone number :: ',slots['phoneNumber'])
        # extracting the back details :
        params = {
            'phoneNumber':phoneNumber
        }
        bankDetails = upiGateway.getBankDetails(params)
        responseText = """You have accounts in following
                         accounts {} with last four digits in account {} and {} with {} as 
                         last four digits. Please say which account you wish for registration""".format(bankDetails[0]['bankName'],bankDetails[0]['accountNumber'],bankDetails[1]['bankName'],bankDetails[1]['accountNumber'])
        lexResponse["dialogAction"] =  {
            "type": "ElicitSlot",
            "message": {
                "contentType": "PlainText",
                "content": responseText
            },
            "intentName": "upiRegistration",
            "slots": slots,
            "slotToElicit" : 'bankName',
        }
        return lexResponse
    
    # case 2
    else:
        lexResponse["dialogAction"] =   {
            "type": "ElicitSlot",
            "message": {
              "contentType": "PlainText",
              "content": "Please enter your phone number!"
            },
           "intentName": "upiRegistration",
           "slots": {},
           "slotToElicit" : "phoneNumber"
          }

        return lexResponse
    
    phoneNumber = str(phoneNumber)
    
    lexResponse = {
        "sessionAttributes": {},
        "recentIntentSummaryView": [
            {
                "intentName": "upiRegistration",
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
              "content": "You have sucessfully registered with phoneNumber {} . Congratulation!!".format(phoneNumber)
            }
          }
    }
    return lexResponse
