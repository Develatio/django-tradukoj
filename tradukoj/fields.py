# pylint: disable=W0212
import uuid
from django.db import models
from django.db.models.fields.related_descriptors import (
    ForwardOneToOneDescriptor,
    ReverseOneToOneDescriptor,
)
from django.db.models.fields.reverse_related import OneToOneRel
from django.utils.translation import gettext_lazy as _


class TradukojForwardOneToOneDescriptor(ForwardOneToOneDescriptor):
    def __set__(self, instance, value):
        # TODO: delete previous key on new key set?
        # try:
        #     related_object = self.field.get_cached_value(instance)
        # except KeyError:
        #     val = self.field.get_local_related_value(instance)
        #     if None in val:
        #         related_object = None
        #     else:
        #         related_object = self.get_object(instance)
        # if related_object:
        #     related_object.delete()

        if not value.text and value.auto_key_text is not None:
            value.text = (
                f"{instance._meta.app_label}_{instance._meta.model_name}_{self.field.name}_{uuid.uuid4().hex}"
            )
            value.save()

        return super().__set__(instance, value)


class OneToOneTradukojField(models.ForeignKey):

    # Field flags
    many_to_many = False
    many_to_one = False
    one_to_many = False
    one_to_one = True

    related_accessor_class = ReverseOneToOneDescriptor
    forward_related_accessor_class = TradukojForwardOneToOneDescriptor
    rel_class = OneToOneRel

    description = _("One-to-one tradukoj relationship")

    def __init__(self,
                 to="tradukoj.TranslationKey",
                 on_delete=models.PROTECT,
                 to_field=None,
                 **kwargs):
        kwargs['unique'] = True
        to = "tradukoj.TranslationKey"
        super().__init__(to, on_delete, to_field=None, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if "unique" in kwargs:
            del kwargs['unique']
        return name, path, args, kwargs

    # pylint: disable=W0221
    def formfield(self, **kwargs):
        if self.remote_field.parent_link:
            return None
        return super().formfield(**kwargs)

    def save_form_data(self, instance, data):
        if isinstance(data, self.remote_field.model):
            setattr(instance, self.name, data)
        else:
            setattr(instance, self.attname, data)

    def _check_unique(self, **kwargs):
        # Override ForeignKey since check isn't applicable here.
        return []
