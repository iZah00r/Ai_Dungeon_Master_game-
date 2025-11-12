import random
import json
import os
import logging
from datetime import datetime, time
from enum import Enum
import yaml
from typing import List, Dict, Set, Optional

# Enums
class Weather(Enum):
    SUNNY = "sunny"
    RAINY = "rainy"
    SNOWY = "snowy"
    CLOUDY = "cloudy"

class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class MentalState(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    OKAY = "okay"
    STRESSED = "stressed"
    BURNOUT = "burnout"

class MajorPlot(Enum):
    ACADEMIC_EXCELLENCE = "Academic Excellence"
    SOCIAL_BUTTERFLY = "Social Butterfly"
    ENTREPRENEURIAL_SPIRIT = "Entrepreneurial Spirit"
    RESEARCH_PIONEER = "Research Pioneer"

class Item:
    def __init__(self, name: str, item_type: str, value: int):
        self.name = name
        self.type = item_type
        self.value = value

class ResearchProject:
    def __init__(self, name: str, difficulty: int, duration: int):
        self.name = name
        self.difficulty = difficulty
        self.duration = duration
        self.progress = 0
        self.completed = False

    def work_on_project(self, hours: int, skill_level: int):
        progress_made = hours * (skill_level + random.randint(1, 5))
        self.progress += progress_made
        if self.progress >= 100:
            self.completed = True
        return progress_made

class Course:
    def __init__(self, name: str, credits: int, difficulty: int):
        self.name = name
        self.credits = credits
        self.difficulty = difficulty
        self.assignments = []
        self.midterm_grade = 0.0
        self.final_grade = 0.0
        self.attendance = 0
        self.participation = 0.0

    def add_assignment(self, name: str, weight: float):
        self.assignments.append({"name": name, "weight": weight, "grade": 0.0})

    def grade_assignment(self, assignment_index: int, grade: float):
        self.assignments[assignment_index]["grade"] = grade

    def calculate_final_grade(self):
        assignment_total = sum(a["grade"] * a["weight"] for a in self.assignments)
        self.final_grade = (assignment_total * 0.4) + (self.midterm_grade * 0.3) + (self.final_grade * 0.3)
        return self.final_grade

class StoryArc:
    def __init__(self, name: str, milestones: List[str]):
        self.name = name
        self.milestones = milestones
        self.current_milestone = 0

    def advance(self):
        if self.current_milestone < len(self.milestones) - 1:
            self.current_milestone += 1
            return True
        return False

    def get_current_milestone(self) -> str:
        return self.milestones[self.current_milestone]

class StoryProgress:
    def __init__(self):
        self.semester = 1
        self.major_plot: Optional[MajorPlot] = None
        self.story_arcs: Dict[str, StoryArc] = {
            "personal_growth": StoryArc("Personal Growth", [
                "Freshman Orientation",
                "Identity Crisis",
                "Finding Your Passion",
                "Leadership Opportunity",
                "Personal Transformation",
                "Legacy Planning"
            ]),
            "academic_journey": StoryArc("Academic Journey", [
                "First Major Assignment",
                "Choosing Specialization",
                "Internship Application",
                "Research Project",
                "Thesis Proposal",
                "Final Presentation"
            ]),
            "social_life": StoryArc("Social Life", [
                "Roommate Introduction",
                "Club Fair",
                "Campus Event Organization",
                "Relationship Dilemma",
                "Spring Break Adventure",
                "Graduation Party Planning"
            ]),
            "career_development": StoryArc("Career Development", [
                "Career Center Visit",
                "First Job Fair",
                "Summer Internship",
                "Networking Event",
                "Job Interview Preparation",
                "Job Offer Negotiation"
            ])
        }
        self.relationships: Dict[str, int] = {}
        self.key_decisions: Dict[str, str] = {}
        self.global_awareness = 0
        self.achievements: Set[str] = set()

    def advance_semester(self):
        self.semester += 1
        for arc in self.story_arcs.values():
            arc.advance()

    def set_major_plot(self, plot: MajorPlot):
        self.major_plot = plot

    def update_relationship(self, character: str, value: int):
        self.relationships[character] = self.relationships.get(character, 0) + value

    def make_key_decision(self, decision: str, choice: str):
        self.key_decisions[decision] = choice

    def increase_global_awareness(self, value: int):
        self.global_awareness += value

    def add_achievement(self, achievement: str):
        self.achievements.add(achievement)

    def get_story_summary(self) -> str:
        summary = f"Semester: {self.semester}\n"
        summary += f"Major Plot: {self.major_plot.value if self.major_plot else 'Not chosen yet'}\n\n"
        
        for arc_name, arc in self.story_arcs.items():
            summary += f"{arc.name}: {arc.get_current_milestone()}\n"
        
        summary += f"\nRelationships: {self.relationships}\n"
        summary += f"Key Decisions: {self.key_decisions}\n"
        summary += f"Global Awareness: {self.global_awareness}\n"
        summary += f"Achievements: {', '.join(self.achievements)}\n"
        
        return summary

class Student:
    def __init__(self, name: str, major: str, difficulty: Difficulty = Difficulty.MEDIUM):
        self.name = name
        self.major = major
        self.semester = 1
        self.energy = 100
        self.max_energy = 100
        self.gpa = 0.0
        self.credits = 0
        self.inventory: List[Item] = []
        self.skills: List[str] = []
        self.money = 1000 if difficulty == Difficulty.EASY else 500
        self.mental_state = MentalState.GOOD
        self.stress_level = 0
        self.relationships = {}  # name: friendship_level
        self.courses: List[Course] = []
        self.job = None
        self.extracurriculars = []
        self.stats = {
            "classes_attended": 0,
            "assignments_completed": 0,
            "social_events": 0,
            "money_earned": 0
        }
        self.research_projects: List[ResearchProject] = []
        self.skill_levels: Dict[str, int] = {
            "Research": 1,
            "Writing": 1,
            "Programming": 1,
            "Presentation": 1,
            "Teamwork": 1
        }

    def add_item(self, item: Item):
        self.inventory.append(item)

    def remove_item(self, item: Item):
        if item in self.inventory:
            self.inventory.remove(item)

    def semester_up(self):
        self.semester += 1
        self.max_energy += 10
        self.energy = self.max_energy
        if self.semester % 2 == 0:
            new_skill = f"{self.major} Expertise Level {self.semester // 2}"
            self.skills.append(new_skill)
            print(f"You learned a new skill: {new_skill}!")

    def update_mental_state(self):
        if self.stress_level < 20:
            self.mental_state = MentalState.EXCELLENT
        elif self.stress_level < 40:
            self.mental_state = MentalState.GOOD
        elif self.stress_level < 60:
            self.mental_state = MentalState.OKAY
        elif self.stress_level < 80:
            self.mental_state = MentalState.STRESSED
        else:
            self.mental_state = MentalState.BURNOUT

    def work_part_time(self, hours: int):
        if self.job:
            earned = hours * self.job["hourly_rate"]
            self.money += earned
            self.energy -= hours * 5
            self.stress_level += hours * 2
            self.stats["money_earned"] += earned
            return earned
        return 0

    def start_research_project(self, project: ResearchProject):
        self.research_projects.append(project)

    def work_on_research(self, project_index: int, hours: int):
        if project_index < len(self.research_projects):
            project = self.research_projects[project_index]
            progress = project.work_on_project(hours, self.skill_levels["Research"])
            self.energy -= hours * 5
            self.stress_level += hours * 2
            if project.completed:
                self.skill_levels["Research"] += 1
                print(f"Congratulations! You completed the research project: {project.name}")
            return progress
        return 0

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "major": self.major,
            "semester": self.semester,
            "energy": self.energy,
            "max_energy": self.max_energy,
            "gpa": self.gpa,
            "credits": self.credits,
            "inventory": [{"name": item.name, "type": item.type, "value": item.value} 
                         for item in self.inventory],
            "skills": self.skills,
            "money": self.money,
            "mental_state": self.mental_state.value,
            "stress_level": self.stress_level,
            "relationships": self.relationships,
            "job": self.job,
            "extracurriculars": self.extracurriculars,
            "stats": self.stats,
            "research_projects": [
                {
                    "name": p.name,
                    "difficulty": p.difficulty,
                    "duration": p.duration,
                    "progress": p.progress,
                    "completed": p.completed
                } for p in self.research_projects
            ],
            "skill_levels": self.skill_levels
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Student':
        student = cls(data["name"], data["major"])
        student.semester = data["semester"]
        student.energy = data["energy"]
        student.max_energy = data["max_energy"]
        student.gpa = data["gpa"]
        student.credits = data["credits"]
        student.inventory = [Item(item["name"], item["type"], item["value"]) 
                           for item in data["inventory"]]
        student.skills = data["skills"]
        student.money = data.get("money", 500)
        student.mental_state = MentalState(data.get("mental_state", "good"))
        student.stress_level = data.get("stress_level", 0)
        student.relationships = data.get("relationships", {})
        student.job = data.get("job", None)
        student.extracurriculars = data.get("extracurriculars", [])
        student.stats = data.get("stats", {
            "classes_attended": 0,
            "assignments_completed": 0,
            "social_events": 0,
            "money_earned": 0
        })
        student.research_projects = [
            ResearchProject(p["name"], p["difficulty"], p["duration"])
            for p in data.get("research_projects", [])
        ]
        for p, proj in zip(data.get("research_projects", []), student.research_projects):
            proj.progress = p["progress"]
            proj.completed = p["completed"]
        student.skill_levels = data.get("skill_levels", {
            "Research": 1,
            "Writing": 1,
            "Programming": 1,
            "Presentation": 1,
            "Teamwork": 1
        })
        return student

class UniversityLifeSimulator:
    def __init__(self):
        self.player: Student = None
        self.scenarios = self.load_scenarios()
        self.setup_logging()
        self.load_config()
        self.current_time = time(8, 0)  # Start at 8 AM
        self.current_weather = random.choice(list(Weather))
        self.research_projects = self.load_research_projects()
        self.story_progress = StoryProgress()

    def setup_logging(self):
        logging.basicConfig(
            filename='university_sim.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def load_config(self):
        try:
            with open('config.yaml', 'r') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            self.config = self.get_default_config()

    def get_default_config(self):
        return {
            "jobs": [
                {"title": "Library Assistant", "hourly_rate": 12},
                {"title": "Cafe Barista", "hourly_rate": 15},
                {"title": "Teaching Assistant", "hourly_rate": 18},
                {"title": "Research Assistant", "hourly_rate": 20},
                {"title": "Campus Tour Guide", "hourly_rate": 14}
            ],
            "extracurriculars": [
                "Student Government",
                "Chess Club",
                "Sports Team",
                "Drama Club",
                "Coding Club",
                "Debate Team",
                "Music Band",
                "Environmental Club"
            ],
            "course_list": [
                {"name": "Introduction to Programming", "credits": 3, "difficulty": 2},
                {"name": "Advanced Mathematics", "credits": 4, "difficulty": 3},
                {"name": "Business Ethics", "credits": 3, "difficulty": 2},
                {"name": "Data Structures", "credits": 4, "difficulty": 3},
                {"name": "World History", "credits": 3, "difficulty": 2}
            ]
        }

    def load_scenarios(self) -> Dict:
        return {
            "locations": [
                "library during finals", "crowded cafeteria", "student union", 
                "lecture hall", "professor's office", "group study room",
                "campus coffee shop", "dormitory", "campus gym", "computer lab",
                "online zoom class", "campus park", "research lab",
                "career fair venue", "student club room"
            ],
            "challenges": [
                "Pop Quiz",
                "Group Project",
                "Final Exam",
                "Research Paper",
                "Presentation",
                "Lab Assignment",
                "Coding Challenge",
                "Field Work",
                "Case Study"
            ],
            "items": [
                Item("Textbook", "study_aid", 50),
                Item("Coffee", "energy_boost", 5),
                Item("Study Guide", "study_aid", 30),
                Item("Energy Drink", "energy_boost", 10),
                Item("Calculator", "study_aid", 20)
            ]
        }

    def load_research_projects(self) -> List[ResearchProject]:
        return [
            ResearchProject("AI in Education", 3, 100),
            ResearchProject("Sustainable Energy Solutions", 4, 150),
            ResearchProject("Blockchain Applications", 3, 120),
            ResearchProject("Genetic Engineering Ethics", 5, 200),
            ResearchProject("Urban Planning Innovations", 2, 80)
        ]

    def create_character(self):
        print("\nCreate your character:")
        name = input("Enter your name: ")
        print("\nChoose your major:")
        majors = ["Computer Science", "Business", "Engineering", "Arts", "Medicine"]
        for i, major in enumerate(majors, 1):
            print(f"{i}. {major}")
        major_choice = int(input("Enter the number of your choice: ")) - 1
        major = majors[major_choice]
        
        print("\nChoose difficulty:")
        difficulties = [d.value for d in Difficulty]
        for i, diff in enumerate(difficulties, 1):
            print(f"{i}. {diff}")
        diff_choice = int(input("Enter the number of your choice: ")) - 1
        difficulty = Difficulty(difficulties[diff_choice])
        
        self.player = Student(name, major, difficulty)

    def generate_scenario(self) -> str:
        location = random.choice(self.scenarios["locations"])
        return f"You are at the {location}..."

    def make_decision(self, options: List[str]) -> int:
        print("\nAvailable actions:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        while True:
            try:
                choice = int(input("Enter the number of your choice: "))
                if 1 <= choice <= len(options):
                    return choice
                print(f"Please enter a number between 1 and {len(options)}")
            except ValueError:
                print("Please enter a valid number")

    def academic_challenge(self, challenge: str, difficulty: int) -> bool:
        print(f"\nChallenge: {challenge}")
        print(f"Difficulty: {difficulty}")
        
        success_chance = (
            (self.player.energy / 2) +
            (len(self.player.skills) * 10) +
            (self.player.gpa * 10) -
            (self.player.stress_level / 2)
        )
        
        if any(item.type == "study_aid" for item in self.player.inventory):
            success_chance += 20
        
        success = random.randint(0, 100) < success_chance
        
        self.player.energy -= 20
        self.player.stress_level += 15
        
        if success:
            print("Success! Your hard work paid off!")
            self.player.gpa = min(4.0, self.player.gpa + 0.1)
            self.player.credits += random.randint(1, 3)
        else:
            print("Unfortunately, you didn't succeed this time.")
            self.player.gpa = max(0.0, self.player.gpa - 0.1)
        
        return success

    def handle_item_usage(self):
        if not self.player.inventory:
            print("You don't have any items!")
            return
            
        print("\nYour items:")
        items = self.player.inventory
        for i, item in enumerate(items, 1):
            print(f"{i}. {item.name} ({item.type})")
            
        choice = self.make_decision([item.name for item in items])
        used_item = items[choice - 1]
        
        if used_item.type == "energy_boost":
            self.player.energy = min(self.player.max_energy, 
                                   self.player.energy + used_item.value)
            print(f"Used {used_item.name}! Energy restored by {used_item.value}")
        elif used_item.type == "study_aid":
            self.player.stress_level = max(0, self.player.stress_level - used_item.value)
            print(f"Used {used_item.name}! Stress reduced by {used_item.value}")
            
        self.player.remove_item(used_item)

    def handle_study_session(self):
        study_outcome = random.choice([
            "skill improvement",
            "energy drain",
            "item discovery",
            "GPA boost"
        ])
        
        print("\nStudying...")
        if study_outcome == "skill improvement":
            self.player.energy -= 10
            print("Your dedicated study session pays off!")
            if random.random() < 0.3 and self.player.semester > 1:
                new_skill = f"{self.player.major} Study Technique {len(self.player.skills) + 1}"
                self.player.skills.append(new_skill)
                print(f"You learned: {new_skill}!")
                
        elif study_outcome == "energy drain":
            energy_loss = random.randint(5, 15)
            self.player.energy = max(0, self.player.energy - energy_loss)
            print(f"Intense studying drains {energy_loss} energy!")
            
        elif study_outcome == "item discovery":
            found_item = random.choice(self.scenarios["items"])
            self.player.add_item(found_item)
            print(f"While studying, you found a {found_item.name}!")
            
        elif study_outcome == "GPA boost":
            gpa_increase = random.uniform(0.05, 0.15)
            self.player.gpa = min(4.0, self.player.gpa + gpa_increase)
            print(f"Your studying improved your GPA by {gpa_increase:.2f}!")

    def handle_rest(self):
        energy_recovery = random.randint(20, 40)
        stress_relief = random.randint(10, 25)
        
        self.player.energy = min(self.player.max_energy, self.player.energy + energy_recovery)
        self.player.stress_level = max(0, self.player.stress_level - stress_relief)
        
        print(f"You took some rest and recovered {energy_recovery} energy!")
        print(f"Your stress level decreased by {stress_relief} points.")

    def apply_weather_effects(self):
        weather_message = f"Current weather: {self.current_weather.value}"
        if self.current_weather == Weather.RAINY:
            self.player.energy -= 5
            self.player.stress_level += 2
            weather_message += " (Energy -5, Stress +2)"
        elif self.current_weather == Weather.SNOWY:
            self.player.energy -= 10
            self.player.stress_level += 5
            weather_message += " (Energy -10, Stress +5)"
        print(weather_message)

    def handle_social_interaction(self):
        available_interactions = [
            "Study Group",
            "Club Meeting",
            "Coffee with Friends",
            "Campus Event",
            "Sports Activity"
        ]
        
        print("\nChoose a social activity:")
        choice = self.make_decision(available_interactions)
        interaction = available_interactions[choice - 1]
        
        energy_cost = random.randint(5, 15)
        stress_relief = random.randint(5, 20)
        
        self.player.energy -= energy_cost
        self.player.stress_level = max(0, self.player.stress_level - stress_relief)
        self.player.stats["social_events"] += 1
        
        print(f"\nYou participated in: {interaction}")
        print(f"Energy cost: {energy_cost}")
        print(f"Stress relieved: {stress_relief}")

        if random.random() < 0.3:
            new_friend = f"Friend_{len(self.player.relationships) + 1}"
            self.player.relationships[new_friend] = 50
            print(f"You made a new friend: {new_friend}!")

    def manage_time(self, hours: int):
        current_datetime = datetime.combine(datetime.today(), self.current_time)
        new_datetime = current_datetime.replace(hour=(current_datetime.hour + hours) % 24)
        self.current_time = new_datetime.time()
        
        if random.random() < 0.2:
            self.current_weather = random.choice(list(Weather))
            print(f"Weather changed to {self.current_weather.value}!")

    def handle_job_activities(self):
        if not self.player.job:
            print("\nAvailable Jobs:")
            job_choice = self.make_decision([job["title"] for job in self.config["jobs"]])
            self.player.job = self.config["jobs"][job_choice - 1]
            print(f"Congratulations! You got a job as {self.player.job['title']}!")
        else:
            try:
                hours = int(input("How many hours do you want to work? (1-8): "))
                hours = min(8, max(1, hours))
                earned = self.player.work_part_time(hours)
                self.manage_time(hours)
                print(f"You earned ${earned} from work!")
                print(f"Current balance: ${self.player.money}")
            except ValueError:
                print("Please enter a valid number of hours.")

    def handle_extracurricular(self):
        if len(self.player.extracurriculars) >= 3:
            print("You're already involved in the maximum number of extracurriculars!")
            return

        available = [x for x in self.config["extracurriculars"] 
                    if x not in self.player.extracurriculars]
        if not available:
            print("No more extracurriculars available!")
            return

        print("\nAvailable Extracurricular Activities:")
        choice = self.make_decision(available)
        activity = available[choice - 1]
        self.player.extracurriculars.append(activity)
        self.player.stress_level += 5
        self.player.energy -= 10
        print(f"You joined {activity}!")

    def manage_courses(self):
        if not self.player.courses:
            print("\nSelect courses for this semester:")
            available_courses = self.config["course_list"]
            while len(self.player.courses) < 4:
                print("\nAvailable courses:")
                remaining_courses = [c for c in available_courses 
                                  if c["name"] not in [course.name for course in self.player.courses]]
                for i, course in enumerate(remaining_courses, 1):
                    print(f"{i}. {course['name']} (Credits: {course['credits']})")
                
                choice = self.make_decision([c["name"] for c in remaining_courses])
                selected = remaining_courses[choice - 1]
                new_course = Course(selected["name"], selected["credits"], selected["difficulty"])
                self.player.courses.append(new_course)
                print(f"Enrolled in {new_course.name}")
        else:
            print("\nCurrent courses:")
            for i, course in enumerate(self.player.courses, 1):
                print(f"{i}. {course.name} (Current Grade: {course.calculate_final_grade():.1f})")
            
            course_choice = self.make_decision([c.name for c in self.player.courses])
            chosen_course = self.player.courses[course_choice - 1]
            
            print(f"\nManaging {chosen_course.name}")
            options = ["Add Assignment", "Grade Assignment", "Take Midterm", "Take Final", "Back"]
            action = self.make_decision(options)
            
            if action == 1:  # Add Assignment
                name = input("Enter assignment name: ")
                weight = float(input("Enter assignment weight (0-1): "))
                chosen_course.add_assignment(name, weight)
                print(f"Assignment '{name}' added to {chosen_course.name}")
            elif action == 2:  # Grade Assignment
                if not chosen_course.assignments:
                    print("No assignments to grade.")
                else:
                    for i, assignment in enumerate(chosen_course.assignments, 1):
                        print(f"{i}. {assignment['name']} (Current Grade: {assignment['grade']})")
                    assignment_choice = int(input("Choose an assignment to grade: ")) - 1
                    grade = float(input("Enter the grade (0-100): "))
                    chosen_course.grade_assignment(assignment_choice, grade)
                    print(f"Assignment graded. New course grade: {chosen_course.calculate_final_grade():.1f}")
            elif action == 3:  # Take Midterm
                grade = self.academic_challenge(f"{chosen_course.name} Midterm", chosen_course.difficulty * 10)
                chosen_course.midterm_grade = grade
                print(f"Midterm grade: {grade:.1f}")
            elif action == 4:  # Take Final
                grade = self.academic_challenge(f"{chosen_course.name} Final", chosen_course.difficulty * 15)
                chosen_course.final_grade = grade
                print(f"Final grade: {grade:.1f}")
            
            print(f"Updated course grade: {chosen_course.calculate_final_grade():.1f}")

    def handle_research_activities(self):
        if not self.player.research_projects:
            print("\nAvailable Research Projects:")
            project_choice = self.make_decision([p.name for p in self.research_projects])
            chosen_project = self.research_projects[project_choice - 1]
            self.player.start_research_project(chosen_project)
            print(f"You've started the research project: {chosen_project.name}")
        else:
            print("\nYour ongoing research projects:")
            for i, project in enumerate(self.player.research_projects, 1):
                print(f"{i}. {project.name} - Progress: {project.progress}%")
            
            project_choice = self.make_decision([p.name for p in self.player.research_projects])
            chosen_project = self.player.research_projects[project_choice - 1]
            
            hours = int(input("How many hours do you want to work on this project? (1-8): "))
            hours = min(8, max(1, hours))
            progress = self.player.work_on_research(project_choice - 1, hours)
            self.manage_time(hours)
            print(f"You made {progress:.2f}% progress on {chosen_project.name}")

    def save_game(self):
        save_data = {
            "player": self.player.to_dict(),
            "current_time": self.current_time.strftime("%H:%M"),
            "current_weather": self.current_weather.value,
            "story_progress": {
                "semester": self.story_progress.semester,
                "major_plot": self.story_progress.major_plot.value if self.story_progress.major_plot else None,
                "story_arcs": {name: arc.current_milestone for name, arc in self.story_progress.story_arcs.items()},
                "relationships": self.story_progress.relationships,
                "key_decisions": self.story_progress.key_decisions,
                "global_awareness": self.story_progress.global_awareness,
                "achievements": list(self.story_progress.achievements)
            }
        }
        
        filename = f"save_{self.player.name.lower()}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(save_data, f)
            print(f"Game saved successfully as {filename}")
        except Exception as e:
            print(f"Error saving game: {e}")

    def load_game(self):
        save_files = [f for f in os.listdir() if f.startswith("save_") and f.endswith(".json")]
        if not save_files:
            print("No save files found.")
            return False
        
        print("Available save files:")
        for i, file in enumerate(save_files, 1):
            print(f"{i}. {file}")
        
        choice = self.make_decision(save_files)
        filename = save_files[choice - 1]
        
        try:
            with open(filename, 'r') as f:
                save_data = json.load(f)
            
            self.player = Student.from_dict(save_data["player"])
            self.current_time = datetime.strptime(save_data["current_time"], "%H:%M").time()
            self.current_weather = Weather(save_data["current_weather"])
            
            story_progress = save_data["story_progress"]
            self.story_progress.semester = story_progress["semester"]
            self.story_progress.major_plot = MajorPlot(story_progress["major_plot"]) if story_progress["major_plot"] else None
            for name, milestone in story_progress["story_arcs"].items():
                self.story_progress.story_arcs[name].current_milestone = milestone
            self.story_progress.relationships = story_progress["relationships"]
            self.story_progress.key_decisions = story_progress["key_decisions"]
            self.story_progress.global_awareness = story_progress["global_awareness"]
            self.story_progress.achievements = set(story_progress["achievements"])
            
            print(f"Game loaded successfully from {filename}")
            return True
        except Exception as e:
            print(f"Error loading game: {e}")
            return False

    def run_game(self):
        print("Welcome to University Life Simulator!")
        
        load_game = input("Do you want to load a saved game? (y/n): ").lower()
        if load_game == 'y':
            if not self.load_game():
                self.create_character()
                self.choose_major_plot()
        else:
            self.create_character()
            self.choose_major_plot()

        while self.story_progress.semester <= 8:  # 4 years, 2 semesters per year
            self.start_semester()
            self.run_semester_events()
            self.end_semester()

        self.graduation_ceremony()

    def choose_major_plot(self):
        print("\nAs you begin your university journey, you feel drawn to a particular path:")
        options = [plot.value for plot in MajorPlot]
        choice = self.make_decision(options)
        self.story_progress.set_major_plot(MajorPlot(options[choice - 1]))
        print(f"You've chosen to focus on {self.story_progress.major_plot.value}!")

    def start_semester(self):
        print(f"\n--- Semester {self.story_progress.semester} Begins ---")
        self.player.energy = self.player.max_energy
        self.player.stress_level = 0
        self.manage_courses()

    def run_semester_events(self):
        for _ in range(3):  # 3 major events per semester
            self.trigger_story_event()
            self.player.update_mental_state()
            if self.player.mental_state == MentalState.BURNOUT:
                print("You're experiencing burnout! Taking a mental health day...")
                self.handle_rest()

    def end_semester(self):
        print(f"\n--- Semester {self.story_progress.semester} Ends ---")
        self.calculate_semester_gpa()
        self.story_progress.advance_semester()
        self.player.semester_up()

    def trigger_story_event(self):
        for arc_name, arc in self.story_progress.story_arcs.items():
            if arc_name == "personal_growth":
                self.personal_growth_event(arc.get_current_milestone())
            elif arc_name == "academic_journey":
                self.academic_journey_event(arc.get_current_milestone())
            elif arc_name == "social_life":
                self.social_life_event(arc.get_current_milestone())
            elif arc_name == "career_development":
                self.career_development_event(arc.get_current_milestone())

    def personal_growth_event(self, milestone: str):
        if milestone == "Freshman Orientation":
            self.freshman_orientation()
        elif milestone == "Identity Crisis":
            self.identity_crisis()
        elif milestone == "Finding Your Passion":
            self.finding_your_passion()
        elif milestone == "Leadership Opportunity":
            self.leadership_opportunity()
        elif milestone == "Personal Transformation":
            self.personal_transformation()
        elif milestone == "Legacy Planning":
            self.legacy_planning()

    def academic_journey_event(self, milestone: str):
        if milestone == "First Major Assignment":
            self.first_major_assignment()
        elif milestone == "Choosing Specialization":
            self.choosing_specialization()
        elif milestone == "Internship Application":
            self.internship_application()
        elif milestone == "Research Project":
            self.research_project()
        elif milestone == "Thesis Proposal":
            self.thesis_proposal()
        elif milestone == "Final Presentation":
            self.final_presentation()

    def social_life_event(self, milestone: str):
        if milestone == "Roommate Introduction":
            self.roommate_introduction()
        elif milestone == "Club Fair":
            self.club_fair()
        elif milestone == "Campus Event Organization":
            self.campus_event_organization()
        elif milestone == "Relationship Dilemma":
            self.relationship_dilemma()
        elif milestone == "Spring Break Adventure":
            self.spring_break_adventure()
        elif milestone == "Graduation Party Planning":
            self.graduation_party_planning()

    def career_development_event(self, milestone: str):
        if milestone == "Career Center Visit":
            self.career_center_visit()
        elif milestone == "First Job Fair":
            self.first_job_fair()
        elif milestone == "Summer Internship":
            self.summer_internship()
        elif milestone == "Networking Event":
            self.networking_event()
        elif milestone == "Job Interview Preparation":
            self.job_interview_preparation()
        elif milestone == "Job Offer Negotiation":
            self.job_offer_negotiation()

    # Example implementation of one event from each story arc
    def freshman_orientation(self):
        print("\nWelcome to Freshman Orientation!")
        choice = self.make_decision([
            "Attend all the informational sessions",
            "Focus on meeting new people",
            "Attend the fun activities",
            "Skip the orientation and explore the campus",
            "Explore the campus on your own"
        ])
        if choice == 1:
            print("You gain valuable information about university resources.")
            self.player.skill_levels["Academic"] = self.player.skill_levels.get("Academic", 0) + 1
        elif choice == 2:
            print("You make several new friends!")
            self.story_progress.update_relationship("New Friends", 20)
        else:
            print("You discover some hidden spots on campus.")
            self.story_progress.increase_global_awareness(5)
        self.story_progress.add_achievement("Oriented Freshman")

    def first_major_assignment(self):
        print("\nYour first major assignment is due soon!")
        choice = self.make_decision([
            "Pull an all-nighter to complete it",
            "Seek help from a study group",
            "Ask for an extension"
        ])
        if choice == 1:
            success = self.academic_challenge("All-Night Study Session", 70)
            if success:
                print("Your hard work pays off!")
                self.player.gpa += 0.2
            else:
                print("You're exhausted and your work suffers.")
                self.player.gpa -= 0.1
        elif choice == 2:
            print("Collaborating improves your understanding.")
            self.player.gpa += 0.1
            self.story_progress.update_relationship("Classmates", 10)
        else:
            print("Your professor grants the extension but seems disappointed.")
            self.story_progress.update_relationship("Professor", -5)
        self.story_progress.add_achievement("First Assignment Survivor")

    def roommate_introduction(self):
        print("\nTime to meet your roommate, Xahoor!")
        choice = self.make_decision([
            "Suggest going out for coffee to get to know each other",
            "Propose setting up room rules right away",
            "Keep to yourself and be polite but distant"
        ])
        if choice == 1:
            print("You and Xahoor hit it off over coffee!")
            self.story_progress.update_relationship("Xahoor", 20)
        elif choice == 2:
            print("You and Xahoor establish clear boundaries.")
            self.story_progress.update_relationship("Xahoor", 10)
        else:
            print("Things remain cordial but cool with Xahoor.")
        self.story_progress.add_achievement("Roommate Roulette Survivor")

    def career_center_visit(self):
        print("\nYou decide to visit the university's career center.")
        choice = self.make_decision([
            "Get help with your resume",
            "Explore internship opportunities",
            "Take a career aptitude test"
        ])
        if choice == 1:
            print("Your resume is now much more professional!")
            self.player.skill_levels["Professional Writing"] = self.player.skill_levels.get("Professional Writing", 0) + 1
        elif choice == 2:
            print("You find some interesting internship leads.")
            self.story_progress.make_key_decision("Internship Focus", "Early Explorer")
        else:
            print("The test results give you new career ideas to consider.")
            self.story_progress.increase_global_awareness(10)
        self.story_progress.add_achievement("Career Planner")

    def roommate_drama_event(self):
        print("Your roommate Xahoor has been acting strange lately...")
        choice = self.make_decision([
            "Confront Xahoor directly",
            "Explore the coredoor with freinds",
            "Have fun with all others and your own",
            "Using trends of your University and ",
            "See the resturants and food quality of the University",
            "Talk to your Resident Advisor",
            "Ignore the situation and hope it improves"
        ])
        if choice == 1:
            print("You have a heart-to-heart with Xahoor and resolve your issues.")
            self.story_progress.update_relationship("Xahoor", 20)
            self.player.stress_level -= 10
        elif choice == 2:
            print("Your RA mediates the situation, but things remain a bit awkward.")
            self.story_progress.update_relationship("Xahoor", 5)
            self.player.stress_level -= 5
        else:
            print("The tension with Xahoor continues to build...")
            self.story_progress.update_relationship("Xahoor", -10)
            self.player.stress_level += 15
        
        self.story_progress.add_achievement("Roommate Drama Survivor")

    def calculate_semester_gpa(self):
        total_credits = sum(course.credits for course in self.player.courses)
        weighted_grades = sum(course.calculate_final_grade() * course.credits for course in self.player.courses)
        semester_gpa = weighted_grades / total_credits if total_credits > 0 else 0
        self.player.gpa = (self.player.gpa + semester_gpa) / 2  # Average with previous GPA
        print(f"Your semester GPA: {semester_gpa:.2f}")
        print(f"Your cumulative GPA: {self.player.gpa:.2f}")

    def graduation_ceremony(self):
        print("\nCongratulations! You've made it to graduation!")
        print(f"Your final GPA: {self.player.gpa:.2f}")
        print("As you reflect on your university journey, you feel:")
        choice = self.make_decision([
            "Proud of Your academic achievements",
            "Gratefull for the friendships you've made",
            "Confident for the future ahead",
            "Exited for the next chapter",
            "Reflective abour your experiences",
            "Hopeful about your future",
            "Nervous about the real world",
            "Curious about your next steps",
            "Excited about your career prospects",
            "Nostalgic about your time on campus"
        ])
        if choice == 1:
            self.story_progress.add_achievement("Academic Superstar")
        elif choice == 2:
            self.story_progress.add_achievement("Social Butterfly")
        elif choice == 3:
            self.story_progress.add_achievement("Future Leader")
        else:
            self.story_progress.add_achievement("Campus Enthusiast")
        
        print("\nYour University Life Summary:")
        print(self.story_progress.get_story_summary())
        print("\nThank you for playing University Life Simulator!")

if __name__ == "__main__":
    game = UniversityLifeSimulator()
    game.run_game()
    