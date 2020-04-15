"""
This file is for lambda initialization and validation of parameters
"""

import upiGateway


def lambdaInitialization(req):
    intentName = request["currentIntent"]["name"]
    if intentName == "upiRegistration":
        buildLexResponseForRegistrationResponse(request)
    return res


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
    lexResponse = {
        "sessionAttributes": {},
        "recentIntentSummaryView": [
            {
                "intentName": "Name",
                "checkpointLabel": "Label",
                "slots": {},
                "confirmationStatus": None,
                "dialogActionType": "ElicitSlot",
                "fulfillmentState": "Fulfilled",
                "slotToElicit": None
            }
        ],
        "dialogAction": {}
    }

    lexResponse = dict(lexSampleResponse)

    # logic 1:
    slots = request['currentIntent']['slots']
    if 'phoneNumber' in slots:
        if slots['phoneNumber'] != 'None' and slots['phoneNumber'] = None:
            if 'bankName' in slots:
                if slots['bankName'] != 'None' and slots['bankName'] = None:
                    params = {
                        "phoneNumber": slots['phoneNumber']
                    }
                    bankDetails = upiGateway.getBankDetails(params)

                    # adding in slots
                    for key, val in bankDetails.items():
                        slots[key] = val

                     # adding relavant details:
                     lexResponse["dialogAction"] =  {
                        "type": "ElicitSlot",
                        "message": {
                          "contentType": "PlainText",
                          "content": "Please enter 4 digit number as for your pin for setting it for future payments"
                        },
                       "intentName": "upiRegistration",
                       "slots": slots,
                       "slotToElicit" : 'pinNumber',
                    }
                    return lexResponse
    else:
        lexResponse["dialogAction"] =  {
            "type": "ElicitSlot",
            "message": {
              "contentType": "PlainText",
              "content": "Please enter 4 digit number as for your pin for setting it for future payments"
            },
           "intentName": "upiRegistration",
           "slots": slots,
           "slotToElicit" : 'phoneNumber',
        }
        return lexResponse
        
        
    return lexResponse
