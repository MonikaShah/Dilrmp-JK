from django.db import models
import datetime
from django.db.models import Max  # Import Max here

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