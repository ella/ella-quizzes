from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from app_data.forms import multiform_factory
from .models import Result

ResultMultiForm = multiform_factory(Result)

class ResultInlineFormset(BaseInlineFormSet):
    def clean(self):
        super(ResultInlineFormset, self).clean()

        # non-valid Quiz, don't bother
        if self.instance.choices is None:
            return

        required_choices = set(range(self.instance.choices))

        new_choices = set()
        # go through existing Results and check
        for form in self.initial_forms:
            # deleted form, skip
            if self.can_delete and self._should_delete_form(form):
                continue
            new_choices.add(form.cleaned_data['choice'])

        # new Results
        for form in self.extra_forms:
            # not changed, not adding a Result
            if not form.has_changed():
                continue
            new_choices.add(form.cleaned_data['choice'])

        missing = required_choices - new_choices
        if missing:
            raise ValidationError('You have to provide a Result for choices (%s).' % ', '.join(map(str, sorted(missing))))

        extra = new_choices - required_choices
        if extra:
            raise ValidationError('You suppliad a Result for choices (%s) that are not defined on the Quiz.' % ', '.join(map(str, sorted(extra))))
