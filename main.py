import os
from openai import OpenAI
from dotenv import load_dotenv
from resume_parser import LatexResumeParser
from resume_reshaper import ResumeReshaper
from resume_repackager import LatexResumeRepackager

def get_user_input():
    """
    Get input from the user for the job description and the resume path.
    """
    # Prompt the user for the job description
    job_description = input("Please enter the job description: ")

    # Prompt the user for the path to their .tex resume file
    resume_path = input("Please enter the path to your LaTeX resume (.tex file): ")

    # Ensure the file exists before proceeding
    if not os.path.exists(resume_path):
        print(f"Error: The file '{resume_path}' does not exist. Please try again.")
        exit(1)
    
    return job_description, resume_path

def main():
    """
    Main function to handle user inputs and process the resume.
    """
    # Load the environment variables (including OpenAI API key) from .env file
    load_dotenv()

    # Fetch the OpenAI API key from the environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OpenAI API key not found in the environment. Make sure it is set in the .env file.")
        exit(1)

    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)

    # Step 1: Get job description and resume path from the user
    job_description, resume_path = get_user_input()

    # Step 2: Parse the user's LaTeX resume
    print(f"Parsing resume: {resume_path}")
    parser = LatexResumeParser(resume_path)

    # Step 3: Reshape the resume experience, education, and skills based on the job description
    print("Reshaping resume to align with the job description...")

    # Instantiate the ResumeReshaper
    reshaper = ResumeReshaper(client=client, parser=parser, job_description=job_description)

    # Extract keywords from the job description
    reshaper.extract_keywords()

    # Reshape the experience section
    new_experience = reshaper.reshape_experience()

    # Reshape the technical skills section
    new_technical_skills = reshaper.reshape_technical_skills()

    # Optionally, reshape education if needed
    new_education = reshaper.reshape_education()

    # Step 4: Update the resume with the new information
    print("Updating the resume with new experience, skills, and education...")
    repackager = LatexResumeRepackager(parser)

    repackager.replace_experience(new_experience)
    repackager.replace_technical_skills(new_technical_skills)

    # Step 5: Save the updated resume to a new file
    output_file = 'updated_resume.tex'
    repackager.save_to_file(output_file)

    print(f"Resume updated and saved as {output_file}")

# Entry point of the script
if __name__ == "__main__":
    main()
