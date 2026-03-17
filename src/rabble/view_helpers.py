import json
from django.middleware.csrf import get_token
from django.urls import reverse


def serialize_form(form, extra_fields=None):
    """Serialize a Django form into a JSON-serializable dict for Vue components."""
    fields = {}
    for name, field in form.fields.items():
        bf = form[name]
        field_data = {
            'name': name,
            'label': str(field.label or name),
            'value': bf.value() if bf.value() is not None else '',
            'errors': [str(e) for e in bf.errors],
            'required': field.required,
            'type': _get_field_type(field),
            'placeholder': field.widget.attrs.get('placeholder', ''),
            'attrs': {
                k: v
                for k, v in field.widget.attrs.items()
                if k not in ('placeholder',)
            },
        }
        if hasattr(field, 'choices'):
            field_data['choices'] = [
                {'value': str(c[0]), 'label': str(c[1])}
                for c in field.choices
                if c[0] != ''
            ]
        if hasattr(field, 'queryset'):
            field_data['choices'] = [
                {'value': str(obj.pk), 'label': str(obj)}
                for obj in field.queryset
            ]
        if hasattr(field, 'help_text') and field.help_text:
            field_data['help_text'] = str(field.help_text)
        fields[name] = field_data

    result = {
        'fields': fields,
        'non_field_errors': [str(e) for e in form.non_field_errors()],
        'is_edit': bool(form.instance.pk) if hasattr(form, 'instance') else False,
    }
    if extra_fields:
        result.update(extra_fields)
    return result


def _get_field_type(field):
    widget_class = type(field.widget).__name__
    type_map = {
        'TextInput': 'text',
        'Textarea': 'textarea',
        'CheckboxInput': 'checkbox',
        'PasswordInput': 'password',
        'EmailInput': 'email',
        'FileInput': 'file',
        'Select': 'select',
        'SelectMultiple': 'select-multiple',
        'Select2MultipleWidget': 'select-multiple',
    }
    return type_map.get(widget_class, 'text')


def page_context(request, data):
    """Wrap page data with common context (csrf_token, auth info)."""
    data['csrf_token'] = get_token(request)
    data['is_authenticated'] = request.user.is_authenticated
    if request.user.is_authenticated:
        data['username'] = request.user.username
        data['user_id'] = request.user.id
    return data
