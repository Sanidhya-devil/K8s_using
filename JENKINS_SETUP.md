# Project 3: CI/CD Pipeline with Jenkins + Docker

Automates build → test → containerize → push → deploy for a simple Flask app.

## Project Structure
```
cicd_pipeline/
├── app/
│   ├── app.py              # Flask application
│   └── requirements.txt
├── tests/
│   └── test_app.py         # Unit tests run in the pipeline
├── Dockerfile
├── docker-compose.yml       # For local testing
├── .dockerignore
├── Jenkinsfile              # Pipeline definition
└── docs/JENKINS_SETUP.md
```

## Step 1: Install Jenkins
On an EC2 instance / local machine (Ubuntu example):
```bash
sudo apt update
sudo apt install openjdk-17-jdk -y
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
  "https://pkg.jenkins.io/debian-stable binary/" | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update
sudo apt install jenkins -y
sudo systemctl start jenkins
sudo systemctl enable jenkins
```
Access Jenkins at `http://<server-ip>:8080` and unlock using:
```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

## Step 2: Install Required Plugins
From **Manage Jenkins → Plugins**, install:
- Docker Pipeline
- Git
- Pipeline
- JUnit (usually pre-installed)

## Step 3: Give Jenkins Docker Access
```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

## Step 4: Add Credentials
**Manage Jenkins → Credentials → System → Global credentials → Add Credentials**
- Kind: Username with password
- ID: `dockerhub-creds` (must match the Jenkinsfile)
- Username/Password: your Docker Hub login

If deploying to a remote server via SSH, also add an SSH key credential and configure passwordless SSH from the Jenkins server to your deploy target.

## Step 5: Create the Pipeline Job
1. **New Item** → Name it `cicd-flask-pipeline` → select **Pipeline** → OK
2. Under **Pipeline** section:
   - Definition: "Pipeline script from SCM"
   - SCM: Git
   - Repository URL: your GitHub repo URL
   - Script Path: `Jenkinsfile`
3. Save.

## Step 6: Before Running — Edit the Jenkinsfile
Update these placeholders in `Jenkinsfile`:
- `IMAGE_NAME` → your Docker Hub username/repo
- `DEPLOY_SERVER` → your target server's SSH address (or remove the Deploy stage if you're just testing build/push)

## Step 7: Run the Pipeline
Click **Build Now**. Jenkins will:
1. Pull the latest code
2. Install dependencies & run tests
3. Build the Docker image
4. Push it to Docker Hub
5. SSH into the deploy server, pull the new image, and restart the container

## Local Testing (without Jenkins)
```bash
docker-compose up --build
# Visit http://localhost:5000
```

## Key Concepts Demonstrated
- CI/CD pipeline stages: build, test, package, deploy
- Docker image build & multi-tagging (build number + latest)
- Secure credential handling via Jenkins Credentials Store
- Automated testing gate before deployment (fails pipeline if tests fail)
- Zero-downtime-ish redeploy via SSH + container restart
- Health checks at both the Docker and application level
