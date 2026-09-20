use crate::domain::{SiteId, SiteUrl, UserId};

#[derive(Debug, Clone)]
pub struct Site {
    pub id: Option<SiteId>,
    pub user_id: UserId,
    pub url: SiteUrl,
    pub active: bool,
}

impl Site {
    pub fn new(url: SiteUrl, user_id: UserId) -> Self {
        Self {
            id: None,
            user_id,
            url,
            active: false,
        }
    }

    pub fn with_id(id: SiteId, url: SiteUrl, user_id: UserId, active: bool) -> Self {
        Self {
            id: Some(id),
            user_id,
            url,
            active,
        }
    }
}
