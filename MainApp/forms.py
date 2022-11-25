from django.forms import ModelForm, TextInput, Textarea, CharField, PasswordInput
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from MainApp.models import Comment, Snippet


class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        # Описываем поля, которые будем заполнять в форме
        fields = ['name', 'lang', 'public', 'code']
        labels = {
            'name': '',
            'lang': '',
            'code': ''
        }
        widgets = {
            'name': TextInput(attrs={"placeholder": "Название сниппета",
                                     "class": "blue"}),
            'code': Textarea(attrs={"placeholder": "Код сниппета"})
        }


class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    password1 = CharField(label="password", widget=PasswordInput)
    password2 = CharField(label="password confirm", widget=PasswordInput)

    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")
        if pass1 and pass2 and pass1 == pass2:
            return pass2
        raise ValidationError("Пароли не совпадают или пустые")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image', False)

        if image:

            # validate content type
            main, sub = image.content_type.split('/')
            if not (main == 'image' and sub.lower() in ['jpeg', 'pjpeg', 'png', 'jpg']):
                raise ValidationError('Please use a JPEG or PNG image.')

            # validate file size
            if len(image) > (1 * 1024 * 1024):
                raise ValidationError('Image file too large ( maximum 1mb )')
        else:
            raise ValidationError("Couldn't read uploaded image")
        return image
