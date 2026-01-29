package repository

import (
	"context"
	"errors"
	"time"

	"github.com/zwphyro/redirect/services/redirect-service/internal/domain"

	"github.com/redis/go-redis/v9"
	"gorm.io/gorm"
)

type RedirectRepository struct {
	db    *gorm.DB
	redis *redis.Client
}

func NewRedirectRepository(db *gorm.DB, redis *redis.Client) *RedirectRepository {
	return &RedirectRepository{db: db, redis: redis}
}

func (r *RedirectRepository) GetFromCache(ctx context.Context, code string) (string, error) {
	return r.redis.Get(ctx, code).Result()
}

func (r *RedirectRepository) SetToCache(ctx context.Context, code string, url string, ttl time.Duration) error {
	return r.redis.Set(ctx, code, url, ttl).Err()
}

func (r *RedirectRepository) GetFromDB(ctx context.Context, code string) (domain.RedirectURL, error) {
	var redirectURL domain.RedirectURL
	result := r.db.WithContext(ctx).Take(&redirectURL, "short_code = ?", code)
	return redirectURL, result.Error
}

func (r *RedirectRepository) IsRedisNil(err error) bool {
	return errors.Is(err, redis.Nil)
}

func (r *RedirectRepository) IsRecordNotFound(err error) bool {
	return errors.Is(err, gorm.ErrRecordNotFound)
}
