from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        data = form.cleaned_data
        user.username = data['email']  # username not in use
        user.email = data['email']
        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password()

        user.save()
        return user
