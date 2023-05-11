import json
  
def reportGenerator(event_file: str, input_file: str): 
    """
    This function is used to generate Bid, Ask and QuoteStatus base on Event and Input
    :param event_file: path to event log
    :param input_file: path to input log
    """
    # Opening JSON file
    events = open(event_file)
    inputs = open(input_file)
    NUMBEROFDAYINMONTH = 30
    # returns JSON object as 
    # a dictionary
    eventList = json.load(events)
    input = json.load(inputs)

    #Add Sequence of Input Id
    for i, data in enumerate(input): 
        data["SequenceId"] = i

    #Sort Input according to Event Id
    sorted_input = sorted(input, key=lambda input: input['EventId'])

    # Dict for rate exchange
    fx = {}
    # Dict for position 
    positions = {}
    # pointer for input index
    ptr = 0
    # output array
    output = []
    # lastest Configuration
    lastestConfigEvent = None
    # list of order
    order = []
    for eventId, event in enumerate(eventList):
        #Check if it is a Config Event
        if(event["EventType"]=='ConfigEvent'):
            lastestConfigEvent = event
        #Check if it is a FXMid Event 
        if(event["EventType"]=="FXMidEvent"):
            fx[event["Ccy"]] = event["rate"]
        #Check if it is a Trade Event 
        if(event["EventType"]=="TradeEvent"):
            # If (currency, tenor) index is not in position dictionary, create a dummy entry 
            if((event["Ccy"], event["Tenor"]) not in positions.keys()):
                positions[(event["Ccy"], event["Tenor"])] = 0
            # Increase the position if it is a buy option
            if event["BuySell"]=="buy":
                positions[(event["Ccy"], event["Tenor"])] = positions[(event["Ccy"], event["Tenor"])] + event["Quantity"]
            # Deduct the position if it is a buy option
            elif event["BuySell"]=="sell":
                positions[(event["Ccy"], event["Tenor"])] = positions[(event["Ccy"], event["Tenor"])] - event["Quantity"]
            # Eliminate position entry if it's value is zero
            if(positions[(event["Ccy"], event["Tenor"])]==0):
                positions.pop((event["Ccy"], event["Tenor"]))

        # Check if current eventId is matched with input
        while ptr<len(sorted_input) and sorted_input[ptr]["EventId"]==eventId+1:
            # Currency for Input Entry
            currency = sorted_input[ptr]["Ccy"]
            # Tenor for Input Entry
            tenor = sorted_input[ptr]["Tenor"]
            # Sequence for Input Entry
            sequenceId = sorted_input[ptr]["SequenceId"]
            # If key is not in position return an EXCEPTION record
            if (currency, tenor) not in positions.keys():
                order.append({
                    "EventId": eventId+1,
                    "Ccy": currency,
                    "Tenor": tenor,
                    "Position": "NA",
                    "Bid": "NA",
                    "Ask": "NA",
                    "QuoteStatus": "EXCEPTION",
                    "SequenceId": sequenceId
                })
            # If there is missing data return an EXCEPTION record
            elif lastestConfigEvent==None or currency not in fx.keys():
                    order.append({
                        "EventId": eventId+1,
                        "Ccy": currency,
                        "Tenor": tenor,
                        "Position": positions[(currency, tenor)],
                        "Bid": "NA",
                        "Ask": "NA",
                        "QuoteStatus": "EXCEPTION",
                        "SequenceId": sequenceId
                    })
            # Else return a Acceptable order
            else:
                variance = lastestConfigEvent["m"]*NUMBEROFDAYINMONTH*int(tenor[:-1]) + lastestConfigEvent["b"]
                skew = positions[(currency, tenor)] / lastestConfigEvent["DivisorRatio"] * variance
                newMid = fx[currency] - skew
                bid = newMid - (0.5*lastestConfigEvent["Spread"]/10000)
                ask = newMid + (0.5*lastestConfigEvent["Spread"]/10000)

                #Check if it match the condition to be tradable or not
                if bid > ask or abs(bid-fx[currency]) > 0.1*fx[currency] or abs(ask-fx[currency]) > 0.1*fx[currency]:
                    order.append({
                            "EventId": eventId+1,
                            "Ccy": currency,
                            "Tenor": tenor,
                            "Position": positions[(sorted_input[ptr]["Ccy"], sorted_input[ptr]["Tenor"])],
                            "Bid": bid,
                            "Ask": ask,
                            "QuoteStatus": "NON-TRADABLE",
                            "SequenceId": sequenceId
                        })
                else:
                    order.append({
                            "EventId": eventId+1,
                            "Ccy": currency,
                            "Tenor": tenor,
                            "Position": positions[(sorted_input[ptr]["Ccy"], sorted_input[ptr]["Tenor"])],
                            "Bid": bid,
                            "Ask": ask,
                            "QuoteStatus": "TRADABLE",
                            "SequenceId": sequenceId
                        })
            
            #Iterate through Input
            ptr = ptr + 1

    # Reorder the output to match the sequence in input
    output = sorted(order, key=lambda order: order['SequenceId'])
    # Drop Redundant Sequence Id
    for datapoint in output:
        datapoint = datapoint.pop("SequenceId")
    return output

if __name__=="__main__":
    event_file = 'events.json'
    input_file = 'input.json'
    data = reportGenerator(event_file, input_file)
    # Serializing json
    json_object = json.dumps(data, indent=4)
    
    # Writing to sample.json
    with open("output.json", "w") as outfile:
        outfile.write(json_object)

