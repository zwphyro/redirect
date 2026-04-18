package domain

import (
	"time"
)

type RedirectEvent struct {
	EventTime time.Time `json:"event_time"`
	ShortCode string    `json:"short_code"`
	IP        string    `json:"ip"`
	UserAgent string    `json:"user_agent"`
	Language  string    `json:"language"`
	Origin    string    `json:"origin"`
}
