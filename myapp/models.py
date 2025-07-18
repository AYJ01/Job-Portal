from django.db import models
from django.contrib.auth.models import AbstractUser


class Login(AbstractUser):
    userType = models.CharField(max_length=100)
    viewPass = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True,default="Pending")
    pdate = models.DateField(max_length=100, null=True)

class UserRegistration(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=300, null=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(null=True, upload_to="profile")
    resume = models.FileField(null=True, upload_to="resume")
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
    Rating=models.CharField(max_length=100, null=True)

class Client_reg(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=300, null=True)
    gender = models.CharField(max_length=100)
    image = models.ImageField(null=True, upload_to="profile")
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
    proof = models.FileField(null=True)


class Job_Portal(models.Model):
    cid = models.ForeignKey(Client_reg, on_delete=models.CASCADE, null=True)
    jname = models.CharField(max_length=100, null=True)
    salary = models.CharField(max_length=300, null=True, blank=True)
    ex_level = models.CharField(max_length=300, null=True)
    job_type = models.CharField(max_length=300, null=True)
    description = models.CharField(max_length=300, null=True)
    date = models.CharField(max_length=300, null=True, blank=True)
    image = models.ImageField(null=True, upload_to="profile")

    


class Job_Application(models.Model):
    company = models.ForeignKey(Client_reg, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, null=True)
    job = models.ForeignKey(Job_Portal, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=300, null=True, blank=True)
    education = models.CharField(max_length=300, null=True)
    field = models.CharField(max_length=300, null=True)
    resume = models.FileField(null=True, upload_to="profile")
    status = models.FileField(null=True, default="Applied")
    interviewdate = models.DateField(null=True)
    interviewtime = models.TimeField(null=True)
    message = models.CharField(max_length=300, null=True)

class Work(models.Model):
    job = models.ForeignKey(Job_Portal, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Client_reg, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, null=True)
    pdate = models.CharField(max_length=300, null=True, blank=True)
    ldate = models.CharField(max_length=300, null=True)
    desc = models.CharField(max_length=300, null=True)
    title = models.CharField(max_length=300, null=True)
    amount = models.CharField(max_length=300, null=True,default="Not_defined")
    status = models.FileField(null=True, default="Assigned")
    payment = models.FileField(null=True, default="Not_Paid")
    
class Message(models.Model):
    sender = models.ForeignKey(Client_reg, on_delete=models.CASCADE, null=True)
    senderemail = models.CharField(max_length=300, null=True, blank=True)
    reciveremail = models.CharField(max_length=300, null=True, blank=True)
    receiver = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=300, null=True, blank=True)
    time = models.CharField(max_length=300, null=True)
    type = models.CharField(max_length=300, null=True)
    message = models.CharField(max_length=300, null=True)
    # status = models.FileField(null=True, default="Added")
    
class Feedback(models.Model):
    cid = models.ForeignKey(Client_reg, on_delete=models.CASCADE, null=True)
    wid=models.ForeignKey(Work, on_delete=models.CASCADE, null=True)
    uid = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, null=True)
    feed = models.EmailField(max_length=100, null=True)
    rating = models.IntegerField(null=True, blank=True)
    Tavg = models.CharField(max_length=100,  null=True, blank=True)
    
class Guidence(models.Model):
    name=models.CharField(max_length=100,null=True)
    url=models.CharField(max_length=100,null=True)
    desc=models.CharField(max_length=300,null=True)

class UserFeedback(models.Model):
    uid = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, null=True)
    wid = models.ForeignKey(Job_Portal, on_delete=models.CASCADE, null=True)
    feed = models.CharField(max_length=500, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    amount = models.CharField(max_length=100, null=True)

class Posts(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True)
    desc = models.CharField(max_length=300, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(null=True, upload_to="profile")

class Requests(models.Model):
   user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, null=True)
   company = models.ForeignKey(Client_reg, on_delete=models.CASCADE, null=True)
   date = models.DateTimeField(auto_now_add=True, null=True)
   salary = models.CharField(max_length=100, null=True)
   status = models.CharField(max_length=100, null=True,default="Requested")
   interviewdate = models.DateField(null=True)
   interviewtime = models.TimeField(null=True)
   message = models.CharField(max_length=300, null=True)

class UserAdminChat(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    adminmessage = models.CharField(max_length=300, null=True)
    usermessage = models.CharField(max_length=300, null=True)
   
class UserPayment(models.Model):
    user_amount=models.CharField(max_length=100, null=True)
    client_amount = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

class Allpayments(models.Model):
    amount = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
    endingdate=models.DateField(null=True)
