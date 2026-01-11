package main

import (
	"context"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/redis/go-redis/v9"
)

var RedisClient = redis.NewClient(&redis.Options{
	Addr:     "localhost:6379",
	Password: "",
	DB:       0,
})

func redirect(ctx *gin.Context) {
	id := ctx.Param("id")

	redisContext := context.Background()
	redirectLink, error := RedisClient.Get(redisContext, id).Result()
	if error != nil {
		ctx.JSON(http.StatusNotFound, gin.H{"error": "Not Found"})
		return
	}

	ctx.Redirect(http.StatusFound, redirectLink)
}

func main() {
	app := gin.Default()
	app.GET("/:id", redirect)
	app.Run(":8080")
}
