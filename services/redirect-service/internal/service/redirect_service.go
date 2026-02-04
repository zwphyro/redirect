package service

import (
	"context"
	"time"

	"github.com/zwphyro/redirect/services/redirect-service/internal/broker"
	"github.com/zwphyro/redirect/services/redirect-service/internal/repository"

	"golang.org/x/sync/singleflight"
)

type RedirectService struct {
	repository    *repository.RedirectRepository
	broker        *broker.RabbitMQProducer
	redirectGroup singleflight.Group
}

func NewRedirectService(repository *repository.RedirectRepository, broker *broker.RabbitMQProducer) *RedirectService {
	return &RedirectService{
		repository: repository,
		broker:     broker,
	}
}

func (s *RedirectService) GetOriginalURL(ctx context.Context, shortCode string) (string, error) {
	originalURL, err := s.repository.GetFromCache(ctx, shortCode)
	if err == nil {
		go func() {
			_ = s.broker.PublishRedirect(ctx, shortCode)
		}()
		return originalURL, nil
	}

	if !s.repository.IsRedisNil(err) {
		return "", err
	}

	result, err, _ := s.redirectGroup.Do(shortCode, func() (any, error) {
		redirectURL, err := s.repository.GetFromDB(ctx, shortCode)
		if err != nil {
			return "", err
		}

		_ = s.repository.SetToCache(context.Background(), shortCode, redirectURL.OriginalURL, 1*time.Minute)

		return redirectURL.OriginalURL, nil
	})

	if err != nil {
		return "", err
	}

	go func() {
		_ = s.broker.PublishRedirect(ctx, shortCode)
	}()

	return result.(string), nil
}
