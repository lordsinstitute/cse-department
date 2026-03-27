# B3 — Dynamic Web Based Resume Builder

A fully client-side resume builder that runs entirely in the browser. No server, no database, no installation needed — just open the HTML file and start building professional resumes.

## Project Structure

```
code/
├── index.html              # Main application (single-page)
├── css/
│   └── style.css           # Dark theme builder + light resume styles + 5 templates
├── js/
│   ├── app.js              # Core application logic (CRUD, preview, ATS, export, undo/redo, login)
│   └── ai-suggestions.js   # Claude API integration for AI content rewriting
├── README.md               # This file
└── PROJECT_EXPLANATION.md   # Detailed project explanation for viva
```

## Features

| Feature | Description |
|---|---|
| **Live Preview** | See your resume update in real-time as you type |
| **5 Templates** | Professional, Modern, Minimal, Creative, Executive — switch instantly |
| **7 Sections** | Personal Info, Experience, Education, Skills, Projects, Certifications, Awards |
| **ATS Scoring** | Applicant Tracking System compatibility checker (0-100%) |
| **Job Keyword Match** | Paste a job description to check keyword match percentage |
| **PDF Export** | Export resume as high-quality PDF using html2pdf.js |
| **JSON Import/Export** | Save and share resume data as JSON files |
| **Browser Storage** | Save/Load resume to browser's localStorage |
| **Collapsible Editor** | Toggle the editor panel for full-screen preview |
| **Zoom Controls** | Fit-to-screen or 100% zoom for the preview |
| **Dark Theme Builder** | Eye-friendly dark theme for the editing interface |
| **Responsive Design** | Works on desktop, tablet, and mobile |
| **Undo/Redo** | Undo and redo changes with Ctrl+Z / Ctrl+Y (max 50 states) |
| **Login System** | localStorage-based login with per-user resume data |
| **Delete Confirmation** | Modal confirmation before deleting any entry |
| **Reset Button** | Clear all resume data with confirmation dialog |
| **Progress Indicator** | Profile completeness bar showing how filled your resume is |
| **Spelling/Grammar Check** | Browser spellcheck + rule-based grammar warnings (passive voice, weak verbs) |
| **AI Content Rewriting** | Claude API integration for AI-powered content suggestions and rewriting |

## Technologies Used

| Technology | Purpose |
|---|---|
| HTML5 | Page structure and semantic markup |
| CSS3 | Styling, dark theme, 5 resume templates, print styles |
| JavaScript (ES6) | Application logic, DOM manipulation, CRUD, undo/redo, login |
| Bootstrap 5 | Responsive grid, components, modals, dark navbar |
| Bootstrap Icons | Icon library for UI elements |
| Google Fonts | Inter, Playfair Display, Roboto Mono fonts |
| html2pdf.js | Client-side PDF generation from HTML |
| localStorage API | Browser-based data persistence and user authentication |
| Claude API (Anthropic) | AI-powered content rewriting and suggestions |

## How to Run (Windows)

**Step 1:** Navigate to the project folder

```
Open File Explorer → Go to the B3/code/ folder
```

**Step 2:** Open the application

```
Double-click index.html
```

That's it! The application opens in your default web browser. No installation, no server, no commands needed.

### Alternative: Using Command Prompt

```bash
cd code
start index.html
```

### Alternative: Using Python HTTP Server (if CDN resources don't load)

```bash
cd code
python -m http.server 5003
```

Then open: `http://127.0.0.1:5003`

---

## Resume Sections

### 1. Personal Information
- First Name, Last Name
- Professional Title
- Email, Phone
- Location
- LinkedIn, GitHub, Portfolio Website
- Professional Summary (2-3 sentences)

### 2. Work Experience
- Company name, Position/Role
- Start Date, End Date (or "Current" checkbox)
- Description with bullet point support (lines starting with "- ")

### 3. Education
- School/University name
- Degree, Field of Study
- Start Date, End Date
- GPA
- Description (coursework, honors, activities)

### 4. Skills
- Skill name
- Proficiency level: Beginner, Intermediate, Advanced, Expert
- Displayed as skill bars on the resume

