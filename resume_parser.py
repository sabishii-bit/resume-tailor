import re

class LatexResumeParser:
    def __init__(self, latex_file_path):
        self.content = None
        self.experience = []
        self.education = []
        self.technical_skills = []
        self.markers = {}  # Stores positions of parsed sections
        
        # Load the LaTeX content from the file
        with open(latex_file_path, 'r') as file:
            self.content = file.read()

        # Parse the sections automatically upon initialization
        self.parse_experience()
        self.parse_education()
        self.parse_technical_skills()

    def parse_experience(self):
        # Extract the Experience section and store position
        experience_section = self._extract_section(r'\\section{Experience}', r'\\section{', self.content)
        if not experience_section:
            return

        experience_start = self.content.find(experience_section)
        self.markers['experience_start'] = experience_start
        self.markers['experience_end'] = experience_start + len(experience_section)

        # Find all the jobs with company, title, dates, and location
        experience_entries = re.findall(
            r'\\resumeSubheading\s*?\{(.*?)\}\s*?\{(.*?)\}\s*?\{(.*?)\}\s*?\{(.*?)\}', 
            experience_section, 
            re.DOTALL
        )

        self.experience = []
        for title, dates, company, location in experience_entries:
            bullets = self._extract_bullet_points(experience_section, title)
            self.experience.append({
                'job_title': title.strip(),
                'company': company.strip(),
                'location': location.strip(),
                'dates': dates.strip(),
                'bullet_points': bullets
            })

    def parse_education(self):
        # Extract the Education section and store position
        education_section = self._extract_section(r'\\section{Education}', r'\\section{', self.content)
        if not education_section:
            return

        education_start = self.content.find(education_section)
        self.markers['education_start'] = education_start
        self.markers['education_end'] = education_start + len(education_section)

        # Find all the education entries
        education_entries = re.findall(
            r'\\resumeSubheading\s*?\{(.*?)\}\s*?\{(.*?)\}\s*?\{(.*?)\}\s*?\{(.*?)\}', 
            education_section, 
            re.DOTALL
        )

        self.education = []
        for institution, dates, major, _ in education_entries:
            self.education.append({
                'institution': institution.strip(),
                'major': major.strip(),
                'dates': dates.strip()
            })

    def parse_technical_skills(self):
        # Extract the Technical Skills section and store position
        tech_section = self._extract_section(r'\\section{Technical Skills}', r'\\section{', self.content)
        if not tech_section:
            return

        tech_start = self.content.find(tech_section)
        self.markers['technical_skills_start'] = tech_start
        self.markers['technical_skills_end'] = tech_start + len(tech_section)

        # Extract technical skills categories and the associated skills
        tech_entries = re.findall(r'\\textbf{(.*?)}{: (.*?)}', tech_section, re.DOTALL)

        self.technical_skills = {}
        for label, skills in tech_entries:
            self.technical_skills[label.strip()] = [skill.strip() for skill in skills.split(',')]

    def _extract_section(self, start_pattern, end_pattern, content):
        # Find the start of the section
        start_match = re.search(start_pattern, content)
        if not start_match:
            return None

        # Find the end of the section (next section or end of document)
        end_match = re.search(end_pattern, content[start_match.end():])
        if end_match:
            return content[start_match.end():start_match.end() + end_match.start()]
        else:
            return content[start_match.end():]  # If no end match, return till the end of the document

    def _extract_bullet_points(self, section_content, job_title):
        # Extract the bullet points associated with a job
        job_start = re.search(re.escape(job_title), section_content)
        if not job_start:
            return []

        bullet_section = section_content[job_start.end():]
        bullet_points = re.findall(r'\\resumeItem\{(.*?)\}', bullet_section, re.DOTALL)

        return [bullet.strip() for bullet in bullet_points]


# Example usage
if __name__ == "__main__":
    parser = LatexResumeParser('resume.tex')
    print("Experience:", parser.experience)
    print("Education:", parser.education)
    print("Technical Skills:", parser.technical_skills)
