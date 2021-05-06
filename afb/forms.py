from django import forms


# Abstract class for forms, initiating Bootstrap during creation, also init decimal place step in widget based on model
class AFBForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs = {'class': 'form-control'}
            if isinstance(self.fields[field], forms.fields.DecimalField):
                step = 1 / 10 ** self.fields[field].decimal_places
                self.fields[field].widget.attrs.update({"step": "{}".format(step)})
