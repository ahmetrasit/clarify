from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


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


class AnswerType(models.Model):
    QUICK = 'aQ'
    SHORT = 'aS'
    DETAILED = 'aD'
    ANSWER_TYPE_CHOICES = (
        (QUICK, 'Quick'),
        (SHORT, 'Short'),
        (DETAILED, 'Detailed'),
    )
    answer_type = models.CharField(max_length=2, choices=ANSWER_TYPE_CHOICES, default=SHORT)



class QuestionType(models.Model):
    FEEDBACK = 'qF'
    CLARIFICATION = 'qC'
    INFORMATION = 'qI'
    QUESTION_TYPE_CHOICES = (
        (FEEDBACK, 'Feedback'),
        (CLARIFICATION, 'Clarification'),
        (INFORMATION, 'Information'),
    )
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPE_CHOICES, default=CLARIFICATION)


class ResponseTime(models.Model):
    FAST = 'rF'
    SLOW = 'rS'
    ANYTIME = 'rA'
    RESPONSE_TYPE_CHOICES = (
        (FAST, 'Fast'),
        (SLOW, 'Slow'),
        (ANYTIME, 'Anytime'),
    )
    response_time = models.CharField(max_length=2, choices=RESPONSE_TYPE_CHOICES, default=SLOW)


class ParticipantType(models.Model):
    SINGLE = 'pS'
    DUEL = 'pD'
    COMPETITION = 'pC'
    PARTICIPANT_TYPE_CHOICES = (
        (SINGLE, 'Single'),
        (DUEL, 'Duel'),
        (COMPETITION, 'Competition'),
    )
    participant_type = models.CharField(max_length=2, choices=PARTICIPANT_TYPE_CHOICES, default=SINGLE)



class Dewey(models.Model):
    number = models.IntegerField(null=True)
    label = models.TextField()
    level = models.IntegerField()
    parents = models.ForeignKey('Dewey', related_name='dewey_parents', on_delete=models.DO_NOTHING, null=True)
    children = models.ForeignKey('Dewey', related_name='dewey_children', on_delete=models.DO_NOTHING, null=True)



class Flag(models.Model):
    user = models.OneToOneField('User', on_delete=models.DO_NOTHING)
    flag_type = models.CharField(max_length=128)
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()


class QuestionFlags(models.Model):
    question = models.OneToOneField('Question', on_delete=models.DO_NOTHING)
    flags = models.ForeignKey(Flag, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=64)
    is_valid = models.BooleanField()
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()


class AnswerFlags(models.Model):
    answer = models.OneToOneField('Answer', on_delete=models.DO_NOTHING)
    flags = models.ForeignKey(Flag, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=64)
    is_valid = models.BooleanField()
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()


class Attachment(models.Model):
    url_path = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()




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
    full_video = models.ForeignKey(Record, related_name='full_video_record', null=True, on_delete=models.DO_NOTHING)
    full_audio = models.ForeignKey(Record, related_name='full_audio_record', null=True, on_delete=models.DO_NOTHING)
    intro_video = models.ForeignKey(Record, related_name='intro_video_record', null=True, on_delete=models.DO_NOTHING)
    intro_audio = models.ForeignKey(Record, related_name='intro_audio_record', null=True, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now=True)


class RatingType(models.Model):
    rating_type = models.CharField(max_length=128)


class Rating(models.Model):
    QUESTIONER = 'rQ'
    ANSWERER = 'rA'
    ROLE_CHOICES = (
        (QUESTIONER, 'Questioner'),
        (ANSWERER, 'Answerer'),
    )
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    user_role = models.CharField(max_length=2, choices=ROLE_CHOICES, default='questioner')
    rating_type = models.ForeignKey(RatingType, on_delete=models.DO_NOTHING)
    score = models.IntegerField()


class AverageRating(models.Model):
    rating_type = models.OneToOneField(RatingType, on_delete=models.DO_NOTHING)
    score = models.DecimalField(decimal_places=4, max_digits=7)


class Ratings(models.Model):
    ratings = models.ForeignKey(Rating, on_delete=models.DO_NOTHING)
    average_ratings = models.ForeignKey(AverageRating, on_delete=models.DO_NOTHING)
    rating_types = models.ForeignKey(RatingType, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()
    is_average = models.BooleanField(default=False)
    no_of_votes = models.IntegerField()


class Transcript(models.Model):
    answer = models.ForeignKey('Answer', related_name='transcript_answer',  on_delete=models.DO_NOTHING)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now=True)


