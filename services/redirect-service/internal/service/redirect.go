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
	GetFromDB(ctx context.Context, code string) (domain.RedirectLink, error)
	IsRedisNil(err error) bool
}

type RedirectService struct {
	repository    RedirectRepository
	redirectGroup singleflight.Group
}

func NewRedirectService(repository RedirectRepository) *RedirectService {
	return &RedirectService{repository: repository}
}

func (s *RedirectService) GetTargetURL(ctx context.Context, shortCode string) (string, error) {
	targetURL, err := s.repository.GetFromCache(ctx, shortCode)
	if err == nil {
		return targetURL, nil
	}

	if !s.repository.IsRedisNil(err) {
		return "", err
	}

	result, err, _ := s.redirectGroup.Do(shortCode, func() (any, error) {
		redirectLink, err := s.repository.GetFromDB(ctx, shortCode)
		if err != nil {
			return "", err
		}

		_ = s.repository.SetToCache(context.Background(), shortCode, redirectLink.TargetURL, 1*time.Minute)

		return redirectLink.TargetURL, nil
	})

	if err != nil {
		return "", err
	}

	return result.(string), nil
}
