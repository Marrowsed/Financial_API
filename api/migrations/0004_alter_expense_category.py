# Generated by Django 4.0.6 on 2022-08-08 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_expense_category_alter_expense_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(choices=[('Alimentação', 'Alimentação'), ('Saúde', 'Saúde'), ('Moradia', 'Moradia'), ('Transporte', 'Transporte'), ('Educação', 'Educação'), ('Lazer', 'Lazer'), ('Imprevistos', 'Imprevistos'), ('Outras', 'Outras')], default='Outras', max_length=200),
        ),
    ]
