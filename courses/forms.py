from django import forms
from .models import *
import re


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'for_everybody']

    def clean_course_name(self):
        course_name = self.cleaned_data.get('course_name')

        regexp = re.compile(r'[0-9a-zA-Z ]')
        if not regexp.match(course_name):
            raise forms.ValidationError("Please make sure course name contains (a-z, A-Z, 0-9, space) characters")

        return course_name


class AddChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['chapter_name']

    def clean_chapter_name(self):
        chapter_name = self.cleaned_data.get('chapter_name')
        regexp = re.compile(r'[0-9a-zA-Z ]')

        if not regexp.match(chapter_name):
            raise forms.ValidationError("Please make sure chapter name contains (a-z, A-Z, 0-9, space) characters")

        return chapter_name


class AddLinkForm(forms.ModelForm):
    class Meta:
        model = YTLink
        fields = ['link']


class AddTxtForm(forms.ModelForm):
    class Meta:
        model = TextBlock
        fields = ["lesson"]


class EditCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'for_everybody']


class EditChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['chapter_name']


class EditYTLinkForm(forms.ModelForm):
    class Meta:
        model = YTLink
        fields = ['link']


class EditTxtForm(forms.ModelForm):
    class Meta:
        model = TextBlock
        fields = ["lesson"]


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['file']


class AddNewAbout(forms.ModelForm):
    class Meta:
        model = About
        fields = ['title', 'sub_title', 'about_message']

    def clean_title(self):
        about_name = self.cleaned_data.get('title')

        regexp = re.compile(r'[0-9a-zA-Z!.? ]')
        if not regexp.match(about_name):
            raise forms.ValidationError(
                "Please make sure topic name contains (a-z, A-Z, 0-9, !.?' ') characters")

        return about_name

    def clean_sub_title(self):
        about_sub_name = self.cleaned_data.get('sub_title')

        regexp = re.compile(r'[0-9a-zA-Z!.? ]')
        if not regexp.match(about_sub_name):
            raise forms.ValidationError(
                "Please make sure topic name contains (a-z, A-Z, 0-9, !.?' ') characters")

        return about_sub_name



class AddNewContact(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['address', 'phonenumber', 'email']

    def clean_address(self):
        contact_address = self.cleaned_data.get('address')

       
        if not contact_address:
            raise forms.ValidationError(
                "Please fill in address")

        return contact_address

    def clean_phonenumber(self):
        contact_phonenumber = self.cleaned_data.get('phonenumber')

        if not contact_phonenumber:
            raise forms.ValidationError(
                "Please fill in phonenumber")

        return contact_phonenumber


