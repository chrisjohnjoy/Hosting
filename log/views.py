from django.shortcuts import redirect, render
from logi.models import Medicine


def index(request):

    if request.user.is_superuser:
        return redirect('/login/admin_dashboard/')
    # Retrieve the list of medicines from the database
    medicines = Medicine.objects.all()

    context = {
        'medicines': medicines,
    }

    return render(request, 'index.html', context)

def about(req):
    if req.user.is_superuser:
        return redirect('/login/admin_dashboard/')
    return render(req,'about.html')
