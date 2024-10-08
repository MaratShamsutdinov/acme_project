from django import forms

from django.core.exceptions import ValidationError


# Импорт функции для отправки почты.
from django.core.mail import send_mail


BEATLES = {'Джон Леннон', 'Пол Маккартни', 'Джордж Харрисон', 'Ринго Старр'}


class BirthdayForm(forms.ModelForm):

    class Meta:
        model = models.Birthday
        fields = [
            'first_name',
            'last_name',
            'birthday',
            'description',
            'image',
            'tags',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name.split()[0]

    def clean(self):
        super().clean()
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if f'{first_name} {last_name}' in BEATLES:

            # Отправляем письмо, если кто-то представляется
            # именем одного из участников Beatles.
            send_mail(
                subject='Another Beatles member',
                message=f'{first_name} {last_name} пытался опубликовать запись!',
                from_email='birthday_form@acme.not',
                recipient_list=['admin@acme.not'],
                fail_silently=True,
            )

            raise ValidationError(
                'Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!'
            )


class CongratulationForm(forms.ModelForm):

    class Meta:
        model = models.Congratulation
        fields = ('text',)

    # !!!--- Явное задание формы ---!!!
    # class BirthdayForm(forms.Form):
    #     first_name = forms.CharField(
    #         label='Имя',
    #         max_length=20
    #     )
    #     last_name = forms.CharField(
    #         label='Фамилия',
    #         required=False,
    #         help_text='Необязательное поле'
    #     )
    #     description = forms.CharField(
    #         label='Описание',
    #         required=False,
    #         help_text='Необязательное поле',
    #         max_length=200,
    #         min_length=5,
    #         widget=forms.Textarea(
    #             attrs={
    #                 'rows': 3,
    #                 'cols': 50,
    #                 'placeholder': 'Введите описание',
    #             }
    #         )
    #     )
    #     birthday = forms.DateField(
    #         label='Дата рождения',
    #         widget=forms.DateInput(
    #             attrs={
    #                 'type': 'date'
    #             }
    #         ),
    #         validators=(
    #             validators.real_age,
    #         ),
    #     )
