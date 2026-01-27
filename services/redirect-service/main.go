package main

import (
	"context"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/redis/go-redis/v9"
	"golang.org/x/sync/singleflight"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var (
	DB          *gorm.DB
	RedisClient = redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "",
		DB:       0,
	})
	RedirectGroup = singleflight.Group{}
)

type RedirectURL struct {
	gorm.Model
	ShortCode   string
	OriginalURL string
}

func Redirect(ctx *gin.Context) {
	id := ctx.Param("id")

	redirectURL, err := RedisClient.Get(context.Background(), id).Result()

	if err == nil {
		ctx.Redirect(http.StatusFound, redirectURL)
		return
	}

	switch err {
	case redis.Nil:
		ctx.JSON(http.StatusNotFound, gin.H{"error": "Not Found"})
		return
	case context.DeadlineExceeded:
		ctx.JSON(http.StatusRequestTimeout, gin.H{"error": "Request Timeout"})
		return
	}

	ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Internal Server Error"})
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
	app.GET("/:id", Redirect)
	app.Run(":8001")
}
