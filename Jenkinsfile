pipeline {
    agent any

    environment {
        GEMINI_API_KEY = credentials('geminiKey') // Gemini API key stored in Jenkins credentials
//        GOOGLE_APPLICATION_CREDENTIALS = credentials('gcpJson') // GCP key file stored in Jenkins credentials
//        PROJECT_ID = "${params.PROJECT_ID}" // Project ID parameter
        USER_PROMPT = "${params.USER_PROMPT}" // User prompt parameter
    }

    parameters {
//        string(name: 'PROJECT_ID', defaultValue: '', description: 'GCP Project ID')
        string(name: 'USER_PROMPT', defaultValue: '', description: 'User prompt for Gemini API')
//        string(name: 'BUCKET_NAME', defaultValue: '', description: 'GCS bucket name for uploading Terraform state and code')
    }

    stages {
        stage('Checkout Git Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/dineshjiyani/ai_infra_provision.git'
            }
        }

        stage('Get Terraform Code from Gemini API') {
            steps {
                script {
                    // Change to the directory where the code is located
                    dir('./') {
                        // Install required Python package
                        sh 'python3 -m venv myenv'
                        sh 'bash -c "source myenv/bin/activate"'
                        sh 'bash -c "pip install -q -U google-genai"'
                        sh 'ls'
                        // Run the Python script to get Terraform code from Gemini API
                        sh """'bash -c "source myenv/bin/activate && python3 ./geminiApi.py "${USER_PROMPT}""'"""

                        // List files for debugging
                        sh 'ls'
                    }
                }
            }
        }

        stage('Run Terraform Code') {
            steps {
                script {
                    // Change to the directory where the code is located
                    dir('./') {
                        // Initialize and apply Terraform
                        sh """
                            terraform init
                            terraform apply --auto-approve
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded! Terraform code generated, applied, and uploaded to GCS."
        }
        failure {
            echo "Pipeline failed. Check logs for details."
        }
    }
}