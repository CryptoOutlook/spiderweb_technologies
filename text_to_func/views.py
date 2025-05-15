from django.shortcuts import render

# Create your views here.
def homepage(request):
    answer = None
    if request.method == "POST":
        input1 = request.POST.get('input1')
        input2 = request.POST.get('input2')
        answer = f"{input1} {input2}"
    return render(request, 'homepage.html', {'answer': answer})