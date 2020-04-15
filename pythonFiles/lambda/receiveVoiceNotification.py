
def receiveVoiceNotification(lexRequest):
    """ Building response for receiveVoiceNotifications
    lexRequest :: request from the response
    Note :: Right now it is only when you receive payment notification
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
              "content": "Your transaction is done. You have received the payment"
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
        text = "You have received payment from {}".format(phoneNumber_)
        lexSampleResponse["dialogAction"]["message"]["content"] = text

    if "amount" in lexRequest["sessionAttributes"]:
        lexSampleResponse["sessionAttributes"] = {
            "amount": lexRequest["sessionAttributes"]["phone number"] 
        }
        amount =lexRequest["sessionAttributes"]["phone number"] 
        text = "You have received payment from {}".format(amount)
        lexSampleResponse["dialogAction"]["message"]["content"] = text

    return lexSampleResponse
