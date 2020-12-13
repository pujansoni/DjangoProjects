from django import forms
from myapp.models import Order, Review, Student
from django.forms import ModelForm
from string import Template
from django.utils.safestring import mark_safe
from django.forms import ImageField


class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, **kwargs):
        html = Template("""<img src="/media/$link"/>""")
        return mark_safe(html.substitute(link=value))


class SearchForm(forms.Form):
    LENGTH_CHOICES = [
        (8, '8 Weeks'),
        (10, '10 Weeks'),
        (12, '12 Weeks'),
        (14, '14 Weeks'),
    ]
    name = forms.CharField(max_length=100, required=False, label="Student Name")
    length = forms.TypedChoiceField(widget=forms.RadioSelect, choices=LENGTH_CHOICES,
                                    coerce=int, required=False, label="Preferred course duration")
    max_price = forms.IntegerField(min_value=0, label="Maximum Price")


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['courses', 'student', 'order_status']
        widgets = {'courses': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect}
        labels = {'student': u'Student Name', }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'course', 'rating', 'comments']
        widgets = {'course': forms.RadioSelect()}
        labels = {'reviewer': u'Please enter a valid email',
                  'rating': u'Rating: An integer between 1 (worst) and 5 (best)', }


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'username', 'password', 'level', 'address', 'province',
                  'registered_courses', 'interested_in', 'profile_image']


class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'username', 'level', 'address', 'province',
                  'registered_courses', 'interested_in', 'profile_image']
        # widgets = {'profile_image': PictureWidget}


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
