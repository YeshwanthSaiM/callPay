"""
This file make a payment.
Takes a request 
    validates all the fields
Makes a payment call
returns the response i.e lambda response
"""


def makePayment(request):
    """
    params : 
        lex request object
    returns:
        upi payment acknolwdgement in form of lambda response
    """


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
    lexSampleResponse = {
        "sessionAttributes": {},
        "recentIntentSummaryView": [],
        "dialogAction": {}
    }
    lexResponse = dict(lexSampleResponse)

    # extracting the required information whater ever can be 
    # extracted from request boject
    """
    required slots:
        receiver : {
            name :
            phoneNumber
            bank details
        }
        payer : {
            name
            phoneNumber
            bank details
        }
    """
    slots = request['currentIntent']['slots']
    intentName = request['currentIntent']['name']

    requiredSlots = ['pinNumber','phoneNumber']
    nonEmptySlots = [key for key,val in slots.items if val != None]

    for reqSlot in requiredSlots:
        if reqSlot not in nonEmptySlots:
            lexResponse["dialogAction"] =  {
                "type": "ElicitSlot",
                "message": {
                  "contentType": "PlainText",
                  "content": "Please enter {} in order to complete the payment".format(reqSlot)
                },
               "intentName": intentName,
               "slots": slots,
               "slotToElicit" : reqSlot,
            }
            return lexResponse
    
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
              "content": "Your money is sent successfully"
            }
          }
    }
    return lexResponse


