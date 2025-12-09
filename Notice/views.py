from django.shortcuts import render, redirect
from .forms import NoticeForm
from Notice import urls
from .models import Notice

def create_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create-notice')
    else:
        form = NoticeForm()
    return render(request, 'create_notice.html', {'form': form})


def notice_list(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'notice_list.html', {'notices': notices})

