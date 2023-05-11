import json

NUMBEROFDAYINMONTH = 30
class PricingEngine:
    def __init__(self):
        self.positionList = {}
        self.lastestConfigEvent = None
        self.fx = {}
    def processRequest(self, request):
        order = []
        if(request["EventType"]=='ConfigEvent'):
            self.lastestConfigEvent = request
        #Check if it is a FXMid Event 
        if(request["EventType"]=="FXMidEvent"):
            self.fx[request["Ccy"]] = request["rate"]
        #Check if it is a Trade Event 
        if(request["EventType"]=="TradeEvent"):
            # If (currency, tenor) index is not in position dictionary, create a dummy entry 
            if((request["Ccy"], request["Tenor"]) not in request.keys()):
                self.positionList[(request["Ccy"], request["Tenor"])] = 0
            # Increase the position if it is a buy option
            if request["BuySell"]=="buy":
                self.positionList[(request["Ccy"], request["Tenor"])] = self.positionList[(request["Ccy"], request["Tenor"])] + int(request["Quantity"])
            # Deduct the position if it is a buy option
            elif request["BuySell"]=="sell":
                self.positionList[(request["Ccy"], request["Tenor"])] = self.positionList[(request["Ccy"], request["Tenor"])] - int(request["Quantity"])
            # Eliminate position entry if it's value is zero
            if(self.positionList[(request["Ccy"], request["Tenor"])]==0):
                self.positionList.pop((request["Ccy"], request["Tenor"]))
        for k, v in self.positionList.items():
            currency = k[0]
            tenor = k[1]
            position = v
            if(self.lastestConfigEvent==None) or currency not in self.fx.keys():
                order.append((currency, tenor, position, "NA", "NA", "EXCEPTION"))
            else:
                variance = self.lastestConfigEvent["m"]*NUMBEROFDAYINMONTH*int(tenor[:-1]) + self.lastestConfigEvent["b"]
                skew = position / self.lastestConfigEvent["DivisorRatio"] * variance
                newMid = self.fx[currency] - skew
                bid = newMid - (0.5*self.lastestConfigEvent["Spread"]/10000)
                ask = newMid - (0.5*self.lastestConfigEvent["Spread"]/10000)
                if bid > ask or abs(bid-self.fx[currency]) > 0.1*self.fx[currency] or abs(ask-self.fx[currency]) > 0.1*self.fx[currency]:
                    order.append((currency, tenor, position, bid, ask, "NONE-TRADABLE"))
                else:
                    order.append((currency, tenor, position, bid, ask, "TRADABLE"))
        return order

if __name__=="__main__":
    event_file = 'sample_events.json'
    input_file = 'sample_input.json'
    events = open(event_file)
    eventList = json.load(events)
    a = PricingEngine()
    for event in eventList:
        print()
        print(a.processRequest(event))
    #reportGenerator(event_file, input_file)