# products/forms.py
from django import forms
from .models import Product, ProductVariant, ProductSizeGuide

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        # Ensure main image is provided
        # if not cleaned_data.get('main_image'):
        #     self.add_error('main_image', 'Main image is required.')

        # Ensure at least one product variant is provided
        # if not self.instance.variants.exists() and not cleaned_data.get('variants'):
        #     raise forms.ValidationError('At least one product variant is required.')

        # Ensure at least one product size guide is provided
        # if not self.instance.size_guides.exists() and not cleaned_data.get('size_guides'):
        #     raise forms.ValidationError('At least one product size guide is required.')

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
