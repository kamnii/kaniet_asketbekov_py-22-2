from django import forms


class ProductCreateForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    price = forms.IntegerField()


class ReviewCreateForm(forms.Form):
    text = forms.CharField(min_length=8, max_length=150)
