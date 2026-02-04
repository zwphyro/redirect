package service

import (
	"context"
	"time"

	"github.com/zwphyro/redirect/services/redirect-service/internal/domain"

	"golang.org/x/sync/singleflight"
)

type RedirectRepository interface {
	GetFromCache(ctx context.Context, code string) (string, error)
	SetToCache(ctx context.Context, code string, url string, ttl time.Duration) error
	GetFromDB(ctx context.Context, code string) (domain.RedirectURL, error)
	IsRedisNil(err error) bool
}

type RedirectBroker interface {
	PublishRedirect(ctx context.Context, shortCode string) error
	Close() error
}

type RedirectService struct {
	repository    RedirectRepository
	broker        RedirectBroker
	redirectGroup singleflight.Group
}

func NewRedirectService(repository RedirectRepository, broker RedirectBroker) *RedirectService {
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
