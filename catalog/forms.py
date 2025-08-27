from django.forms import ModelForm, BooleanField
from catalog.models import Product, Category
from django.core.exceptions import ValidationError


FORBIDDEN_WORDS =  ['казино',
                    'криптовалюта',
                    'крипта',
                    'биржа',
                    'дешево',
                    'бесплатно',
                    'обман',
                    'полиция',
                    'радар']


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    #def __init__(self, *args, **kwargs):
    #    super(ProductForm, self).__init__(*args, **kwargs)
    #    self.fields['name'].widget.attrs.update({
    #        'class': 'form-control',
    #        'placeholder': 'Введите название продукта'
    #    })

    #    self.fields['desc'].widget.attrs.update({
    #        'class': 'form-control',
    #        'placeholder': 'Введите описание'
    #    })

    #    self.fields['image'].widget.attrs.update({
    #        'class': 'form-control',
    #        'accept': 'media/images/*'
    #    })

    #    self.fields['category'].widget.attrs.update({
    #        'class': 'form-control'
    #    })

    #    self.fields['price'].widget.attrs.update({
    #        'class': 'form-control',
    #        'placeholder': 'Введите цену'
    #    })

    #    self.fields['created_at'].widget.attrs.update({
    #        'class': 'form-control',
    #        'type': 'date'
    #    })

    #    self.fields['updated_at'].widget.attrs.update({
    #        'class': 'form-control',
    #        'type': 'date'
    #    })

    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        lowered = name.lower()
        for word in FORBIDDEN_WORDS:
            if word in lowered:
                raise ValidationError(f'Наименование не должно содержать слово "{word}"!')
        return name

    def clean_desc(self):
        description = self.cleaned_data.get("desc", "")
        lowered = description.lower()
        for word in FORBIDDEN_WORDS:
            if word in lowered:
                raise ValidationError(f'Описание не должно содержать слово "{word}"!')
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price <= 0:
            raise ValidationError("Цена не может быть меньше или равна нулю!")
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1025:
                raise ValidationError("Файл больше 5МБ!")
            if not (image.name.endswith('.jpg') or image.name.endswith('.jpeg') or image.name.endswith('.png')):
                raise ValidationError("Недопустимый формат файла!")
        return image

class CategoryForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'desc']