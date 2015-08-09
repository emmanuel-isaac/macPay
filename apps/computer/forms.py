from django.forms import ModelForm

from apps.computer.models import Computer


class ComputerCreationForm(ModelForm):

    class Meta:
        model = Computer
        fields = ['name', 'model', 'cost']
