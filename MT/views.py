from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from .forms import MasterTrainerFeedbackForm,MTRecordForm
from .models import MasterTrainerFeedback,MTRecord
from django.contrib import messages
import json
from collections import Counter
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Avg
from .forms import MasterTrainerFeedbackForm
from .models import MasterTrainerFeedback,QuizResponse
from django.conf.urls.i18n import set_language
from django.utils import translation
from django.utils.translation import gettext_lazy as _


# Create your views here.
# trainers/views.py

from .forms import MasterTrainerForm,CourseForm
from .models import Course, Attendance

def home_page(request):
    return render(request,"home.html")

def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("course_list")  # Redirect to course list after saving
    else:
        form = CourseForm()
    
    return render(request, "courses/add_course.html", {"form": form})

def course_list(request):
    courses = Course.objects.all()
    return render(request, "courses/course_list.html", {"courses": courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, "courses/course_detail.html", {"course": course})

def attendance_list(request):
    attendances = Attendance.objects.all()
    return render(request, "attendance/attendance_list.html", {"attendances": attendances})

def attendance_detail(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    return render(request, "attendance/attendance_detail.html", {"attendance": attendance})


def register_trainer(request):
    if request.method == 'POST':
        form = MasterTrainerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register')  # Redirect to a success page
    else:
        form = MasterTrainerForm()
    return render(request, 'register_mt.html', {'form': form})



def feedback_view(request):
    rating_questions = {
        "qgis_installation": "How confident are you in installing QGIS on your computer?",
        "qfield_installation": "How confident are you in installing QField on your mobile device?",
        "import_xls": "How confident are you in importing an Excel (.xls) file into QGIS?",
        "merge_shapefiles": "How confident are you in merging shapefiles and creating a shape file?",
        "read_census_codes": "Can you read village census codes from LG Directory?",
        "upload_shapefile": "How much confident in uploading a shapefile?",
        "download_shapefile": "Can you download a district boundary shapefile from a given link?",
        "set_crs": "Are you able to identify CRS and change the CRS (e.g., to UTM 43N)?",
        "georeference_image": "Can you georeference an image and digitize features on it?",
        "trace_polygons": "Can you trace polygons in QField with attributes like name, photo, etc.?",
        "transfer_qfield_project": "Can you transfer a QField project to your mobile or from the QField to QGIS?",
        "map_projections": "Do you understand map projections and their usage?",
        "gis_concepts": "Rate GIS concepts taught?",
    }

    rating_fields = list(rating_questions.keys())

    # Handle form submission
    if request.method == "POST":
        form = MasterTrainerFeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Feedback submitted successfully.")
            return redirect('feedback_form')
        else:
            messages.error(request, "There was an error submitting your feedback. Please check the form.")
    else:
        form = MasterTrainerFeedbackForm()

    # Compute average ratings for each question
    averages = MasterTrainerFeedback.objects.aggregate(
        **{field: Avg(field) for field in rating_fields}
    )

    # Filter out None values (e.g., no responses yet)
    valid_averages = {k: v for k, v in averages.items() if v is not None}

    if valid_averages:
        max_question = max(valid_averages, key=valid_averages.get)
        min_question = min(valid_averages, key=valid_averages.get)

        def get_rating_distribution(field):
            values = MasterTrainerFeedback.objects.exclude(**{f"{field}__isnull": True}).values_list(field, flat=True)
            dist = dict(Counter(values))
            return [dist.get(i, 0) for i in range(1, 6)]  # For 1 to 5 stars

        max_dist = get_rating_distribution(max_question)
        min_dist = get_rating_distribution(min_question)
    else:
        max_question = min_question = None
        max_dist = min_dist = [0, 0, 0, 0, 0]

    context = {
        'form': form,
        'feedbacks': MasterTrainerFeedback.objects.all(),
        'rating_questions': rating_questions,
        'max_question': max_question,
        'min_question': min_question,
        'max_dist': max_dist,
        'min_dist': min_dist,
    }
    return render(request, 'feedback_form.html', context)

def get_distribution(values):
    # Count how many 1s, 2s, 3s, 4s, and 5s
    dist = {}
    for v in values:
        dist[v] = dist.get(v, 0) + 1
    return dist

def feedback_list(request):
    feedbacks = MasterTrainerFeedback.objects.all()

    rating_questions = {
        "qgis_installation": "QGIS Installation",
        "qfield_installation": "QField Installation",
        "import_xls": "Import Excel",
        "merge_shapefiles": "Merge Shapefiles",
        "read_census_codes": "Read Census Codes",
        "upload_shapefile": "Upload Shapefile",
        "download_shapefile": "Download Shapefile",
        "set_crs": "Set CRS",
        "georeference_image": "Georeference Image",
        "trace_polygons": "Trace Polygons",
        "transfer_qfield_project": "Transfer QField Project",
        "map_projections": "Map Projections",
        "gis_concepts": "GIS Concepts",
    }

    # Calculate average ratings
    avg_ratings = {}
    for field in rating_questions:
        values = feedbacks.values_list(field, flat=True)
        values = [v for v in values if v is not None]
        avg_ratings[field] = sum(values) / len(values) if values else 0

# Initialize dictionaries
    max_ratings = {}
    min_ratings = {}
    # Find most and least confident for each trainer
    for feedback in feedbacks:
        trainer_id = feedback.trainer_id  # Assuming feedback has a user field
        for field, _ in rating_questions.items():
            rating = getattr(feedback, field, None)
            if rating is not None:
                # Track the highest rating for each trainer
                if trainer_id not in max_ratings or rating > max_ratings[trainer_id]:
                    max_ratings[trainer_id] = rating
                # Track the lowest rating for each trainer
                if trainer_id not in min_ratings or rating < min_ratings[trainer_id]:
                    min_ratings[trainer_id] = rating


    max_question = max(avg_ratings, key=avg_ratings.get)
    min_question = min(avg_ratings, key=avg_ratings.get)

    # Get distributions for max and min
    max_values = feedbacks.values_list(max_question, flat=True)
    max_values = [v for v in max_values if v is not None]
    max_dist = get_distribution(max_values)

    min_values = feedbacks.values_list(min_question, flat=True)
    min_values = [v for v in min_values if v is not None]
    min_dist = get_distribution(min_values)
    

    context = {
        "feedbacks": feedbacks,
        # "feedbacks1": list(feedbacks.objects.all().values()),

        "rating_questions": rating_questions,
        "avg_ratings": json.dumps(avg_ratings),
        "max_question": max_question,
        "min_question": min_question,
        "max_dist": json.dumps(max_dist),
        "min_dist": json.dumps(min_dist),
        "rating_labels": json.dumps(list(rating_questions.values())),
        "max_ratings": max_ratings,  # Pass max_ratings
        "min_ratings": min_ratings,  # Pass min_ratings
        "feedback_json": list(feedbacks.values()),  # Add this

    }
    return render(request, "feedback_list.html", context)

def feedback_success(request):
    return render(request, 'feedback_success.html')

def upload_mt(request):
   
    if request.method == 'POST':
        form = MTRecordForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Add success message
            messages.success(request, 'Screenshot submitted successfully. Thank you!')
            return redirect('upload_mt')  # Redirect to the same page or a different page after submission
    else:
        form = MTRecordForm()

    return render(request, 'upload_mt.html', {'form': form})

def quiz_view(request):
    questions = [
        {
            'text': _('What is the main purpose of GIS?'),
            'options': [
                _('To create websites'),
                _('To analyze spatial and geographic data'),
                _('To manage financial records'),
                _('To design architectural structures')
            ],
            'answer': _('To analyze spatial and geographic data')
        },
        {
            'text': _('In GIS, what does "attribute data" refer to?'),
            'options': [
                _('Data about the spatial location'),
                _('Data about the characteristics of spatial features'),
                _('Data about the coordinate system'),
                _('Data about the map scale')
            ],
            'answer': _('Data about the characteristics of spatial features')
        },
        {
            'text': _('Which of the following is NOT a raster data format?'),
            'options': [
                _('TIFF'),
                _('JPEG'),
                _('Shapefile'),
                _('IMG')
            ],
            'answer': _('Shapefile')
        },
        {
            'text': _('What is the main drawback of the Mercator projection?'),
            'options': [
                _('It distorts distances near the equator'),
                _('It distorts shapes near the poles'),
                _('It cannot represent the entire Earth'),
                _('It is difficult to construct')
            ],
            'answer': _('It distorts shapes near the poles')
        },
        {
            'text': _('What is the main purpose of using map projections?'),
            'options': [
                _('To reduce map size'),
                _('To represent the 3D Earth on a 2D surface'),
                _('To enhance colors'),
                _('To simplify data')
            ],
            'answer': _('To represent the 3D Earth on a 2D surface')
        },
        {
            'text': _('Which of the following is a common method of georeferencing?'),
            'options': [
                _('Using random points'),
                _('Assigning arbitrary numbers'),
                _('Using Ground Control Points (GCPs)'),
                _('Estimating positions visually')
            ],
            'answer': _('Using Ground Control Points (GCPs)')
        },
        {
            'text': _('What is the purpose of georeferencing an image?'),
            'options': [
                _('To enhance its resolution'),
                _('To align it with a coordinate system'),
                _('To change its color scheme'),
                _('To compress its size')
            ],
            'answer': _('To align it with a coordinate system')
        },
        {
            'text': _('Which software is commonly used for georeferencing?'),
            'options': [
                _('Microsoft Word'),
                _('Adobe Photoshop'),
                _('QGIS'),
                _('VLC Media Player')
            ],
            'answer': _('QGIS')
        },
        {
            'text': _('What is required for accurate georeferencing?'),
            'options': [
                _('High-speed internet'),
                _('Ground Control Points'),
                _('3D glasses'),
                _('Color printer')
            ],
            'answer': _('Ground Control Points')
        },
        {
            'text': _('What is the minimum number of GCPs required for Second-order polynomial transformation?'),
            'options': [
                _('2'),
                _('6'),
                _('4'),
                _('5')
            ],
            'answer': _('6')
        },
        {
            'text': _('Which tool in QGIS is used for georeferencing?'),
            'options': [
                _('Georeferencer'),
                _('Digitizer'),
                _('Map Composer'),
                _('Coordinate Editor')
            ],
            'answer': _('Georeferencer')
        },
        {
            'text': _('Which of the following is not a step in georeferencing?'),
            'options': [
                _('Adding GCPs'),
                _('Selecting transformation type'),
                _('Digitizing features'),
                _('Saving the georeferenced image')
            ],
            'answer': _('Digitizing features')
        },
        {
            'text': _('What is the purpose of a map legend?'),
            'options': [
                _('To provide scale'),
                _('To show directions'),
                _('To explain symbols on the map'),
                _('To display map title')
            ],
            'answer': _('To explain symbols on the map')
        },
        {
            'text': _('All projections cause some kind of what?'),
            'options': [
                _('Accuracy'),
                _('Distortion'),
                _('Perfection'),
                _('Realism')
            ],
            'answer': _('Distortion')
        },
        {
            'text': _('Which datum is commonly used globally?'),
            'options': [
                _('NAD83'),
                _('WGS84'),
                _('ED50'),
                _('Tokyo Datum')
            ],
            'answer': _('WGS84')
        },
        {
            'text': _('Local datums are used because:'),
            'options': [
                _('They are free'),
                _('They fit local areas better'),
                _('They are pretty'),
                _('They don’t need coordinates')
            ],
            'answer': _('They fit local areas better')
        },
    ]

    if request.method == 'POST':
        trainer_id = request.POST.get('trainer_id', 'anonymous')
        for i, q in enumerate(questions):
            selected = request.POST.get(f'q{i}')
            if selected:
                QuizResponse.objects.create(
                    trainer_id=trainer_id,
                    question=q['text'],
                    selected_option=selected,
                    correct_answer=q['answer'],
                )
        return redirect('quiz_thankyou')

    return render(request, 'quiz.html', {'questions': questions})

def set_language(request):
    user_language = request.POST.get('language', 'en')  # Default to 'en' if not specified
    print('language selected is',user_language)
    translation.activate(user_language)  # Activate the chosen language
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language  # Store the selected language in the session
    return HttpResponseRedirect(request.POST.get('next', '/'))  # Redirect back to the previous page or home page
