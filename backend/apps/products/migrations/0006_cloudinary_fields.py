# Generated manually for CloudinaryField migration

from django.db import migrations, models
import cloudinary.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_featured_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, folder='categories/', help_text='Category cover image', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='brand',
            name='logo',
            field=cloudinary.models.CloudinaryField(blank=True, folder='brands/', help_text='Brand logo', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='featured_image',
            field=cloudinary.models.CloudinaryField(blank=True, folder='products/featured/', help_text='Main product image', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=cloudinary.models.CloudinaryField(folder='products/gallery/', help_text='Product gallery image', max_length=255),
        ),
    ]