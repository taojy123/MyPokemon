# Generated by Django 2.1.4 on 2019-09-02 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20190902_1827'),
    ]

    operations = [
        migrations.CreateModel(
            name='Battle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('events', models.TextField()),
                ('winner', models.ImageField(default=0, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winner', models.ImageField(default=0, upload_to='')),
                ('battles', models.ManyToManyField(to='game.Battle')),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player1_match_set', to='game.Player')),
                ('player2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player2_match_set', to='game.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Wild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winner', models.ImageField(default=0, upload_to='')),
                ('battles', models.ManyToManyField(to='game.Battle')),
            ],
        ),
        migrations.AlterField(
            model_name='card',
            name='status',
            field=models.IntegerField(choices=[(-1, '弃牌'), (0, '牌堆'), (1, '手牌'), (2, '休息')], default=0),
        ),
        migrations.AddField(
            model_name='wild',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Card'),
        ),
        migrations.AddField(
            model_name='wild',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Player'),
        ),
        migrations.AddField(
            model_name='battle',
            name='card1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card1_battle_set', to='game.Card'),
        ),
        migrations.AddField(
            model_name='battle',
            name='card2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card2_battle_set', to='game.Card'),
        ),
    ]