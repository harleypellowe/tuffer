from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load


class PostSchema(Schema):
    text = fields.Str()
    tags = fields.List(fields.Str())
    publish_date = fields.Date()
    integrations = fields.List(fields.Str())

    @post_load
    def make_post(self, data, **kwargs) -> "Post":
        from tuffer.models.post import Post
        return Post(**data)

    def __repr__(self) -> str:
        return (
            f"<Post(text={self.text[:30]}, publish_date={self.publish_date})>"
        )
