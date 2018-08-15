from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from rdmo.core.serializers import MarkdownSerializerMixin
from rdmo.conditions.models import Condition
from rdmo.domain.models import AttributeEntity, Attribute
from rdmo.options.models import OptionSet, Option

from rdmo.questions.models import QuestionSet, Question


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'text',
            'additional_input'
        )


class OptionSetSerializer(serializers.ModelSerializer):

    options = OptionSerializer(many=True)

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'options',
            'conditions'
        )


class AttributeSerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
        )


class AttributeEntitySerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

    id_attribute = serializers.SerializerMethodField()

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'id_attribute',
        )

    def get_id_attribute(self, obj):
        try:
            return {'id': obj.children.get(key='id').pk}
        except AttributeEntity.DoesNotExist:
            return None


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'source',
            'relation',
            'target_text',
            'target_option'
        )


class QuestionSerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

    markdown_fields = ('help', )

    attribute = AttributeSerializer(source='attribute_entity.attribute', default=None)
    optionsets = OptionSetSerializer(many=True)

    verbose_name = serializers.SerializerMethodField()
    verbose_name_plural = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            'id',
            'order',
            'help',
            'text',
            'verbose_name',
            'verbose_name_plural',
            'widget_type',
            'value_type',
            'unit',
            'minimum',
            'maximum',
            'step',
            'attribute',
            'optionsets',
            'is_collection'
        )

    def get_verbose_name(self, obj):
        return obj.verbose_name or _('item')

    def get_verbose_name_plural(self, obj):
        return obj.verbose_name_plural or _('items')


class QuestionSetSerializer(MarkdownSerializerMixin, serializers.ModelSerializer):

    markdown_fields = ('help', )

    questions = QuestionSerializer(many=True)

    next = serializers.SerializerMethodField()
    prev = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    section = serializers.SerializerMethodField()
    subsection = serializers.SerializerMethodField()

    attribute_entity = AttributeEntitySerializer()

    conditions = ConditionSerializer(default=None, many=True)

    verbose_name = serializers.SerializerMethodField()
    verbose_name_plural = serializers.SerializerMethodField()

    class Meta:
        model = QuestionSet
        fields = (
            'id',
            'help',
            'verbose_name',
            'verbose_name_plural',
            'attribute_entity',
            'is_collection',
            'next',
            'prev',
            'progress',
            'section',
            'subsection',
            'questions',
            'conditions'
        )

    def get_prev(self, obj):
        try:
            return QuestionSet.objects.get_prev(obj.pk).pk
        except QuestionSet.DoesNotExist:
            return None

    def get_next(self, obj):
        try:
            return QuestionSet.objects.get_next(obj.pk).pk
        except QuestionSet.DoesNotExist:
            return None

    def get_progress(self, obj):
        try:
            return QuestionSet.objects.get_progress(obj.pk)
        except QuestionSet.DoesNotExist:
            return None

    def get_section(self, obj):
        return {
            'id': obj.subsection.section.id,
            'title': obj.subsection.section.title
        }

    def get_subsection(self, obj):
        return {
            'id': obj.subsection.id,
            'title': obj.subsection.title
        }

    def get_verbose_name(self, obj):
        return obj.verbose_name or _('set')

    def get_verbose_name_plural(self, obj):
        return obj.verbose_name_plural or _('sets')
