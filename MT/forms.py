# trainers/forms.py
from django import forms
from django.utils import timezone
from .models import MasterTrainer,Course,MasterTrainerFeedback,MTRecord

YES_NO_CHOICES = [
    ('yes', 'Yes'),
    ('no', 'No'),
]

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
    

class MasterTrainerFeedbackForm(forms.ModelForm):
    class Meta:
        model = MasterTrainerFeedback
        fields = '__all__'
        exclude = ['submitted_at']
        widgets = {
            'trainer_id': forms.TextInput(attrs={'class': 'form-control'}),
            'expectations_met': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'most_useful_part': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'implementation_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'additional_resources': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'follow_up_support': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'application_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'gcp_understanding': forms.RadioSelect(choices=YES_NO_CHOICES),
            'clarity_of_concepts': forms.RadioSelect(choices=YES_NO_CHOICES), 
            'materials_support': forms.RadioSelect(choices=YES_NO_CHOICES),
            'prepared_to_train': forms.RadioSelect(choices=YES_NO_CHOICES),
        }
class MTRecordForm(forms.ModelForm):
    class Meta:
        model = MTRecord
        fields = ['mt_id', 'day', 'question_number', 'image_description', 'photo']
        widgets = {
            'day': forms.Select(choices=[(f"Day {i}", f"Day {i}") for i in range(1, 6)]),
            'question_number': forms.Select(choices=[(i, f"Question {i}") for i in range(1, 11)]),
            'image_description': forms.TextInput(attrs={'placeholder': 'Enter a short description'}),
        }