import { Event } from "./Event";

export class FXMidEvent extends Event {
    Ccy
    rate

    constructor(eventId, eventType, cCY, rate) {
        super()
        this.EventId = eventId
        this.EventType = eventType
        this.Ccy = cCY
        this.rate = rate
    }
}