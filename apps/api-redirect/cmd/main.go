package main

import (
	"context"
	"log"

	"github.com/zwphyro/redirect/services/redirect-service/internal/broker"
	"github.com/zwphyro/redirect/services/redirect-service/internal/handler"
	"github.com/zwphyro/redirect/services/redirect-service/internal/middleware"
	"github.com/zwphyro/redirect/services/redirect-service/internal/repository"
	"github.com/zwphyro/redirect/services/redirect-service/internal/service"

	"github.com/gin-gonic/gin"

	"github.com/zwphyro/redirect/services/redirect-service/internal/config"
)

func main() {
	config := config.LoadConfig()

	db, err := repository.InitDB(config.Postgres)
	if err != nil {
		log.Fatalf("Failed to connect to DB: %v", err)
	}

	redisClient := repository.InitRedis(config.Redis)
	if _, err := redisClient.Ping(context.Background()).Result(); err != nil {
		log.Fatalf("Failed to connect to Redis: %v", err)
	}

	redirectRepository := repository.NewPostgresRepository(db, redisClient)

	rabbitMQConnection, err := broker.InitRabbitMQ(config.RabbitMQ)
	if err != nil {
		log.Fatalf("Failed to connect to RabbitMQ: %v", err)
	}
	defer rabbitMQConnection.Close()

	redirectProducer, err := broker.NewRabbitMQProducer(rabbitMQConnection)
	if err != nil {
		log.Fatalf("Failed to create RabbitMQ producer: %v", err)
	}
	defer redirectProducer.Close()

	redirectService := service.NewRedirectService(redirectRepository)
	analyticsService := service.NewAnalyticsService(redirectProducer)
	redirectHandler := handler.NewHandler(redirectService, analyticsService)

	app := gin.Default()

	app.Use(middleware.Timeout(config.HTTPServer.Timeout))
	app.Use(middleware.StartTime())

	app.GET("/:short_code", redirectHandler.Redirect)

	serverAddres := ":" + config.HTTPServer.Port
	log.Printf("Server starting on %s", serverAddres)

	if err := app.Run(serverAddres); err != nil {
		log.Fatal(err)
	}
}
