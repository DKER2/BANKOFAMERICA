import data from '../Asset/sample_events.json'
import { ConfigEvent } from '../Models/ConfigEvent'
import { FXMidEvent } from '../Models/FXMidEvent'
import { TradeEvent } from '../Models/TradeEvent'

export const event = []

// Event from the market
data.forEach(element => {
    let newEvent
    switch (element.EventType) {
        case "TradeEvent":
            newEvent = new TradeEvent(element.EventId, element.EventType, element.BuySell, element.Ccy, element.Tenor, element.Quantity, element.TradeId)
            break;
        case "FXMidEvent":
            newEvent = new FXMidEvent(element.EventId, element.EventType, element.Ccy, element.rate)
            break;
        case "ConfigEvent":
            newEvent = new ConfigEvent(element.EventId, element.EventType, element.m, element.b, element.DivisorRatio, element.Spread)
            break;
        default:
            break;
    }
    event.push(newEvent)
})
