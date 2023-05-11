import { Event } from "./Event";

export class TradeEvent extends Event {
    // 1. Attribute
    BuySell
    Ccy
    Tenor
    Quantity
    TradeId

    // 2. Constructor
    constructor(eventId, eventType, buySell, cCy, tenor, quantity, tradeId) {
        super()
        this.EventId = eventId
        this.EventType = eventType
        this.BuySell = buySell
        this.Ccy = cCy
        this.Tenor = tenor
        this.Quantity = quantity
        this.TradeId = tradeId
    }
}