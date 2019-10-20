from django.http import HttpResponse
from django.shortcuts import render
from receiptreader.models import RawReceipt

# Create your views here.
def index(request):
  documents = RawReceipt.objects.all()
  #output = ', '.join([d.filename for d in documents])
  #return HttpResponse(output)



  return render(request, 'index.html', {'documents':documents})
