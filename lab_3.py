from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
import re
from datetime import datetime


@dataclass
class PersonalInfo:
    """Collection of all personal data about employee"""
    __name: str = "name surname"
    first_name: str = field(default="first_name", init=False)
    second_name: str = field(default="surname", init=False)
    _address: str = "address"
    _phone_number: str = "+1000000000"
    email: str = "email@com"
    _position: int = -1
    _rank: str = "rank"
    _salary: float = -1
    id_counter = 0

    def __post_init__(self):
        self.id = PersonalInfo.id_counter
        PersonalInfo.id_counter += 1
        self.name = self.__name
        if re.match("^\\+?[1-9][0-9]{7,14}$", self._phone_number) is None:
            raise ValueError("Phone number is not valid!")


class Employee:
    """Container for all employees"""
    def __init__(self, personal_info: PersonalInfo = None, projects=None):
        self.personal_info = personal_info
        if projects is None:
            projects = []
        self.projects: [Project] = projects

    def calculate_salary(self):
        return self.personal_info._salary


@dataclass
class Team:
    """"Collection of info about members, connected to certain project"""
    project_id: int
    member_list: list = field(default_factory=lambda: [])
    title: str = "Default title"
    id_counter = 0

    def __post_init__(self):
        self.id = PersonalInfo.id_counter
        PersonalInfo.id_counter += 1


class Developer(Employee):
    """Basis developer, that inherits from Employee"""
    def __init__(self, personal_info: PersonalInfo = None, projects=[]):
        try:
            Employee.__init__(personal_info, projects)
        except Exception as e:
            raise ValueError("Developer instantiation error! " + str(e))

    def assigned_projects(self):
        """ Get all assigned project to developer."""
        return self.projects


class AssignManagement:
    """Handles all assignments"""
    def __init__(self, project, emp):
        try:
            self.project: Project = project
            self.emp: Employee = emp
        except Exception as e:
            raise ValueError("Assignment error! " + str(e))

    def assign(self):
        """Adds developer to specified project"""
        try:
            if self.project.limit <= len(self.project.team.member_list):
                raise ValueError("Project developer limit is exceeded!")
            if self.emp in self.project.team.member_list:
                raise ValueError("Developer is already in the list!")
            self.project.team.member_list.append(self.emp)
            self.emp.projects.append(self.project)
        except ValueError as e:
            raise ValueError("Failed to add developer! " + str(e))

    def unassign(self):
        """Removes developer from project"""
        try:
            self.project.team.member_list.remove(self.emp)
            self.emp.projects.remove(self.project)
        except ValueError:
            raise ValueError("Developer was not found in the project!")

    def assign_possibility(self):
        """Checks if developer can be added to the project"""
        return not self.project.limit <= len(self.project.team.member_list)


class Project(metaclass=ABCMeta):
    """General Project factory"""
    id_counter = 0

    @abstractmethod
    def __init__(self, title, start_date, task_list, team, limit):
        try:
            self.id: int = self.id_counter
            Project.id_counter += 1
            if team is None:
                team = Team(self.id, [], str(title + "'s team"))
            if task_list is None:
                task_list = []
            self.task_list: [int] = []
            self.title: str = title
            self.start_date: datetime = start_date
            self.task_list: [str] = task_list
            self.team: Team = team
            self.limit: int = limit
        except Exception as e:
            raise ValueError("Project instantiation error! " + str(e))

    @abstractmethod
    def add_employee(self, emp: Employee):
        """Adds employee to project"""
        pass
        # mgn = AssignManagement(self, dev)
        # mgn.assign()

    @abstractmethod
    def remove_employee(self, emp: Employee):
        """Removes employee to project"""
        pass
        # mgn = AssignManagement(self, dev)
        # mgn.unassign()


class Web(Project):
    def __init__(self, title="Title", start_date=None, task_list=None, team=None, limit=-1, domain="/", host_provider="host name"):
        super().__init__(title, start_date, task_list, team, limit)
        self.domain = domain
        self.host_provider = host_provider

    def add_employee(self, emp: Employee):
        mgn = AssignManagement(self, emp)
        mgn.assign()

    def remove_employee(self, emp: Employee):
        mgn = AssignManagement(self, emp)
        mgn.unassign()


class Mobile(Project):
    def __init__(self, title="Title", start_date=None, task_list=None, team=None, limit=-1, is_crossplatform: bool = True):
        super().__init__(title, start_date, task_list, team, limit)
        self.is_crossplatform = is_crossplatform

    def add_employee(self, emp: Employee):
        mgn = AssignManagement(self, emp)
        mgn.assign()

    def remove_employee(self, emp: Employee):
        mgn = AssignManagement(self, emp)
        mgn.unassign()


class Embedded(Project):
    def __init__(self, title="Title", start_date=None, task_list=None, team=None, limit=-1, open_source: bool = True):
        super().__init__(title, start_date, task_list, team, limit)
        self.open_source = open_source

    def add_employee(self, emp: Employee):
        mgn = AssignManagement(self, emp)
        mgn.assign()

    def remove_employee(self, emp: Employee):
        mgn = AssignManagement(self, emp)
        mgn.unassign()


class SoftwareArchitect(Employee, metaclass=ABCMeta):

    def fill_project(self, team: Team, project: Project):
        try:
            if project not in self.projects:
                raise ValueError(f"Architect has no access to '{project.title}'!")
            map(lambda emp: emp.projects.append(project), project.team.member_list)
            project.team = team
        except ValueError as e:
            raise ValueError(f"Filling project failed! {e}")

    @abstractmethod
    def create_project(self):
        pass


class WebArchitect(SoftwareArchitect):
    def create_project(self, *args, **kwargs):
        project = Web(*args, **kwargs)
        self.projects.append(project)
        return project


class MobileArchitect(SoftwareArchitect):
    def create_project(self, *args, **kwargs):
        project = Mobile(*args, **kwargs)
        self.projects.append(project)
        return project


class EmbeddedArchitect(SoftwareArchitect):
    def create_project(self, *args, **kwargs):
        project = Embedded(*args, **kwargs)
        self.projects.append(project)
        return project



