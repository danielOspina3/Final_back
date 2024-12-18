from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import AbstractUser, Group, Permission, AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, last_name,document_type,role,num_document,is_active=True,is_admin=False, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            last_name=last_name,
            document_type=document_type,
            role = role,
            num_document=num_document,
            is_active=is_active,
            is_admin=is_admin
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    

class TypeDocument(models.TextChoices):
    AS = 'AS', 'AS'
    CC = 'CC', 'CC'
    CE = 'CE', 'CE'
    MS = 'MS', 'MS'
    NU = 'NU', 'NU'
    PA = 'PA', 'PA'
    PE = 'PE', 'PE'
    PT = 'PT', 'PT'
    RC = 'RC', 'RC'
    TI = 'TI', 'TI'

# class TypeRequest(models.TextChoices):
#     ACTUALIZACION = 'ACTUALIZACION', 'ACTUALIZACION'
#     CAPACITACION = 'CAPACITACION', 'CAPACITACION'
#     CREACION_DE_US_PRO_MED_CON_SUM = 'CREACION_DE_US_PRO_MED_CON_SUM', 'CREACION_DE_US_PRO_MED_CON_SUM'
#     ERROR_DE_SISTEMA = 'ERROR_DE_SISTEMA', 'ERROR_DE_SISTEMA'
#     ERROR_EN_SISTEMA = 'ERROR_EN_SISTEMA', 'ERROR_EN_SISTEMA'
#     ESTADISTICAS = 'ESTADISTICAS', 'ESTADISTICAS'
#     INQUIERTUD = 'INQUIERTUD', 'INQUIERTUD'
#     INSTALACION = 'INSTALACION', 'INSTALACION'
#     INVENTARIOS = 'INVENTARIOS', 'INVENTARIOS'
#     SOLICITUD = 'SOLICITUD', 'SOLICITUD'

class role(models.TextChoices):
    ADMINISTRADOR = 'ADMINISTRADOR', 'ADMINISTRADOR'
    CAPACITACION = 'CAPACITACION', 'CAPACITACION'
    INFORMES = 'INFORMES', 'INFORMES'
    AUDITORIA = 'AUDITORIA', 'AUDITORIA'
    CONTRATACION = 'CONTRATACION', 'CONTRATACION'
    TESORERIA = 'TESORERIA', 'TESORERIA'
    GERENCIA = 'GERENCIA', 'GERENCIA'
    TI = 'TI', 'TI'
    

from django.db import models

class role2(models.TextChoices):
    SECRETARIA_GENERAL = 'SECRETARIA_GENERAL', 'Secretaría General'
    PLANIFICACION = 'PLANIFICACION', 'Planificación'
    CONTROL_INTERNO = 'CONTROL_INTERNO', 'Control Interno'
    GESTION_SOCIAL = 'GESTION_SOCIAL', 'Gestión Social'
    COMUNICACIONES = 'COMUNICACIONES', 'Comunicaciones'
    RECURSOS_HUMANOS = 'RECURSOS_HUMANOS', 'Recursos Humanos'
    FINANZAS = 'FINANZAS', 'Finanzas'
    SISTEMAS = 'SISTEMAS', 'Sistemas'
    TRANSPORTE = 'TRANSPORTE', 'Transporte'
    LOGISTICA = 'LOGISTICA', 'Logística'
    GERENCIA = 'GERENCIA', 'GERENCIA'



class How_is_conclude(models.TextChoices):
    EXISTOSO = 'EXISTOSO', 'EXISTOSO'
    EN_PROGRESO = 'EN_PROGRESO', 'EN_PROGRESO'
    
    
class medio(models.TextChoices):
    CORREO = 'CORREO', 'CORREO'
    WHATSAPP = 'WHATSAPP', 'WHATSAPP'
    TELEFONO = 'TELEFONO', 'TELEFONO'



class CustomerUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255,blank=True,default='',unique=True,null=True)
    num_document = models.CharField(max_length=20,unique=True,db_index=True)
    name = models.CharField(max_length=255, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=True, default='')
    document_type = models.CharField(max_length=2, choices=TypeDocument.choices, default=TypeDocument.CC)
    role = models.CharField(max_length=15, choices=role.choices, default=role.ADMINISTRADOR)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name']

    def _str_(self):
        return self.email


class Municipio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_municipio = models.CharField(max_length=255, blank=True, default='', null=True)
    codigo_municipio = models.CharField(max_length=255, unique=True, blank=True, default='', null=True)

    def _str_(self):
        return self.nombre_municipio

class Ips(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    nombre_ips = models.CharField(max_length=255, blank=True, default='', null=True)
    cod_ips = models.CharField(max_length=255, unique=True, blank=True, default='', null=True)
    municipio_id = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    def _str_(self):
        return self.nombre_ips
    
class typeRequest(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    typerequest = models.CharField(max_length=255,blank=True,default='',null=True)
    
    def _str_(self):
        return self.typerequest



class SubtypeRequest(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    type_request_id = models.ForeignKey(typeRequest, on_delete=models.CASCADE)
    subtype_request = models.CharField(max_length=255,blank=True,default='',null=True)
    
    def _str_(self):
        return self.subtype_request
    

class Support(models.Model):
    id = models.AutoField(primary_key=True)
    id_ips = models.ForeignKey(Ips, on_delete=models.CASCADE)
    id_CustomerUser = models.ForeignKey(CustomerUser, on_delete=models.CASCADE,related_name='id_CustomerUser')
    name_solicited = models.CharField(max_length=255,blank=True,default='',null=True)
    role2 = models.CharField(max_length=30, choices=role2.choices, default=role2.GERENCIA)
    medio = models.CharField(max_length=30, choices=medio.choices, default=medio.CORREO)
    number = models.CharField(max_length=255,blank=True,default='',null=True)
    email = models.CharField(max_length=255,blank=True,default='',null=True)
    requirement = models.TextField(blank=True,default='',null=True)
    answer = models.TextField(blank=True,default='',null=True)
    is_active = models.BooleanField(default=True)
    is_close = models.BooleanField(default=True)
    id_CustomerUser2 = models.ForeignKey(CustomerUser, on_delete=models.CASCADE,related_name='id_CustomerUser2')
    how_it_conclude = models.CharField(
    max_length=30,
    choices=How_is_conclude.choices,
    blank=True,
    null=True,
    default=None)
    typerequest_id = models.ForeignKey(typeRequest, on_delete=models.CASCADE)##vamos aca
    subtype_request = models.ForeignKey(SubtypeRequest, on_delete=models.CASCADE)##vamos aca
    support_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    update_date = models.DateTimeField(null=True, blank=True)
    
    def _str_(self):
        
        return self.id_ips

class Comments(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    id_support = models.ForeignKey(Support, on_delete=models.CASCADE)
    text = models.TextField(blank=True,default='',unique=True,null=True)
    image = models.TextField(blank=True,default='',null=True)
    
    def _str_(self):
        return self.id_support