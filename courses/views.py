from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import *
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def courses(request):
    if request.user.is_lecturer or request.user.is_site_admin:
        queryset = Course.objects.all()
    else:
        queryset = Course.objects.filter(for_everybody=True)

    context = {
        "title": "Admin Panel",
        "queryset": queryset,
    }

    return render(request, "adminpan.html", context)


@user_passes_test(lambda user: user.is_lecturer)
def course(request, course_name=None):
    add_chapter_form = AddChapterForm(request.POST or None)
    queryset_chapter = Chapter.objects.filter(course__course_name=course_name)

    context = {
        "title": course_name,
        "add_chapter_form": add_chapter_form,
        "queryset_chapter": queryset_chapter,
        "course_name": course_name,
        "path": "Profile",
        "redirect_path": "profile",
    }

    if add_chapter_form.is_valid():
        instance = add_chapter_form.save(commit=False)
        instance.course = Course.objects.get(course_name=course_name)
        instance.save()
        return redirect(reverse('professor_course', kwargs={'course_name': course_name}))

    return render(request, "courses/course.html", context)


@user_passes_test(lambda user: user.is_lecturer)
def chapter(request, course_name=None, slug=None):
    place = Chapter.objects.get(course__course_name=course_name, slug=slug)

    add_link_form = AddLinkForm(request.POST or None)
    add_txt_form = AddTxtForm(request.POST or None)
    file_upload_form = FileUploadForm(request.POST or None, request.FILES or None)

    queryset_txt_block = TextBlock.objects.filter(text_block_fk__id=place.id)
    queryset_yt_link = YTLink.objects.filter(yt_link_fk__id=place.id)
    queryset_files = FileUpload.objects.filter(file_fk__id=place.id)

    context = {
        "title": place.chapter_name,
        "course_name": course_name,
        "slug": slug,
        "add_link_form": add_link_form,
        "add_txt_form": add_txt_form,
        "queryset_yt_link": queryset_yt_link,
        "queryset_txt_block": queryset_txt_block,
        "queryset_files": queryset_files,
        "path": "Profile",
        "redirect_path": "profile",
        "file_upload_form": file_upload_form,
    }

    if add_link_form.is_valid() and 'add_link' in request.POST:
        instance = add_link_form.save(commit=False)
        instance.yt_link_fk = Chapter.objects.get(id=place.id)

        key = add_link_form.cleaned_data.get("link")

        if 'embed' not in key and 'youtube' in key:
            key = key.split('=')[1]
            instance.link = 'https://www.youtube.com/embed/' + key

        instance.yt_link_fk = Chapter.objects.get(id=place.id)
        instance.save()
        return redirect(reverse('chapter', kwargs={'course_name': course_name,
                                                   'slug': slug}))

    if add_txt_form.is_valid() and 'add_text' in request.POST:
        instance = add_txt_form.save(commit=False)
        instance.text_block_fk = Chapter.objects.get(id=place.id)
        instance.save()
        return redirect(reverse('chapter', kwargs={'course_name': course_name,
                                                   'slug': slug}))

    if file_upload_form.is_valid() and 'add_file' in request.POST:
        instance = file_upload_form.save(commit=False)
        instance.file_fk = Chapter.objects.get(id=place.id)
        instance.save()
        return redirect(reverse('chapter', kwargs={'course_name': course_name,
                                                   'slug': slug}))

    return render(request, "courses/chapter.html", context)


@user_passes_test(lambda user: user.is_lecturer)
def delete_course(request, course_name=None):
    instance = Course.objects.get(course_name=course_name)
    instance.delete()
    return HttpResponseRedirect(reverse('profile'))


@user_passes_test(lambda user: user.is_lecturer)
def delete_chapter(request, course_name=None, slug=None):
    instance = Chapter.objects.get(slug=slug)
    instance.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda user: user.is_lecturer)
def delete_yt_link(request, yt_id=None):
    instance = YTLink.objects.get(id=yt_id)
    instance.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda user: user.is_lecturer)
def delete_text_block(request, txt_id=None):
    instance = TextBlock.objects.get(id=txt_id)
    instance.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda user: user.is_lecturer)
def delete_file(request, file_id=None):
    instance = FileUpload.objects.get(id=file_id)
    instance.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda user: user.is_lecturer)
