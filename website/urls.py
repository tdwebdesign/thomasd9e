from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("process_question/", views.process_question, name="process_question"),
    path("cfb_assistant/", views.cfb_assistant, name="cfb_assistant"),
    path("skills/", views.skills, name="skills"),
    path("projects/", views.projects, name="projects"),
    path("contact/", views.contact, name="contact"),
    path("color_palette/", views.color_palette, name="color-palette"),
]
