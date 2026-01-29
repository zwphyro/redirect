package main

import (
	"context"
	"errors"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/redis/go-redis/v9"
	"golang.org/x/sync/singleflight"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

// TODO: add logging

// --- Singletons setups ---

var (
	DB *gorm.DB
	// TODO: check authentification error
	RedisClient = redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "root",
		DB:       0,
	})
	RedirectGroup = singleflight.Group{}
)

// --- Models ---

type RedirectURL struct {
	ShortCode   string `gorm:"column:short_code"`
	OriginalURL string `gorm:"column:original_url"`
}

func (RedirectURL) TableName() string {
	return "redirecturls"
}

func GetOriginalURL(shortCode string) (string, error) {
	originalURL, err := RedisClient.Get(context.Background(), shortCode).Result()

	if err == nil {
		return originalURL, nil
	}

	if !errors.Is(err, redis.Nil) {
		return "", err
	}

	result, err, _ := RedirectGroup.Do(shortCode, func() (any, error) {
		var redirectURL RedirectURL
		result := DB.Take(&redirectURL, "short_code = ?", shortCode)

		if result.Error == nil {
			RedisClient.Set(context.Background(), shortCode, redirectURL.OriginalURL, 1*time.Minute)
		}

		return redirectURL.OriginalURL, result.Error
	})

	originalURL = result.(string)

	return originalURL, err
}

// --- Routes/Views ---

func Redirect(ctx *gin.Context) {
	shortCode := ctx.Param("short_code")

	originalURL, err := GetOriginalURL(shortCode)

	if err == nil {
		ctx.Redirect(http.StatusFound, originalURL)
		return
	}

	switch {
	case errors.Is(err, context.DeadlineExceeded):
		ctx.JSON(http.StatusRequestTimeout, gin.H{"error": "Request timeout"})
		return
	case errors.Is(err, gorm.ErrRecordNotFound):
		ctx.JSON(http.StatusNotFound, gin.H{"error": "Redirect URL not found"})
		return
	}

	ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
}

// --- Middleware ---

func TimeoutMiddleware(timeout time.Duration) gin.HandlerFunc {
	return func(ctx *gin.Context) {
		timeoutContext, cancel := context.WithTimeout(ctx.Request.Context(), timeout)

		defer cancel()

		ctx.Request = ctx.Request.WithContext(timeoutContext)
		ctx.Next()
	}
}

// --- Entrypoint ---

func main() {
	// # TODO: read values from .env config
	dns := "host=localhost user=admin password=root dbname=redirect_db port=5432 sslmode=disable"
	var err error
	DB, err = gorm.Open(postgres.Open(dns), &gorm.Config{})
	if err != nil {
		panic(err)
	}

	app := gin.Default()
	app.Use(TimeoutMiddleware(1 * time.Second))
	app.GET("/:short_code", Redirect)
	app.Run(":8001")
}
