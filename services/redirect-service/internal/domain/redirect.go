package domain

type RedirectURL struct {
	ShortCode   string `gorm:"column:short_code"`
	OriginalURL string `gorm:"column:original_url"`
}

func (RedirectURL) TableName() string {
	return "redirect_urls"
}
