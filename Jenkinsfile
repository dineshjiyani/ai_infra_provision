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
        stage('Set Up Virtual Environment') {
            steps {
                sh '''
                    #!/bin/bash
                    python3 -m venv myenv
                    source myenv/bin/activate
                '''
            }
        }
        stage('Run Python Script') {
            steps {
                sh """
                    #!/bin/bash
                    source myenv/bin/activate
                    python3 ./geminiApi.py ""${USER_PROMPT}""
                """
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