### 5. Projects
- Project name
- Technologies used
- Project link (GitHub, live URL)
- Description with bullet point support

### 6. Certifications
- Certification name
- Issuing organization
- Date obtained
- Credential ID

### 7. Awards & Achievements
- Award title
- Issuing organization
- Date
- Description

---

## Resume Templates

| Template | Style | Best For |
|---|---|---|
| **Professional** | Classic centered header, navy blue accents, underlined section titles | Corporate jobs, traditional industries |
| **Modern** | Gradient header banner, blue accents, left-bordered sections | Tech companies, startups, creative roles |
| **Minimal** | Serif name font, clean lines, minimal styling | Academic positions, minimalist preference |
| **Creative** | Two-column layout with teal sidebar for contact/skills, main content area | Designers, creatives, portfolio-style resumes |
| **Executive** | Bold dark header with gold accent lines, serif font, corporate feel | Senior roles, executives, management positions |

---

## ATS Compatibility Scoring

The ATS (Applicant Tracking System) scorer evaluates your resume on a 0-100% scale:

| Category | Max Points | Criteria |
|---|---|---|
| Personal Info | 30 | Full name (8), Email (7), Phone (7), Summary 30+ chars (8) |
| Experience | 20 | 2+ entries (12), Descriptions present (8) |
| Education | 15 | At least 1 entry (15) |
| Skills | 20 | 5+ skills (20), 3-4 skills (12), 1-2 skills (5) |
| Extras | 15 | Projects (5), Certifications (5), Awards (5) |

### Job Description Keyword Matching

Paste a job description in the ATS section → The tool compares keywords with your resume content and shows match percentage.

---

## Test Cases

### Test Case 1: Create a Complete Resume

1. Open `index.html` in browser
2. Fill in Personal Info:
   - First Name: `Rahul`
   - Last Name: `Sharma`
   - Title: `Full Stack Web Developer`
   - Email: `rahul.sharma@email.com`
   - Phone: `+91 98765 43210`
   - Location: `Hyderabad, India`
   - LinkedIn: `linkedin.com/in/rahulsharma`
   - GitHub: `github.com/rahulsharma`
   - Summary: `Passionate full stack developer with 3 years of experience building scalable web applications using React, Node.js, and Python.`

**Expected:** Live preview on the right shows the resume with name, title, contact info, and summary — updating in real-time as you type.

---

### Test Case 2: Add Work Experience

1. Click **Experience** tab
2. Click **+ Add** button
3. Fill in:
   - Company: `TCS (Tata Consultancy Services)`
   - Position: `Software Developer`
   - Start Date: `2022-06`
   - End Date: (leave empty) → Check **Current**
   - Description:
     ```
     - Developed RESTful APIs using Node.js and Express
     - Built responsive UIs with React and Bootstrap
     - Reduced page load time by 35% through lazy loading
     ```
4. Click **+ Add** again for a second entry:
   - Company: `Infosys`
   - Position: `Junior Developer Intern`
   - Start Date: `2021-06`
   - End Date: `2022-05`
   - Description:
     ```
     - Assisted in developing a customer portal using HTML, CSS, and JavaScript
     - Wrote unit tests using Jest achieving 85% code coverage
     ```

**Expected:** Preview shows "Work Experience" section with both entries. TCS shows "Jun 2022 — Present". Infosys shows "Jun 2021 — May 2022". Descriptions display as bullet-point lists.

---

### Test Case 3: Add Education

1. Click **Education** tab
2. Click **+ Add**
3. Fill in:
   - School: `Lords Institute of Engineering and Technology`
   - Degree: `B.Tech`
   - Field of Study: `Computer Science and Engineering`
   - Start Date: `2018-08`
   - End Date: `2022-06`
   - GPA: `8.5/10`
   - Description: `Relevant coursework: Data Structures, Algorithms, Web Development, DBMS, Machine Learning`

**Expected:** Preview shows "Education" section with school name, "B.Tech in Computer Science and Engineering | GPA: 8.5/10", date range, and coursework description.

---

### Test Case 4: Add Skills

