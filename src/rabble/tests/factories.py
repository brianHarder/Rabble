from factory import Sequence, Faker, SubFactory, PostGenerationMethodCall, post_generation
from factory.django import DjangoModelFactory
from rabble.models import User, Rabble, SubRabble, Post, Comment

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Sequence(lambda n: f"user{n}")
    email = Sequence(lambda n: f"user{n}@example.com")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    bio = Faker("sentence")
    profile_picture = ""
    date_joined = Faker("date_time_this_year", before_now=True, after_now=True)
    password = PostGenerationMethodCall("set_password", "password")

class CommunityFactory(DjangoModelFactory):
    class Meta:
        model = Rabble

    community_id = Sequence(lambda n: f"community-{n}")
    owner = SubFactory(UserFactory)

class SubRabbleFactory(DjangoModelFactory):
    class Meta:
        model = SubRabble

    subrabble_community_id = Sequence(lambda n: f"subrabble-{n}")
    subrabble_name = Faker("sentence", nb_words=3)
    description = Faker("paragraph")
    allow_anonymous = True
    private = False
    rabble_id = SubFactory(CommunityFactory)
    user_id = SubFactory(UserFactory)

    @post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for user in extracted:
                self.members.add(user)

class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = Faker("sentence", nb_words=5)
    body = Faker("paragraph")
    user_id = SubFactory(UserFactory)
    subrabble_id = SubFactory(SubRabbleFactory)
    anonymous = False

class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    parent_id = None
    user_id = SubFactory(UserFactory)
    post_id = SubFactory(PostFactory)
    text = Faker("sentence")
    anonymous = False
