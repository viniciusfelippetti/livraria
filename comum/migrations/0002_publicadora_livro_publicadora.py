# Generated by Django 4.1 on 2024-09-25 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publicadora',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='livro',
            name='publicadora',
            field=models.ManyToManyField(to='comum.publicadora', verbose_name='Publicadoras'),
        ),
    ]
