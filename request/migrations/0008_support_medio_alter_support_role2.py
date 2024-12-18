# Generated by Django 5.1 on 2024-11-05 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0007_rename_role_support_role2'),
    ]

    operations = [
        migrations.AddField(
            model_name='support',
            name='medio',
            field=models.CharField(choices=[('CORREO', 'CORREO'), ('WHATSAPP', 'WHATSAPP'), ('TELEFONO', 'TELEFONO')], default='CORREO', max_length=30),
        ),
        migrations.AlterField(
            model_name='support',
            name='role2',
            field=models.CharField(choices=[('SECRETARIA_GENERAL', 'Secretaría General'), ('PLANIFICACION', 'Planificación'), ('CONTROL_INTERNO', 'Control Interno'), ('GESTION_SOCIAL', 'Gestión Social'), ('COMUNICACIONES', 'Comunicaciones'), ('RECURSOS_HUMANOS', 'Recursos Humanos'), ('FINANZAS', 'Finanzas'), ('SISTEMAS', 'Sistemas'), ('TRANSPORTE', 'Transporte'), ('LOGISTICA', 'Logística'), ('GERENCIA', 'GERENCIA')], default='GERENCIA', max_length=30),
        ),
    ]
