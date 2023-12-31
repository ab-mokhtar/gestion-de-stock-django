from django.contrib.auth.models import Group
from django.db import models
from datetime import datetime, date
from django.contrib.auth.models import User,AbstractUser



# Create your models here.
class Familles(models.Model):
    famille = models.CharField(max_length=50)
    
    def __str__(self):
        return self.famille


class Contact(models.Model):
    fournisseur = models.CharField(max_length=80)
    nom = models.CharField(max_length=80)
    adresse = models.CharField(max_length=250,blank=True, null=True)
    tel1 = models.CharField(max_length=50,blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    fax = models.CharField(max_length=50,blank=True, null=True)
    mail = models.CharField(max_length=80,blank=True, null=True)
    activite = models.CharField(max_length=80,blank=True, null=True)
    obs = models.CharField(max_length=250,blank=True, null=True)
    ville = models.CharField(max_length=20,blank=True, null=True)

    def __str__(self):
        return self.fournisseur
class SousFamille(models.Model):
    choix = (
        ('oui', 'oui'),
        ('non', 'non'),
    )
    choix_ville = (
        ('tunis', 'tunis'),
        ('sousse', 'sousse'),
        ('nice','nice'),
    ),
    id_famille = models.ForeignKey(Familles,verbose_name="Les Articles",on_delete=models.CASCADE)
    designation = models.CharField(max_length=20)
    marque = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    seuil = models.IntegerField()
    groupresp = models.ForeignKey(Group,verbose_name='groupe_resp',on_delete=models.CASCADE,default=1)
    pid1 = models.CharField(max_length=20,unique=True)
    active = models.CharField(max_length=3,verbose_name="consommable",choices=choix)
    ville = models.CharField(max_length=6,blank=True, null=True)
    icon = models.CharField(max_length=120,blank=True, null=True)
    def __str__(self):
        return self.designation + ': ' + self.model 
    @property
    def get_group_email(self):
        return self.groupresp.email

class Contrat(models.Model):
    choix_ville = (('tunis', 'tunis'),('sousse', 'sousse'),('nice','nice'),)
    article = models.ForeignKey(SousFamille,on_delete=models.CASCADE)
    designation = models.CharField(max_length=20)
    fournisseur = models.ForeignKey(Contact,on_delete=models.CASCADE)
    dateacquisition = models.DateField(db_column='dateAcquisition',blank=True, null=True)  # Field name made lowercase.
    echeance = models.DateField(blank=True, null=True)
    montant = models.CharField(max_length=20)   
    observation = models.CharField(max_length=20,blank=True, null=True)
    ville = models.CharField(max_length=6,choices=choix_ville)


class User(AbstractUser):
    USER_TYPE_CHOICES = (
      (1, 'admin'),
      (2, 'user'),
      (4, 'superadmin'),)

    role = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,default=4)
    
class Facture(models.Model):

    phone_number = models.ForeignKey(Contact,verbose_name="fournisseur",on_delete=models.CASCADE)
    ref = models.CharField(max_length=50,default='0',verbose_name='Réference facture', blank=True, null=True)
    Society = models.CharField(max_length=50,default='0', blank=True, null=True)
    facture_print = models.FileField(upload_to='media/facture',blank=True,null=True)
    bondlev = models.FileField(upload_to='media/bon_livraison',blank=True,null=True)
    dateen = models.DateField()
    
class distinations(models.Model):
   
    nom_dis = models.CharField(max_length=50)
    societe = models.CharField(max_length=50,default='0', blank=True, null=True)
    
    class Meta:
        unique_together = ['nom_dis','societe']
    def __str__(self):
        return self.nom_dis+'-'+self.societe
    
class Stock(models.Model):
    id_sous_famille = models.ForeignKey(SousFamille,verbose_name="Article",on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True)
    receive_quantity = models.IntegerField( blank=True, null=True)
    receive_by = models.ForeignKey(User,related_name="ReceiveUser",on_delete=models.CASCADE,default=1)
    issue_quantity = models.IntegerField(default=0,blank=True, null=True)
    issue_by = models.ForeignKey(User,related_name="IssueUser",on_delete=models.CASCADE,default=1)
    issue_to = models.ForeignKey(distinations,verbose_name="Emplacement",on_delete=models.CASCADE,default=1)
    fac =  models.ForeignKey(Facture,on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,related_name="CreatUser",on_delete=models.CASCADE,default=1)
    reorder_level = models.IntegerField(default='0',verbose_name="garantie", blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    ci=models.CharField(max_length=50, blank=True, null=True)
    prix = models.IntegerField(default=0,blank=True, null=True)
    def __str__(self):
        return self.id_sous_famille.designation
	

class Historique_Stock(models.Model):
	codeibar=models.CharField(max_length=50, blank=True, null=True)
	id_sous_famille = models.ForeignKey(SousFamille,on_delete=models.CASCADE,default=1)
	quantity = models.IntegerField(default='0', blank=True, null=True)
	receive_quantity = models.IntegerField(default='0', blank=True, null=True)
	receive_by = models.ForeignKey(User,related_name="hisReceiveUser",on_delete=models.CASCADE,default=1)
	issue_quantity = models.IntegerField(default='0', blank=True, null=True)
	issue_by = models.ForeignKey(User,related_name="hisIssueUser",on_delete=models.CASCADE,default=1)
	issue_to = models.ForeignKey(distinations,verbose_name="Emplacement",on_delete=models.CASCADE,default=1)
	ci=models.CharField(max_length=50, blank=True, null=True)
	created_by = models.ForeignKey(User,related_name="HisCreatUser",on_delete=models.CASCADE,default=1)
	reorder_level = models.IntegerField(default='0', blank=True, null=True)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
class Task(models.Model):
    title = models.TextField(verbose_name='Description de tache')
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    by = models.CharField(max_length=50, blank=True, null=True)
    follows= models.ManyToManyField(User,related_name='follows')
    
class demande(models.Model):
    choix_etat = (
        ('en-cours', 'en-cours'),
        ('rejeter', 'rejeter'),
        ('valider','valider'),)
    article = models.ForeignKey(Stock,on_delete=models.CASCADE)
    demander = models.ForeignKey(User,on_delete=models.CASCADE)
    quantite  = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    validation = models.CharField(max_length=50, blank=True, null=True,choices=choix_etat)
#add an attribute email to group model
Group.add_to_class('email',models.EmailField(max_length = 254,default=''))

class reparation_materiel(models.Model):
    choix_etat = (
        ('en-maintenance', 'en-maintenance'),
        ('resolu', 'resolu'),
        ('en-panne','en-panne'),)
    article = models.ForeignKey(Stock,on_delete=models.CASCADE)
    demander = models.ForeignKey(User,on_delete=models.CASCADE)
    etat=  models.CharField(max_length=50, blank=True, null=True,choices=choix_etat)
    observation = models.TextField( blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null=True)

class Demande_Devis(models.Model):
    article = models.ForeignKey(SousFamille,verbose_name="Article",on_delete=models.CASCADE)
    fournisseur = models.ManyToManyField(Contact,verbose_name="Fournisseur",blank=True)
    quantite= models.IntegerField()
    avg = models.IntegerField(blank=True, null=True)
