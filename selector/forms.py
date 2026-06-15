from django import forms

from .models import RoomCondition

# Plausible indoor temperature bounds (°C) for server-side validation.
TEMPERATURE_MIN = -30
TEMPERATURE_MAX = 60


class RoomConditionForm(forms.ModelForm):
    """The six microclimate parameters entered by the user."""

    class Meta:
        model = RoomCondition
        fields = [
            "light_level",
            "humidity",
            "temperature",
            "room_size",
            "has_pets",
            "care_time",
        ]
        widgets = {
            "temperature": forms.NumberInput(
                attrs={"min": TEMPERATURE_MIN, "max": TEMPERATURE_MAX, "step": 1}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap classes in one place instead of repeating per field.
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(widget, forms.Select):
                widget.attrs.setdefault("class", "form-select")
            else:
                widget.attrs.setdefault("class", "form-control")

    def clean_temperature(self):
        temperature = self.cleaned_data["temperature"]
        if not TEMPERATURE_MIN <= temperature <= TEMPERATURE_MAX:
            raise forms.ValidationError(
                f"Укажите реалистичную температуру (от {TEMPERATURE_MIN} "
                f"до {TEMPERATURE_MAX} °C)."
            )
        return temperature
