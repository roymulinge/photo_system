from django import forms
from .models import Photo,Tag
from django.contrib.auth.forms import PasswordChangeForm

class PhotoForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple  
    )
    class Meta:
        model = Photo
        fields = ["title", "description", "image", "tags"]


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # Option 1: inline style
            field.widget.attrs.update({
                "style": "border: 1px solid #000; padding: 4px;",
                # Option 2: CSS class (add both if you want)
                "class": "simple-input"
            })