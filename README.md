# Web-application-for-the-registration-and-control-of-paint-materials
This project was developed as my Graduation Thesis for my Associate Degree (TSU) in Computer Science. The goal was twofold: to solve a real-world inventory problem and to push my limits using a micro-framework to build a robust, production-ready web application.

Technical Philosophy: Why Raw SQL?
Unlike many modern applications that rely on ORMs, I made the conscious decision to use Raw SQL with PostgreSQL.

Control & Visibility: I prefer to see exactly how data is being fetched and manipulated.

Optimization: Writing manual queries allows for fine-tuned performance that ORMs often abstract away.

Systematic Approach: It ensures a deeper understanding of the relational schema and data integrity.

The Tech Stack
Backend: Python with Flask. I utilized Flask Blueprints to maintain a modular, clean, and scalable architecture.

Database: PostgreSQL (Strictly Raw SQL).

Frontend: Tailwind CSS. Chosen to streamline the UI development process and ensure a modern, responsive design without sacrificing performance.

Infrastructure: Docker. The project is fully containerized for consistent deployment.

Project Structure & Deployment
This repository is a "clean" version of the original development. To protect security, all sensitive keys and history from the initial commits were purged and modularized.

Database Schema: Included in the /database directory.

Containerization: Use the provided Dockerfile and docker-compose.yml to spin up the environment.

# Quick Start
docker-compose up --build

A Note on Communication & Growth
I am a Venezuelan developer currently at a B1/B2 English level. This project served not only as a technical challenge but also as a practice ground for my professional English writing. While my earlier commits in other versions were in Spanish, this repository reflects my commitment to mastering English for the global tech market.