class Question(models.Model):
    # q:question, a:answer, r:response_time, p:participant_type
    raw_question = models.TextField()
    processed_question = models.TextField()
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    classification = models.ManyToManyField(Dewey)
    question_types = models.ManyToManyField(QuestionType)
    answer_types = models.ManyToManyField(AnswerType)
    response_times = models.ManyToManyField(ResponseTime)
    participant_types = models.ManyToManyField(ParticipantType)
    flags = models.OneToOneField(QuestionFlags, related_name='question_flags', null=True, on_delete=models.DO_NOTHING)
    follow_up = models.BooleanField(default=False)
    questionnaire = models.BooleanField(default=False)
    attachment = models.ForeignKey(Attachment, null=True, on_delete=models.SET_NULL)
    records = models.ForeignKey(Records, null=True, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()


class Answer(models.Model):
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    classification = models.ManyToManyField(Dewey)
    rating = models.ForeignKey(Ratings, null=True, on_delete=models.SET_NULL)
    question_type = models.ManyToManyField(QuestionType)
    answer_type = models.ManyToManyField(AnswerType)
    response_time = models.ManyToManyField(ResponseTime)
    participant_type = models.ManyToManyField(ParticipantType)
    flags = models.OneToOneField(AnswerFlags, related_name='answer_flags', null=True, on_delete=models.DO_NOTHING)
    transcript = models.ForeignKey(Transcript, related_name='answer_transcript', null=True, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()
    records = models.ForeignKey(Records, on_delete=models.DO_NOTHING)


class Bid(models.Model):
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    short_message = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()
    is_shown = models.BooleanField(default=False)
    is_accepted_by_user = models.BooleanField(default=False)
    is_accepted_by_platform = models.BooleanField(default=False)
    is_fullfilled = models.BooleanField(default=False)



class Bids(models.Model):
    question = models.OneToOneField(Question, on_delete=models.DO_NOTHING)
    bids = models.ForeignKey(Bid, on_delete=models.DO_NOTHING)
    winners = models.ForeignKey('User', related_name='winners_user', on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now=True)
    resolved_on = models.DateTimeField(null=True)




class UserLocation(models.Model):
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()


class UserExpertise(models.Model):
    dewey = models.ForeignKey(Dewey, on_delete=models.DO_NOTHING)
    rating_score = models.DecimalField(decimal_places=4, max_digits=7)
    answers = models.ForeignKey(Answer, on_delete=models.DO_NOTHING)


class UserLogin(models.Model):
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()
    details= models.TextField


class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('You need to provide a valid e-mail address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)



class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    date_of_birth = models.DateField(null=True)
    can_ask = models.BooleanField(default=False)
    can_tell = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, null=True)
    email_confirmed = models.BooleanField(default=False)
    phone_confirmed = models.BooleanField(default=False)
    languages = models.ForeignKey(UserLanguage, on_delete=models.CASCADE, null=True)
    answers = models.ForeignKey(Answer, related_name='user_answers', on_delete=models.DO_NOTHING, null=True)
    questions = models.ForeignKey(Question, related_name='user_questions', on_delete=models.DO_NOTHING, null=True)
    bids = models.ManyToManyField(Bids, related_name='user_bids')
    expertise = models.ForeignKey(UserExpertise, on_delete=models.DO_NOTHING, null=True)
    locations = models.ForeignKey(UserLocation, on_delete=models.DO_NOTHING, null=True)
    multilingual = models.BooleanField(default=False, null=True)
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField(null=True)
    logins = models.ForeignKey(UserLogin, related_name='user_logins', on_delete=models.DO_NOTHING, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class RewardCard(models.Model):
    # r:role
    QUESTIONER = 'rQ'
    ANSWERER = 'rA'
    ROLE_CHOICES = (
        (QUESTIONER, 'Questioner'),
        (ANSWERER, 'Answerer'),
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    user_role = models.CharField(max_length=2, choices=ROLE_CHOICES, default=QUESTIONER)
    card_type = models.CharField(max_length=128)
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()


class RewardPoint(models.Model):
    # r:role
    QUESTIONER = 'rQ'
    ANSWERER = 'rA'
    ROLE_CHOICES = (
        (QUESTIONER, 'Questioner'),
        (ANSWERER, 'Answerer'),
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    user_role = models.CharField(max_length=2, choices=ROLE_CHOICES, default=QUESTIONER)
    event = models.CharField(max_length=128)
    point = models.IntegerField()
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()


class Rewards(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    current_cards = models.ForeignKey(RewardCard, related_name='rewards_current_cards', null=True, on_delete=models.DO_NOTHING)
    used_cards = models.ForeignKey(RewardCard, related_name='rewards_used_cards', null=True, on_delete=models.DO_NOTHING)
    current_points = models.ForeignKey(RewardPoint, related_name='rewards_current_points', null=True, on_delete=models.DO_NOTHING)
    used_points = models.ForeignKey(RewardPoint, related_name='rewards_used_points', null=True, on_delete=models.DO_NOTHING)



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

    source = models.ForeignKey(User, related_name='source_user', on_delete=models.DO_NOTHING)    # platform is a user, too
    target = models.ForeignKey(User, related_name='target_user', on_delete=models.DO_NOTHING)
    communication_type = models.CharField(max_length=3, choices=COMMUNICATION_TYPE_CHOICES, default=USER2USER)
    message_type = models.CharField(max_length=3, choices=MESSAGE_TYPE_CHOICES, default=COMMUNICATION)
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()
    is_read = models.BooleanField(default=False)
    is_answered = models.BooleanField(default=False)


class Advice(models.Model):
    answer = models.OneToOneField(Answer, on_delete=models.DO_NOTHING)
    ratings = models.ForeignKey(Ratings, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now=True)
    intro_views = models.IntegerField()
    intro_viewers = models.ForeignKey(User, related_name='intro_viewer_user', on_delete=models.DO_NOTHING)
    full_views = models.IntegerField()
    full_viewers = models.ForeignKey(User, related_name='full_viewer_user', on_delete=models.DO_NOTHING)



class PaymentEvent(models.Model):
    status = models.TextField()
    created_on = models.DateTimeField(auto_now=True)



class DisputeEvents(models.Model):
    status = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()


class Dispute(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    events = models.ForeignKey(DisputeEvents, on_delete=models.DO_NOTHING)
    is_resolved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now=True)
    resolved_on = models.DateTimeField(null=True)
    location = models.TextField()



class PaymentReceived(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    method = models.TextField()
    events = models.ForeignKey(PaymentEvent, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()
    amount = models.DecimalField(decimal_places=6, max_digits=20)
    currency = models.CharField(max_length=128)
    status = models.CharField(max_length=64)
    disputes = models.ForeignKey(Dispute, null=True, on_delete=models.DO_NOTHING)
    success = models.BooleanField(default=False)
    refund = models.BooleanField(default=False)
    chargeback = models.BooleanField(default=False)


class PaymentMade(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    method = models.TextField()
    events = models.ForeignKey(PaymentEvent, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()
    amount = models.DecimalField(decimal_places=6, max_digits=20)
    currency = models.CharField(max_length=128)
    status = models.CharField(max_length=64)
    disputes = models.ForeignKey(Dispute, null=True, on_delete=models.DO_NOTHING)
    success = models.BooleanField(default=False)


class EmailConfirmation(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    sent_key = models.CharField(max_length=16)
    status = models.BooleanField(default=False)  #True if confirmed, False if waiting
    created_on = models.DateTimeField(auto_now=True)
    confirmed_on = models.DateTimeField(null=True)


class UserEvent(models.Model):
    CONFIRMATION_OF_EMAIL = 'cEM'
    CONFIRMATION_OF_PHONE_NUMBER = 'cPN'
    WRONG_PASSWORD = 'wPW'
    WRONG_EMAIL_CONFIRMATION_CODE = 'wEC'
    WRONG_PHONE_CONFIRMATION_CODE = 'wPC'
    CHANGE_OF_PAYMENT_INFO = 'cPI'
    CHANGE_OF_PHONE_NUMBER = 'cPN'
    CHANGE_OF_ADDRESS = 'cAD'
    REQUEST_OF_PASSWORD_RESET = 'rPR'
    REQUEST_OF_PASSWORD_CHANGE = 'rPC'
    EVENTS = (
        (CONFIRMATION_OF_EMAIL, 'cEM'),
        (CONFIRMATION_OF_PHONE_NUMBER, 'cPN'),
        (WRONG_PASSWORD, 'wrong password'),
        (WRONG_EMAIL_CONFIRMATION_CODE, 'wrong email confirmation code'),
        (WRONG_PHONE_CONFIRMATION_CODE, 'wrong phone confirmation code'),
        (CHANGE_OF_PAYMENT_INFO, 'change of payment info'),
        (CHANGE_OF_PHONE_NUMBER, 'change of phone number'),
        (CHANGE_OF_ADDRESS, 'change of address'),
        (REQUEST_OF_PASSWORD_RESET, 'request of password reset'),
        (REQUEST_OF_PASSWORD_CHANGE, 'request of password change')
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    event = models.CharField(max_length=3, choices=EVENTS)
    detail = models.CharField(max_length=64, null=True)
    created_on = models.DateTimeField(auto_now=True)
    location = models.TextField()