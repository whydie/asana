from django.conf import settings

client = settings.ASANA


def create_project(project) -> str:
    """
    :param project: Project object.
    :return: Objects gid.
    """
    result = client.projects.create_project({"name": project.name, "workspace": settings.WORKSPACE_GID})

    return result["gid"]


def update_project(project):
    """
    :param project: Project object.
    """
    client.projects.update_project(project.gid, {"name": project.name})


def create_task(task) -> str:
    """
    :param task: Task object.
    :return: Task gid.
    """
    result = client.tasks.create_task({
        "notes": task.notes,
        "projects": [task.project.gid],
        "assignee": task.assignee.gid
    })

    return result["gid"]


def update_task(task):
    """
    :param task: Task object.
    """
    client.tasks.update_task(task.gid, {
        "notes": task.notes,
        "assignee": task.assignee.gid
    })
