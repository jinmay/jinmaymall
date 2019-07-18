from django import forms

class ProductImageInlineFormset(forms.models.BaseInlineFormSet):

    def clean(self):
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data['is_representative']:
                    count += 1
            except:
                pass
        if count > 1:
            raise forms.ValidationError('대표 사진이 두 장 이상입니다. 하나의 사진만 대표 사진으로 지정해주세요.')