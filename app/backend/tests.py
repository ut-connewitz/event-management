from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from backend.models.user import Team, TeamMember

class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username="normal", email="normal@user.test", password="test")
        self.assertEqual(user.username, "normal")
        self.assertEqual(user.email, "normal@user.test")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsInstance(user, AbstractUser)

        try:
            self.assertIsNotNone(user.groups)
        except AttributeError:
            pass

        try:
            self.assertIsNotNone(user.objects)
        except AttributeError:
            pass

        try:
            self.assertIsNone(user.team)
        except AttributeError:
            pass

        try:
            self.assertIsNone(user.nothing)
        except AttributeError:
            pass

        try:
            self.assertIsInstance(user, NoClass)
        except NameError:
            pass


        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(username="")
        with self.assertRaises(ValueError):
            User.objects.create_user(username="", password="test")


    def test_create_superuser(self):
        User = get_user_model()
        superuser = User.objects.create_superuser(username="super", email="super@user.test", password="super")
        self.assertEqual(superuser.username, "super")
        self.assertEqual(superuser.email, "super@user.test")
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertIsInstance(superuser, AbstractUser)

        try:
            self.assertIsNotNone(superuser.groups)
        except AttributeError:
            pass

        try:
            self.assertIsNotNone(superuser.objects)
        except AttributeError:
            pass

        try:
            self.assertIsNone(superuser.team)
        except AttributeError:
            pass

        try:
            self.assertIsNone(superuser.nothing)
        except AttributeError:
            pass

        try:
            self.assertIsInstance(superuser, NoClass)
        except NameError:
            pass


        with self.assertRaises(TypeError):
            User.objects.create_superuser()
        with self.assertRaises(ValueError):
            User.objects.create_superuser(username="")
        with self.assertRaises(ValueError):
            User.objects.create_superuser(username="", password="test")
        with self.assertRaises(ValueError):
            User.objects.create_superuser(username="super2", password="test", is_superuser=False)


    def test_create_admin(self):
        User = get_user_model()
        admin = User.objects.create_user(username="admin", email="admin@user.test", password="admin")
        self.assertEqual(admin.username, "admin")
        self.assertEqual(admin.email, "admin@user.test")
        self.assertTrue(admin.is_active)
        self.assertFalse(admin.is_staff)
        self.assertFalse(admin.is_superuser)
        self.assertIsInstance(admin, AbstractUser)

        try:
            self.assertIsNotNone(admin.groups)
        except AttributeError:
            pass

        try:
            self.assertIsNotNone(admin.objects)
        except AttributeError:
            pass

        try:
            self.assertIsNone(admin.team)
        except AttributeError:
            pass

        try:
            self.assertIsNone(admin.nothing)
        except AttributeError:
            pass

        try:
            self.assertIsInstance(admin, NoClass)
        except NameError:
            pass


        admin_group, created = Team.objects.get_or_create(name="UT-Admin")
        #admin_group.user_set.add(admin)
        admin.groups.add(admin_group)
        admin.save()
        print(str(list(TeamMember.objects.filter(user=admin))))
        admin = User.objects.get(username="admin")
        self.assertTrue(admin.is_staff)
        self.assertFalse(admin.is_superuser)
