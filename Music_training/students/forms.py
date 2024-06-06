from django import forms
from courses.models import Course

class CourseEnrollForm(forms.Form): # page 355 возможность записываться на курсы
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                     widget=forms.HiddenInput)
