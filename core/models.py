from django.db import models
from django.db.models import Q
import unicodedata

class Port(models.Model):
    name = models.CharField(max_length=10, blank=False)
    value = models.CharField(max_length=100, blank=False)
    tcp = models.BooleanField(default=True, blank=False)
    udp = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return (self.name)

class Client(models.Model):
    nickname = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200, blank=False)
    last_name = models.CharField(max_length=200, blank=False)
    unrestricted = models.BooleanField(default=False, null=False, blank=False)

    @staticmethod
    def search(pattern):
        return Client.objects.filter(Q(surnom=pattern) | Q(nom=pattern) | Q(prenom=pattern))

    def get_absolute_url(self):
        return reverse('client_edit', kwargs={'pk': self.pk})

    def __str__(self):
        identifier = self.nickname if self.nickname else (self.first_name + self.last_name)

        identifier = str(unicodedata.normalize('NFKD', identifier).encode('ascii', 'ignore'))
        identifier.replace(" ", "")
        identifier.replace("-", "")
        identifier.replace("_", "")
        identifier.replace("@", "a")
        identifier.replace(";", "")
        identifier = identifier.strip("b\'")

        return identifier

class Supplier(models.Model):
    ip = models.CharField(max_length=32, unique=True, blank=False)
    server_name = models.CharField(max_length=50, unique=True, blank=False)
    client = models.ForeignKey(Client, models.CASCADE, null=False)

    def getTotalActivations(self):
        return len(self.activation_set.all())

    def __str__(self):
        return self.server_name + " (" + str(self.client) + ")"

class Mac(models.Model):
    address = models.CharField(max_length=32, unique=True, blank=False)

    client = models.ForeignKey(Client, models.CASCADE, null=False, default=0);

    def __str__(self):
        return str(self.client) + " : " + self.address

    def save(self, *args, **kwargs):

        self.address = self.address.replace("-", ":")
        self.address = self.address[:17]

        super(Mac, self).save(*args, **kwargs)

class Activation(models.Model):

    subscription = models.IntegerField(default=25, null=False)
    active = models.BooleanField(default=True, null=False)

    client = models.ForeignKey(Client, models.CASCADE, null=False, unique=False)
    supplier = models.ForeignKey(Supplier, default=0, null=False)

    duration = models.IntegerField(default=5, null=False)

    creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return  str(self.supplier) + ": " + str(self.client)

class Forward(models.Model):
    port = models.ForeignKey(Port, null=False)
    supplier = models.ForeignKey(Supplier, null=False)

    def __str__(self):
        return (str(self.supplier) + ": " + str(self.port))

class Input(models.Model):
    port = models.ForeignKey(Port, null=False)
    supplier = models.ForeignKey(Supplier, null=False)

    def __str__(self):
        return (str(self.supplier) + ": " + str(self.port))

