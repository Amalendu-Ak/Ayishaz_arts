from django.db import models

class user(models.Model):
    uid=models.AutoField(primary_key=True)
    utype=models.CharField(max_length=30)
    uname=models.CharField(max_length=30)
    adrs = models.CharField(max_length=200)
    eml = models.CharField(max_length=30)
    phn=models.CharField(max_length=10)
    pas = models.CharField(max_length=30)

class PasswordReset(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    #security
    token=models.CharField(max_length=4)


class item(models.Model):
    iid=models.AutoField(primary_key=True)
    image=models.FileField()
    iname=models.CharField(max_length=30)
    rate=models.IntegerField()
    qty=models.IntegerField()
    prate=models.IntegerField()
    pqty = models.IntegerField(default=1)

class cart(models.Model):

    uid = models.ForeignKey(user, on_delete=models.CASCADE)
    iid=models.ForeignKey(item, on_delete=models.CASCADE)
    cqty=models.IntegerField(default=1)
    trate = models.IntegerField()

class order(models.Model):
    oid=models.AutoField(primary_key=True)
    uid = models.ForeignKey(user, on_delete=models.CASCADE)
    iid=models.ForeignKey(item, on_delete=models.CASCADE)
    oadrs=models.CharField(max_length=200,default='')
    ono = models.CharField(max_length=10,default='')
    odate=models.DateField()
    ddate=models.DateField(default=None)
    tqty = models.IntegerField(default=1)
    frate = models.IntegerField(default=1)#finalrate

