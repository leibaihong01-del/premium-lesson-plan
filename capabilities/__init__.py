# capabilities package: 教师发展、教研、成果能力模块

from .competition import competition_plan, defense_questions, lesson_design, speech_script
from .research import paper_outline, project_application
from .achievements import patent_disclosure, software_copyright


def generate(capability, context):
    course = context.get("course", "课程")
    major = context.get("major", "专业")
    topic = context.get("topic", "教学主题")
    if capability == "competition_plan":
        return competition_plan(course, major, topic)
    if capability == "lesson_design":
        return lesson_design(course, major, topic)
    if capability == "speech_script":
        return speech_script(course, major, topic)
    if capability == "defense_questions":
        return defense_questions(course, major, topic)
    if capability == "project_application":
        return project_application(course, major, topic)
    if capability == "paper_outline":
        return paper_outline(course, major, topic)
    if capability == "software_copyright":
        return software_copyright(course, major, topic)
    if capability == "patent_disclosure":
        return patent_disclosure(course, major, topic)
    return "# 未知能力模块"
