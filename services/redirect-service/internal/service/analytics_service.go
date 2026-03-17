package service

import (
	"context"
	"log"
	"time"

	"github.com/zwphyro/redirect/services/redirect-service/internal/broker"
)

type AnalyticsService struct {
	producer *broker.RedirectProducer
}

func NewAnalyticsService(producer *broker.RedirectProducer) *AnalyticsService {
	return &AnalyticsService{producer: producer}
}

func (s *AnalyticsService) PublishRedirectEvent(data broker.RedirectData) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := s.producer.PublishRedirect(ctx, data); err != nil {
		log.Printf("failed to publish redirect event: %v", err)
	}
}
