package main

import (
	"context"
	"fmt"
	"log"

	"github.com/zwphyro/redirect/services/redirect-service/internal/handler"
	"github.com/zwphyro/redirect/services/redirect-service/internal/middleware"
	"github.com/zwphyro/redirect/services/redirect-service/internal/repository"
	"github.com/zwphyro/redirect/services/redirect-service/internal/service"

	"github.com/gin-gonic/gin"
	"github.com/redis/go-redis/v9"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"

	"github.com/zwphyro/redirect/services/redirect-service/internal/config"
)

func main() {
	cfg := config.LoadConfig()

	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=disable",
		cfg.Postgres.Host,
		cfg.Postgres.User,
		cfg.Postgres.Password,
		cfg.Postgres.DBName,
		cfg.Postgres.Port,
	)

	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatalf("Failed to connect to DB: %v", err)
	}

	addr := fmt.Sprintf("%s:%s", cfg.Redis.Host, cfg.Redis.Port)

	redisClient := redis.NewClient(&redis.Options{
		Addr:     addr,
		Password: cfg.Redis.Password,
		DB:       cfg.Redis.DB,
	})

	if _, err := redisClient.Ping(context.Background()).Result(); err != nil {
		log.Fatalf("Failed to connect to Redis: %v", err)
	}

	redirectRepo := repository.NewRedirectRepository(db, redisClient)
	redirectService := service.NewRedirectService(redirectRepo)
	h := handler.NewHandler(redirectService)

	app := gin.Default()

	app.Use(middleware.Timeout(cfg.HTTPServer.Timeout))

	app.GET("/:short_code", h.Redirect)

	serverAddr := ":" + cfg.HTTPServer.Port
	log.Printf("Server starting on %s", serverAddr)

	if err := app.Run(serverAddr); err != nil {
		log.Fatal(err)
	}
}
