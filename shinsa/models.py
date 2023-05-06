from django.db import models

# Create your models here.
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
# Create your models here.

# イベントテーブル
class Events(models.Model):
    event_name = models.CharField(
        verbose_name='イベント名',
        max_length=70
    )
    event_date = models.DateField(
        verbose_name='開催日',
        blank=False,
        null=False
    )
    marker1 = models.CharField(
        max_length=25,
        verbose_name='審査員1'
    )
    marker2 = models.CharField(
        max_length=25,
        verbose_name='審査員2'
    )
    marker3 = models.CharField(
        max_length=25,
        verbose_name='審査員3'
    )
    marker4 = models.CharField(
        max_length=25,
        verbose_name='審査員4',
        blank=True,
        null=True
    )
    marker5 = models.CharField(
        max_length=25,
        verbose_name='審査員5',
        blank=True,
        null=True
    )
    def __str__(self):
        return self.event_name

# 国
class Country(models.Model):
    country = models.CharField(
        verbose_name='所在国',
        max_length=30
    )
    country_eng = models.CharField(
        verbose_name='country',
        max_length=30
    )
    def __str__(self):
        return f"{self.country} : { self.country_eng }"

# 道場テーブル
class Dojos(models.Model):
    dojo_number = models.CharField(
        unique=True,
        verbose_name='道場番号',
        max_length=4,
        validators=[
            MinLengthValidator(4, 'Four digits'),
            RegexValidator(r'^[0-9]*$', 'only numbers')],
        blank=True,
        null=True
    )
    dojo_name = models.CharField(
        verbose_name='道場名',
        max_length=50
    )
    dojo_name_eng = models.CharField(
        verbose_name='Dojo Name',
        max_length=50
    )
    country = models.ForeignKey(
        Country,
        verbose_name='所在国',
        on_delete=models.CASCADE
        )

    class Meta:
        ordering = ('dojo_number', )

    def __str__(self):
        return f"{self.dojo_number}, {self.dojo_name}, { self.country.country_eng }"

# 段位テーブル
class Grade(models.Model):
    grade_name = models.CharField(
        max_length=4,
        verbose_name='段位'
    )
    grade_name_eng = models.CharField(
        max_length=30,
        verbose_name='Grade'
    )
    def __str__(self):
        return self.grade_name

#    GRADE_CHOICES = (
#        (1, "初段"),
#        (2, "二段"),
#        (3, "三段"),
#        (4, "四段"),
#        (5, "五段"),
#        (6, "六段"),
#        (7, "練士"),
#        (8, "七段"),
#        (9, "教士"),
#    )
#    # grade_id = models.IntegerField()
#    grade_id = models.IntegerField(
#        verbose_name='段位',
#        choices=GRADE_CHOICES
#        )
#    exam_grade = models.IntegerField(
#        choices=GRADE_CHOICES,
#        verbose_name='受審段位'
#        )

class Status(models.Model):
    status = models.CharField(
        max_length=20,
        verbose_name='状態',
    )
    status_eng = models.CharField(
        max_length=20,
        verbose_name='status',
    )
    def __str__(self):
        return f"{self.status}   / { self.status_eng }"


# 受審者テーブル
class Testee(models.Model):
    membership_number = models.CharField(
        unique=True,
        verbose_name='会員番号',
        max_length=7,
        validators=[
            MinLengthValidator(7, 'Seven digits'),
            RegexValidator(r'^[0-9]*$', 'only numbers')],
        help_text="Please enter membership number(7digits). like ”0101001” (your dojo number(4 digits) + your dojo’s membership number(3 digits). or space.",
        blank=True,
        null=True
    )
    testee_name = models.CharField(
        max_length=20,
        verbose_name='Name Japanese',
        help_text="English is okay if you difficult to enter Japanese.",
        )
    testee_name_eng = models.CharField(
        max_length=20,
        verbose_name='Name English'
        )
    status = models.ForeignKey(
        Status,
        verbose_name='状態',
        on_delete=models.CASCADE
        )
    first_grade = models.DateField(
        verbose_name='初段取得日(yyyy-mm-dd)',
        blank=True,
        null=True
    )
    second_grade = models.DateField(
        verbose_name='二段取得日(yyyy-mm-dd)',
        blank=True,
        null=True
    )
    third_grade = models.DateField(
        verbose_name='三段取得日(yyyy-mm-dd)',
        blank=True,
        null=True
    )
    fourth_grade = models.DateField(
        verbose_name='四段取得日(yyyy-mm-dd)',
        blank=True,
        null=True
    )
    fifth_grade = models.DateField(
        verbose_name='五段取得日(yyyy-mm-dd)',
        blank=True,
        null=True
    )
    sixth_grade = models.DateField(
        verbose_name='六段取得日(yyyy-mm-dd)',
        blank=True,
        null=True
    )
    renshi = models.DateField(
        verbose_name='練士取得日(yyyy-mm-dd)',
        blank=True,
        null=True
    )
    seventh_grade = models.DateField(
        verbose_name='七段取得日(yyyy-mm-dd)',
        blank=True,
        null=True
    )
    kyoshi = models.DateField(
        verbose_name='教士取得日(yyyy-mm-dd)',
        blank=True,
        null=True
    )
    eighth_grade = models.DateField(
        verbose_name='八段取得日(yyyy-mm-dd)',
        blank=True,
        null=True
    )
    hanshi = models.DateField(
        verbose_name='範士取得日(yyyy-mm-dd)',
        blank=True,
        null=True
    )

    dojo = models.ForeignKey(
        Dojos,
        verbose_name='道場',
        on_delete=models.CASCADE
    )
