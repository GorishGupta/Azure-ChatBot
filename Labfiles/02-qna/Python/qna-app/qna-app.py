from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient

def main():
    try:
        # Load configuration settings
        if not load_dotenv():
            print("Warning: .env file not found. Make sure environment variables are set.")

        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')
        ai_project_name = os.getenv('QA_PROJECT_NAME')
        ai_deployment_name = os.getenv('QA_DEPLOYMENT_NAME')

        if not all([ai_endpoint, ai_key, ai_project_name, ai_deployment_name]):
            raise ValueError("One or more environment variables are missing.")

        # Create Azure Question Answering client
        credential = AzureKeyCredential(ai_key)
        ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)

        # Interactive Q&A loop
        print("Type 'quit' to exit the program.")
        user_question = ""
        while user_question.lower() != "quit":
            user_question = input("\nQuestion:\n")
            if user_question.lower() == "quit":
                print("Exiting the program.")
                break

            response = ai_client.get_answers(
                question=user_question,
                project_name=ai_project_name,
                deployment_name=ai_deployment_name
            )

            for candidate in response.answers:
                print("\nAnswer:")
                print(candidate.answer)
                print(f"Confidence: {candidate.confidence:.2f}")
                print(f"Source: {candidate.source}\n")
    except Exception as ex:
        print(f"An error occurred: {ex}")

if __name__ == "__main__":
    main()
