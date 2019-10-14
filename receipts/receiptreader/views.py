from django.http import HttpResponse
from django.shortcuts import render
from receiptreader.models import Document

# Create your views here.
def index(request):
  documents = Document.objects.all()
  #output = ', '.join([d.filename for d in documents])
  #return HttpResponse(output)



  return render(request, 'index.html', {'documents':documents})