1. Click **Skills** tab
2. Add these skills one by one using **+ Add**:
   - JavaScript → Advanced
   - Python → Advanced
   - React.js → Intermediate
   - Node.js → Intermediate
   - HTML/CSS → Expert
   - SQL → Intermediate
   - Git → Advanced

**Expected:** Preview shows "Skills" section with 7 skill bars. Expert skills show longer bars, Intermediate shorter. Each skill displays a progress bar.

---

### Test Case 5: Add Projects

1. Click **Projects** tab
2. Click **+ Add**
3. Fill in:
   - Project Name: `E-Commerce Platform`
   - Technologies: `React, Node.js, MongoDB, Stripe API`
   - Project Link: `https://github.com/rahulsharma/ecommerce`
   - Description:
     ```
     - Built a full-stack e-commerce platform with user authentication
     - Integrated Stripe payment gateway for secure transactions
     - Deployed on AWS EC2 with Nginx reverse proxy
     ```

**Expected:** Preview shows "Projects" section with project name, clickable [Link], technologies, and bullet-point description.

---

### Test Case 6: Add Certifications and Awards

1. Click **Certs** tab → Click **+ Add**
   - Name: `AWS Solutions Architect - Associate`
   - Issuer: `Amazon Web Services`
   - Date: `2023-03`
   - Credential ID: `AWS-SAA-C03-12345`

2. Click **Awards** tab → Click **+ Add**
   - Title: `Best Project Award`
   - Issuer: `Lords Institute of Engineering`
   - Date: `2022-04`
   - Description: `Awarded for developing an innovative ML-based attendance system`

**Expected:** Preview shows both "Certifications" and "Awards & Achievements" sections with all details.

---

### Test Case 7: Switch Templates

1. With a filled resume, click **Modern** template button
2. Observe the preview changes to a blue gradient header
3. Click **Minimal** template button
4. Observe the preview changes to a serif font, clean minimal design
5. Click **Professional** template button
6. Resume returns to the classic centered design

**Expected:** All three templates display the same content with different visual styles. Template switching is instant with no data loss.

---

### Test Case 8: ATS Score Check

1. Click **ATS** tab
2. With the full resume from Test Cases 1-6, observe the ATS score

**Expected:** ATS score should be **90-100%** (green). Checklist shows:
- Full name provided (green check)
- Email address provided (green check)
- Phone number provided (green check)
- Professional summary included (green check)
- 2 work experience entries (green check)
- All experiences have descriptions (green check)
- Education information provided (green check)
- 7 skills listed (excellent) (green check)
- 1 project(s) listed (green check)
- 1 certification(s) listed (green check)
- 1 award(s) listed (green check)

---

### Test Case 9: ATS Job Description Keyword Match

1. In the ATS section, paste this job description:
   ```
   We are looking for a Full Stack Developer with experience in React, Node.js, JavaScript, and Python.
   The candidate should have knowledge of REST APIs, MongoDB, and AWS cloud services.
   Strong problem-solving skills and experience with Git version control required.
   ```
2. Click **Re-analyze ATS Score**

**Expected:** A keyword match percentage appears (should be 50%+ showing "good" in green), because the resume contains matching keywords like React, Node.js, JavaScript, Python, REST, MongoDB, AWS, Git.

---

### Test Case 10: Save and Load from Browser

1. Click **Save** button in the navbar
2. See toast message: "Resume saved to browser storage!"
3. Close the browser tab
4. Re-open `index.html`
5. The resume auto-loads from saved data

**Expected:** All data (personal info, experience, education, skills, projects, certifications, awards) is restored exactly as saved. Template selection is also preserved.

---

### Test Case 11: Export and Import JSON

1. Click the **JSON export** button (download icon) in the navbar
2. A file like `Rahul_Sharma.json` downloads
3. Clear the resume (close and reopen without saving)
4. Click the **JSON import** button (upload icon)
5. Select the downloaded JSON file

**Expected:** All resume data is restored from the JSON file. Toast shows "Resume imported successfully!"

---

### Test Case 12: Export PDF

1. Click **Export PDF** button (yellow button in navbar)
2. Wait for PDF generation

**Expected:** A PDF file downloads (e.g., `Rahul_Sharma.pdf`). The PDF matches the live preview — proper formatting, fonts, layout. Toast shows "PDF exported successfully!"

