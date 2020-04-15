"""
This file for making upi payments
"""

# libraryes

def makePayment(params):
    """
    collects relevant information and initiates the payment
    returns the response
    """
    receiver = params['receiver']
    payer = params['payer']
    amount = params['amount']
    
    
    res = {
    'status':'success',
    'receiver': receiver,
    'payer': payer,
    'amount': amount
    }
    return res
    
def getBankDetails(params):
    """
    phoneNumber
    """
    phoneNumber = params['phoneNumber']
    
    # an upi api call
    
    #####
    
    res = {
        'banks': [
            {
                "bankName": "HDFC",
                "branchName": 'Madhapur',
                "accountNumber": "1204"
            },
            {
                "bankName": "SBI",
                "branchName": 'Kondapur',
                "accountNumber": "5364"
            }
        ]
        
    }
    return res