#    def __str__(self):
#        return self.dojo_name
    class Meta:
        ordering = ('membership_number', )

    def __str__(self):
        return f"{self.membership_number}, {self.testee_name}   : { self.dojo.dojo_name }"

# 昇段審査採点表テーブル
class Scoringsheet(models.Model):
    POINT_CHOICES = (
        (0.0, 0.0),
        (0.5, 0.5),
        (1.0, 1.0),
        (1.5, 1.5),
        (2.0, 2.0),
        (2.5, 2.5),
        (3.0, 3.0),
        (3.5, 3.5),
        (4.0, 4.0),
        (4.5, 4.5),
        (5.0, 5.0),
        (5.5, 5.5),
        (6.0, 6.0),
        (6.5, 6.5),
        (7.0, 7.0),
        (7.5, 7.5),
        (8.0, 8.0),
        (8.5, 8.5),
        (9.0, 9.0),
        (9.5, 9.5),
        (10.0, 10.0),
    )
    POINT_CHOICES2 = (
        (0, 0),
        (5, 5),
        (10, 10),
        (15, 15),
        (20, 20),
        (25, 25),
        (30, 30),
        (35, 35),
        (40, 40),
        (45, 45),
        (50, 50),
        (55, 55),
        (60, 60),
        (65, 65),
        (70, 70),
        (75, 75),
        (80, 80),
        (85, 85),
        (90, 90),
        (95, 95),
        (100, 100),
    )
#    RESULT_CHOICES = (
#        ("不合格", "不合格"),
#        ("合格", "合格"),
#    )
    testee = models.ForeignKey(
        Testee,
        verbose_name='受審者',
        on_delete=models.PROTECT
    )
    grade = models.ForeignKey(
        Grade,
        verbose_name='受審段位',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    score1 = models.FloatField(
        choices=POINT_CHOICES,
        verbose_name='審査員１',
        default=0.0
    )
    score2 = models.FloatField(
        choices=POINT_CHOICES,
        verbose_name='審査員２',
        default=0.0
    )
    score3 = models.FloatField(
        choices=POINT_CHOICES,
        verbose_name='審査員３',
        default=0.0
    )
    score4 = models.FloatField(
        choices=POINT_CHOICES,
        verbose_name='審査員４',
        default=0.0
    )
    score5 = models.FloatField(
        choices=POINT_CHOICES,
        verbose_name='審査員５',
        default=0.0
    )
    pratical_points = models.FloatField(
        verbose_name='実技得点',
        default=0.0
    )
    written_points = models.IntegerField(
        verbose_name='筆記得点',
        choices=POINT_CHOICES2,
        default=0
        )
    events = models.ForeignKey(
        Events,
        verbose_name='受審催事',
        on_delete=models.PROTECT,
    )
    def __str__(self):
        return f"{self.events.event_name}, { self.testee.testee_name }"

# 演武審査採点表テーブル
class Embuscoringsheet(models.Model):
    POINT_CHOICES = (
        (0.0, 0.0),
        (0.5, 0.5),
        (1.0, 1.0),
        (1.5, 1.5),
        (2.0, 2.0),
        (2.5, 2.5),
        (3.0, 3.0),
        (3.5, 3.5),
        (4.0, 4.0),
        (4.5, 4.5),
        (5.0, 5.0),
        (5.5, 5.5),
        (6.0, 6.0),
        (6.5, 6.5),
        (7.0, 7.0),
        (7.5, 7.5),
        (8.0, 8.0),
        (8.5, 8.5),
        (9.0, 9.0),
        (9.5, 9.5),
        (10.0, 10.0),
    )
    POINT_CHOICES2 = (
        (0, 0),
        (5, 5),
        (10, 10),
        (15, 15),
        (20, 20),
        (25, 25),
        (30, 30),
        (35, 35),
        (40, 40),
        (45, 45),
        (50, 50),
        (55, 55),
        (60, 60),
        (65, 65),
        (70, 70),
        (75, 75),
        (80, 80),
        (85, 85),
        (90, 90),
        (95, 95),
        (100, 100),
    )
#    RESULT_CHOICES = (
#        ("不合格", "不合格"),
#        ("合格", "合格"),
#    )
    testee = models.ForeignKey(
        Testee,
        verbose_name='受審者',
        on_delete=models.PROTECT
    )
    grade = models.ForeignKey(
        Grade,
        verbose_name='受審段位',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    score1 = models.FloatField(
        choices=POINT_CHOICES,
        verbose_name='審査員１',
        default=0.0
    )
    score2 = models.FloatField(
        choices=POINT_CHOICES,
        verbose_name='審査員２',
        default=0.0
    )
    score3 = models.FloatField(
        choices=POINT_CHOICES,
        verbose_name='審査員３',
        default=0.0
    )
    score4 = models.FloatField(
        choices=POINT_CHOICES,
        verbose_name='審査員４',
        default=0.0
    )
    score5 = models.FloatField(
        choices=POINT_CHOICES,
        verbose_name='審査員５',
        default=0.0
    )
    events = models.ForeignKey(
        Events,
        verbose_name='受審催事',
        on_delete=models.PROTECT,
    )
    def __str__(self):
        return f"{self.events.event_name}, { self.testee.testee_name }"
