from django.forms import ModelForm
from . models import Flight
from django import forms


# Create the adding hunt form
class CreateHuntForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args,**kwargs)
        # erase all labels. purpose: doing this here only for not write a lot
        for f in self.fields:
            self.fields[f].label = ''

    class Meta:
        model = Flight

        # can change labels in this way, but... more write:
        # labels = {
        #     "image_load": ""
        # }

        # selecting fields to input by user. rest are going to be saved automatically
        fields = ['image_load', 'title', 'body',
                  'flight_url', 'price_amount', 'depart_on', 'arrive_on',
                  'airline']

        # styling all inputs. ImageField is switched to display off.
        # Purpose: styling of Django's FileInput's button is impossible.
        # But there is possibility of styling related label
        # which is made in create.html file
        widgets = {
            'image_load': forms.ClearableFileInput(
                attrs={
                    'class': 'primary small',
                    'style': "display: none",
                },

            ),

            'title': forms.TextInput(
                attrs={
                    'class': 'mt-10 single-input',
                    'placeholder': 'Tytuł',
                    'onfocus': "this.placeholder = ''",
                    'onblur': "this.placeholder = 'Tytuł'"
                }
            ),

            'body': forms.TextInput(
                attrs={
                    'class': 'mt-10  single-input',
                    'placeholder': 'Opis',
                    'onfocus': "this.placeholder = ''",
                    'onblur': "this.placeholder = 'Opis'"
                }
            ),

            'flight_url': forms.URLInput(
                attrs={
                    'class': 'mt-10  single-input',
                    'placeholder': 'Link do lotu',
                    'onfocus': "this.placeholder = ''",
                    'onblur': "this.placeholder = 'Link do lotu'"
                }
            ),

            'price_amount': forms.NumberInput(
                attrs={
                    'class': 'mt-10  single-input',
                    'placeholder': 'Cena lotu',
                    'onfocus': "this.placeholder = ''",
                    'onblur': "this.placeholder = 'Cena lotu'"
                }
            ),

            'depart_on': forms.DateInput(
                attrs={
                    'class': 'datepicker mt-10  single-input',
                    'placeholder': 'Data wylotu',
                    'onfocus': "this.placeholder = ''",
                    'onblur': "this.placeholder = 'Data wylotu'"
                }
            ),

            'arrive_on': forms.DateInput(
                attrs={
                    'class': 'datepicker mt-10 single-input',
                    'placeholder': 'Data przylotu',
                    'onfocus': "this.placeholder = ''",
                    'onblur': "this.placeholder = 'Data przylotu'"
                }
            ),

            'airline': forms.TextInput(
                attrs={
                    'class': 'mt-10 single-input',
                    'placeholder': 'Linia',
                    'onfocus': "this.placeholder = ''",
                    'onblur': "this.placeholder = 'Linia'"
                }
            ),

        }
