# Generated by Django 4.0.6 on 2022-07-17 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Участник')),
            ],
            options={
                'verbose_name': 'Участник',
                'verbose_name_plural': 'Участники',
            },
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Описание тусовки')),
            ],
            options={
                'verbose_name': 'Мероприятие',
                'verbose_name_plural': 'Мероприятия',
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expenses', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Потратил')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Описание траты')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_exp', to='count.member')),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='date_exp', to='count.party')),
            ],
            options={
                'verbose_name': 'Расход',
                'verbose_name_plural': 'Расходы',
            },
        ),
        migrations.CreateModel(
            name='PurchaseExclude',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membering', to='count.member')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchasing', to='count.purchase')),
            ],
            options={
                'verbose_name': 'Исключение',
                'verbose_name_plural': 'Исключения',
            },
        ),
        migrations.AddField(
            model_name='member',
            name='party',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dateparty', to='count.party'),
        ),
    ]
