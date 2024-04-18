from django.shortcuts import render,redirect,get_object_or_404
from feed.models import *
from django.views.generic import ListView,TemplateView
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class FeedLV(ListView):
    model=Feed

@login_required
def create_feed(request):
    if request.method == 'POST':
        user = request.user
        feeds_title = request.POST.get('title')
        feeds_description = request.POST.get('description')
                # 이미지 저장 및 url 설정 내용
        fs=FileSystemStorage()
        uploaded_file = request.FILES['file']
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)

        if feeds_title and feeds_description and url:
            feed = Feed.objects.create(user=user,title=feeds_title, description=feeds_description)
            image = Image.objects.create(user=user, feed=feed, image_url=url)
            return redirect('feed:index')  # 피드 목록 페이지로 리다이렉트
    return render(request, 'feed/feed_create.html', {})

def user_feed(request):
    # 현재 로그인한 사용자의 피드만 필터링
    user_feeds = Feed.objects.filter(user=request.user)
    context = {
        'object_list': user_feeds
    }
    return render(request, 'feed/user_feed_list.html', context)


@login_required
def feed_update(request, feed_id):
    # 피드 객체 가져오기
    feed = get_object_or_404(Feed, id=feed_id)
    
    # 현재 로그인한 사용자가 해당 피드의 작성자인지 확인
    if request.user != feed.user:
        # 작성자가 아니라면 권한이 없는 메시지를 반환하거나, 다른 처리를 수행할 수 있습니다.
        return redirect('feed:user_feed')
    
    # POST 요청일 경우 폼 데이터 처리
    if request.method == 'POST':
        feed.title = request.POST['title']
        feed.description = request.POST['description']
        feed.save()

        return redirect('feed:user_feed')
    # 수정할 피드를 템플릿에 전달
    return render(request, 'feed/feed_update.html', {'feed': feed})


@login_required
def feed_delete(request, feed_id):    
    # 피드 객체 가져오기
    feed = get_object_or_404(Feed, id=feed_id)
    
    # 현재 로그인한 사용자가 해당 피드의 작성자인지 확인
    if request.user != feed.user:
        # 작성자가 아니라면 권한이 없는 메시지를 반환하거나, 다른 처리를 수행할 수 있습니다.
        return redirect('feed:user_feed')
    
    feed.delete()
    return redirect('feed:user_feed')


@login_required
def feed_like(request, feed_id):
    # 피드 객체 가져오기
    feed = get_object_or_404(Feed, id=feed_id)
    
    # 현재 로그인한 사용자가 해당 피드에 이미 좋아요를 눌렀는지 확인
    if request.user in feed.likes.all():
        # 이미 좋아요를 눌렀다면 취소
        feed.likes.remove(request.user)
    else:
        # 좋아요 추가
        feed.likes.add(request.user)

    # JSON 응답으로 좋아요 수 반환
    return redirect('feed:index')


#--- Tag View
class TagCloudTV(LoginRequiredMixin,TemplateView):
    template_name = 'taggit/taggit_cloud.html'


class TaggedObjectLV(LoginRequiredMixin,ListView):
    template_name = 'feed/feed_list.html'
    model = Feed

    def get_queryset(self):
        return Feed.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context
