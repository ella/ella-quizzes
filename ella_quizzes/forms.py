from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

class ResultInlineFormset(BaseInlineFormSet):
    def clean(self):
        super(ResultInlineFormset, self).clean()
        # we need save to populate [changed|deleted|new]_objects
        self.save(commit=False)

        new_choices = set(result.choice for result in self.new_objects + self.changed_objects)
        required_choices = set(range(self.instance.choices))

        missing = required_choices - new_choices
        if missing:
            raise ValidationError('You have to provide a Result for choices (%s).' % ', '.join(map(str, sorted(missing))))

        extra = new_choices - required_choices
        if extra:
            raise ValidationError('You suppliad a Result for choices (%s) that are not defined on the Quiz.' % ', '.join(map(str, sorted(extra))))
