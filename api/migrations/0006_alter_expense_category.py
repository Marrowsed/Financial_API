# Generated by Django 4.0.6 on 2022-08-12 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_expense_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(choices=[('Alimentação', 'Alimentação'), ('Saúde', 'Saúde'), ('Moradia', 'Moradia'), ('Transporte', 'Transporte'), ('Educação', 'Educação'), ('Lazer', 'Lazer'), ('Imprevistos', 'Imprevistos'), ('Outras', 'Outras')], default='Outras', max_length=200),
        ),
    ]
