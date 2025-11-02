from faker import Faker
from django.core.management.base import BaseCommand
from apps.accounts.models import CustomUser, Profile
from apps.blog.models import Article, Category
import random

# _______________________________________________________

category_list = ["علمی", "پزشکی", "تکنولوژی", "پژوهشی"]


class Command(BaseCommand):
    help = "Insert Dummy Data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = CustomUser.objects.create(email=self.fake.email(), password="Aa123456@")
        profile = Profile.objects.get(user=user)
        profile.name = self.fake.first_name()
        profile.family = self.fake.last_name()
        profile.save()

        for name in category_list:
            Category.objects.get_or_create(category_title=name)

        for _ in range(3):
            Article.objects.create(
                article_title=self.fake.text(max_nb_chars=20),
                article_text=self.fake.text(max_nb_chars=100),
                slug=self.fake.slug(),
                is_active=False,
                author=profile,
                # image_name = self.fake.image(),
                category=Category.objects.get(
                    category_title=random.choice(category_list)
                ),
            )


# _______________________________________________________
