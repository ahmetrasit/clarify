from django.contrib.auth.models import AbstractUser
from django.db import models


class Question(models.Model):
    # q:question, a:answer, r:response_time, p:participant_number
    FEEDBACK = 'qF'
    CLARIFICATION = 'qC'
    INFORMATION = 'qI'
    QUESTION_TYPE_CHOICES = (
        (FEEDBACK, 'Feedback'),
        (CLARIFICATION, 'Clarification'),
        (INFORMATION, 'Information'),
    )

    QUICK = 'aQ'
    SHORT = 'aS'
    DETAILED = 'aD'
    ANSWER_TYPE_CHOICES = (
        (QUICK, 'Quick'),
        (SHORT, 'Short'),
        (DETAILED, 'Detailed'),
    )

    FAST = 'rF'
    SLOW = 'rS'
    ANYTIME = 'rA'
    RESPONSE_TYPE_CHOICES = (
        (FAST, 'Fast'),
        (SLOW, 'Slow'),
        (ANYTIME, 'Anytime'),
    )

    SINGLE = 'pS'
    DUEL = 'pD'
    COMPETITION = 'pC'
    PARTICIPANT_TYPE_CHOICES = (
        (SINGLE, 'Single'),
        (DUEL, 'Duel'),
        (COMPETITION, 'Competition'),
    )

    raw_question = models.TextField()
    processed_question = models.TextField()
    user = models.ForeignKey(User)
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPE_CHOICES, default=CLARIFICATION)
    answer_type = models.CharField(max_length=2, choices=ANSWER_TYPE_CHOICES, default=SHORT)
    response_type = models.CharField(max_length=2, choices=RESPONSE_TYPE_CHOICES, default=SLOW)
    participant_type = models.CharField(max_length=2, choices=PARTICIPANT_TYPE_CHOICES, default=SINGLE)
    follow_up = models.BooleanField(default=False)
    questionnaire = models.BooleanField(default=False)
    attachment = models.ForeignKey(Attachment, null=True)
    records = models.ForeignKey(Records, null=True)
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()


class Answer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    rating = models.ForeignKey(Rating, null=True)
    transcript = models.ForeignKey(Transcript, null=True)
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()
    records = models.ForeignKey(Records)


class Rewards(models.Model):
    user = models.ForeignKey(User)


class Transcript(models.Model):
    answer = models.ForeignKey(Answer)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now=True)


class Record(models.Model):
    url_path = models.TextField()   # url or file path
    properties = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()



class Records(models.Model):
    # s:source
    QUESTION = 'sQ'
    ANSWER = 'sA'
    SOURCE_TYPE_CHOICES = (
        (QUESTION, 'Question'),
        (ANSWER, 'Answer'),
    )
    source_type = models.CharField(max_length=2, choices=SOURCE_TYPE_CHOICES, default=ANSWER)
    full_video = models.ForeignKey(Record, null=True)
    full_audio = models.ForeignKey(Record, null=True)
    intro_video = models.ForeignKey(Record, null=True)
    intro_audio = models.ForeignKey(Record, null=True)
    created_on = models.DateTimeField(auto_now=True)



class Ratings(models.Model):
    rating = models.ForeignKey(Rating)
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()



class Rating(models.Model):
    voters = models.ForeignKey(User)
    type = models.TextField()
    score = models.DecimalField()
    is_average = models.BooleanField(default=False)
    no_of_votes = models.IntegerField()



class Attachment(models.Model):
    url_path = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()


class UserLanguage(models.Model):
    NATIVE = 'lN'
    FLUENT = 'lF'
    PROFICIENT = 'lP'
    CONVERSANT = 'lC'
    BASIC = 'lB'
    PROFICIENCY_CHOICES = (
        (NATIVE, 'Native'),
        (FLUENT, 'Fluent'),
        (PROFICIENT, 'Proficient'),
        (CONVERSANT, 'Conversant'),
        (BASIC, 'Basic'),
    )

    language = models.CharField(max_length=128)
    reading_proficiency = models.CharField(max_length=2, choices=PROFICIENCY_CHOICES, default=NATIVE)
    writing_proficiency = models.CharField(max_length=2, choices=PROFICIENCY_CHOICES, default=NATIVE)
    speaking_proficiency = models.CharField(max_length=2, choices=PROFICIENCY_CHOICES, default=NATIVE)


class User(AbstractUser):
    languages = models.ForeignKey(UserLanguage)
    bilingual = models.BooleanField(default=False)


class Message(models.Model):
    # c:communication, m: message type
    USER2USER= 'cUU'
    PLATFORM2USER= 'cPU'
    USER2PLATFORM = 'cUP'
    BROADCAST = 'cBC'
    COMMUNICATION_TYPE_CHOICES = (
        (USER2USER, 'User to User'),
        (PLATFORM2USER, 'Platform to User'),
        (USER2PLATFORM, 'User to Platform'),
        (BROADCAST, 'Broadcast'),
    )

    COMMUNICATION = 'mCO'   # basically, only for USER2USER
    INFO = 'mIN'
    REQUEST = 'mRE'
    TIME_SENSITIVE = 'mTS'
    WARNING = 'mWA'
    GOOD_NEWS = 'mGN'
    SPAM = 'mSP'
    HELP = 'mHE'
    MESSAGE_TYPE_CHOICES = (
        (COMMUNICATION, 'User to User'),
        (INFO, 'Information'),
        (REQUEST, 'Request'),
        (TIME_SENSITIVE, 'Time sensitive'),
        (WARNING, 'Warning'),
        (GOOD_NEWS, 'Good news'),
        (SPAM, 'Spam'),
        (HELP, 'Help')
    )

    source = models.ForeignKey(User)    # platform is a user, too
    target = models.ForeignKey(User)
    communication_type = models.CharField(max_length=3, choices=COMMUNICATION_TYPE_CHOICES, default=USER2USER)
    message_type = models.CharField(max_length=3, choices=MESSAGE_TYPE_CHOICES, default=COMMUNICATION)
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()
    is_read = models.BooleanField(default=False)
    is_answered = models.BooleanField(default=False)


class Bids(models.Model):
    question = models.ForeignKey(Question, unique=True)
    bids = models.ForeignKey(Bid)
    winners = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now=True)
    resolved_on = models.DateTimeField(null=True)



class Bid(models.Model):
    user = models.ForeignKey(User)
    short_message = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()
    is_shown = models.BooleanField(default=False)
    is_accepted_by_user = models.BooleanField(default=False)
    is_accepted_by_platform = models.BooleanField(default=False)
    is_fullfilled = models.BooleanField(default=False)
