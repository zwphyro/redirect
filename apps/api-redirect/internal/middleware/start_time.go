package middleware

import (
	"time"

	"github.com/gin-gonic/gin"
)

func StartTime() gin.HandlerFunc {
	return func(ctx *gin.Context) {
		startTime := time.Now()
		ctx.Set("startTime", startTime)
		ctx.Next()
	}
}