---

### Test Case 13: Empty Resume Warning

1. Open a fresh `index.html` (clear localStorage first)
2. Click **Export PDF** without filling any data

**Expected:** Toast message: "Please fill in your resume before exporting." No PDF generated.

---

### Test Case 14: Collapsible Entries

1. Add 2+ experience entries
2. Click on the header of an experience card (e.g., "Software Developer")
3. The form fields collapse
4. Click again to expand

**Expected:** Entry cards toggle between expanded (showing all fields) and collapsed (showing only the title). Useful for managing multiple entries.

---

### Test Case 15: Toggle Editor and Zoom

1. Click the collapse button (sidebar icon) in the preview header
2. The editor panel hides, giving full-width preview
3. Click the sidebar icon again to bring editor back
4. Click **100%** zoom button
5. Preview shows at actual A4 size (may need scrolling)
6. Click **Fit** to auto-fit to screen

**Expected:** Editor toggles smoothly. Zoom switches between fit-to-window and actual size.

---

### Test Case 16: Delete Entries (with Confirmation)

1. Add 2 experience entries
2. Click the **trash** icon on the first entry
3. A confirmation modal appears: "Delete 'Software Developer at TCS'?"
4. Click **Delete** to confirm

**Expected:** Entry is removed only after confirmation. Preview updates instantly. Clicking "Cancel" keeps the entry intact.

---

### Test Case 17: Login and Registration

1. Open `index.html` in browser (clear localStorage first)
2. A login modal appears on page load
3. Click **Register** tab
4. Fill in: Name: `Rahul`, Username: `rahul`, Password: `pass123`
5. Click **Register** → Success message appears
6. Switch to **Login** tab → Enter `rahul` / `pass123` → Click **Login**
7. Navbar shows "Hi, Rahul" with a **Logout** button

**Expected:** Login modal appears on first visit. After registration and login, the modal closes. User name appears in navbar. Resume data is stored per-user.

---

### Test Case 18: Multi-User Data Isolation

1. Login as `rahul` → Fill personal info: First Name: `Rahul`, Last Name: `Sharma`
2. Click **Save** → Logout
3. Register a new user: Name: `Priya`, Username: `priya`, Password: `test123`
4. Login as `priya` → The resume is empty (no data from rahul)
5. Fill personal info: First Name: `Priya`, Last Name: `Patel`
6. Save → Logout → Login as `rahul` again

**Expected:** Rahul's data is intact (Rahul Sharma). Each user has completely separate resume data stored under different localStorage keys.

---

### Test Case 19: Switch to Creative Template

1. With a filled resume, click the **Creative** template button
2. Observe the two-column layout with teal sidebar

**Expected:** Preview changes to a two-column design — left sidebar (teal background) shows contact info and skills. Right main area shows experience, education, projects. All content is preserved.

---

### Test Case 20: Switch to Executive Template

1. Click the **Executive** template button
2. Observe the bold dark header with gold accents

**Expected:** Preview changes to a corporate executive style — dark background header with name and title, gold accent lines separating sections, serif fonts. All content is preserved.

---

### Test Case 21: Undo and Redo

1. Fill personal info: First Name: `Rahul`
2. Add an experience entry: Company: `TCS`
3. Press **Ctrl+Z** (or click the Undo button in navbar)
4. The experience entry is removed (undone)
5. Press **Ctrl+Z** again — personal info changes undo
6. Press **Ctrl+Y** (or click the Redo button) — changes come back

**Expected:** Undo reverts the last change. Redo restores it. Up to 50 states are tracked. Undo/Redo buttons are disabled when stacks are empty.

---

### Test Case 22: Undo/Redo Keyboard Shortcuts

1. Make several changes (add/edit entries)
2. Press **Ctrl+Z** multiple times — changes undo one by one
3. Press **Ctrl+Y** multiple times — changes redo one by one

**Expected:** Keyboard shortcuts work seamlessly. Each undo/redo updates the preview in real-time.

---

### Test Case 23: Spelling Check

