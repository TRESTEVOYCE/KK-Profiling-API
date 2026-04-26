from django.db import models


class ProfilingInformations(models.Model):

    class SexChoices(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    class CivilStatusChoices(models.TextChoices):
        SINGLE = "single", "Single"
        MARRIED = "married", "Married"
        WIDOWED = "widowed", "Widowed"
        DIVORCED = "divorced", "Divorced"
        SEPARATED = "separated", "Separated"
        ANNULLED = "annulled", "Annulled"
        UNKNOWN = "unknown", "Unknown"
        LIVE_IN = "live_in", "Live-in"

    class EducationalBackgroundChoices(models.TextChoices):
        ELEMENTARY_LEVEL = "elementary_level", "Elementary Level"
        ELEMENTARY_GRAD = "elementary_graduate", "Elementary Graduate"
        HIGHSCHOOL_LEVEL = "highschool_level", "High School Level"
        HIGHSCHOOL_GRAD = "highschool_graduate", "High School Graduate"
        VOCATIONAL_GRAD = "vocational_graduate", "Vocational Graduate"
        COLLEGE_LEVEL = "college_level", "College Level"
        COLLEGE_GRAD = "college_graduate", "College Graduate"
        MASTER_LEVEL = "master_level", "Master Level"
        DOCTORATE_LEVEL = "doctorate_level", "Doctorate Level"
        DOCTORATE_GRAD = "doctorate_graduate", "Doctorate Graduate"

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)

    age = models.IntegerField(default=0, null=True, blank=True)
    birthdate = models.DateField(blank=True, null=True)

    email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=20)

    sex = models.CharField(
        max_length=10,
        choices=SexChoices.choices,
        blank=True,
        null=True
    )

    civil_status = models.CharField(
        max_length=20,
        choices=CivilStatusChoices.choices,
        blank=True,
        null=True
    )

    educational_background = models.CharField(
        max_length=30,
        choices=EducationalBackgroundChoices.choices,
        blank=True,
        null=True
    )

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class KKAddress(models.Model):

    kk_name = models.OneToOneField(
        ProfilingInformations,
        on_delete=models.CASCADE,
        related_name='addresses'
    )

    region = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    municipality_or_city = models.CharField(max_length=255)
    barangay = models.CharField(max_length=255)
    purok = models.CharField(max_length=255, blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.kk_name} - {self.barangay}"


class YouthStatus(models.Model):

    class YouthAgeGroupChoices(models.TextChoices):
        CHILD_YOUTH = "child_youth", "Child Youth"
        CORE_YOUTH = "core_youth", "Core Youth"
        YOUNG_ADULT = "young_adult", "Young Adult"

    class YouthClassificationChoices(models.TextChoices):
        IN_SCHOOL_YOUTH = "in_school_youth", "In-School Youth"
        OUT_OF_SCHOOL_YOUTH = "out_of_school_youth", "Out-of-School Youth"
        WORKING_YOUTH = "working_youth", "Working Youth"

    class YouthWithSpecificNeedsChoices(models.TextChoices):
        PERSON_WITH_DISABILITY = "person_with_disability", "Person with Disability"
        CHILDREN_IN_CONFLICT_WITH_LAW = "children_in_conflict_with_law", "Children in Conflict with Law"
        INDIGENOUS_PEOPLE = "indigenous_people", "Indigenous People"

    class WorkingStatusChoices(models.TextChoices):
        EMPLOYED = "employed", "Employed"
        UNEMPLOYED = "unemployed", "Unemployed"
        SELF_EMPLOYED = "self_employed", "Self-Employed"
        LOOKING_FOR_JOB = "looking_for_job", "Currently Looking for a Job"
        NOT_LOOKING_FOR_JOB = "not_looking_for_job", "Not Interested in Looking for a Job"

    kk_name = models.OneToOneField(ProfilingInformations,on_delete=models.CASCADE,related_name='youth_statuses')

    youth_classification = models.CharField(max_length=50,choices=YouthClassificationChoices.choices,blank=True,null=True)

    youth_age_group = models.CharField(max_length=50,choices=YouthAgeGroupChoices.choices,blank=True,null=True)
    youth_with_specific_needs = models.CharField(max_length=50,choices=YouthWithSpecificNeedsChoices.choices,blank=True,null=True)

    working_status = models.CharField(max_length=50,choices=WorkingStatusChoices.choices,blank=True,null=True)
    is_sk_voter = models.BooleanField(default=True)
    is_regular_voter = models.BooleanField(default=False)
    attended_kk_assembly = models.BooleanField(default=True)
    times_attended = models.IntegerField(default=0)
    did_not_attend_reason = models.TextField(blank=True,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.kk_name} - Youth Status"