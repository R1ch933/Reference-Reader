from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
import docx
from django.contrib import messages
import googlesearch
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django import template

# the home page view function
# ties the neccessary html file with the view model
def index (request):
    return render(request, 'reference_reading/index.html')
# the page with the list of files uploaded
# redirects to login page if no one is logged in with @login_required
@login_required
def files(request):
    file = File_Name.objects.filter(owner=request.user).order_by('date_added')
    context = {"file": file}
    return render(request, 'reference_reading/files.html', context)
# function that searches for the right info to display for references
# Finds the author and title of the source
# could use some improvement
def handle_uploaded_file(list, rtn_list):
    if list != []: # empty list?
        for para in list[:-1]: # for each paragraph in the list received from read_dcx()
            if '“' in para: # removes the extra " present
                para = para.replace('“','')
            part = para.split('.') # splits the paragraphs by sentence using the period as stamps
            part[0] = part[0] + ':' # adds colon next to the author name(s) for display when rendered
            if len(para[0]) <= 21: # if the first element is over 21 characters (to check if its a name), it won't recognize
                                   # the citation as a proper mla format and skips it
                rtn_list.append(' '.join(part[0:2])) # specifically joins only the author and title elements
            else:
                pass
        return rtn_list
    else:
        return rtn_list
# uses the docx API in order to read and organize a docx file by paragraph
def read_dcx(file):
    fullText = []
    for para in file.paragraphs: # takes each paragraph and inserts them into a list
        fullText.append(para.text)
    full = ''.join(fullText)
    return fullText
#
def google_search_reference(list, rtn_list): # unused because the execution time is too slow
    if list != []:
        ele = googlesearch.search(list[0], tld='com', lang='en', num=10, start=0, stop=None, pause=2.0)
        rtn_list.append(ele[0])
        google_search_reference(list[1:], rtn_list)
    elif list == []:
        pass
    return rtn_list

# Function to download file being currently viewed
def download(request, file_id):
    file = get_object_or_404(File_Name, id=file_id) # grabs current file
    file_path = os.path.join(settings.MEDIA_ROOT, file.name.path)
    if os.path.exists(file_path) and request.method == 'POST': # if the file path exists and POST is present
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
    # this would technically replace context rendered when opening the page with this one
    # however because the page doesn't need to update or alter after already being rendered
    # this isn't a problem and would respectfully reset after reopening this page
    context = {'files': file}
    return render(request, 'reference_reading/cite.html', context)

def delete_file(request, file_id):
    file = get_object_or_404(File_Name, id=file_id)
    if request.method == 'POST':
        file.delete()
        os.remove(file.name.path)
        return redirect('reference_reading:files')
    context = {"files": file}
    return render(request, 'reference_reading:cite.html', context)

# View function for the page full fo the file's references
@login_required
def cite(request, file_id):
    file = get_object_or_404(File_Name, id=file_id)
    if file.owner != request.user: #security
        raise Http404
    # process docx file
    doc = docx.Document(file.name.path)
    full = read_dcx(doc)
    if "Work Cited" in full:
        full = full[((full.index('Work Cited ')) + 1):]
    elif "Work Cited " in full:
        full = full[((full.index('Work Cited')) + 1):]
    elif "Cited" in full:
        full = full[((full.index('Cited'))+1):]
    elif 'Citations' in full:
        full = full[(full.index('Citations'))+1:]
    elif 'Citations ' in full:
        full = full[(full.index('Citations '))+1:]
    elif "Cited " in full:
        full = full[((full.index('Cited ')) + 1):]
    else:
        full = []
    l1 = (handle_uploaded_file(full, []))
    # transfer data to html
    context = {'files': file, 'ref': l1}
    return render(request, 'reference_reading/cite.html', context)
# View function for uploading a new file
# Uploads file along with adding a name to the entry
@login_required
def new_file(request):
    if request.method != 'POST':
        form = UploadFileForm()
    else:
        form = UploadFileForm(request.POST, request.FILES)
        for filename, file in request.FILES.items():
            val = request.FILES[filename].name
        if form.is_valid() and '.docx' in val:
            new_file = form.save(commit=False)
            new_file.owner = request.user
            new_file.save()
            return redirect('reference_reading:files')
        else:
            form = UploadFileForm()
            messages.success(request, 'You may only upload a ".DOCX" file')
    context = {'form': form}
    return render(request, 'reference_reading/new_file.html', context)

def decor(file_name):
    file_name = os.path.abspath('bg_jumbo.jpg')
    return file_name






