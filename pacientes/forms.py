from django import forms
from .models import Paciente


class PacienteRapidoForm(forms.ModelForm):
    """Formulario corto de creación desde el frontend (reemplaza el alta por /admin/).
    Solo pide lo indispensable primero; el resto de campos del modelo (antecedentes,
    EPS, etc.) se completa después desde la Ficha del Paciente, sin bloquear el
    flujo de firma del día."""

    class Meta:
        model = Paciente
        fields = [
            'tipo_documento', 'documento', 'nombres', 'apellidos',
            'fecha_nacimiento', 'telefono', 'es_menor',
            'acudiente_nombre', 'acudiente_documento', 'acudiente_telefono', 'acudiente_parentesco',
        ]
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'cr-select'}),
            'documento': forms.TextInput(attrs={'class': 'cr-input', 'autofocus': True}),
            'nombres': forms.TextInput(attrs={'class': 'cr-input'}),
            'apellidos': forms.TextInput(attrs={'class': 'cr-input'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'cr-input', 'type': 'date'}),
            'telefono': forms.TextInput(attrs={'class': 'cr-input'}),
            'es_menor': forms.CheckboxInput(attrs={'id': 'id_es_menor'}),
            'acudiente_nombre': forms.TextInput(attrs={'class': 'cr-input'}),
            'acudiente_documento': forms.TextInput(attrs={'class': 'cr-input'}),
            'acudiente_telefono': forms.TextInput(attrs={'class': 'cr-input'}),
            'acudiente_parentesco': forms.TextInput(attrs={'class': 'cr-input'}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('es_menor') and not cleaned.get('acudiente_nombre'):
            self.add_error('acudiente_nombre', 'Obligatorio cuando el paciente es menor de edad.')
        return cleaned
