from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100)
    host = models.ForeignKey('Users', on_delete=models.CASCADE)  # host user
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    location_permission = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} in {self.group.name}"

class StudentLocation(models.Model):
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    last_updated = models.DateTimeField(auto_now=True)
    battery_level = models.CharField(max_length=10, blank=True, null=True)  # optional

    def __str__(self):
        return f"{self.user.name} location in {self.group.name}"
