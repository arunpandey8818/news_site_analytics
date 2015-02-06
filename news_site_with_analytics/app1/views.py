from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404,render

from app1.models import *
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def logout_view(request):
    logout(request)
    return render_to_response('app1/index.html', {'logout' : 1})


def my_view(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['passwd']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session["username"] = user
                
                u = UserLoginTrack()
                u.user=user
                u.save()
                return HttpResponseRedirect('/app1/index/home/')
                # Redirect to a success page.
            else:
                cxt = {'disable_error' : 1 }
                return render_to_response('app1/disabledaccount.html', cxt)
                # Return a 'disabled account' error message
        else:
            return render_to_response('app1/index.html', {'wrongpass' : 1})
            # Return an 'invalid login' error message.
 

def user_profile(request):
    return render_to_response('app1/index.html')


def index(request):
    return render_to_response('app1/index.html')


@login_required(login_url='/app1/index/')
def user_prof(request):
    usrname = request.POST.get('username')
    pas = request.POST.get('pass')
    cpas = request.POST.get('cpass')
    fnm = request.POST.get('fname')
    lnm = request.POST.get('lname')
    age = request.POST.get('age')
    stf = request.POST.get('staff')
    mob = request.POST.get('mobno')
    prefer = request.POST.getlist('prefrences')
    prefer = map(int, prefer)
         
    if stf == "True":
        staff_status = 1
        stf_stat = True
    if stf == "False":
        staff_status = 2
        stf_stat = False
    
    if cpas != pas:
        alltag = Tag.objects.all()
        cxt = {
         'usr' : usrname , 'f_nm' : fnm , 'l_nm' : lnm , 'age_' : age , 'stf_' : staff_status , 'mob_no' : mob ,  
         'tags' : alltag , 'prefer_' : prefer ,
         'passerror': 1
           }
        return render_to_response('app1/signup.html', cxt)
    
    newUser = UserProfile()
    
    user = User()
    user.username = usrname
    user.first_name = fnm
    user.last_name = lnm
    #user.password = pas
    user.set_password(pas)
    user.is_staff = stf_stat
    user.save()
    newUser.user = user
    newUser.age = age
    newUser.mobile_no = mob
    newUser.save()
    newUser.prefrences.add(*prefer) 
    cxt = {  'pass_error': 1
           }
    return render_to_response('app1/index.html', cxt)
    
    
@login_required(login_url='/app1/index/')    
def detail(request, storyId):
    storytag = StoryTagTrack()
    story_istance= Story.objects.get(id=storyId)
    storytag.storyid = story_istance
    story_tag_list = story_istance.prefrence.all()
    storytag.save()
    new_tag_list = []
    for i in story_tag_list:
        new_tag_list.append(i.id)
    storytag.tagid.add(*new_tag_list)
    user_story_track = UserStoryTrack()
    user_story_track.user = request.user
    user_story_track.storyid = Story.objects.get(id=storyId)
    
    user_story_track.save()
    s = Story.objects.get(id = storyId)
    s.counter = s.counter + 1
    s.save()
    
    story_tag_track = StoryTagTrack()
    story_tag_track.storyid = Story.objects.get(id=storyId)
    taglist = story_tag_track.storyid.prefrence.all()
    
    story = get_object_or_404(Story, id=storyId)
    cxt = {
        'story': story
    }
    return render_to_response('app1/detail.html', cxt)
    s = Story.objects.get(id = storyId)

    
@login_required(login_url='/app1/index/')
def home(request):
        all_story = Story.objects.all()
        sorted_story = all_story.order_by('-pub_date')
        top_story = sorted_story.filter(is_top_news = "True")
        items = top_story.order_by('-pub_date')[:5]
        print request.session["username"]   
        logged_user = UserProfile.objects.get(user__username__exact=request.user)
        logged_pref = logged_user.prefrences.all()
        c = 0
        prelist = list(logged_pref)
        alist = []
        for temp in sorted_story:
            if c < 5:
                storylst = temp.prefrence.all()
                storylist = list(storylst)
                any_in = any(i in storylist for i in prelist)
                if any_in:
                    c = c + 1
                    alist.append(temp)
            usr = UserProfile.objects.get(user__username__exact=request.user)
    
        prefr = usr.prefrences.all()
        ppr = list(prefr)    
        story_stories = Story.objects.order_by('-counter')[:5]
        
        cxt = {'tagg' : ppr, 'tgs' : alist, 'stories_list' : story_stories, 'stories': items }
        return render_to_response('app1/home.html', cxt, context_instance=RequestContext(request))
         
         
@login_required(login_url='/app1/index/')
def analytics(request):
    staff_status = request.user.is_staff
    if staff_status == True:
        return render_to_response('app1/analytics.html')
    else:
        return HttpResponseRedirect('/app1/index/home/')
         

            
@login_required(login_url='/app1/index/')
def tagusage(request):
    import datetime
    
    e_day = datetime.datetime.now()
    s_day = datetime.datetime.now() - datetime.timedelta(days=1)
    from datetime import datetime
    current_date = datetime.strftime(e_day, '%Y-%m-%d')
    last_date = datetime.strftime(s_day, '%Y-%m-%d')
    if request.method == "POST":
        sday = request.POST.get('sday')
        eday = request.POST.get('eday')
        sday_ = datetime.strptime(sday, '%Y-%m-%d')
        eday_ = datetime.strptime(eday, '%Y-%m-%d')
        
        story_tag = StoryTagTrack.objects.filter(tagtime__gte = sday_).filter(tagtime__lte = eday_).values('tagid__name').annotate(count=Count('storyid')).order_by('-count')
               
        cxt = {'storytag' : story_tag , 'start_date' : last_date , 'end_date' : current_date}
        return render_to_response('app1/tagusage.html', cxt)
    else:
        cxt = {'start_date' : last_date , 'end_date' : current_date }
        return render_to_response('app1/tagusage.html', cxt)

    
@login_required(login_url='/app1/index/')    
def useractivity(request):
    import datetime
    
    e_day = datetime.datetime.now()
    s_day = datetime.datetime.now() - datetime.timedelta(days=1)
    from datetime import datetime
    current_date = datetime.strftime(e_day, '%Y-%m-%d')
    last_date = datetime.strftime(s_day, '%Y-%m-%d')
    from datetime import date
    if request.method == "POST":
        sday = request.POST.get('sday')
        eday = request.POST.get('eday')
        sday_ = datetime.strptime(sday, '%Y-%m-%d')
        eday_ = datetime.strptime(eday, '%Y-%m-%d')
                
        user_log = UserLoginTrack.objects.filter(usertime__gte = sday_).filter(usertime__lte = eday_).values('user','user__username').annotate(count=Count('user')).order_by('-count')         
                
        userstory = UserStoryTrack.objects.filter(storytime__gte = sday_).filter(storytime__lte = eday_).values('user','user__username').annotate(count=Count('user')).order_by('user')
        
        temp={}
        for i in user_log:
            temp[i['user']]={'logincount':i['count'], 'username':i['user__username'], 'storycount':0 }
        for j in userstory:
            if j['user'] in temp:
                temp[j['user']]['storycount'] = j['count']
        cxt = {'temp_': temp, 'start_date' : last_date , 'end_date' : current_date }
        
        return render_to_response('app1/useractivity.html', cxt, context_instance=RequestContext(request))
    else:
        cxt = {'start_date' : last_date , 'end_date' : current_date }
        return render_to_response('app1/useractivity.html', cxt, context_instance=RequestContext(request))
    

def signup(request):
    alltag = Tag.objects.all()
    return render_to_response('app1/signup.html', {'tags' : alltag})

