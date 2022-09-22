# Generated by Django 4.0.6 on 2022-09-22 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_rename_user_issues_contributor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issues',
            name='priority',
            field=models.CharField(choices=[(1, 'FAIBLE'), (2, 'MOYENNE'), (3, 'ÉLEVÉE')], default='FAIBLE', max_length=50, verbose_name='Priorité'),
        ),
        migrations.AlterField(
            model_name='issues',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.projects', verbose_name='Projet'),
        ),
        migrations.AlterField(
            model_name='issues',
            name='status',
            field=models.CharField(choices=[(1, 'À faire'), (2, 'En cours'), (3, 'Terminé')], default='À faire', max_length=50, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='issues',
            name='tag',
            field=models.CharField(choices=[(1, 'BUG'), (2, 'AMÉLIORATION'), (3, 'TÂCHE')], default='BUG', max_length=50, verbose_name='Tag'),
        ),
    ]