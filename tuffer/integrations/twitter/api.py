import webbrowser
from dataclasses import dataclass
from typing import ClassVar

import requests
from requests_oauthlib import OAuth1

from tuffer import load_config
from tuffer.integrations.twitter.exceptions import TwitterRequestTokenException
from tuffer.integrations.twitter.exceptions import TwitterAccessTokenException

config_data = load_config()
twitter_config = config_data.get("twitter", dict())


@dataclass
class Twitter:
    BASE_URL: ClassVar[str] = "https://api.twitter.com"
    CONSUMER_KEY: ClassVar[str] = None
    CONSUMER_KEY_SECRET: ClassVar[str] = None
    oauth_token: str = None
    oauth_token_secret: str = None

    def __post_init__(self):
        app_config = twitter_config.get("app")
        assert app_config is not None

        self.CONSUMER_KEY = app_config["consumer_key"]
        self.CONSUMER_KEY_SECRET = app_config["consumer_key_secret"]

        if self.oauth_token is None:
            self.request_token()
            pin_code = self.authorize()
            self.request_access_token(oauth_verifier=pin_code)

    def request_token(self):
        url = f"{self.BASE_URL}/oauth/request_token"
        use_pin_based_auth = "oob"
        auth = OAuth1(
            client_key=self.CONSUMER_KEY,
            client_secret=self.CONSUMER_KEY_SECRET,
            callback_uri=use_pin_based_auth,
            signature_method="HMAC-SHA1",
        )
        response = self.make_request(method="POST", url=url, auth=auth)
        if response.status_code != 200:
            return TwitterRequestTokenException

        fields = self.parse_raw_response_body(response.text)
        self.oauth_token = fields.get("oauth_token")
        self.oauth_token_secret = fields.get("oauth_token_secret")

    def authorize(self):
        assert self.oauth_token is not None

        url = f"{self.BASE_URL}/oauth/authorize?oauth_token={self.oauth_token}"
        print(
            "After authorizing Tuffer in your web browser, place the PIN code"
            "provided by Twitter below."
        )
        webbrowser.open(url)
        return input("PIN code:")

    def request_access_token(self, oauth_verifier: str):
        url = f"{self.BASE_URL}/oauth/access_token"
        params = dict(
            oauth_token=self.oauth_token, oauth_verifier=oauth_verifier
        )
        response = self.make_request(method="GET", url=url, params=params)
        if response.status_code != 200:
            return TwitterAccessTokenException

        fields = self.parse_raw_response_body(response.text)
        self.oauth_token = fields.get("oauth_token")
        self.oauth_token_secret = fields.get("oauth_token_secret")

    @staticmethod
    def parse_raw_response_body(text: str) -> dict:
        fields = text.split("&")
        payload = dict()
        for field in fields:
            key, value = field.split("=")
            payload[key] = value
        return payload

    @staticmethod
    def make_request(
        method: str,
        url: str,
        auth: OAuth1 = None,
        data: dict = None,
        headers: dict = None,
        params: dict = None,
    ) -> requests.Response:
        return requests.request(
            method=method,
            url=url,
            auth=auth,
            data=data,
            headers=headers,
            params=params,
        )
