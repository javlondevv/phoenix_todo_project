from rest_framework.serializers import ModelSerializer

from apps.about.models import (Banner, Contact, IndexAboutSection,
                               IndexContentSection, IndexService)
from apps.utils import SymbolValidationMixin


class BaseImageUpdateSerializer(SymbolValidationMixin, ModelSerializer):
    # this serializer is used to delete old image after updating
    def update(self, instance, validated_data):
        if "image" in validated_data:
            new_image = validated_data["image"]
            if instance.image:
                instance.image.delete()
            instance.image = new_image

        instance = super().update(instance, validated_data)
        instance.save()
        return instance


class BannerSerializer(BaseImageUpdateSerializer):
    class Meta:
        model = Banner
        fields = (
            "id",
            "title_uz",  # noqa
            "title_ru",  # noqa
            "title_en",  # noqa
            "image",
        )


class IndexAboutSectionSerializer(SymbolValidationMixin, ModelSerializer):
    class Meta:
        model = IndexAboutSection
        fields = (
            "id",
            "title_uz",  # noqa
            "title_ru",  # noqa
            "title_en",  # noqa
            "sub_title_uz",  # noqa
            "sub_title_ru",  # noqa
            "sub_title_en",  # noqa
        )


class IndexContentSectionSerializer(SymbolValidationMixin, ModelSerializer):
    class Meta:
        model = IndexContentSection
        fields = (
            "id",
            "title_uz",  # noqa
            "title_ru",  # noqa
            "title_en",  # noqa
            "sub_title_uz",  # noqa
            "sub_title_ru",  # noqa
            "sub_title_en",  # noqa
            "video",
        )

    # this function is used to delete old video after updating
    def update(self, instance, validated_data):
        if "video" in validated_data:
            new_video = validated_data["video"]
            if instance.video:
                instance.video.delete()
            instance.video = new_video

        instance = super().update(instance, validated_data)
        instance.save()
        return instance


class IndexServiceSerializer(BaseImageUpdateSerializer):
    class Meta:
        model = IndexService
        fields = (
            "id",
            "title_uz",  # noqa
            "title_ru",  # noqa
            "title_en",  # noqa
            "image",
        )


class ContactSerializer(SymbolValidationMixin, ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            "id",
            "address_uz",  # noqa
            "address_ru",  # noqa
            "address_en",  # noqa
            "phone1",
            "phone2",
            "email1",
            "email2",
            "map",
            "instagram",
            "facebook",
            "telegram",
        )
