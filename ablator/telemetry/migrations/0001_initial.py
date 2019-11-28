# Generated by Django 2.1.7 on 2019-11-28 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_at', models.DateTimeField(auto_now_add=True)),
                ('parameters', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SignalType',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.App')),
            ],
        ),
        migrations.AddField(
            model_name='signal',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telemetry.SignalType'),
        ),
        migrations.AddField(
            model_name='signal',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ClientUser'),
        ),
    ]
