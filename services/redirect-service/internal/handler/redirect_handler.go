package handler

import (
	"context"
	"errors"
	"net/http"
	"time"

	"github.com/zwphyro/redirect/services/redirect-service/internal/broker"
	"github.com/zwphyro/redirect/services/redirect-service/internal/service"
	"gorm.io/gorm"

	"github.com/gin-gonic/gin"
)

type Handler struct {
	service *service.RedirectService
	broker  *broker.RedirectProducer
}

func NewHandler(service *service.RedirectService, broker *broker.RedirectProducer) *Handler {
	return &Handler{service: service, broker: broker}
}

func (h *Handler) Redirect(ctx *gin.Context) {
	shortCode := ctx.Param("short_code")

	originalURL, err := h.service.GetOriginalURL(ctx.Request.Context(), shortCode)

	if err == nil {
		ctx.Redirect(http.StatusFound, originalURL)

		var startTime time.Time
		if t, exsists := ctx.Get("startTime"); !exsists {
			startTime = t.(time.Time)
		}

		go func() {
			h.broker.PublishRedirect(
				ctx.Request.Context(),
				broker.RedirectData{
					Time:      startTime,
					ShortCode: shortCode,
					IP:        ctx.ClientIP(),
					UserAgent: ctx.GetHeader("User-Agent"),
					Language:  ctx.GetHeader("Accept-Language"),
					Origin:    ctx.GetHeader("Origin"),
				},
			)
		}()

		return
	}

	switch {
	// TODO: add custom errors
	case errors.Is(err, gorm.ErrRecordNotFound):
		ctx.JSON(http.StatusNotFound, gin.H{"error": "Redirect URL not found"})
	case errors.Is(err, context.DeadlineExceeded):
		ctx.JSON(http.StatusRequestTimeout, gin.H{"error": "Request timeout"})
	default:
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
	}
}
