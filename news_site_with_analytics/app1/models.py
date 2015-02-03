from django.contrib import admin
from django.db import models

from django.contrib.auth.models import User   
        

class Pref(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class UserProf(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField()  
    mobile_no = models.CharField(max_length=10)       
    prefrences = models.ManyToManyField(Pref)

    def __unicode__(self):
       return self.user.username


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField()  
    mobile_no = models.CharField(max_length=10)
class Pref(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name
class Register(models.Model):
    username = models.CharField(max_length=200)
    passwrd = models.CharField(max_length=200)
    cpasswrd = models.CharField(max_length=200) 
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    mobile_no = models.IntegerField(max_length=254)
    prefrences = models.ManyToManyField(Pref)
    def __unicode__(self):
        return self.username
class Stories(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    prefrence = models.ManyToManyField(Pref)
    is_top_news = models.BooleanField()    
    def __unicode__(self):
        return self.title
class UserLoginTrack(models.Model):
    usertime = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User)
class UserLoginTrackNew(models.Model):
    usertime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)    
class UserStoryTrack(models.Model):
    storytime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    storyid = models.ForeignKey(Stories)
class StoryTagTrack(models.Model):
    tagtime = models.DateTimeField(auto_now_add=True)
    storyid = models.ForeignKey(Stories)
class StoryTagTrackNew(models.Model):
    tagtime = models.DateTimeField(auto_now_add=True)
    storyid = models.ForeignKey(Stories)
    tagid = models.ManyToManyField(Pref)


class Story(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    prefrence = models.ManyToManyField(Pref)
    is_top_news = models.BooleanField()  
    counter = models.IntegerField()  

    def __unicode__(self):
        return self.title
    

class StoryTagTrackNewM(models.Model):
    tagtime = models.DateTimeField(auto_now_add=True)
    storyid = models.ForeignKey(Story)
    tagid = models.ManyToManyField(Pref)


class UserStoryTrackNewM(models.Model):
    storytime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    storyid = models.ForeignKey(Story)


class UserLoginTrackNewM(models.Model):
    usertime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)    
    

admin.site.register(Story)    
admin.site.register(UserProf)
admin.site.register(Pref)

