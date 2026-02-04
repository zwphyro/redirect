package main

import (
	"context"
	"fmt"
	"log"

	"github.com/zwphyro/redirect/services/redirect-service/internal/broker"
	"github.com/zwphyro/redirect/services/redirect-service/internal/handler"
	"github.com/zwphyro/redirect/services/redirect-service/internal/middleware"
	"github.com/zwphyro/redirect/services/redirect-service/internal/repository"
	"github.com/zwphyro/redirect/services/redirect-service/internal/service"

	"github.com/gin-gonic/gin"
	amqp "github.com/rabbitmq/amqp091-go"
	"github.com/redis/go-redis/v9"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"

	"github.com/zwphyro/redirect/services/redirect-service/internal/config"
)

func main() {
	config := config.LoadConfig()

	postgresDSN := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=disable",
		config.Postgres.Host,
		config.Postgres.User,
		config.Postgres.Password,
		config.Postgres.DBName,
		config.Postgres.Port,
	)

	db, err := gorm.Open(postgres.Open(postgresDSN), &gorm.Config{})
	if err != nil {
		log.Fatalf("Failed to connect to DB: %v", err)
	}

	redisAddres := fmt.Sprintf("%s:%s", config.Redis.Host, config.Redis.Port)

	redisClient := redis.NewClient(&redis.Options{
		Addr:     redisAddres,
		Password: config.Redis.Password,
		DB:       config.Redis.DB,
	})

	if _, err := redisClient.Ping(context.Background()).Result(); err != nil {
		log.Fatalf("Failed to connect to Redis: %v", err)
	}

	redirectRepository := repository.NewRedirectRepository(db, redisClient)

	rabbitMQURL := fmt.Sprintf("amqp://%s:%s@%s:%s/",
		config.RabbitMQ.User,
		config.RabbitMQ.Password,
		config.RabbitMQ.Host,
		config.RabbitMQ.Port,
	)

	rabbitMQConnection, err := amqp.Dial(rabbitMQURL)
	if err != nil {
		log.Fatalf("Failed to connect to RabbitMQ: %v", err)
	}

	defer rabbitMQConnection.Close()

	rabbitMQProducer, err := broker.NewRabbitMQProducer(rabbitMQConnection)
	if err != nil {
		log.Fatalf("Failed to create RabbitMQ producer: %v", err)
	}
	defer rabbitMQProducer.Close()

	redirectService := service.NewRedirectService(redirectRepository, rabbitMQProducer)
	redirectHandler := handler.NewHandler(redirectService)

	app := gin.Default()

	app.Use(middleware.Timeout(config.HTTPServer.Timeout))

	app.GET("/:short_code", redirectHandler.Redirect)

	serverAddres := ":" + config.HTTPServer.Port
	log.Printf("Server starting on %s", serverAddres)

	if err := app.Run(serverAddres); err != nil {
		log.Fatal(err)
	}
}
