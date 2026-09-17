Workout Tracker Backend

A backend-only REST API for planning workouts, scheduling workout sessions, recording actual performance, reviewing completed workouts, and viewing basic progress reports.

This is a learning project focused on building a small, production-aware Django backend. It is not intended to be a polished fitness SaaS.

Current status

Planning and initial setup

Project scope and main product decisions are defined.

Repository and development environment setup are in progress.

Database models and API endpoints have not been implemented yet.

Planned functionality

Exercise catalog with repeatable seed data

User registration and JWT authentication

Reusable workout plans with exercises and planned targets

Scheduled workout sessions

Actual sets, repetitions, weight, and optional comments

Pending, active, and completed workout states

Completed workout history

Progress reports based on completed workouts

Owner-only access to private workout data

Pagination, validation, and consistent API errors

Automated tests and OpenAPI/Swagger documentation

Chosen stack

Python

Django

Django REST Framework

PostgreSQL

Simple JWT

drf-spectacular / OpenAPI

Automated Django API tests

Docker

Gunicorn

Nginx

HTTPS

Git and GitHub

Project documentation

docs/decisions.md — project scope and important product decisions

docs/build-plan.md — step-by-step implementation plan

Setup

Local installation and environment instructions will be added after the initial Django project setup is complete.
