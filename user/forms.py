from django import forms


class Reg2(forms.Form):
    username = forms.CharField(max_length=30, label='请输入用户名')
    password = forms.CharField(max_length=30, label='请输入密码',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=30, label='再次输入密码',
                                widget=forms.PasswordInput)
    rem = forms.BooleanField(label='记住用户名')

    def clean_username(self):
        name = self.cleaned_data['username']
        if '*' in name:
            raise forms.ValidationError('用户名错误！')
        return name

    def clean(self):
        pwd1 = self.cleaned_data['password']
        pwd2 = self.cleaned_data['password2']
        if pwd1 != pwd2:
            raise forms.ValidationError('两次输入的密码不一致！')
        return self.cleaned_data  # 此处必须返回cleaned_data
