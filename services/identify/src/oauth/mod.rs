use strum::EnumString;

#[derive(EnumString, PartialEq, Debug, Clone, Copy)]
#[strum(serialize_all = "SCREAMING_SNAKE_CASE")]
pub enum OAuthProviders {
    Google,
}
