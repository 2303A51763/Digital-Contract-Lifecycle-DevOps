# Digital Contract Lifecycle and Approval Management System

A beginner-friendly DevOps mini-project. Contract owners can submit agreements and reviewers can approve or reject them. The project demonstrates a Python web application, automated tests, containerization, and CI pipelines.

## Features
- Submit a contract with title, department, owner, and description
- Track Pending, Approved, and Rejected contracts
- Record an approval/rejection note
- Health-check endpoint at `/health`
- SQLite persistence using a Docker named volume
- Pytest automated tests
- GitHub Actions CI and Jenkins pipeline examples

## Technology stack
- Python 3.12, Flask, SQLite
- HTML/CSS
- Docker and Docker Compose
- GitHub Actions / Jenkins
- Pytest

## Run locally
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python -c "from app import init_db; init_db()"
python app.py
```
Open http://localhost:5000.

## Run with Docker Compose
Install Docker Desktop, open a terminal in this project folder, then:
```bash
docker compose up --build
```
Open http://localhost:5000. Stop with `Ctrl+C`, or run `docker compose down`.
Data is stored in the `contract_data` Docker volume.

## Run tests
```bash
pip install -r requirements.txt
pytest -q
```

## CI/CD demonstration
### GitHub Actions
1. Create a GitHub repository and push this project to the `main` branch.
2. GitHub Actions automatically runs `.github/workflows/ci.yml` on push and pull request.
3. View results under the repository's Actions tab.

### Jenkins
1. Install Jenkins and ensure the Jenkins agent has Python 3, pip, and Docker.
2. Create a Pipeline job connected to your Git repository.
3. Select "Pipeline script from SCM" and point it to this repository.
4. Run Build Now. The Jenkinsfile installs dependencies, runs tests, and builds the Docker image.

## Suggested presentation flow
1. Open the dashboard and submit a new contract.
2. Show its Pending status.
3. Approve or reject it and add a note.
4. Refresh to demonstrate SQLite persistence.
5. Run `pytest -q` to show automated tests.
6. Run `docker compose up --build` to demonstrate container deployment.
7. Push a commit to GitHub and show the CI workflow result.

## Project architecture
Browser -> Flask routes -> SQLite database
                  |
                  +-> Pytest tests
Git push / pull request -> GitHub Actions -> Tests -> Docker image build
Jenkins pipeline -> Install -> Tests -> Docker image build

## Important limitations
This is an academic demonstration, not a production contract platform. It does not include real user authentication, digital signatures, encryption/key management, legal e-signature compliance, email notifications, or fine-grained approval roles. Do not upload confidential contracts. Before production use, add authentication/authorization, CSRF protection, secure secrets, file scanning, audit logging, backups, and a managed database.
