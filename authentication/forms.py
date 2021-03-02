from django import forms
from authentication.models import User, Blogs, Comments 

class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=200)
    date_of_birth = forms.DateField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'date_of_birth', 'email', 'profile_pic', 'password')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['profile_pic'].required = False


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=200)
    date_of_birth = forms.DateField()
    email = forms.EmailField()
    class Meta():
        model = User
        fields = ('username', 'date_of_birth', 'email', 'profile_pic')

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['profile_pic'].required = False

class writeBlogs(forms.ModelForm):
    title = forms.CharField(max_length=200)
    blog = forms.CharField(widget=forms.Textarea, max_length=500000)

    class Meta():
        model = Blogs
        fields = ('title', 'blog', 'thumbnail')

class commentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea, max_length=50000)

    class Meta():
        model = Comments
        fields = ('comment', )