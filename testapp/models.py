import json

from django import forms
from django.db import models
from django_jsonform.models.fields import JSONField as JSONField
from django_jsonform.widgets import JSONFormWidget


class Gender(models.TextChoices):
    M = "m", "m"
    F = "f", "f"
    O = "o", "o"


model_schema = {
    "type": "array",
    "title": "Test Form",
    "items": {
        "type": "object",
        "description": "Test Form",
        "keys": {
            "name": {"type": "string"},
            "gender": {"type": "string", "choices": ["male", "female", "other"]},
        },
    },
}


def xform(value):
    if not value:
        return value
    MAP = {"m": "male", "f": "female", "o": "other"}
    for item in value:
        if len(item["gender"]) != 1:
            continue
        item["gender"] = MAP[item["gender"]]
    return value


class AModel(models.Model):
    name = models.CharField(blank=False, max_length=5)
    desc = models.CharField(blank=False, max_length=5)
    bld = JSONField(blank=False, schema=model_schema)


class GendersFormWidget(JSONFormWidget):
    def render(self, name, value, attrs=None, renderer=None):
        value = json.loads(value)
        xformed_value = json.dumps(xform(value))
        return super().render(name, xformed_value, attrs=attrs, renderer=renderer)


class AModelEditForm(forms.ModelForm):
    class Meta:
        model = AModel
        exclude = []

    def __init__(self, *args, **kwargs):
        """overridden to transform build rules into form schema"""
        super().__init__(*args, **kwargs)
        self.fields["bld"].widget = GendersFormWidget(model_schema)

    def clean(self):
        MAP = {"male": "m", "female": "f", "other": "o"}
        cleaned_data = super().clean()
        for item in cleaned_data["bld"]:
            item["gender"] = MAP[item["gender"]]
        return cleaned_data
