from django import forms
from .models import Post, Answer

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
        if count == 0:
            raise forms.ValidationError('대표 사진이 없습니다. 하나의 사진으르 대표사진으로 지정해주세요.')
            

class QnaForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title', 'content', )


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('content', )