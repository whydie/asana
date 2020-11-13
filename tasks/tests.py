from django.conf import settings
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Project


client = settings.ASANA


class ProjectTests(APITestCase):
    def setUp(self):
        self.project_name = "test"
        self.user_name = "name"

        self.user = self._create_user(name=self.user_name)
        self.project = self._create_project(self.project_name)

    def _create_user(self, **kwargs) -> dict:
        return self.client.post(reverse("users"), data={**kwargs}).json()

    def _get_project(self, project_gid: str):
        return client.projects.get_project(project_gid)

    def _delete_project(self, project_gid: str):
        self.client.delete(reverse("project", kwargs={"gid": project_gid}))

    def _create_project(self, name: str) -> dict:
        return self.client.post(reverse("projects"), data={"name": name}).json()

    def _patch_project(self, gid: str, **kwargs):
        self.client.patch(reverse("project", kwargs={"gid": gid}), data={**kwargs})

    def test_create(self):
        project = self._get_project(self.project["gid"])

        self.assertEqual(project["name"], self.project_name)

    def test_update(self):
        new_name = "test2"

        self._patch_project(self.project["gid"], name=new_name)

        project = self._get_project(self.project["gid"])

        self.assertEqual(project["name"], new_name)

    def test_delete(self):
        name = "test3"
        project = self._create_project(name)

        self._delete_project(project["gid"])

        asana_project = self._get_project(project["gid"])

        does_asana_project_exist = "gid" in asana_project
        self.assertTrue(does_asana_project_exist)

        does_db_project_exist = Project.objects.filter(gid=project["gid"]).exists()
        self.assertFalse(does_db_project_exist)


class TaskTests(APITestCase):
    def setUp(self):
        self.task_notes = "task notes"
        self.project_name = "test"
        self.user_name = "name"
        self.user_gid = "1198720398060592"

        self.user = self._create_user(name=self.user_name, gid=self.user_gid)
        self.project = self._create_project(self.project_name)
        self.task = self._create_task(self.task_notes, self.user["pk"], self.project["pk"])

    def _create_user(self, **kwargs) -> dict:
        return self.client.post(reverse("users"), data={**kwargs}).json()

    def _get_task(self, task_gid: str):
        return client.tasks.get_task(task_gid)

    def _destroy_task(self, task_gid: str):
        self.client.delete(reverse("task", kwargs={"gid": task_gid}))

    def _create_project(self, name: str) -> dict:
        return self.client.post(reverse("projects"), data={"name": name}).json()

    def _create_task(self, notes: str, assignee_pk: int, project_pk: int) -> dict:
        return self.client.post(reverse("tasks"), data={
            "notes": notes,
            "assignee": assignee_pk,
            "project": project_pk
        }).json()

    def _patch_task(self, gid: str, **kwargs):
        self.client.patch(reverse("task", kwargs={"gid": gid}), data={**kwargs})

    def test_create(self):
        task = self._get_task(self.task["gid"])

        self.assertEqual(task["gid"], self.task["gid"])

    def test_update(self):
        new_notes = "New notes"

        self._patch_task(self.task["gid"], notes=new_notes)

        project = self._get_task(self.task["gid"])

        self.assertEqual(new_notes, project["notes"])

    def test_destroy(self):
        notes = "Test notes 3"
        task = self._create_task(notes, self.user["pk"], self.project["pk"])

        self._destroy_task(task["gid"])

        asana_task = self._get_task(task["gid"])

        does_asana_task_exist = "gid" in asana_task
        self.assertTrue(does_asana_task_exist)

        does_db_task_exist = Project.objects.filter(gid=task["gid"]).exists()
        self.assertFalse(does_db_task_exist)
