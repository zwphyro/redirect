package handler

import (
	"context"
	"errors"
	"net/http"

	"github.com/zwphyro/redirect/services/redirect-service/internal/service"
	"gorm.io/gorm"

	"github.com/gin-gonic/gin"
)

type Handler struct {
	service *service.RedirectService
}

func NewHandler(service *service.RedirectService) *Handler {
	return &Handler{service: service}
}

func (h *Handler) Redirect(ctx *gin.Context) {
	shortCode := ctx.Param("short_code")

	originalURL, err := h.service.GetOriginalURL(ctx.Request.Context(), shortCode)

	if err == nil {
		ctx.Redirect(http.StatusFound, originalURL)
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