1. Click **Experience** tab → Add entry
2. In the Description field, type: `Developd RESTful APIs and improvd performance`
3. Observe red underlines on misspelled words (`Developd`, `improvd`)

**Expected:** Browser's built-in spellcheck highlights misspelled words with red squiggly underlines. Right-clicking shows correction suggestions.

---

### Test Case 24: Grammar Check

1. Fill in experience descriptions with passive voice, e.g.: `The system was developed by the team`
2. Use weak action verbs, e.g.: `Was responsible for managing the project`
3. Click the **Check Grammar** button (or observe warnings on section tabs)

**Expected:** Grammar warnings appear for passive voice usage and weak verbs. Warning badges show on section tabs when issues are found. Suggestions recommend stronger action verbs.

---

### Test Case 25: Reset Resume Data

1. Fill in several sections with data
2. Click the **Reset** button (warning icon) in the navbar
3. A confirmation modal appears: "This will clear ALL resume data. This cannot be undone."
4. Click **Reset** to confirm

**Expected:** All resume data is cleared — personal info, experience, education, skills, projects, certifications, awards. Preview shows an empty resume. Toast confirms "Resume data has been reset."

---

### Test Case 26: Reset Cancellation

1. Fill in resume data
2. Click **Reset** button → Confirmation modal appears
3. Click **Cancel** (do not confirm)

**Expected:** No data is lost. Resume remains exactly as it was.

---

### Test Case 27: Profile Completeness Progress Bar

1. Open a fresh resume (after reset or new user)
2. Observe the progress bar below the template selector — shows low percentage (red)
3. Fill personal info (name, email, phone, summary) — progress increases
4. Add 1+ experience — progress increases more
5. Add 1+ education — continues increasing
6. Add 3+ skills — continues increasing
7. Add 1+ project — reaches high percentage (green)

**Expected:** Progress bar updates in real-time with each change. Color changes: red (<40%), yellow (40-70%), green (>70%). Percentage text shows exact completion. A fully filled resume reaches 90-100%.

---

### Test Case 28: AI Content Rewriting (Setup)

1. Click the **AI Settings** button (gear icon)
2. Enter a valid Claude API key from [console.anthropic.com](https://console.anthropic.com)
3. Click **Save**

**Expected:** API key is stored in localStorage. The settings modal shows "API key saved" confirmation. AI Suggest buttons become active on description fields.

---

### Test Case 29: AI Content Suggestion

1. Add an experience entry with a basic description:
   ```
   Worked on web applications. Fixed bugs. Helped with the team.
   ```
2. Click the **AI Suggest** button next to the description field
3. Wait for the AI response

**Expected:** A suggestion panel appears below the field with an improved version using stronger action verbs and quantified achievements (e.g., "Developed and maintained 5+ web applications..."). Shows "Accept" and "Reject" buttons.

---

### Test Case 30: AI Section Rewrite

1. Fill an entire experience section with multiple entries
2. Click **Rewrite Section** for the experience section
3. Wait for AI response

**Expected:** The AI rewrites the entire section with professional language, action verbs, and quantified impact. User can accept or reject the rewritten version.

---

### Test Case 31: AI Without API Key

1. Remove the Claude API key from settings (or use a fresh browser)
2. Click **AI Suggest** on any description field

**Expected:** A message prompts the user to set up their API key in AI Settings first. No API call is made.

---

## Notes

- This is a **100% client-side application** — no server, no database, no backend
- All data stays in your browser (localStorage) — nothing is sent to any server except AI suggestions (sent to Claude API only)
- Internet connection is needed for loading Bootstrap, fonts, html2pdf.js from CDN, and for AI features
- To use completely offline (without AI), download the CDN files locally
- Supported browsers: Chrome, Firefox, Edge, Safari (latest versions)
- The resume preview is designed for A4 paper size (210mm x 297mm)
- PDF export uses html2pdf.js library for high-quality output
- JSON export/import allows sharing resume data between computers
- Login system uses localStorage — each user's data is stored separately under `resumeforge_data_<username>`
- Undo/Redo tracks up to 50 state changes per session
- AI features require a Claude API key from [console.anthropic.com](https://console.anthropic.com)
- To reset everything, clear browser localStorage for this site
