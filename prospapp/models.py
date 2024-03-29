from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.timezone import utc

import pytz, datetime, base64, hashlib

#################################
##### ----- Constants ----- #####
#################################

ACCOUNT_TYPES = (
    ('CANDIDATE', 'Candidate'),
    ('CLIENT',    'Client'),
    ('ADMIN',     'Admin'),
)

TESTINSTANCE_STATUSES = (
    ('PENDING',   'Pending'),    #User has not started the Test.
    ('ACTIVE',    'Active'),     #User has started the Test.
    ('PROCESSING','Processing'), #User has finished the Test and it is being processed.
    ('COMPLETE',  'Complete'),   #Test is ready for Client inspection.
    ('FINISHED',  'Finished'),   #Client has closed the test.
    ('CANCELLED', 'Cancelled'),  #User has cancelled the Test.
)

################################
##### ----- Managers ----- #####
################################

class AccountManager(models.Manager):
    def all(self):
        return self.get_query_set().filter(is_active=True)

    def get(self, *args, **kwargs):
        kwargs['is_active'] = True
        try:
            ret = self.get_query_set().get(*args, **kwargs)
        except self.model.DoesNotExist:
            ret = False
        return ret

    def all_with_deleted(self):
        return super(AccountManager, self).all()

    def get_with_deleted(self, *args, **kwargs):
        return super(AccountManager, self).get(*args, **kwargs)

class BaseManager(models.Manager):
    def all(self):
        return self.get_query_set().filter(deleted_at=None)

    def get(self, *args, **kwargs):
        kwargs['deleted_at'] = None
        try:
            ret = self.get_query_set().get(*args, **kwargs)
        except self.model.DoesNotExist:
            ret = False 
        return ret

    def all_with_deleted(self):
        return super(BaseManager, self).all()

    def get_with_deleted(self, *args, **kwargs):
        return super(BaseManager, self).get(*args, **kwargs)

##############################
##### ----- Models ----- #####
##############################

### User class extension ###
class Account(AbstractUser):
    objects = AccountManager()
    type = models.CharField(choices=ACCOUNT_TYPES, max_length=31, default='CANDIDATE')

### Base model class with CRUD data. ###
class BaseModel(models.Model):
    objects    = BaseManager()
    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def fe_delete(self):
        time = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.deleted_at = time
        self.save()

    def save(self, *args, **kwargs):
        time = datetime.datetime.utcnow().replace(tzinfo=utc)
        if not self.id:
            self.created_at = time
        self.updated_at = time
        super(BaseModel, self).save(*args, **kwargs)

### Database representation of a Docker image. ###
class BaseImage(BaseModel):
    label      = models.CharField(max_length=31)                                                           # (Front-facing) label for the image.
    name       = models.CharField(max_length=31)                                                           # The name of the actual Docker image.
    tag        = models.CharField(max_length=31, blank=True)                                               # The tag of the actual Docker image.
    identifier = models.CharField(max_length=127, blank=True)                                              # The ID of the actual Docker image.
    parent     = models.ForeignKey('self', blank=True, null=True, related_name='images', parent_link=True) # (Front-facing) This image's parent (not always Dockerfile 'from')
    
    def __unicode__(self):
        return self.label + ' (' + self.name + ':' + self.tag + ')'

### Database representation of a Clonable Docker 'Test' ###
class TestImage(BaseImage):
    owner            = models.ForeignKey(Account, related_name='images', parent_link=True)

    #Private TestImages do not exist yet.
    is_public        = models.BooleanField(default=True)
    instructions     = models.TextField(default='')

    def __unicode__(self):
        return self.name + ':' + self.tag

### Database representation of an open Prospop 'Test'. ###
class Test(BaseModel):
    label        = models.CharField(max_length=31)
    image        = models.ForeignKey(TestImage, related_name='tests', parent_link=True) 
    is_public    = models.BooleanField(default=True)
    owner        = models.ForeignKey(Account, related_name='tests', parent_link=True)
    instructions = models.TextField(default='')

def clone_instructions(sender, instance, created, **kwargs):  
    if created:
        instance.instructions = instance.image.instructions
        instance.save()

post_save.connect(clone_instructions, sender=Test) 

### Database representation of a Docker container running a Test ###
class TestInstance(BaseModel):
    test   = models.ForeignKey(Test, related_name='instances', parent_link=True)
    owner  = models.ForeignKey(Account, related_name='instances', parent_link=True)
    status = models.CharField(choices=TESTINSTANCE_STATUSES,max_length=31,default='PENDING') 

### A Permissions object between Tests and Accounts ###
class TestAuth(BaseModel):
    test  = models.ForeignKey(Test, related_name='authorizations')
    user  = models.ForeignKey(Account, related_name='authorizations', blank=True, null=True)
    email = models.CharField(max_length=255, blank=True)
    key   = models.CharField(max_length=32,  blank=True)

def get_key(sender, instance, created, **kwargs):
    if created:
        hasher = hashlib.sha1(str(instance.created_at) + str(instance.id))
        instance.key = base64.urlsafe_b64encode(hasher.digest()[0:31])
        instance.save()

post_save.connect(get_key, sender=TestAuth)