from django.db import models
import datetime
from django.db.models import Max  # Import Max here
from django.utils import timezone

# Create your models here.

class Course(models.Model):
    state = models.CharField(max_length=100)
    state_agency = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    venue_name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.course_name} ({self.state})"
class MasterTrainer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    specialization_subject = models.CharField(max_length=100)
    institution =models.CharField(max_length=100)
    experience_years_gis = models.PositiveIntegerField()
    experience_details = models.TextField()
    city =models.CharField(max_length=100)
    district =models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    regis_date = models.DateField(auto_now_add=True)  
    # courses = models.ManyToManyField(Course)  # Linking to Course model
# Custom ID field
    id = models.CharField(max_length=20, unique=True, blank=True,primary_key=True)

    def save(self, *args, **kwargs):
        if not self.id:  # Only generate a new ID if not already set
            state_abbreviation = self.state[:2].upper()  # Get the first two letters of the state abbreviation
            today_date = datetime.datetime.today().strftime('%Y%m%d')  # Get the current date in YYYYMMDD format
            
            # Get the highest existing ID for today and the same state, then increment it
            last_id = MasterTrainer.objects.filter(id__startswith=f'MTas{state_abbreviation}{today_date}').aggregate(Max('id'))
            last_number = last_id['id__max']
            
            if last_number:
                # Extract the number from the last ID and increment by 1
                last_increment = int(last_number[-1])  # Get the last digit from the previous ID
                new_increment = last_increment + 1
            else:
                # Start with 1 if it's the first record for today and the given state
                new_increment = 1
            
            # Construct the new ID
            self.id = f'MT{state_abbreviation}{today_date}{new_increment}'

        super(MasterTrainer, self).save(*args, **kwargs)  # Call the parent save method

    

    def __str__(self):
        return self.name
       
class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="attendances")
    training_date = models.DateField()
    master_trainers = models.ManyToManyField("MasterTrainer")  # Many trainers can attend

    @property
    def venue_name(self):
        return self.course.venue_name  # Fetch venue dynamically

    def __str__(self):
        return f"Attendance for {self.course.course_name} at {self.venue_name} on {self.training_date}"
    

# class MasterTrainerFeedback(models.Model):
#     TRAINING_RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

#     trainer_id = models.CharField(max_length=20, unique=True, verbose_name="Master Trainer ID")
#     overall_effectiveness = models.IntegerField(choices=TRAINING_RATING_CHOICES, verbose_name="Overall Effectiveness (1-5)")
#     expectations_met = models.TextField(verbose_name="Did the training meet your expectations? Why or why not?")
#     most_useful_part = models.TextField(verbose_name="What was the most useful part of the training?")
#     confidence_georeferencing = models.IntegerField(choices=TRAINING_RATING_CHOICES, verbose_name="Confidence in Georeferencing (1-5)")
#     gcp_understanding = models.CharField(verbose_name="Did the session on GCPs help you understand field validation?", choices=[('Yes', 'Yes'), ('No', 'No')])
#     clarity_of_concepts = models.CharField(verbose_name="Were map projections and coordinate systems explained clearly?", choices=[('Yes', 'Yes'), ('No', 'No')])
#     implementation_challenges = models.TextField(verbose_name="Challenges in implementing georeferencing and ground truthing")
#     hands_on_effectiveness = models.IntegerField(choices=TRAINING_RATING_CHOICES, verbose_name="Effectiveness of Hands-on Exercises (1-5)")
#     materials_support = models.BooleanField(verbose_name="Did training materials support your learning effectively?")
#     additional_resources = models.TextField(verbose_name="Additional resources/topics that would have helped")
#     prepared_to_train = models.CharField(verbose_name="Do you feel prepared to train others?", choices=[('Yes', 'Yes'), ('No', 'No')])
#     follow_up_support = models.TextField(verbose_name="What kind of follow-up support would be helpful?")
#     application_plan = models.TextField(verbose_name="How do you plan to apply georeferencing in projects?")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Feedback from Trainer {self.trainer_id}"


class MasterTrainerFeedback(models.Model):
    from django.db import models

class MasterTrainerFeedback(models.Model):
    trainer_id = models.CharField(max_length=100)

    # Star rating questions (integers from 1 to 5)
    qgis_installation = models.IntegerField()
    qfield_installation = models.IntegerField()
    import_xls = models.IntegerField()
    merge_shapefiles = models.IntegerField()
    read_census_codes = models.IntegerField()
    upload_shapefile = models.IntegerField()
    download_shapefile = models.IntegerField()
    set_crs = models.IntegerField()
    georeference_image = models.IntegerField()
    trace_polygons = models.IntegerField()
    transfer_qfield_project = models.IntegerField()
    map_projections = models.IntegerField()
    gis_concepts = models.IntegerField()

    # Dropdowns (Yes/No answers)
    materials_support = models.CharField(max_length=10, choices=[("Yes", "Yes"), ("No", "No")])
    prepared_to_train = models.CharField(max_length=10, choices=[("Yes", "Yes"), ("No", "No")])

    # Text areas
    most_useful_part = models.TextField(blank=True, null=True)
    follow_up_support = models.TextField(blank=True, null=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.trainer_id}"

class MTRecord(models.Model):
    mt_id = models.CharField(max_length=20)
    day = models.CharField(max_length=20)  # increased
    question_number = models.CharField(max_length=20)  # increased
    image_description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='mt_photos/')
    datetime = models.DateTimeField(auto_now_add=True)  # automatically non-editable
    
    class Meta:
        db_table = 'MT_mtrecord'  # Specify the desired table name
    
    def __str__(self):
        return f"{self.mt_id} - {self.day} - Q{self.question_number}"

class QuizResponse(models.Model):
    trainer_id = models.CharField(max_length=100)
    question = models.TextField()
    selected_option = models.TextField()
    correct_answer = models.TextField()
    date_of_submission = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.trainer_id} - {self.question[:30]}..."

