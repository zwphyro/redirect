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

type PostgresRepository struct {
	db    *gorm.DB
	redis *redis.Client
}

func NewPostgresRepository(db *gorm.DB, redis *redis.Client) *PostgresRepository {
	return &PostgresRepository{db: db, redis: redis}
}

func (r *PostgresRepository) ShortCodeKey(shortCode string) string {
	return "short_code:" + shortCode
}

func (r *PostgresRepository) GetFromCache(ctx context.Context, shortCode string) (string, error) {
	return r.redis.Get(ctx, r.ShortCodeKey(shortCode)).Result()
}

func (r *PostgresRepository) SetToCache(ctx context.Context, shortCode string, url string, ttl time.Duration) error {
	return r.redis.Set(ctx, r.ShortCodeKey(shortCode), url, ttl).Err()
}

func (r *PostgresRepository) GetFromDB(ctx context.Context, shortCode string) (domain.RedirectLink, error) {
	var redirectLink domain.RedirectLink
	result := r.db.WithContext(ctx).Take(&redirectLink, "short_code = ?", shortCode)
	return redirectLink, result.Error
}

func (r *PostgresRepository) IsRedisNil(err error) bool {
	return errors.Is(err, redis.Nil)
}

func (r *PostgresRepository) IsRecordNotFound(err error) bool {
	return errors.Is(err, gorm.ErrRecordNotFound)
}
