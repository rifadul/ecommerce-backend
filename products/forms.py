from django import forms
from .models import Product, ProductVariant, ProductSizeGuide

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class ProductVariantInlineForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('color'):
            raise forms.ValidationError('Variant color is required.')
        if not cleaned_data.get('size'):
            raise forms.ValidationError('Variant size is required.')
        if not cleaned_data.get('quantity'):
            raise forms.ValidationError('Variant quantity is required.')
        if not cleaned_data.get('image'):
            raise forms.ValidationError('Variant image is required.')
        return cleaned_data

class ProductSizeGuideInlineForm(forms.ModelForm):
    class Meta:
        model = ProductSizeGuide
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('size'):
            raise forms.ValidationError('Size guide size is required.')
        if not cleaned_data.get('chest'):
            raise forms.ValidationError('Size guide chest is required.')
        if not cleaned_data.get('length'):
            raise forms.ValidationError('Size guide length is required.')
        if not cleaned_data.get('sleeve'):
            raise forms.ValidationError('Size guide sleeve is required.')
        return cleaned_data
