package service

import (
	"context"
	"errors"
	"testing"
	"time"

	"github.com/zwphyro/redirect/services/redirect-service/internal/domain"
)

type fakeRedirectRepository struct {
	cacheValue   string
	cacheError   error
	dbValue      domain.RedirectURL
	dbError      error
	setToCacheFn func(code string, url string, ttl time.Duration)
}

func (f *fakeRedirectRepository) GetFromCache(_ context.Context, _ string) (string, error) {
	return f.cacheValue, f.cacheError
}

func (f *fakeRedirectRepository) SetToCache(_ context.Context, code string, url string, ttl time.Duration) error {
	if f.setToCacheFn != nil {
		f.setToCacheFn(code, url, ttl)
	}
	return nil
}

func (f *fakeRedirectRepository) GetFromDB(_ context.Context, _ string) (domain.RedirectURL, error) {
	return f.dbValue, f.dbError
}

func (f *fakeRedirectRepository) IsRedisNil(err error) bool {
	return errors.Is(err, ErrRedisNil)
}

var ErrRedisNil = errors.New("redis: nil")

func TestRedirectService_GetOriginalURL_CacheHit(t *testing.T) {
	repo := &fakeRedirectRepository{
		cacheValue: "https://example.com",
		cacheError: nil,
	}

	service := NewRedirectService(repo)

	url, err := service.GetOriginalURL(context.Background(), "abc123")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if url != "https://example.com" {
		t.Fatalf("expected url %q, got %q", "https://example.com", url)
	}
}

func TestRedirectService_GetOriginalURL_DBHitAndCacheSet(t *testing.T) {
	var cachedCode string
	var cachedURL string

	repo := &fakeRedirectRepository{
		cacheError: ErrRedisNil,
		dbValue: domain.RedirectURL{
			OriginalURL: "https://example.com",
		},
		setToCacheFn: func(code string, url string, _ time.Duration) {
			cachedCode = code
			cachedURL = url
		},
	}

	service := NewRedirectService(repo)

	code := "abc123"
	url, err := service.GetOriginalURL(context.Background(), code)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if url != "https://example.com" {
		t.Fatalf("expected url %q, got %q", "https://example.com", url)
	}

	if cachedCode != code || cachedURL != "https://example.com" {
		t.Fatalf("expected cache to be set for code %q with url %q, got code=%q url=%q", code, "https://example.com", cachedCode, cachedURL)
	}
}

