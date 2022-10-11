from dataclasses import dataclass, field
import re
from datetime import datetime

@dataclass
class PersonalInfo:
    """Collection of all personal data about employee"""
    # TODO: add default values
    # TODO: add class wide id counter
    id_counter = 0
    __name: str = "name surname"
    first_name: str = field(default="first_name", init=False)
    second_name: str = field(default="surname", init=False)
    _address: str = "address"
    _phone_number: str = "+1000000000"
    email: str = "email@com"
    _position: int = -1
    _rank: str = "rank"
    _salary: float = -1

    def __post_init__(self):
        self.id = PersonalInfo.id_counter
        PersonalInfo.id_counter += 1
        self.name = self.__name
        if re.match("^\\+?[1-9][0-9]{7,14}$", self._phone_number) is None:
            raise ValueError("Phone number is not valid!")

    @property
    def name(self) -> str:
        return str(self.first_name + self.second_name)

    @name.setter
    def name(self, value: str) -> (str, str):
        self.first_name, self.second_name = value.split(maxsplit=2)


class Employee:
    """Container for all employees"""
    def __init__(self, personal_info: PersonalInfo = None):
        self.personal_info = personal_info

    def calculate_salary(self):
        return self.personal_info._salary

    #Todo: fix

    # def ask_sick_leave(self, pm: ProjectManager):
    #     return True


class Developer(Employee):
    """Basis developer, that inherits from Employee"""
    def __init__(self, personal_info: PersonalInfo = None, projects=[]):
        try:
            Employee.__init__(personal_info)
            self.projects: [Project] = projects
        except Exception as e:
            raise ValueError("Developer instantiation error! " + str(e))

    def assigned_projects(self):
        """ Get all assigned project to developer."""
        return self.projects


class QAEngineer(Employee):
    """Developer with access to testing"""
    def __init__(self, personal_info: PersonalInfo = None):
        Employee.__init__(self, personal_info)

    def test_feature(self, *feature):
        return str(*feature)


class Project:
    """General Project with task list"""
    #Todo: finish
    def __init__(self, title="Title", start_date=None, task_list=[], developers=[], limit=-1):
        try:
            self.title: str = title
            self.start_date: datetime = start_date
            self.task_list: [str] = task_list
            self.developers: [Developer] = developers
            self.limit: int = limit
        except Exception as e:
            raise ValueError("Project instantiation error! " + str(e))


class ProjectManager(Employee):
    """Developer with access to testing"""
    def __init__(self, personal_info: PersonalInfo = None, project: Project = None):
        Employee.__init__(self, personal_info)
        self.project = project

    def discuss_progress(self, dev: Developer):
        try:
            if dev not in self.project.developers:
                raise ValueError("Project manager has no access to developer!")
            print(f"Discussion with {dev.personal_info.name} happened")
        except ValueError as e:
            raise ValueError(f"Discussion with {dev.name} failed! " + str(e))


class Task:
    """Sub-tasks with due date"""
    id_counter = 0

    def __init__(self, title: str = "task", items: [str] = None, is_done: bool = False, deadline: datetime = None):
        self.id = Task.id_counter
        Task.id_counter += 1
        self.title = title
        self.items = items
        self.deadline = deadline
        self.is_done = is_done
        self.comments = "None"
        self.__finished_items = self.items if is_done else []

    def implement_item(self, item: str):
        try:
            if item not in self.items:
                raise ValueError("Item was not found in item list!")
            if item in self.__finished_items:
                raise ValueError("Item was already implemented!")
            self.__finished_items.append(item)

            #status_update
            if len(self.__finished_items) >= len(self.items):
                self.is_done = True
        except ValueError as e:
            raise ValueError("Item implementation error! " + str(e))

    def add_comment(self, text: str):
        self.comments += "\n" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + text

    def __str__(self):
        return f"{self.title} — {self.deadline}: {str(list([item for item in self.items]))}"


class Assignment:
    """Tasks with due date"""
    def __init__(self, project, dev, description: str = "Description"):
        self.parent_project: Project = project
        self.received_tasks = []
        self.is_done = False
        self.description = description
        self.status = "0%"
        self.developer: Developer = dev

    def __str__(self):
        return f"Assignment from project '{self.parent_project.title}' is {'' if self.is_done else 'not'} done." \
               f"\nTask list:{str(list([str(task) for task in self.received_tasks]))} "

    def __update_status(self):
        """Updates assignment status according to percent of completed tasks"""
        if len(self.received_tasks) > 0:
            percentage = len(list(filter(lambda x: x.is_done, self.received_tasks))) / len(self.received_tasks)
            self.status = str(percentage)+"%"

    def add_task(self, task: Task):
        """Adds task to assignment"""
        try:
            if len(self.parent_project.task_list) <= len(self.received_tasks):
                raise ValueError("Assignment task list cannot be longer than project task list!")
            self.received_tasks.append(task)
            self.__update_status()
        except Exception as e:
            raise ValueError("Task creation error! " + str(e))

    def get_tasks_to_datetime(self, date: datetime):
        """Get list of all tasks before the specified date"""
        return list([(task.deadline, task) for task in self.received_tasks if date > task.deadline])


class AssignManager:
    """Handles all assignments"""

    def assign(self, project: Project, dev: Developer):
        """Adds developer to specified project"""
        try:
            if project.limit <= len(project.developers):
                raise ValueError("Project developer limit is exceeded!")
            if dev in project.developers:
                raise ValueError("Developer is already in the list!")
            project.developers.append(dev)
            dev.projects.append(project)
        except ValueError as e:
            raise ValueError("Failed to add developer! " + str(e))

    def unassign(self, project: Project, dev: Developer):
        """Removes developer from project"""
        try:
            project.developers.remove(dev)
            dev.projects.remove(project)
        except ValueError:
            raise ValueError("Developer was not found in the project!")

    def assign_possibility(self, project: Project, dev: Developer):
        """Checks if developer can be added to the project"""
        return not project.limit <= len(project.developers)

#TODO: task7