package broker

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/google/uuid"
	amqp "github.com/rabbitmq/amqp091-go"
	"github.com/zwphyro/redirect/services/redirect-service/internal/config"
	"github.com/zwphyro/redirect/services/redirect-service/internal/domain"
)

func InitRabbitMQ(config config.RabbitMQ) (*amqp.Connection, error) {
	return amqp.Dial(fmt.Sprintf("amqp://%s:%s@%s:%s/",
		config.User,
		config.Password,
		config.Host,
		config.Port,
	))
}

type RabbitMQProducer struct {
	connection  *amqp.Connection
	channel     *amqp.Channel
	celeryQueue amqp.Queue
}

type CeleryMessage struct {
	ID      string               `json:"id"`
	Task    string               `json:"task"`
	Args    []any                `json:"args"`
	Kwargs  domain.RedirectEvent `json:"kwargs"`
	Retries int                  `json:"retries"`
	Eta     any                  `json:"eta"`
}

func NewRabbitMQProducer(connection *amqp.Connection) (*RabbitMQProducer, error) {
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

	return &RabbitMQProducer{
		connection:  connection,
		channel:     channel,
		celeryQueue: queue,
	}, nil
}

func (p *RabbitMQProducer) PublishRedirect(
	ctx context.Context,
	event domain.RedirectEvent,
) error {
	task := CeleryMessage{
		ID:     uuid.New().String(),
		Task:   "src.redirect_events.task.store_redirect_events",
		Args:   []any{},
		Kwargs: event,
	}

	body, err := json.Marshal(task)
	if err != nil {
		return err
	}

	return p.channel.PublishWithContext(
		ctx,
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

func (p *RabbitMQProducer) Close() error {
	return p.connection.Close()
}
