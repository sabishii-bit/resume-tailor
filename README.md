# Resume Tailor

`Resume Tailor` is a Python-based tool that tailors your LaTeX-based resume to fit job descriptions more effectively. It parses an existing LaTeX `.tex` resume, extracts relevant sections (such as experience, education, and technical skills), and reshapes them to align with keywords extracted from a given job description. The reshaped resume is then saved to a new `.tex` file, which can be converted to PDF using LaTeX tools.

This project leverages OpenAI's GPT model to rewrite resume sections to help ensure that your resume passes through Applicant Tracking Systems (ATS) and captures relevant keywords from job descriptions.

## Features

- **Keyword Extraction**: Extracts relevant keywords from job descriptions to match ATS filtering.
- **Resume Reshaping**: Automatically rewrites experience, education, and technical skills sections of your resume to align with job descriptions.
- **LaTeX Parsing & Updating**: Parses LaTeX `.tex` resumes and replaces sections with reshaped content.
- **Save & Compile**: Generates a new `.tex` file with tailored content and optional PDF generation.

## Requirements

To use this project, ensure that you have the following:

- Python 3.7 or higher
- An OpenAI API key
- LaTeX distribution installed (if you want to generate PDF from LaTeX, e.g., `MiKTeX` for Windows or `TeX Live` for other platforms)

### Python Libraries

This project requires several Python libraries. You can install them via `requirements.txt`:

```bash
pip install -r requirements.txt
```

Here’s a breakdown of the libraries used:

- `openai`: For interacting with the OpenAI API.
- `python-dotenv`: For loading environment variables like the OpenAI API key from a `.env` file.

## Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/resume-tailor.git
cd resume-tailor
```

### Step 2: Set Up OpenAI API Key

1. Create a `.env` file in the root directory.
2. Add your OpenAI API key to the `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Ensure LaTeX is Installed

If you want to convert `.tex` files to PDF, make sure you have a LaTeX distribution installed:

- **For Windows**: Install [MiKTeX](https://miktex.org/download).
- **For Linux/macOS**: Install [TeX Live](https://www.tug.org/texlive/).

## Usage

Run the main script `main.py` to start tailoring your resume:

```bash
python main.py
```

The program will prompt you for:
1. **Job Description**: Enter the full job description (paste it into the terminal).
2. **Path to Resume**: Provide the path to your existing LaTeX `.tex` resume file.

The script will then:
1. Parse your LaTeX resume.
2. Extract keywords from the provided job description.
3. Rewrite your resume's experience, education, and technical skills sections based on the job description.
4. Save the updated LaTeX resume as `updated_resume.tex`.

### Generating a PDF

If you have LaTeX installed and want to convert the updated `.tex` file to a `.pdf`, you can run:

```bash
python tex_to_pdf.py
```

This will generate a PDF version of your updated resume.

## File Structure

```
.
├── main.py               # Entry point of the project
├── resume_parser.py       # Contains the class to parse the LaTeX resume
├── resume_reshaper.py     # Uses OpenAI to reshape resume sections
├── resume_repackager.py   # Updates LaTeX resume with reshaped content
├── tex_to_pdf.py          # Optional script to convert .tex files to .pdf
├── .env                   # Contains your OpenAI API key (excluded from version control)
├── requirements.txt       # List of Python libraries required
└── README.md              # Project documentation
```

## Example

**Original Resume** (`resume.tex`):
```latex
\section{Experience}
\resumeSubHeadingListStart
    \resumeSubheading
      {Senior Developer}{June 2019 -- Present}
      {TechCorp}{San Francisco, CA}
      \resumeItemListStart
        \resumeItem{Developed high-performance applications using Python and Angular.}
        \resumeItem{Led a team of 5 engineers.}
      \resumeItemListEnd
\resumeSubHeadingListEnd
```

**Job Description**:
```
We are seeking a Senior Full-Stack Developer with expertise in Angular, AWS, Docker, and Python.
```

**Updated Resume** (`updated_resume.tex`):
```latex
\section{Experience}
\resumeSubHeadingListStart
    \resumeSubheading
      {Senior Developer}{June 2019 -- Present}
      {TechCorp}{San Francisco, CA}
      \resumeItemListStart
        \resumeItem{Developed scalable applications using Angular, Docker, and AWS.}
        \resumeItem{Led a team of 5 engineers, increasing project delivery speed by 20\%.}
        \resumeItem{Optimized CI/CD pipelines using AWS and Docker.}
      \resumeItemListEnd
\resumeSubHeadingListEnd
```

## License

This project is licensed under the MIT License.