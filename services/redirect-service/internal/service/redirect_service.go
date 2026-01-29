package service

import (
	"context"
	"time"

	"github.com/zwphyro/redirect/services/redirect-service/internal/repository"

	"golang.org/x/sync/singleflight"
)

type RedirectService struct {
	repo          *repository.RedirectRepository
	redirectGroup singleflight.Group
}

func NewRedirectService(repo *repository.RedirectRepository) *RedirectService {
	return &RedirectService{
		repo: repo,
	}
}

func (s *RedirectService) GetOriginalURL(ctx context.Context, shortCode string) (string, error) {
	originalURL, err := s.repo.GetFromCache(ctx, shortCode)
	if err == nil {
		return originalURL, nil
	}

	if !s.repo.IsRedisNil(err) {
		return "", err
	}

	result, err, _ := s.redirectGroup.Do(shortCode, func() (any, error) {
		redirectURL, err := s.repo.GetFromDB(ctx, shortCode)
		if err != nil {
			return "", err
		}

		_ = s.repo.SetToCache(context.Background(), shortCode, redirectURL.OriginalURL, 1*time.Minute)

		return redirectURL.OriginalURL, nil
	})

	if err != nil {
		return "", err
	}

	return result.(string), nil
}
