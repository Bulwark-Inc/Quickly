from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 "
                         "file:rounded file:border-0 file:text-sm file:font-semibold "
                         "file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            }
        )
    )

    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "block w-full rounded-md border border-gray-300 p-3 text-gray-900 "
                         "dark:bg-gray-700 dark:text-white focus:ring-blue-500 focus:border-blue-500"
            }
        )
    )

    school_portal_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "block w-full rounded-md border border-gray-300 p-3 text-gray-900 "
                         "dark:bg-gray-700 dark:text-white focus:ring-blue-500 focus:border-blue-500"
            }
        )
    )

    class Meta:
        model = User
        fields = ['profile_picture', 'phone_number', 'school_portal_password']
