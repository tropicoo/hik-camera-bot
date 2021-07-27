from marshmallow import (
    INCLUDE, Schema, fields as f, validate as v,
    validates_schema,
)


class BaseTemplate(Schema):
    _inner_validation_schema_cls = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._inner_validation_schema = self._inner_validation_schema_cls()
        self._template_validator = f.String(
            required=True,
            validate=v.Length(min=1))

    @validates_schema
    def validate_all(self, data: dict, **kwargs) -> None:
        for tpl_name, tpl_conf in data.items():
            self._template_validator.validate(tpl_name)
            self._inner_validation_schema.load(tpl_conf)  # noqa

    class Meta:
        unknown = INCLUDE


class Youtube(BaseTemplate):
    class _Youtube(Schema):
        channel = f.Integer(required=True, validate=v.Range(min=1))
        restart_period = f.Integer(required=True, validate=v.Range(min=1))
        restart_pause = f.Integer(required=True, validate=v.Range(min=1))
        url = f.String(required=True, validate=v.Length(min=1))
        key = f.String(required=True, validate=v.Length(min=1))

    _inner_validation_schema_cls = _Youtube


class Icecast(BaseTemplate):
    class _Icecast(Schema):
        class _IceStream(Schema):
            ice_genre = f.String(required=True, validate=v.Length(min=1))
            ice_name = f.String(required=True, validate=v.Length(min=1))
            ice_description = f.String(required=True, validate=v.Length(min=1))
            ice_public = f.Integer(required=True)
            url = f.String(required=True, validate=v.Length(min=1))
            password = f.String(required=True, validate=v.Length(min=1))
            content_type = f.String(required=True, validate=v.Length(min=1))

        channel = f.Integer(required=True, validate=v.Range(min=1))
        restart_period = f.Integer(required=True, validate=v.Range(min=1))
        restart_pause = f.Integer(required=True, validate=v.Range(min=1))
        ice_stream = f.Nested(_IceStream, required=True)

    _inner_validation_schema_cls = _Icecast


class Twitch(BaseTemplate):
    class _Twitch(Schema):
        channel = f.Integer(required=True, validate=v.Range(min=1))
        restart_period = f.Integer(required=True, validate=v.Range(min=1))
        restart_pause = f.Integer(required=True, validate=v.Range(min=1))
        url = f.String(required=True, validate=v.Length(min=1))
        key = f.String(required=True, validate=v.Length(min=1))

    _inner_validation_schema_cls = _Twitch


class Livestream(Schema):
    youtube = f.Nested(Youtube, required=True)
    icecast = f.Nested(Icecast, required=True)
    twitch = f.Nested(Twitch, required=True)