def update_course(request, course_name=None):
    instance = Course.objects.get(course_name=course_name)
    update_course_form = EditCourseForm(request.POST or None, instance=instance)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()

    context = {
        "title": "Edit",
        "form": update_course_form,
        "path": path,
        "redirect_path": redirect_path,
    }

    if update_course_form.is_valid():
        update_course_form.save()
        return redirect(reverse('profile'))

    return render(request, "courses/edit.html", context)


@user_passes_test(lambda user: user.is_lecturer)
def update_chapter(request, course_name=None, slug=None):
    instance = Chapter.objects.get(slug=slug)
    update_chapter_form = EditChapterForm(request.POST or None, instance=instance)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()

    context = {
        "title": "Edit",
        "course_name": course_name,
        "form": update_chapter_form,
        "path": path,
        "redirect_path": redirect_path,
    }

    if update_chapter_form.is_valid():
        update_chapter_form.save()
        return redirect(reverse('professor_course', kwargs={'course_name': course_name}))

    return render(request, "courses/edit.html", context)


@user_passes_test(lambda user: user.is_lecturer)
def update_yt_link(request, course_name=None, slug=None, yt_id=None):
    instance = YTLink.objects.get(id=yt_id)
    update_link_form = EditYTLinkForm(request.POST or None, instance=instance)

    context = {
        "title": "Edit",
        "course_name": course_name,
        "yt_id": yt_id,
        "slug": slug,
        "form": update_link_form,
        "path": "Profile",
        "redirect_path": "profile",
    }

    if update_link_form.is_valid():
        update_link_form.save()
        return redirect(reverse('chapter', kwargs={'course_name': course_name,
                                                   "slug": slug}))

    return render(request, "courses/edit.html", context)


@user_passes_test(lambda user: user.is_lecturer)
def update_text_block(request, course_name=None, slug=None, txt_id=None):
    instance = TextBlock.objects.get(id=txt_id)
    update_txt_form = EditTxtForm(request.POST or None, instance=instance)

    context = {
        "title": "Edit",
        "course_name": course_name,
        "text_id": txt_id,
        "form": update_txt_form,
        "slug": slug,
        "path": "Profile",
        "redirect_path": "profile",
    }

    if update_txt_form.is_valid():
        update_txt_form.save()
        return redirect(reverse('chapter', kwargs={'course_name': course_name,
                                                   "slug": slug}))

    return render(request, "courses/edit.html", context)


@user_passes_test(lambda user: user.is_lecturer)
def list_students(request, course_name=None):
    course = Course.objects.get(course_name=course_name)
    added_students = UserProfile.objects.filter(students_to_course=course)
    excluded_students = UserProfile.objects.exclude(students_to_course=course).filter(is_lecturer=False).filter(
        is_site_admin=False)

    query_first = request.GET.get("q1")
    if query_first:
        excluded_students = excluded_students.filter(username__icontains=query_first)

    query_second = request.GET.get("q2")
    if query_second:
        added_students = added_students.filter(username__icontains=query_second)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()

    context = {
        "title": "Edit students in course " + course_name,
        "excluded_students": excluded_students,
        "added_students": added_students,
        "course_name": course_name,
        "path": path,
        "redirect_path": redirect_path,
    }

    return render(request, "courses/add_students.html", context)


def add_students(request, student_id, course_name=None):
    student = UserProfile.objects.get(id=student_id)
    course = Course.objects.get(course_name=course_name)
    course.students.add(student)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda user: user.is_lecturer)
def remove_students(request, student_id, course_name=None):
    student = UserProfile.objects.get(id=student_id)
    course = Course.objects.get(course_name=course_name)
    course.students.remove(student)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




@login_required()
def addabout(request):
    topic_list = About.objects.all().order_by('-date_updated')
    first_abut = About.objects.get(id=1)
    add_new_topic = AddNewAbout(request.POST or None)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()

    search = request.GET.get("search")
    if search:
        topic_list = topic_list.filter(title__startswith=search)

    paginator = Paginator(topic_list, 10)

    if add_new_topic.is_valid():
        instance = add_new_topic.save(commit=False)
        instance.staff = request.user
        slug = slugify(instance.title)
        exists = About.objects.filter(slug=slug).exists()
        try:
            max_id = About.objects.latest('id').id
            max_id += 1
        except Exception, e:
            pass

        # If slug exist append slug by id
        if exists:
            slug = "%s-%s" % (slug, max_id)

        instance.slug = slug

        if not instance.title:
            instance.save()

        return redirect(reverse("courses"))

    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "title": "About",
        "add_new_topic_form": add_new_topic,
        "topic_list": queryset,
        "path": path,
        "redirect_path": redirect_path,
    }

    return render(request, "adminpan.html", context)






