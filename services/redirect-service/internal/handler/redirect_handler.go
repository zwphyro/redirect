package handler

import (
	"context"
	"errors"
	"net/http"
	"time"

	"github.com/zwphyro/redirect/services/redirect-service/internal/service"
	"gorm.io/gorm"

	"github.com/gin-gonic/gin"
)

type RedirectBroker interface {
	PublishRedirect(
		ctx context.Context,
		timestamp int64,
		shortCode string,
		ip string,
		userAgent string,
		language string,
		origin string,
	) error
	Close() error
}

type Handler struct {
	service *service.RedirectService
	broker  RedirectBroker
}

func NewHandler(service *service.RedirectService, broker RedirectBroker) *Handler {
	return &Handler{service: service, broker: broker}
}

func (h *Handler) Redirect(ctx *gin.Context) {
	shortCode := ctx.Param("short_code")

	originalURL, err := h.service.GetOriginalURL(ctx.Request.Context(), shortCode)

	if err == nil {
		ctx.Redirect(http.StatusFound, originalURL)

		ip := ctx.ClientIP()
		userAgent := ctx.GetHeader("User-Agent")
		language := ctx.GetHeader("Accept-Language")
		origin := ctx.GetHeader("Origin")

		var timestamp int64
		if startTime, exsists := ctx.Get("startTime"); exsists {
			timestamp = startTime.(time.Time).Unix()
		}

		go func() {
			h.broker.PublishRedirect(ctx.Request.Context(), timestamp, shortCode, ip, userAgent, language, origin)
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
