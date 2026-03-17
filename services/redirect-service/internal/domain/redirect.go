package domain

type RedirectLink struct {
	ShortCode string `gorm:"column:short_code"`
	TargetURL string `gorm:"column:target_url"`
}

func (RedirectLink) TableName() string {
	return "redirect_links"
}
