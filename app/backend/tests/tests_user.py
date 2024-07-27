from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from backend.models.user import AdminGroup, AdminGroupMember

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


        admin_group, created = AdminGroup.objects.get_or_create(name="Veranstaltungsorganisation")
        #admin_group.user_set.add(admin) #does not call save() of TeamMember
        #admin.groups.add(admin_group) #does not call save() on TeamMember
        #admin.save()
        # use this for assigning users to admin group via code for automatically setting user.is_staff = True
        membership, created = AdminGroupMember.objects.get_or_create(user=admin, admin_group=admin_group)
        print("1"+ str(list(AdminGroupMember.objects.filter(user=admin))))
        admin.refresh_from_db()
        try:
            self.assertTrue(admin.is_staff)
        except AssertionError:
            print(str(admin.is_staff) + " is not true")
            pass
        self.assertFalse(admin.is_superuser)

        # testing the bulk deletion method from the QuerySet
        admin.groups.remove(admin_group)
        #admin.save()
        print("post bulk delete " +str(admin.is_staff))
        # bulk deletion of admin group membership needs db refresh for the user object
        self.assertTrue(admin.is_staff)
        admin.refresh_from_db()
        self.assertFalse(admin.is_staff)
        print("post bulk delete refresh " +str(admin.is_staff))
        print("2"+ str(list(AdminGroupMember.objects.filter(user=admin))))

        membership, created = AdminGroupMember.objects.get_or_create(user=admin, admin_group=admin_group)
        print("3"+ str(list(AdminGroupMember.objects.filter(user=admin))))
        admin.refresh_from_db()
        try:
            self.assertTrue(admin.is_staff)
        except AssertionError:
            print(str(admin.is_staff) + " is not true")
            pass

        # testing the model instance delete() method
        # model instance deletion of teammembership does not need db refresh for the user object
        membership.delete()
        print("4"+ str(list(AdminGroupMember.objects.filter(user=admin))))
        print("post instance delete" +str(admin.is_staff))
        try:
            self.assertTrue(admin.is_staff)
        except AssertionError:
            print(str(admin.is_staff) + " is not true (expected)")
            pass
        admin.refresh_from_db()
        print("post instance delete refresh " +str(admin.is_staff))
        self.assertFalse(admin.is_staff)
