from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User   
        

class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField()  
    mobile_no = models.CharField(max_length=10)       
    prefrences = models.ManyToManyField(Tag)

    def __unicode__(self):
       return self.user.username




class Story(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    pub_date = models.DateField(auto_now_add=True)
    prefrence = models.ManyToManyField(Tag)
    is_top_news = models.BooleanField()  
    counter = models.IntegerField()  

    def __unicode__(self):
        return self.title
    

class StoryTagTrack(models.Model):
    tagtime = models.DateField(auto_now_add=True)
    storyid = models.ForeignKey(Story)
    tagid = models.ManyToManyField(Tag)


class UserStoryTrack(models.Model):
    storytime = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User)
    storyid = models.ForeignKey(Story)


class UserLoginTrack(models.Model):
    usertime = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User)    
    

admin.site.register(Story)    
admin.site.register(UserProfile)
admin.site.register(Tag)