@user_passes_test(lambda user: user.is_staff)
def update_about(request):
    topic_list = About.objects.get(id=1)
    add_new_topic = AddNewAbout(instance=topic_list)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()
    queryset = None

    search = request.GET.get("search")
    if search:
        topic_list = topic_list.filter(title__startswith=search)

    paginator = Paginator(topic_list, 10)


    if add_new_topic.is_valid():
        instance = add_new_topic.save(commit=False)
        instance.staff = request.user
        slug = slugify(instance.title)
        exists = About.objects.filter(slug=slug).exists()
        try:
            max_id = About.objects.latest('id').id
            max_id += 1
        except Exception, e:
            pass

        # If slug exist append slug by id
        if exists:
            slug = "%s-%s" % (slug, max_id)

        instance.slug = slug

        if not instance.title:
            instance.save()

        return redirect(reverse("courses"))

    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
         k = 12
      
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "title": "update",
        "add_new_topic_form": add_new_topic,
        "topic_list": queryset,
        "path": path,
        "redirect_path": redirect_path,
    }



    return render(request, "adminpan.html", context)





def update_post(request):
    topic_list = About.objects.get(id=1)
    add_new_topic = AddNewAbout(request.POST or None)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()
    queryset = None

    search = request.GET.get("search")
    if search:
        topic_list = topic_list.filter(title__startswith=search)

    paginator = Paginator(topic_list, 10)


    if add_new_topic.is_valid():
        
        instance = add_new_topic.save(commit=False)
      
        topic_list.title = instance.title
        topic_list.sub_title = instance.sub_title
        topic_list.about_message = instance.about_message
        slug = slugify(topic_list.title)

        exists = About.objects.filter(slug=slug).exists()
       

        topic_list.slug = slug
        if not topic_list.title and topic_list.about_message:
            instance.save()
        
        topic_list.save()

        return redirect(reverse("courses"))
        


    return render(request, "adminpan.html", context)





@login_required()
def addcontact(request):
    topic_list = Contact.objects.all().order_by('-date_updated')

    try:
        first_abut =Contact.objects.get(id=1) 
    except Exception, e:
        pass
    add_new_topic = AddNewContact(request.POST or None)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()

    search = request.GET.get("search")
    if search:
        topic_list = topic_list.filter(title__startswith=search)

    paginator = Paginator(topic_list, 10)

    if add_new_topic.is_valid():
        instance = add_new_topic.save(commit=False)
        instance.staff = request.user
        slug = slugify(instance.email)
        exists = Contact.objects.filter(slug=slug).exists()
        try:
            max_id = Contact.objects.latest('id').id
            max_id += 1
        except Exception, e:
            pass

        # If slug exist append slug by id
        if exists:
            slug = "%s-%s" % (slug, max_id)

        instance.slug = slug

        if not instance.phonenumber and not instance.email and not  instance.address:
            instance.save()

        return redirect(reverse("courses"))

    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "title": "Contact",
        "add_new_topic_form": add_new_topic,
        "topic_list": queryset,
        "path": path,
        "redirect_path": redirect_path,
    }

    return render(request, "adminpan.html", context)





@user_passes_test(lambda user: user.is_staff)
def update_contact(request):
    topic_list = None 
    try:
        topic_list = Contact.objects.get(id=1)
    except Exception, e:
        pass

    add_new_topic = AddNewAbout(instance=topic_list)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()
    queryset = None

    search = request.GET.get("search")
    if search:
        topic_list = topic_list.filter(email__startswith=search)

    paginator = Paginator(topic_list, 10)


    if add_new_topic.is_valid():
        instance = add_new_topic.save(commit=False)
        instance.staff = request.user
        slug = slugify(instance.title)
        exists = Contact.objects.filter(slug=slug).exists()
        try:
            max_id = Contact.objects.latest('id').id
            max_id += 1
        except Exception, e:
            pass

        # If slug exist append slug by id
        if exists:
            slug = "%s-%s" % (slug, max_id)

        instance.slug = slug

        if not instance.email:
            instance.save()

        return redirect(reverse("courses"))

    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
         k = 12
      
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "title": "update_contact",
        "add_new_topic_form": add_new_topic,
        "topic_list": queryset,
        "path": path,
        "redirect_path": redirect_path,
    }



    return render(request, "adminpan.html", context)

