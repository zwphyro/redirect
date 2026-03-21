package service

import (
	"context"
	"log"
	"time"

	"github.com/zwphyro/redirect/services/redirect-service/internal/domain"
)

type RedirectProducer interface {
	PublishRedirect(ctx context.Context, event domain.RedirectEvent) error
}

type AnalyticsService struct {
	producer RedirectProducer
}

func NewAnalyticsService(producer RedirectProducer) *AnalyticsService {
	return &AnalyticsService{producer: producer}
}

func (s *AnalyticsService) PublishRedirectEvent(event domain.RedirectEvent) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := s.producer.PublishRedirect(ctx, event); err != nil {
		log.Printf("failed to publish redirect event: %v", err)
	}
}
