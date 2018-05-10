from django import forms
import re 

class HomeForm(forms.Form):
	post = forms.CharField(label='', max_length=7
		,widget = forms.TextInput (
		attrs={
			'class':'form-control input-lg',
			'placeholder' : 'Ex: WRT 102',
		}
		)
	)

	def clean_post(self):
		data = self.cleaned_data['post']
		pattern = re.compile('[a-zA-Z]{3} \d{3}')
		if not pattern.match(data):
			raise forms.ValidationError("Please enter a valid class")
		return data