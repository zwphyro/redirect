package config

import (
	"log"
	"time"

	"github.com/ilyakaznacheev/cleanenv"
)

type Config struct {
	HTTPServer HTTPServer
	Postgres   Postgres
	Redis      Redis
}

type HTTPServer struct {
	Port    string        `env:"REDIRECT_SERVICE_PORT" env-default:"8001"`
	Timeout time.Duration `env:"REDIRECT_TIMEOUT" env-default:"1s"`
}

type Postgres struct {
	Host     string `env:"POSTGRES_HOST" env-required:"true"`
	Port     string `env:"POSTGRES_PORT" env-required:"true"`
	User     string `env:"POSTGRES_USER" env-required:"true"`
	Password string `env:"POSTGRES_PASSWORD" env-required:"true"`
	DBName   string `env:"POSTGRES_DB" env-required:"true"`
}

type Redis struct {
	Host     string `env:"REDIS_HOST" env-required:"true"`
	Port     string `env:"REDIS_PORT" env-required:"true"`
	Password string `env:"REDIS_PASSWORD" env-default:""`
	DB       int    `env:"REDIS_DB" env-default:"0"`
}

func LoadConfig() *Config {
	var cfg Config

	if err := cleanenv.ReadConfig("../../.env", &cfg); err != nil {
		log.Fatalf("cannot read config: %s", err)
	}

	return &cfg
}
