config_data = load_config()

twitter_config = config_data.get("twitter", dict())
twitter = Twitter(**twitter_config)

config_data = dict(
    twitter=dict(
        oauth_token=twitter.oauth_token, oauth_token_secret=twitter.oauth_token_secret
    )
)
write_config(config_data)
