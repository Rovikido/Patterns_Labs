import unittest
from lab_3 import *


class ProjectTest(unittest.TestCase):

    def test_web_creation(self):
        pr = Web()
        assert pr.team is not None

    def test_mobile_creation(self):
        pr = Mobile()
        assert pr.team is not None

    def test_embedded_creation(self):
        pr = Embedded()
        assert pr.team is not None


class AssignmentTest(unittest.TestCase):
    def test_assignment(self):
        pr = Web(limit=3)
        joe = Employee(PersonalInfo("Joe Mark"))
        pr.add_employee(joe)
        assert joe in pr.team.member_list
        assert pr in joe.projects

    def test_unassignment(self):
        pr = Web(limit=3)
        joe = Employee(PersonalInfo("Joe Mark"))
        pr.add_employee(joe)
        pr.remove_employee(joe)
        assert joe not in pr.team.member_list
        assert pr not in joe.projects


class SoftwareArchitectTest(unittest.TestCase):
    def test_fill_project(self):
        pr = Web(limit=5)
        sa = WebArchitect(PersonalInfo("Joe Mark"), [pr])
        joe = Employee(PersonalInfo("Joe Mark"))
        team = Team(pr.id, [joe])
        sa.fill_project(team, pr)
        assert pr.team == team

    def test_create_project(self):
        sa = WebArchitect(PersonalInfo("Joe Mark"), [])
        pr = sa.create_project(title="title1", domain="google.com")
        assert pr.domain == "google.com"


if __name__ == '__main__':
    unittest.main()