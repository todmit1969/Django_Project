from django.forms import ModelForm
from .models import Product
from django.core.exceptions import ValidationError

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price"]

    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        lowered = name.lower()
        for word in FORBIDDEN_WORDS:
            if word in lowered:
                raise ValidationError(f'Название не должно содержать слово "{word}".')
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description", "")
        lowered = description.lower()
        for word in FORBIDDEN_WORDS:
            if word in lowered:
                raise ValidationError(f'Описание не должно содержать слово "{word}".')
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return price