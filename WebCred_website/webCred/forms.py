from django import forms


class urlForm(forms.Form):
    url = forms.URLField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter URL', 'class' : 'form-control'}))

class articleNameForm(forms.Form):
    articleName = forms.CharField(label = 'Article Title', widget=forms.TextInput(attrs={'placeholder': 'Enter URL', 'class' : 'form-control'}))

class jobForm(forms.Form):
    title = forms.CharField(label = 'Job Title',
            widget=forms.TextInput(attrs={'placeholder': 'VP of Sales'})
    )

    departmentName = forms.CharField(label = 'Department Name',
            widget=forms.TextInput(attrs={'placeholder': 'Sales'})
    )

    companyName = forms.CharField(label = 'Company Name',
            widget=forms.TextInput(attrs={'placeholder': 'Sample Company LLC.'})
    )

    jobDesc = forms.CharField(label = 'Job Description',
            widget=forms.Textarea(attrs={'placeholder': "Want to be part of a globally focused tech team designing consumer products? Innovative ideas. Creative approaches. Insatiable curiosity. That's what we expect"}),
    )

    requirements = forms.CharField(label = "Requirements",
            widget=forms.Textarea(attrs={'placeholder': '5 Years of Sales Experience \nDegree in finance \nPositive Attitude \nWilling to lead'}),
    )
