package handler

import (
	"context"
	"errors"
	"net/http"
	"time"

	"github.com/zwphyro/redirect/services/redirect-service/internal/domain"
	"github.com/zwphyro/redirect/services/redirect-service/internal/service"
	"gorm.io/gorm"

	"github.com/gin-gonic/gin"
)

type RedirectHandler struct {
	redirectService  *service.RedirectService
	analyticsService *service.AnalyticsService
}

func NewHandler(redirectService *service.RedirectService, analyticsService *service.AnalyticsService) *RedirectHandler {
	return &RedirectHandler{
		redirectService:  redirectService,
		analyticsService: analyticsService,
	}
}

func (h *RedirectHandler) Redirect(ctx *gin.Context) {
	shortCode := ctx.Param("short_code")

	targetURL, err := h.redirectService.GetTargetURL(ctx.Request.Context(), shortCode)

	if err == nil {
		ctx.Redirect(http.StatusFound, targetURL)

		var startTime time.Time
		if t, exsists := ctx.Get("startTime"); exsists {
			startTime = t.(time.Time)
		}

		event := domain.RedirectEvent{
			EventTime: startTime,
			ShortCode: shortCode,
			IP:        ctx.ClientIP(),
			UserAgent: ctx.GetHeader("User-Agent"),
			Language:  ctx.GetHeader("Accept-Language"),
			Origin:    ctx.GetHeader("Origin"),
		}

		go h.analyticsService.PublishRedirectEvent(event)

		return
	}

	switch {
	// TODO: add custom errors
	case errors.Is(err, gorm.ErrRecordNotFound):
		ctx.JSON(http.StatusNotFound, gin.H{"error": "Redirect link not found"})
	case errors.Is(err, context.DeadlineExceeded):
		ctx.JSON(http.StatusRequestTimeout, gin.H{"error": "Request timeout"})
	default:
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
	}
}
