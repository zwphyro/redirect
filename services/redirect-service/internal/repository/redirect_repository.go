package repository

import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/zwphyro/redirect/services/redirect-service/internal/config"
	"github.com/zwphyro/redirect/services/redirect-service/internal/domain"

	"github.com/redis/go-redis/v9"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

func InitDB(config config.Postgres) (*gorm.DB, error) {
	postgresDSN := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=disable",
		config.Host,
		config.User,
		config.Password,
		config.DBName,
		config.Port,
	)

	return gorm.Open(postgres.Open(postgresDSN), &gorm.Config{})
}

func InitRedis(config config.Redis) *redis.Client {
  return redis.NewClient(&redis.Options{
    Addr:     fmt.Sprintf("%s:%s", config.Host, config.Port),
    Password: config.Password,
    DB:       config.DB,
  })
}

type RedirectRepository struct {
	db    *gorm.DB
	redis *redis.Client
}

func NewRedirectRepository(db *gorm.DB, redis *redis.Client) *RedirectRepository {
	return &RedirectRepository{db: db, redis: redis}
}

func (r *RedirectRepository) GetFromCache(ctx context.Context, shortCode string) (string, error) {
	return r.redis.Get(ctx, shortCode).Result()
}

func (r *RedirectRepository) SetToCache(ctx context.Context, shortCode string, url string, ttl time.Duration) error {
	return r.redis.Set(ctx, shortCode, url, ttl).Err()
}

func (r *RedirectRepository) GetFromDB(ctx context.Context, shortCode string) (domain.RedirectURL, error) {
	var redirectURL domain.RedirectURL
	result := r.db.WithContext(ctx).Take(&redirectURL, "short_code = ?", shortCode)
	return redirectURL, result.Error
}

func (r *RedirectRepository) IsRedisNil(err error) bool {
	return errors.Is(err, redis.Nil)
}

func (r *RedirectRepository) IsRecordNotFound(err error) bool {
	return errors.Is(err, gorm.ErrRecordNotFound)
}
