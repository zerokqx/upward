use serde::Deserialize;
use utoipa::{IntoParams, ToSchema};

use crate::domain::UserId;

/// DTO query-параметров для получения пингов сайта
#[derive(Debug, Deserialize, ToSchema, IntoParams)]
#[into_params(parameter_in = Query)]
pub struct GetPingsDto {
    /// Идентификатор пользователя-владельца (извлекается BFF из JWT)
    #[param(value_type = String, example = "usr_01J8ABCDEF1234567890")]
    pub user_id: UserId,
}
