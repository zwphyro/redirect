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

var (
	DB *gorm.DB
	// TODO: check on authentication
	RedisClient = redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "root",
		DB:       0,
	})
	RedirectGroup = singleflight.Group{}
)

type RedirectURL struct {
	ShortCode   string `gorm:"column:short_code"`
	OriginalURL string `gorm:"column:original_url"`
}

func (RedirectURL) TableName() string {
	return "redirecturls"
}

func Redirect(ctx *gin.Context) {
	shortCode := ctx.Param("short_code")

	originalURL, err := RedisClient.Get(context.Background(), shortCode).Result()

	if err == nil {
		ctx.Redirect(http.StatusFound, originalURL)
		return
	}

	if errors.Is(err, redis.Nil) {
		var redirectURL RedirectURL
		result := DB.Take(&redirectURL, "short_code = ?", shortCode)

		if result.Error == nil {
			ctx.Redirect(http.StatusFound, redirectURL.OriginalURL)
			RedisClient.Set(context.Background(), shortCode, redirectURL.OriginalURL, 1*time.Minute)
			return
		}

		switch {
		case errors.Is(result.Error, gorm.ErrRecordNotFound):
			ctx.JSON(http.StatusNotFound, gin.H{"error": "Redirect URL not found"})
			return
		}
	}

	switch {
	case errors.Is(err, context.DeadlineExceeded):
		ctx.JSON(http.StatusRequestTimeout, gin.H{"error": "Request timeout"})
		return
	}

	ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
}

func TimeoutMiddleware(timeout time.Duration) gin.HandlerFunc {
	return func(ctx *gin.Context) {
		timeoutContext, cancel := context.WithTimeout(ctx.Request.Context(), timeout)

		defer cancel()

		ctx.Request = ctx.Request.WithContext(timeoutContext)
		ctx.Next()
	}
}

func main() {
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
