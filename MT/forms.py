# trainers/forms.py
from django import forms
from django.utils import timezone
from .models import MasterTrainer,Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['state', 'state_agency', 'course_name', 'venue_name', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MasterTrainerForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),  # Fetch all courses
        empty_label="Select Course",    # Optional: Placeholder text
        widget=forms.Select(attrs={'class': 'form-control'})  # Optional: Add Bootstrap styling
    )
    
# Adding Bootstrap classes to the form fields
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}))
    specialization_subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter specialization subject'}))
    experience_years_gis = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter years of GIS experience'}))
    details_experience = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter detailed experience'}))

    # Optional: Add more styling or helper classes if needed
    # For example, adding labels with a custom class
    name.label = 'Full Name'
    email.label = 'Email Address'
    phone_number.label = 'Phone Number'
    specialization_subject.label = 'Specialization Subject'
    experience_years_gis.label = 'Years of GIS Experience'
    details_experience.label = 'Detailed Experience'
    # widgets = {
    #         'courses': forms.CheckboxSelectMultiple(),  # Allow multiple course selections
    #     }
    class Meta:
        model = MasterTrainer
        # fields = ['name', 'email', 'phone_number', 'specialization_subject', 'experience_years_gis', 'deatils_experience']
        #fields = '__all__'
        exclude = ['id', 'regis_date']
    def save(self, commit=True):
        instance = super(MasterTrainerForm, self).save(commit=False)
        if not instance.regis_date:
            instance.regis_date = timezone.now().date()  # Set today's date
        if commit:
            instance.save()
        return instance