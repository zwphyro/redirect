package broker

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/google/uuid"
	amqp "github.com/rabbitmq/amqp091-go"
	"github.com/zwphyro/redirect/services/redirect-service/internal/config"
)

func InitRabbitMQ(config config.RabbitMQ) (*amqp.Connection, error) {
	return amqp.Dial(fmt.Sprintf("amqp://%s:%s@%s:%s/",
		config.User,
		config.Password,
		config.Host,
		config.Port,
	))
}

type RedirectProducer struct {
	connection  *amqp.Connection
	channel     *amqp.Channel
	celeryQueue amqp.Queue
}

type CeleryMessage struct {
	ID      string   `json:"id"`
	Task    string   `json:"task"`
	Args    []any    `json:"args"`
	Kwargs  struct{} `json:"kwargs"`
	Retries int      `json:"retries"`
	Eta     any      `json:"eta"`
}

func NewRedirectProducer(connection *amqp.Connection) (*RedirectProducer, error) {
	channel, err := connection.Channel()
	if err != nil {
		return nil, err
	}

	queue, err := channel.QueueDeclare(
		"celery",
		true,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		return nil, err
	}

	return &RedirectProducer{
		connection:  connection,
		channel:     channel,
		celeryQueue: queue,
	}, nil
}

func (p *RedirectProducer) PublishRedirect(context context.Context, shortCode string) error {
	task := CeleryMessage{
		ID:     uuid.New().String(),
		Task:   "task.store_redirect",
		Args:   []any{shortCode},
		Kwargs: struct{}{},
	}

	body, err := json.Marshal(task)
	if err != nil {
		return err
	}

	return p.channel.PublishWithContext(
		context,
		"",
		"celery",
		false,
		false,
		amqp.Publishing{
			ContentType:     "application/json",
			ContentEncoding: "utf-8",
			Body:            body,
			DeliveryMode:    amqp.Persistent,
		},
	)
}

func (p *RedirectProducer) Close() error {
	return p.connection.Close()
}
