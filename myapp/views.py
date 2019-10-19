from django.shortcuts import render
from django.core.files import File
from django.core.files.base import ContentFile
from django.contrib.auth.forms import AuthenticationForm

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import documentSerializers

from myapp.models import Document, New_Document
from myapp.forms import DocumentForm

from .File_Filter_App.code import Airtel_AV_Dashboard
from os.path import basename

class documentsList(APIView):
    def get(self, request):
        docs = Document.objects.all()
        serializer = documentSerializers(docs, many=True)
        return Response(serializer.data)
        
    def post(self):
        pass


def index(request):
    # Handle file upload
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            #Process and create a new file
            try:              
                id = Document.objects.all()[0].id
                filepath = Document.objects.get(id=id).docfile.file.name                
                filename = basename(Document.objects.get(id=id).docfile.name)
                Airtel_AV_Dashboard("Test").process(filepath, filename)

                name = ""
                for l in filename:
                    if l == ".":
                        break            
                    else:
                        name += l
                                
                with open(f"myapp/Final Output/{name} modified.xlsx", "rb") as stored_file:
                    #Store the new file in the database
                    new_doc  = New_Document(docfile = File(stored_file, name = f"{name} modified.xlsx"))
                    new_doc.save()
                    
                #for each_file in Document.objects.all():
                    #each_file.delete()
            
            except Exception as e:
                print(f"Exception {e}")
                #for each_file in Document.objects.all():
                    #each_file.delete()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('index'))
    else:
        
        form = DocumentForm() # A empty, unbound form
        #if len(New_Document.objects.all()) > 0:
            #previous_document = New_Document.objects.all()[0]
            #previous_document.delete()
        
    # Load documents for the list page
    query_set = New_Document.objects.all()
    documents = []
    cnt = len(query_set) - 1
    for i in query_set:
        documents.append(query_set[cnt])
        cnt -= 1
    documents = documents

    # Render file_processing_indexpython manage.py runserver
    #  page with the documents and the form
    return render(request, 'file_processing_index.html', {'documents': documents, 'name':"Download File", 'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        #if form.is_valid():
            #return redirect("index")

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form':form})





