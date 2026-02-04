package broker

import (
	"context"
	"encoding/json"

	"github.com/google/uuid"
	amqp "github.com/rabbitmq/amqp091-go"
)

type RabbitMQProducer struct {
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

func (p *RabbitMQProducer) PublishRedirect(context context.Context, shortCode string) error {
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

func (p *RabbitMQProducer) Close() error {
	return p.connection.Close()
}
