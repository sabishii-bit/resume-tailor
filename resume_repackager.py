import re
from resume_parser import LatexResumeParser

class LatexResumeRepackager:
    def __init__(self, parser: LatexResumeParser):
        self.parser = parser
        self.original_content = self.parser.content

    def replace_experience(self, new_experience):
        # Repack the experience section by replacing the content between markers
        start = self.parser.markers['experience_start']
        end = self.parser.markers['experience_end']
        new_experience_content = self._generate_experience_content(new_experience)
        self.original_content = self.original_content[:start] + new_experience_content + self.original_content[end:]

    def replace_education(self, new_education):
        # Repack the education section by replacing the content between markers
        start = self.parser.markers['education_start']
        end = self.parser.markers['education_end']
        new_education_content = self._generate_education_content(new_education)
        self.original_content = self.original_content[:start] + new_education_content + self.original_content[end:]

    def replace_technical_skills(self, new_skills):
        """
        Find the \section{Technical Skills} tag, and replace the existing \textbf{} lines
        with new content while retaining the structure.
        """
        # Locate the position of the \section{Technical Skills}
        section_pattern = r'\\section\{Technical Skills\}'
        match = re.search(section_pattern, self.original_content)

        if match:
            # Extract everything from the end of \section{Technical Skills} to the end of the section
            start = match.end()

            # Now locate the end of the itemize block by finding where \end{itemize} occurs
            end_match = re.search(r'\\end\{itemize\}', self.original_content[start:])
            if not end_match:
                raise ValueError("Couldn't find the end of the Technical Skills section.")
            
            end = start + end_match.end()

            # Generate the new technical skills section content
            new_skills_content = self._generate_technical_skills_content(new_skills)

            # Replace the old technical skills section with the new content
            self.original_content = (
                self.original_content[:start] + new_skills_content + self.original_content[end:]
            )

    def _generate_technical_skills_content(self, skills):
        """
        Generate LaTeX formatted content for the technical skills section with all \textbf{}
        lines wrapped under a single \small{\item{...}} block.
        """
        skills_content = "\\begin{itemize}[leftmargin=0.15in, label={}]\n    \\small{\\item{\n"

        # Loop over each skill category and its corresponding skills
        for category, skill_list in skills.items():
            # Escape LaTeX special characters
            category_escaped = self._escape_latex_special_chars(category)
            skill_list_escaped = [self._escape_latex_special_chars(skill) for skill in skill_list]

            # Append the \textbf{category} and the list of skills in the format: \textbf{category}: {skills}
            skills_content += f"    \\textbf{{{category_escaped}}}{{: {', '.join(skill_list_escaped)}}} \\\\\n"

        # Close the \small and \item block
        skills_content += "    }}\n"
        
        # Close the itemize block
        skills_content += "\\end{itemize}\n"
        
        return skills_content

    def _escape_latex_special_chars(self, text):
        """Escape special LaTeX characters to prevent breaking the LaTeX syntax."""
        special_chars = {
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '&': r'\&',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
            '\\': r'\textbackslash{}'
        }
        return re.sub(r'([%$#&_{}~^\\])', lambda match: special_chars[match.group()], text)

    def save_to_file(self, output_path):
        """
        Ensure the document ends with \end{document} and save the modified LaTeX content to a file.
        """
        if not self.original_content.strip().endswith("\\end{document}"):
            self.original_content += "\n\\end{document}"

        # Save the modified LaTeX content to a file
        with open(output_path, 'w') as file:
            file.write(self.original_content)
    
    def _generate_experience_content(self, experience):
        """
        Generate LaTeX formatted content for the experience section.
        """
        experience_content = "\\resumeSubHeadingListStart\n"
        for entry in experience:
            # Escape LaTeX special characters
            job_title = self._escape_latex_special_chars(entry.get('job_title', ''))
            company = self._escape_latex_special_chars(entry.get('company', ''))
            location = self._escape_latex_special_chars(entry.get('location', ''))
            dates = self._escape_latex_special_chars(entry.get('dates', ''))

            # Add the formatted subheading (job title, company, dates)
            experience_content += f"\\resumeSubheading{{{job_title}}}{{{dates}}}{{{company}}}{{{location}}}\n"
            experience_content += "\\resumeItemListStart\n"

            # Add the bullet points for each experience entry
            for bullet in entry.get('bullet_points', []):
                bullet_escaped = self._escape_latex_special_chars(bullet)
                experience_content += f"\\resumeItem{{{bullet_escaped}}}\n"

            experience_content += "\\resumeItemListEnd\n"
        experience_content += "\\resumeSubHeadingListEnd\n"

        return experience_content



# Example usage
if __name__ == "__main__":
    parser = LatexResumeParser('resume.tex')
    repackager = LatexResumeRepackager(parser)

    # Example new skills to update
    new_skills = {
        'Languages': ['Java', 'Python', 'Rust', 'TypeScript'],
        'Developer Tools': ['Git', 'Docker', 'AWS', 'Kubernetes'],
        'Cloud Infrastructure & DevOps': ['AWS', 'Docker', 'CI/CD Pipelines'],
        'Full-Stack Development': ['Angular', 'Python', 'Scalable Web Applications']
    }

    # Replace the technical skills section and save it
    repackager.replace_technical_skills(new_skills)
    repackager.save_to_file('updated_resume.tex')
