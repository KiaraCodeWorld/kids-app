from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0002_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedFlashcard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_type', models.CharField(choices=[('word', 'Word'), ('idiom', 'Idiom')], default='word', max_length=10)),
                ('front_text', models.CharField(max_length=200)),
                ('back_text', models.TextField()),
                ('example', models.TextField(blank=True, default='')),
                ('emoji', models.CharField(blank=True, default='', max_length=10)),
                ('extra_json', models.JSONField(blank=True, default=dict)),
                ('saved_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-saved_at'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='savedflashcard',
            unique_together={('card_type', 'front_text')},
        ),
    ]
