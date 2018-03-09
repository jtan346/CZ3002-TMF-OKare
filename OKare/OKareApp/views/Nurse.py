from django.shortcuts import render
# Create your views here.
def index(Request):
    #Id will get from session once login completed
    id = 1
    context = {'id': id}
    return render(Request, 'nurse/index.html', context)
    pass