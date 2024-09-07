import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from resume_repackager import LatexResumeRepackager
from resume_parser import LatexResumeParser

class ResumeReshaper:
    def __init__(self, client, parser, job_description):
        self.parser = parser
        self.job_description = job_description
        self.client = client
        self.keywords = []

    def extract_keywords(self):
        print("Extracting keywords from the job description...")
        prompt = f"""Given the following job description, extract the most relevant keywords and phrases that might be 
        used by an Applicant Tracking System (ATS) to filter applicants. Please return a list of keywords only.
        Job Description: {self.job_description}
        """
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that identifies keywords for job descriptions that are likely to be used in ATS software."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        self.keywords = response.choices[0].message.content.strip().split(', ')
        print("Keywords identified: ", self.keywords)

    def reshape_experience(self):
        print("\nReshaping experience based on the extracted keywords...")
        new_experience = []
        
        for experience_entry in self.parser.experience:
            bullet_point_count = 6
            average_length = sum(len(bp) for bp in experience_entry['bullet_points']) // bullet_point_count

            prompt = f"""
            We're rewriting a resume to get it past Applicant Tracking System (ATS).
            Feel free to fabricate/exaggerate bullet points, use made up metrics, impact, etc. as long as it's within the realm of possibility.
            Rewrite the following work experience to align with the following keywords: {', '.join(self.keywords)}.
            Keep the number of bullet points exactly {bullet_point_count} bullet points. 
            Each bullet point should be roughly {average_length} characters in length. Do NOT exceed {bullet_point_count} bullet points.
            Do NOT alter the original job title.
            Return the result in the following JSON format:
            {{
            "job_title": "<job_title>",
            "company": "<company>",
            "location": "<location>",
            "dates": "<dates>",
            "bullet_points": [
                "<bullet_point_1>",
                "<bullet_point_2>",
                ...
            ]
            }}
            Job Title: {experience_entry['job_title']}
            Company: {experience_entry['company']}
            Location: {experience_entry['location']}
            Dates: {experience_entry['dates']}
            Bullet Points: {', '.join(experience_entry['bullet_points'])}
            """

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an assistant that rewrites resume experience sections in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            reshaped_entry = response.choices[0].message.content.strip()
            print(f"\nGPT Response for Experience:\n{reshaped_entry}")  # Debugging: print the GPT response

            # Parse JSON response and limit bullet points
            reshaped_experience = self._parse_gpt_response(reshaped_entry, max_bullet_points=bullet_point_count)
            new_experience.append(reshaped_experience)
        
        return new_experience


    def reshape_education(self):
        print("\nReshaping education based on the extracted keywords...")
        new_education = []
        for education_entry in self.parser.education:
            prompt = f"""
            Rewrite the following education details to align with the following keywords: {', '.join(self.keywords)}.
            Make the education background sound more relevant to the job description. Return the result in the following JSON format:
            {{
            "institution": "<institution>",
            "major": "<major>",
            "dates": "<dates>"
            }}
            Institution: {education_entry['institution']}
            Major: {education_entry.get('major', 'N/A')}
            Dates: {education_entry['dates']}
            """
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that rewrites education sections of resumes."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            reshaped_entry = response.choices[0].message.content.strip()
            print(f"\nReshaped education for {education_entry['institution']}:\n{reshaped_entry}")
            new_education.append(self._parse_gpt_response(reshaped_entry))
        
        return new_education

    def reshape_technical_skills(self):
        print("\nReshaping technical skills based on the extracted keywords...")
        
        prompt = f"""
        Rewrite the following technical skills to align with the following keywords: {', '.join(self.keywords)}.
        Retain or introduce skill categories as needed, but limit the total number of categories to be no greater than 3. 
        Return the result in the following JSON format:
        {{
        "technical_skills": {{
            "Category 1": ["Skill 1", "Skill 2", "Skill 3"],
            "Category 2": ["Skill 1", "Skill 2", "Skill 3"],
            ...
        }}
        }}
        """
   
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that rewrites technical skills sections and aren't afraid of fabricating skills to get the applicant pass ATS screening software."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        reshaped_skills = response.choices[0].message.content.strip()
        print(f"\nReshaped technical skills:\n{reshaped_skills}")

        # Parse the response into structured technical skills
        return self._parse_gpt_response(reshaped_skills).get('technical_skills', {})

    def _parse_gpt_response(self, response, max_bullet_points=None):
        """
        Parse the GPT response as JSON data and ensure the number of bullet points doesn't exceed the limit.
        
        Params:
        - response (str): The raw GPT response to parse.
        - max_bullet_points (int): The maximum number of bullet points to accept (if provided).
        
        Returns:
        - dict: Parsed experience, education, or technical skills data.
        """
        try:
            parsed_response = json.loads(response)  # Parse GPT response as JSON
            
            # If bullet points are present and max_bullet_points is set, truncate the list if necessary
            if max_bullet_points and 'bullet_points' in parsed_response:
                parsed_response['bullet_points'] = parsed_response['bullet_points'][:max_bullet_points]
            
            return parsed_response
        except json.JSONDecodeError:
            print("Error parsing JSON from GPT response. Response was:")
            print(response)
            return {}




# Example usage
if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Fetch the OpenAI API key from the environment
    api_key = os.getenv("OPENAI_API_KEY")

    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)

    # Define the job description
    job_description = """
    We are looking for a Senior Full-Stack Developer with expertise in Angular, AWS, Docker, and Python. 
    The ideal candidate should have a track record of building scalable web applications and experience with cloud infrastructure. 
    Strong knowledge of CI/CD pipelines and familiarity with Agile methodologies are also required.
    """

    # Instantiate parser (assuming you already have LatexResumeParser implemented and instantiated)
    parser = LatexResumeParser('resume.tex')

    # Instantiate the ResumeReshaper with the OpenAI client
    reshaper = ResumeReshaper(client=client, parser=parser, job_description=job_description)

    # Step 1: Extract keywords from the job description
    reshaper.extract_keywords()

    # Step 2: Reshape the experience section
    new_experience = reshaper.reshape_experience()

    # Step 4: Reshape the technical skills section
    new_technical_skills = reshaper.reshape_technical_skills()

    # Now pass the reshaped data back to the ResumeRepackager class to rewrite the LaTeX document
    repackager = LatexResumeRepackager(parser)

    # Print the reshaped content before saving to file
    print("\nFinal Reshaped Experience:")
    print(new_experience)

    print("\nFinal Reshaped Technical Skills:")
    print(new_technical_skills)

    # Replace and save the updated resume
    repackager.replace_experience(new_experience)
    repackager.replace_technical_skills(new_technical_skills)

    # Save the updated resume to a new file
    repackager.save_to_file('updated_resume.tex')
