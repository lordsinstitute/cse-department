/* ============================================
   ResumeForge — Dynamic Resume Builder
   Main Application JavaScript (FIXED)
   ============================================ */

// ==================== STATE ====================
let resumeData = {
    personal: {
        firstName: '', lastName: '', title: '', email: '', phone: '',
        location: '', linkedin: '', github: '', website: '', summary: ''
    },
    experience: [],
    education: [],
    skills: [],
    projects: [],
    certifications: [],
    awards: [],
    coverLetter: { content: '', generated: false }
};

let currentTemplate = 'professional';
let currentSection = 'personal';
let entryCounters = { experience: 0, education: 0, skills: 0, projects: 0, certifications: 0, awards: 0 };
let previewMode = 'resume'; // 'resume' or 'coverletter'

// ==================== DELETE CONFIRMATION STATE ====================
let pendingDelete = { section: null, id: null };

// ==================== UNDO / REDO STATE ====================
let undoStack = [];
let redoStack = [];
const maxUndoSteps = 50;

// ==================== SECTION NAVIGATION ====================
function showSection(section) {
    currentSection = section;
    document.querySelectorAll('.form-section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.section-tab').forEach(t => t.classList.remove('active'));
    document.getElementById('section-' + section).classList.add('active');
    document.querySelector(`.section-tab[data-section="${section}"]`).classList.add('active');
}

// ==================== TEMPLATE ====================
function setTemplate(template) {
    currentTemplate = template;
    document.querySelectorAll('.template-btn').forEach(b => b.classList.remove('active'));
    document.querySelector(`.template-btn[data-template="${template}"]`).classList.add('active');
    updatePreview();
}

// ==================== TOGGLE EDITOR ====================
function toggleEditor() {
    document.getElementById('editorPanel').classList.toggle('collapsed');
}

// ==================== TOGGLE PREVIEW ====================
function togglePreview() {
    const container = document.querySelector('.main-container');
    if (!container) return;
    container.classList.toggle('preview-hidden');
    const btn = document.getElementById('togglePreviewBtn');
    if (!btn) return;
    const icon = btn.querySelector('i');
    if (container.classList.contains('preview-hidden')) {
        icon.className = 'bi bi-layout-sidebar';
        btn.title = 'Show Preview';
    } else {
        icon.className = 'bi bi-layout-sidebar-inset';
        btn.title = 'Hide Preview';
        setZoom('fit');
    }
}

// ==================== ZOOM ====================
function setZoom(mode) {
    const page = document.getElementById('resumePage');
    const wrapper = document.getElementById('previewWrapper');
    document.getElementById('zoomFit').classList.remove('active');
    document.getElementById('zoom100').classList.remove('active');

    if (mode === 'fit') {
        const wrapperWidth = wrapper.clientWidth - 60;
        const pageWidth = 793;
        const scale = Math.min(wrapperWidth / pageWidth, 1);
        page.style.transform = `scale(${scale})`;
        document.getElementById('zoomFit').classList.add('active');
    } else {
        page.style.transform = 'scale(1)';
        document.getElementById('zoom100').classList.add('active');
    }
}

// ==================== PERSONAL INFO ====================
function getPersonalData() {
    return {
        firstName: document.getElementById('firstName').value.trim(),
        lastName: document.getElementById('lastName').value.trim(),
        title: document.getElementById('title').value.trim(),
        email: document.getElementById('email').value.trim(),
        phone: document.getElementById('phone').value.trim(),
        location: document.getElementById('location').value.trim(),
        linkedin: document.getElementById('linkedin').value.trim(),
        github: document.getElementById('github').value.trim(),
        website: document.getElementById('website').value.trim(),
        summary: document.getElementById('summary').value.trim()
    };
}

function setPersonalData(data) {
    document.getElementById('firstName').value = data.firstName || '';
    document.getElementById('lastName').value = data.lastName || '';
    document.getElementById('title').value = data.title || '';
    document.getElementById('email').value = data.email || '';
    document.getElementById('phone').value = data.phone || '';
    document.getElementById('location').value = data.location || '';
    document.getElementById('linkedin').value = data.linkedin || '';
    document.getElementById('github').value = data.github || '';
    document.getElementById('website').value = data.website || '';
    document.getElementById('summary').value = data.summary || '';
}

// ==================== DELETE CONFIRMATION ====================
function confirmDelete(section, id, name) {
    pendingDelete = { section, id };
    document.getElementById('deleteEntryName').textContent = `"${name}"`;
    const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
    modal.show();
}

function executeDelete() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('deleteModal'));
    if (modal) modal.hide();
    saveState();
    const { section, id } = pendingDelete;
    if (!section || id === null) return;
    switch (section) {
        case 'experience':
            resumeData.experience = resumeData.experience.filter(e => e.id !== id);
            renderExperienceList();
            break;
        case 'education':
            resumeData.education = resumeData.education.filter(e => e.id !== id);
            renderEducationList();
            break;
        case 'skills':
            resumeData.skills = resumeData.skills.filter(s => s.id !== id);
            renderSkillsList();
            break;
        case 'projects':
            resumeData.projects = resumeData.projects.filter(p => p.id !== id);
            renderProjectsList();
            break;
        case 'certifications':
            resumeData.certifications = resumeData.certifications.filter(c => c.id !== id);
            renderCertificationsList();
            break;
        case 'awards':
            resumeData.awards = resumeData.awards.filter(a => a.id !== id);
            renderAwardsList();
            break;
    }
    updatePreview();
    pendingDelete = { section: null, id: null };
}

// ==================== RESET ====================
function showResetModal() {
    const modal = new bootstrap.Modal(document.getElementById('resetModal'));
    modal.show();
}

function resetResume() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('resetModal'));
    if (modal) modal.hide();
    resumeData = {
        personal: { firstName: '', lastName: '', title: '', email: '', phone: '', location: '', linkedin: '', github: '', website: '', summary: '' },
        experience: [],
        education: [],
        skills: [],
        projects: [],
        certifications: [],
        awards: [],
        coverLetter: { content: '', generated: false }
    };
    entryCounters = { experience: 0, education: 0, skills: 0, projects: 0, certifications: 0, awards: 0 };
    undoStack = [];
    redoStack = [];
    updateUndoRedoButtons();
    setPersonalData(resumeData.personal);
    renderExperienceList();
    renderEducationList();
    renderSkillsList();
    renderProjectsList();
    renderCertificationsList();
    renderAwardsList();
    updatePreview();
    saveToLocal();
    showToast('Resume reset to blank state.', 'warning');
}

// ==================== UNDO / REDO ====================
function saveState() {
    const state = JSON.parse(JSON.stringify(resumeData));
    undoStack.push(state);
    if (undoStack.length > maxUndoSteps) undoStack.shift();
    redoStack = [];
    updateUndoRedoButtons();
}

function undo() {
    if (undoStack.length === 0) return;
    const currentState = JSON.parse(JSON.stringify(resumeData));
    redoStack.push(currentState);
    const prevState = undoStack.pop();
    restoreFromState(prevState);
    updateUndoRedoButtons();
    showToast('Undone.', 'info');
}

function redo() {
    if (redoStack.length === 0) return;
    const currentState = JSON.parse(JSON.stringify(resumeData));
    undoStack.push(currentState);
    const nextState = redoStack.pop();
    restoreFromState(nextState);
    updateUndoRedoButtons();
    showToast('Redone.', 'info');
}

function restoreFromState(state) {
    resumeData = JSON.parse(JSON.stringify(state));
    entryCounters.experience = resumeData.experience.length > 0 ? Math.max(...resumeData.experience.map(e => e.id)) : 0;
    entryCounters.education = resumeData.education.length > 0 ? Math.max(...resumeData.education.map(e => e.id)) : 0;
    entryCounters.skills = resumeData.skills.length > 0 ? Math.max(...resumeData.skills.map(s => s.id)) : 0;
    entryCounters.projects = resumeData.projects.length > 0 ? Math.max(...resumeData.projects.map(p => p.id)) : 0;
    entryCounters.certifications = resumeData.certifications.length > 0 ? Math.max(...resumeData.certifications.map(c => c.id)) : 0;
    entryCounters.awards = resumeData.awards.length > 0 ? Math.max(...resumeData.awards.map(a => a.id)) : 0;
    setPersonalData(resumeData.personal);
    renderExperienceList();
    renderEducationList();
    renderSkillsList();
    renderProjectsList();
    renderCertificationsList();
    renderAwardsList();
    updatePreview();
}

function updateUndoRedoButtons() {
    const undoBtn = document.getElementById('undoBtn');
    const redoBtn = document.getElementById('redoBtn');
    if (undoBtn) undoBtn.disabled = undoStack.length === 0;
    if (redoBtn) redoBtn.disabled = redoStack.length === 0;
}

// ==================== EXPERIENCE CRUD ====================
function addExperience(data) {
    saveState();
    const id = ++entryCounters.experience;
    const entry = data || { company: '', position: '', startDate: '', endDate: '', current: false, description: '' };
    resumeData.experience.push({ id, ...entry });
    renderExperienceList();
    updatePreview();
}

function removeExperience(id) {
    const entry = resumeData.experience.find(e => e.id === id);
    const name = entry ? (entry.position || entry.company || 'this experience') : 'this entry';
    confirmDelete('experience', id, name);
}

function updateExperience(id, field, value) {
    const entry = resumeData.experience.find(e => e.id === id);
    if (entry) {
        entry[field] = value;
        updatePreview();
    }
}

function renderExperienceList() {
    const container = document.getElementById('experienceList');
    const empty = document.getElementById('expEmpty');
    empty.style.display = resumeData.experience.length === 0 ? 'block' : 'none';
    container.innerHTML = resumeData.experience.map(exp => `
        <div class="entry-card expanded" id="exp-${exp.id}">
            <div class="entry-header" onclick="this.parentElement.classList.toggle('expanded')">
                <h6>${exp.position || exp.company || 'New Experience'}</h6>
                <div class="entry-actions">
                    <button class="btn-entry" onclick="event.stopPropagation(); this.closest('.entry-card').classList.toggle('expanded')">
                        <i class="bi bi-chevron-down"></i>
                    </button>
                    <button class="btn-entry delete" onclick="event.stopPropagation(); removeExperience(${exp.id})">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </div>
            <div class="entry-body">
                <div class="row g-2">
                    <div class="col-6"><label class="form-label small">Company *</label><input type="text" class="form-control form-control-sm" value="${escapeHTML(exp.company)}" oninput="updateExperience(${exp.id}, 'company', this.value)" placeholder="Google"></div>
                    <div class="col-6"><label class="form-label small">Position *</label><input type="text" class="form-control form-control-sm" value="${escapeHTML(exp.position)}" oninput="updateExperience(${exp.id}, 'position', this.value)" placeholder="Software Engineer"></div>
                    <div class="col-4"><label class="form-label small">Start Date</label><input type="month" class="form-control form-control-sm" value="${exp.startDate}" oninput="updateExperience(${exp.id}, 'startDate', this.value)"></div>
                    <div class="col-4"><label class="form-label small">End Date</label><input type="month" class="form-control form-control-sm" value="${exp.endDate}" ${exp.current ? 'disabled' : ''} oninput="updateExperience(${exp.id}, 'endDate', this.value)"></div>
                    <div class="col-4 d-flex align-items-end"><div class="form-check"><input class="form-check-input" type="checkbox" id="current-${exp.id}" ${exp.current ? 'checked' : ''} onchange="updateExperience(${exp.id}, 'current', this.checked); renderExperienceList();"><label class="form-check-label small" for="current-${exp.id}">Current</label></div></div>
                    <div class="col-12">
                        <div class="d-flex justify-content-between align-items-center mb-1"><label class="form-label small mb-0">Description (use bullet points with "- ")</label><button class="btn btn-xs btn-outline-warning ai-suggest-btn" onclick="triggerAISuggest('exp-desc-${exp.id}', 'experience')" title="AI Rewrite"><i class="bi bi-stars"></i> AI</button></div>
                        <textarea class="form-control form-control-sm" id="exp-desc-${exp.id}" rows="3" spellcheck="true" oninput="updateExperience(${exp.id}, 'description', this.value)" placeholder="- Led team of 5 developers&#10;- Improved API response time by 40%">${escapeHTML(exp.description)}</textarea>
                        <div class="ai-suggestion-panel d-none" id="ai-panel-exp-desc-${exp.id}"></div>
                        <div id="grammar-exp-desc-${exp.id}"></div>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// ==================== EDUCATION CRUD (similar structure, omitted for brevity but must be complete) ====================
function addEducation(data) { saveState(); const id = ++entryCounters.education; const entry = data || { school: '', degree: '', field: '', startDate: '', endDate: '', gpa: '', description: '' }; resumeData.education.push({ id, ...entry }); renderEducationList(); updatePreview(); }
function removeEducation(id) { const entry = resumeData.education.find(e => e.id === id); const name = entry ? (entry.school || entry.degree || 'this education entry') : 'this entry'; confirmDelete('education', id, name); }
function updateEducation(id, field, value) { const entry = resumeData.education.find(e => e.id === id); if (entry) { entry[field] = value; updatePreview(); } }
function renderEducationList() { const container = document.getElementById('educationList'); const empty = document.getElementById('eduEmpty'); empty.style.display = resumeData.education.length === 0 ? 'block' : 'none'; container.innerHTML = resumeData.education.map(edu => `<div class="entry-card expanded" id="edu-${edu.id}"><div class="entry-header" onclick="this.parentElement.classList.toggle('expanded')"><h6>${edu.school || edu.degree || 'New Education'}</h6><div class="entry-actions"><button class="btn-entry" onclick="event.stopPropagation(); this.closest('.entry-card').classList.toggle('expanded')"><i class="bi bi-chevron-down"></i></button><button class="btn-entry delete" onclick="event.stopPropagation(); removeEducation(${edu.id})"><i class="bi bi-trash"></i></button></div></div><div class="entry-body"><div class="row g-2"><div class="col-12"><label class="form-label small">School / University *</label><input type="text" class="form-control form-control-sm" value="${escapeHTML(edu.school)}" oninput="updateEducation(${edu.id}, 'school', this.value)" placeholder="MIT"></div><div class="col-6"><label class="form-label small">Degree *</label><input type="text" class="form-control form-control-sm" value="${escapeHTML(edu.degree)}" oninput="updateEducation(${edu.id}, 'degree', this.value)" placeholder="B.Tech"></div><div class="col-6"><label class="form-label small">Field of Study</label><input type="text" class="form-control form-control-sm" value="${escapeHTML(edu.field || '')}" oninput="updateEducation(${edu.id}, 'field', this.value)" placeholder="Computer Science"></div><div class="col-4"><label class="form-label small">Start Date</label><input type="month" class="form-control form-control-sm" value="${edu.startDate}" oninput="updateEducation(${edu.id}, 'startDate', this.value)"></div><div class="col-4"><label class="form-label small">End Date</label><input type="month" class="form-control form-control-sm" value="${edu.endDate}" oninput="updateEducation(${edu.id}, 'endDate', this.value)"></div><div class="col-4"><label class="form-label small">GPA</label><input type="text" class="form-control form-control-sm" value="${escapeHTML(edu.gpa || '')}" oninput="updateEducation(${edu.id}, 'gpa', this.value)" placeholder="8.5/10"></div><div class="col-12"><label class="form-label small">Description (optional)</label><textarea class="form-control form-control-sm" id="edu-desc-${edu.id}" rows="2" spellcheck="true" oninput="updateEducation(${edu.id}, 'description', this.value)" placeholder="Relevant coursework, honors, activities...">${escapeHTML(edu.description || '')}</textarea><div id="grammar-edu-desc-${edu.id}"></div></div></div></div></div>`).join(''); }

// ==================== SKILLS CRUD ====================
function addSkill(data) { saveState(); const id = ++entryCounters.skills; const entry = data || { name: '', level: 'Intermediate' }; resumeData.skills.push({ id, ...entry }); renderSkillsList(); updatePreview(); }
function removeSkill(id) { const entry = resumeData.skills.find(s => s.id === id); const name = entry ? (entry.name || 'this skill') : 'this skill'; confirmDelete('skills', id, name); }
function updateSkill(id, field, value) { const entry = resumeData.skills.find(s => s.id === id); if (entry) { entry[field] = value; updatePreview(); } }
function renderSkillsList() { const container = document.getElementById('skillsList'); const empty = document.getElementById('skillEmpty'); empty.style.display = resumeData.skills.length === 0 ? 'block' : 'none'; container.innerHTML = resumeData.skills.map(skill => `<div class="skill-entry" id="skill-${skill.id}"><input type="text" class="form-control form-control-sm" style="flex:2" value="${escapeHTML(skill.name)}" placeholder="e.g. JavaScript" oninput="updateSkill(${skill.id}, 'name', this.value)"><select class="form-select form-select-sm" style="flex:1" onchange="updateSkill(${skill.id}, 'level', this.value)"><option value="Beginner" ${skill.level === 'Beginner' ? 'selected' : ''}>Beginner</option><option value="Intermediate" ${skill.level === 'Intermediate' ? 'selected' : ''}>Intermediate</option><option value="Advanced" ${skill.level === 'Advanced' ? 'selected' : ''}>Advanced</option><option value="Expert" ${skill.level === 'Expert' ? 'selected' : ''}>Expert</option></select><button class="btn-entry delete" onclick="removeSkill(${skill.id})"><i class="bi bi-x-lg"></i></button></div>`).join(''); }

// ==================== PROJECTS CRUD ====================
function addProject(data) { saveState(); const id = ++entryCounters.projects; const entry = data || { name: '', description: '', technologies: '', link: '' }; resumeData.projects.push({ id, ...entry }); renderProjectsList(); updatePreview(); }
function removeProject(id) { const entry = resumeData.projects.find(p => p.id === id); const name = entry ? (entry.name || 'this project') : 'this project'; confirmDelete('projects', id, name); }
function updateProject(id, field, value) { const entry = resumeData.projects.find(p => p.id === id); if (entry) { entry[field] = value; updatePreview(); } }
function renderProjectsList() { const container = document.getElementById('projectsList'); const empty = document.getElementById('projEmpty'); empty.style.display = resumeData.projects.length === 0 ? 'block' : 'none'; container.innerHTML = resumeData.projects.map(proj => `<div class="entry-card expanded" id="proj-${proj.id}"><div class="entry-header" onclick="this.parentElement.classList.toggle('expanded')"><h6>${proj.name || 'New Project'}</h6><div class="entry-actions"><button class="btn-entry" onclick="event.stopPropagation(); this.closest('.entry-card').classList.toggle('expanded')"><i class="bi bi-chevron-down"></i></button><button class="btn-entry delete" onclick="event.stopPropagation(); removeProject(${proj.id})"><i class="bi bi-trash"></i></button></div></div><div class="entry-body"><div class="row g-2"><div class="col-12"><label class="form-label small">Project Name *</label><input type="text" class="form-control form-control-sm" value="${escapeHTML(proj.name)}" oninput="updateProject(${proj.id}, 'name', this.value)" placeholder="E-Commerce Platform"></div><div class="col-12"><label class="form-label small">Technologies Used</label><input type="text" class="form-control form-control-sm" value="${escapeHTML(proj.technologies)}" oninput="updateProject(${proj.id}, 'technologies', this.value)" placeholder="React, Node.js, MongoDB"></div><div class="col-12"><label class="form-label small">Project Link</label><input type="text" class="form-control form-control-sm" value="${escapeHTML(proj.link || '')}" oninput="updateProject(${proj.id}, 'link', this.value)" placeholder="https://github.com/..."></div><div class="col-12"><div class="d-flex justify-content-between align-items-center mb-1"><label class="form-label small mb-0">Description</label><button class="btn btn-xs btn-outline-warning ai-suggest-btn" onclick="triggerAISuggest('proj-desc-${proj.id}', 'project')" title="AI Rewrite"><i class="bi bi-stars"></i> AI</button></div><textarea class="form-control form-control-sm" id="proj-desc-${proj.id}" rows="3" spellcheck="true" oninput="updateProject(${proj.id}, 'description', this.value)" placeholder="- Built a full-stack e-commerce platform&#10;- Implemented payment gateway integration">${escapeHTML(proj.description)}</textarea><div class="ai-suggestion-panel d-none" id="ai-panel-proj-desc-${proj.id}"></div><div id="grammar-proj-desc-${proj.id}"></div></div></div></div></div>`).join(''); }

// ==================== CERTIFICATIONS CRUD ====================
function addCertification(data) { saveState(); const id = ++entryCounters.certifications; const entry = data || { name: '', issuer: '', date: '', credentialId: '' }; resumeData.certifications.push({ id, ...entry }); renderCertificationsList(); updatePreview(); }
function removeCertification(id) { const entry = resumeData.certifications.find(c => c.id === id); const name = entry ? (entry.name || 'this certification') : 'this certification'; confirmDelete('certifications', id, name); }
function updateCertification(id, field, value) { const entry = resumeData.certifications.find(c => c.id === id); if (entry) { entry[field] = value; updatePreview(); } }
function renderCertificationsList() { const container = document.getElementById('certificationsList'); const empty = document.getElementById('certEmpty'); empty.style.display = resumeData.certifications.length === 0 ? 'block' : 'none'; container.innerHTML = resumeData.certifications.map(cert => `<div class="entry-card expanded" id="cert-${cert.id}"><div class="entry-header" onclick="this.parentElement.classList.toggle('expanded')"><h6>${cert.name || 'New Certification'}</h6><div class="entry-actions"><button class="btn-entry" onclick="event.stopPropagation(); this.closest('.entry-card').classList.toggle('expanded')"><i class="bi bi-chevron-down"></i></button><button class="btn-entry delete" onclick="event.stopPropagation(); removeCertification(${cert.id})"><i class="bi bi-trash"></i></button></div></div><div class="entry-body"><div class="row g-2"><div class="col-12"><label class="form-label small">Certification Name *</label><input type="text" class="form-control form-control-sm" value="${escapeHTML(cert.name)}" oninput="updateCertification(${cert.id}, 'name', this.value)" placeholder="AWS Solutions Architect"></div><div class="col-6"><label class="form-label small">Issuing Organization</label><input type="text" class="form-control form-control-sm" value="${escapeHTML(cert.issuer)}" oninput="updateCertification(${cert.id}, 'issuer', this.value)" placeholder="Amazon Web Services"></div><div class="col-6"><label class="form-label small">Date Obtained</label><input type="month" class="form-control form-control-sm" value="${cert.date}" oninput="updateCertification(${cert.id}, 'date', this.value)"></div><div class="col-12"><label class="form-label small">Credential ID (optional)</label><input type="text" class="form-control form-control-sm" value="${escapeHTML(cert.credentialId || '')}" oninput="updateCertification(${cert.id}, 'credentialId', this.value)" placeholder="ABC-12345"></div></div></div></div>`).join(''); }

// ==================== AWARDS CRUD ====================
function addAward(data) { saveState(); const id = ++entryCounters.awards; const entry = data || { title: '', issuer: '', date: '', description: '' }; resumeData.awards.push({ id, ...entry }); renderAwardsList(); updatePreview(); }
function removeAward(id) { const entry = resumeData.awards.find(a => a.id === id); const name = entry ? (entry.title || 'this award') : 'this award'; confirmDelete('awards', id, name); }
function updateAward(id, field, value) { const entry = resumeData.awards.find(a => a.id === id); if (entry) { entry[field] = value; updatePreview(); } }
function renderAwardsList() { const container = document.getElementById('awardsList'); const empty = document.getElementById('awardEmpty'); empty.style.display = resumeData.awards.length === 0 ? 'block' : 'none'; container.innerHTML = resumeData.awards.map(award => `<div class="entry-card expanded" id="award-${award.id}"><div class="entry-header" onclick="this.parentElement.classList.toggle('expanded')"><h6>${award.title || 'New Award'}</h6><div class="entry-actions"><button class="btn-entry" onclick="event.stopPropagation(); this.closest('.entry-card').classList.toggle('expanded')"><i class="bi bi-chevron-down"></i></button><button class="btn-entry delete" onclick="event.stopPropagation(); removeAward(${award.id})"><i class="bi bi-trash"></i></button></div></div><div class="entry-body"><div class="row g-2"><div class="col-12"><label class="form-label small">Award Title *</label><input type="text" class="form-control form-control-sm" value="${escapeHTML(award.title)}" oninput="updateAward(${award.id}, 'title', this.value)" placeholder="Best Paper Award"></div><div class="col-6"><label class="form-label small">Issuing Organization</label><input type="text" class="form-control form-control-sm" value="${escapeHTML(award.issuer)}" oninput="updateAward(${award.id}, 'issuer', this.value)" placeholder="IEEE"></div><div class="col-6"><label class="form-label small">Date</label><input type="month" class="form-control form-control-sm" value="${award.date}" oninput="updateAward(${award.id}, 'date', this.value)"></div><div class="col-12"><label class="form-label small">Description (optional)</label><textarea class="form-control form-control-sm" id="award-desc-${award.id}" rows="2" spellcheck="true" oninput="updateAward(${award.id}, 'description', this.value)" placeholder="Brief description of the award...">${escapeHTML(award.description || '')}</textarea><div id="grammar-award-desc-${award.id}"></div></div></div></div></div>`).join(''); }

// ==================== PROFILE COMPLETENESS ====================
function calculateProgress() {
    const p = resumeData.personal;
    let percent = 0;
    if (p.firstName && p.lastName) percent += 10;
    if (p.email) percent += 5;
    if (p.phone) percent += 5;
    if (p.summary) percent += 10;
    if (resumeData.experience.length >= 1) percent += 20;
    if (resumeData.education.length >= 1) percent += 15;
    if (resumeData.skills.filter(s => s.name).length >= 3) percent += 15;
    if (resumeData.projects.length >= 1) percent += 10;
    if (p.title) percent += 5;
    if (p.location) percent += 5;
    return percent;
}

function updateProgress() {
    const percent = calculateProgress();
    const bar = document.getElementById('progressBar');
    const label = document.getElementById('progressPercent');
    const textLabel = document.getElementById('progressLabel');
    if (!bar) return;
    bar.style.width = percent + '%';
    bar.setAttribute('aria-valuenow', percent);
    label.textContent = percent + '%';
    if (percent < 40) {
        bar.style.background = '#e74c3c';
        textLabel.textContent = 'Keep going — add more details!';
        textLabel.style.color = '#e74c3c';
    } else if (percent <= 70) {
        bar.style.background = '#ffc107';
        textLabel.textContent = 'Good progress — almost there!';
        textLabel.style.color = '#ffc107';
    } else {
        bar.style.background = '#2ecc71';
        textLabel.textContent = 'Excellent! Your profile looks complete.';
        textLabel.style.color = '#2ecc71';
    }
}

// ==================== PREVIEW MODE (global) ====================
function setPreviewMode(mode) {
    previewMode = mode;
    const resumeBtn = document.getElementById('previewModeResume');
    const coverBtn = document.getElementById('previewModeCover');
    if (resumeBtn && coverBtn) {
        if (mode === 'resume') {
            resumeBtn.classList.add('active');
            coverBtn.classList.remove('active');
        } else {
            resumeBtn.classList.remove('active');
            coverBtn.classList.add('active');
        }
    }
    updatePreview();
}

function renderCoverLetter() {
    const page = document.getElementById('resumePage');
    const p = resumeData.personal;
    let content = resumeData.coverLetter ? resumeData.coverLetter.content : '';
    if (content) {
        content = content.replace(/\\([()])/g, '$1'); // remove backslashes
    }
    
    if (!content || content.trim() === '') {
        page.innerHTML = `<div class="resume-empty-state"><i class="bi bi-envelope-paper" style="font-size: 3rem;"></i><h5 class="mt-3">No Cover Letter Yet</h5><p>Go to ATS tab → "Generate Cover Letter" to create one.</p></div>`;
        return;
    }
    
    const today = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    const fullName = `${p.firstName} ${p.lastName}`.trim();
    const cleanName = fullName.replace(/^#\s*/, ''); // remove any stray '#'
    const address = p.location || '';
    const email = p.email || '';
    const phone = p.phone || '';
    
    // Use the special business‑letter class (no resume template styling)
    page.className = 'resume-page cover-letter-only';
    
    let html = `
        <div class="resume-header">
            <div class="resume-name">${escapeHTML(cleanName)}</div>
            <div class="resume-contact">${email} ${phone ? '| ' + phone : ''} ${address ? '| ' + address : ''}</div>
        </div>
        <div class="cover-date">${today}</div>
        <div class="resume-summary" style="white-space: pre-wrap; line-height: 1.5;">${escapeHTML(content)}</div>
        <div class="cover-signature">
            Sincerely,<br>
            ${escapeHTML(cleanName)}
        </div>
    `;
    page.innerHTML = html;
}

// ==================== COVER LETTER EDITING ====================
function editCoverLetter() {
    const editor = document.getElementById('coverLetterEditor');
    if (editor) editor.value = resumeData.coverLetter.content || '';
    const modal = new bootstrap.Modal(document.getElementById('coverLetterEditModal'));
    modal.show();
}

function acceptCoverLetterChanges() {
    const newContent = document.getElementById('coverLetterEditor').value;
    resumeData.coverLetter.content = newContent;
    resumeData.coverLetter.generated = true;
    updatePreview();
    showToast('Cover letter updated.', 'success');
    bootstrap.Modal.getInstance(document.getElementById('coverLetterEditModal')).hide();
}

function dismissCoverLetterChanges() {
    bootstrap.Modal.getInstance(document.getElementById('coverLetterEditModal')).hide();
}

function exportCoverLetterPDF() {
    if (!resumeData.coverLetter.content || resumeData.coverLetter.content.trim() === '') {
        showToast('No cover letter to export.', 'warning');
        return;
    }
    const originalMode = previewMode;
    setPreviewMode('coverletter');
    setTimeout(() => {
        const element = document.getElementById('resumePage');
        const opt = { margin: 0, filename: `${resumeData.personal.firstName || 'CoverLetter'}_${resumeData.personal.lastName || ''}.pdf`, image: { type: 'jpeg', quality: 0.98 }, html2canvas: { scale: 2 }, jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' } };
        html2pdf().set(opt).from(element).save().then(() => { setPreviewMode(originalMode); showToast('Cover letter PDF exported!', 'success'); }).catch(() => { setPreviewMode(originalMode); showToast('PDF export failed.', 'danger'); });
    }, 100);
}

// ==================== LIVE PREVIEW ====================
function updatePreview() {
    resumeData.personal = getPersonalData();
    if (previewMode === 'coverletter') {
        renderCoverLetter();
        return;
    }
    const page = document.getElementById('resumePage');
    const p = resumeData.personal;
    // Clean summary text (remove backslashes before parentheses)
    let cleanedSummary = p.summary;
    if (cleanedSummary) {
        cleanedSummary = cleanedSummary.replace(/\\([()])/g, '$1');
    }
    const hasContent = p.firstName || p.lastName || resumeData.experience.length > 0 || resumeData.education.length > 0 || resumeData.skills.length > 0;
    updateProgress();
    if (!hasContent) {
        page.className = 'resume-page';
        page.innerHTML = `<div class="resume-empty-state"><i class="bi bi-file-earmark-person" style="font-size: 3rem; color: #666;"></i><h5 class="mt-3 text-muted">Your Resume Preview</h5><p class="text-muted small">Start filling in the form on the left to see your resume come alive!</p></div>`;
        return;
    }
    page.className = `resume-page ${currentTemplate}`;
    let html = '';
    const fullName = `${p.firstName} ${p.lastName}`.trim();
    const contacts = [];
    if (p.email) contacts.push(`<span>${p.email}</span>`);
    if (p.phone) contacts.push(`<span>${p.phone}</span>`);
    if (p.location) contacts.push(`<span>${p.location}</span>`);
    if (p.linkedin) contacts.push(`<span>${p.linkedin}</span>`);
    if (p.github) contacts.push(`<span>${p.github}</span>`);
    if (p.website) contacts.push(`<span>${p.website}</span>`);
    html = '<div class="resume-header">';
    if (fullName) html += `<div class="resume-name">${escapeHTML(fullName)}</div>`;
    if (p.title) html += `<div class="resume-title">${escapeHTML(p.title)}</div>`;
    if (contacts.length > 0) html += `<div class="resume-contact">${contacts.join(' <span>|</span> ')}</div>`;
    html += '</div>';
    if (cleanedSummary) { html += `<div class="resume-section-title">Professional Summary</div><div class="resume-summary">${escapeHTML(cleanedSummary)}</div>`; }
    if (resumeData.experience.length > 0) {
        const validExp = resumeData.experience.filter(e => e.company || e.position);
        if (validExp.length > 0) {
            html += `<div class="resume-section-title">Work Experience</div>`;
            validExp.forEach(exp => {
                const dateStr = formatDateRange(exp.startDate, exp.endDate, exp.current);
                html += `<div class="resume-entry"><div class="resume-entry-header"><div><div class="resume-entry-title">${escapeHTML(exp.position)}</div><div class="resume-entry-subtitle">${escapeHTML(exp.company)}</div></div><div class="resume-entry-date">${dateStr}</div></div>${exp.description ? `<div class="resume-entry-desc">${formatDescription(exp.description)}</div>` : ''}</div>`;
            });
        }
    }
    if (resumeData.education.length > 0) {
        const validEdu = resumeData.education.filter(e => e.school || e.degree);
        if (validEdu.length > 0) {
            html += `<div class="resume-section-title">Education</div>`;
            validEdu.forEach(edu => {
                const dateStr = formatDateRange(edu.startDate, edu.endDate);
                const degreeField = [edu.degree, edu.field].filter(Boolean).join(' in ');
                html += `<div class="resume-entry"><div class="resume-entry-header"><div><div class="resume-entry-title">${escapeHTML(edu.school)}</div><div class="resume-entry-subtitle">${escapeHTML(degreeField)}${edu.gpa ? ` | GPA: ${escapeHTML(edu.gpa)}` : ''}</div></div><div class="resume-entry-date">${dateStr}</div></div>${edu.description ? `<div class="resume-entry-desc">${formatDescription(edu.description)}</div>` : ''}</div>`;
            });
        }
    }
    if (resumeData.skills.length > 0) {
        const validSkills = resumeData.skills.filter(s => s.name);
        if (validSkills.length > 0) {
            html += `<div class="resume-section-title">Skills</div>`;
            if (currentTemplate === 'creative') {
                html += `<div class="resume-skills-tags">`;
                validSkills.forEach(skill => { html += `<span class="resume-skill-tag-creative">${escapeHTML(skill.name)} <em>${skill.level}</em></span>`; });
                html += `</div>`;
            } else {
                html += `<div style="display: flex; flex-wrap: wrap; gap: 4px 0;">`;
                validSkills.forEach(skill => {
                    const levelPercent = { 'Beginner': 25, 'Intermediate': 50, 'Advanced': 75, 'Expert': 95 }[skill.level] || 50;
                    html += `<div class="resume-skill-item"><span style="font-size: 9pt; min-width: 80px;">${escapeHTML(skill.name)}</span><div class="resume-skill-bar"><div class="resume-skill-fill" style="width: ${levelPercent}%"></div></div></div>`;
                });
                html += `</div>`;
            }
        }
    }
    if (resumeData.projects.length > 0) {
        const validProj = resumeData.projects.filter(p => p.name);
        if (validProj.length > 0) {
            html += `<div class="resume-section-title">Projects</div>`;
            validProj.forEach(proj => { html += `<div class="resume-entry"><div class="resume-entry-title">${escapeHTML(proj.name)}${proj.link ? ` <a class="resume-link" href="${escapeHTML(proj.link)}" target="_blank">[Link]</a>` : ''}</div>${proj.technologies ? `<div class="resume-entry-subtitle">${escapeHTML(proj.technologies)}</div>` : ''}${proj.description ? `<div class="resume-entry-desc">${formatDescription(proj.description)}</div>` : ''}</div>`; });
        }
    }
    if (resumeData.certifications.length > 0) {
        const validCerts = resumeData.certifications.filter(c => c.name);
        if (validCerts.length > 0) {
            html += `<div class="resume-section-title">Certifications</div>`;
            validCerts.forEach(cert => { const dateStr = cert.date ? formatMonth(cert.date) : ''; html += `<div class="resume-entry"><div class="resume-entry-header"><div><div class="resume-entry-title">${escapeHTML(cert.name)}</div>${cert.issuer ? `<div class="resume-entry-subtitle">${escapeHTML(cert.issuer)}${cert.credentialId ? ` — ID: ${escapeHTML(cert.credentialId)}` : ''}</div>` : ''}</div>${dateStr ? `<div class="resume-entry-date">${dateStr}</div>` : ''}</div></div>`; });
        }
    }
    if (resumeData.awards.length > 0) {
        const validAwards = resumeData.awards.filter(a => a.title);
        if (validAwards.length > 0) {
            html += `<div class="resume-section-title">Awards & Achievements</div>`;
            validAwards.forEach(award => { const dateStr = award.date ? formatMonth(award.date) : ''; html += `<div class="resume-entry"><div class="resume-entry-header"><div><div class="resume-entry-title">${escapeHTML(award.title)}</div>${award.issuer ? `<div class="resume-entry-subtitle">${escapeHTML(award.issuer)}</div>` : ''}</div>${dateStr ? `<div class="resume-entry-date">${dateStr}</div>` : ''}</div>${award.description ? `<div class="resume-entry-desc">${escapeHTML(award.description)}</div>` : ''}</div>`; });
        }
    }
    page.innerHTML = html;
    calculateATS();
}

// ==================== ATS SCORING ====================
function calculateATS() {
    const p = resumeData.personal;
    let score = 0, maxScore = 0;
    const checks = [];
    maxScore += 30;
    if (p.firstName && p.lastName) { score += 8; checks.push({ text: 'Full name provided', pass: true }); } else { checks.push({ text: 'Full name missing', pass: false }); }
    if (p.email) { score += 7; checks.push({ text: 'Email address provided', pass: true }); } else { checks.push({ text: 'Email address missing', pass: false }); }
    if (p.phone) { score += 7; checks.push({ text: 'Phone number provided', pass: true }); } else { checks.push({ text: 'Phone number missing', pass: false }); }
    if (p.summary && p.summary.length >= 30) { score += 8; checks.push({ text: 'Professional summary included', pass: true }); } else if (p.summary) { checks.push({ text: 'Summary too short (30+ chars recommended)', pass: 'warn' }); score += 3; } else { checks.push({ text: 'Professional summary missing', pass: false }); }
    maxScore += 20;
    const validExp = resumeData.experience.filter(e => e.company && e.position);
    if (validExp.length >= 2) { score += 12; checks.push({ text: `${validExp.length} work experience entries`, pass: true }); } else if (validExp.length === 1) { score += 6; checks.push({ text: '1 experience entry (2+ recommended)', pass: 'warn' }); } else { checks.push({ text: 'No work experience added', pass: false }); }
    const expWithDesc = validExp.filter(e => e.description && e.description.length > 20);
    if (expWithDesc.length === validExp.length && validExp.length > 0) { score += 8; checks.push({ text: 'All experiences have descriptions', pass: true }); } else if (expWithDesc.length > 0) { score += 4; checks.push({ text: 'Some experiences lack descriptions', pass: 'warn' }); } else if (validExp.length > 0) { checks.push({ text: 'Experience descriptions missing', pass: false }); }
    maxScore += 15;
    const validEdu = resumeData.education.filter(e => e.school && e.degree);
    if (validEdu.length >= 1) { score += 15; checks.push({ text: 'Education information provided', pass: true }); } else { checks.push({ text: 'No education added', pass: false }); }
    maxScore += 20;
    const validSkills = resumeData.skills.filter(s => s.name);
    if (validSkills.length >= 5) { score += 20; checks.push({ text: `${validSkills.length} skills listed (excellent)`, pass: true }); } else if (validSkills.length >= 3) { score += 12; checks.push({ text: `${validSkills.length} skills listed (5+ recommended)`, pass: 'warn' }); } else if (validSkills.length >= 1) { score += 5; checks.push({ text: `Only ${validSkills.length} skill(s) listed`, pass: 'warn' }); } else { checks.push({ text: 'No skills added', pass: false }); }
    maxScore += 15;
    let extraScore = 0;
    const validProj = resumeData.projects.filter(p => p.name);
    const validCerts = resumeData.certifications.filter(c => c.name);
    const validAwards = resumeData.awards.filter(a => a.title);
    if (validProj.length > 0) { extraScore += 5; checks.push({ text: `${validProj.length} project(s) listed`, pass: true }); }
    if (validCerts.length > 0) { extraScore += 5; checks.push({ text: `${validCerts.length} certification(s) listed`, pass: true }); }
    if (validAwards.length > 0) { extraScore += 5; checks.push({ text: `${validAwards.length} award(s) listed`, pass: true }); }
    if (extraScore === 0) { checks.push({ text: 'No projects, certs, or awards', pass: 'warn' }); }
    score += Math.min(extraScore, 15);
    const jobDescEl = document.getElementById('jobDescription');
    const jobDesc = jobDescEl ? jobDescEl.value.trim().toLowerCase() : '';
    if (jobDesc) {
        const words = jobDesc.split(/\s+/).filter(w => w.length > 3);
        const uniqueWords = [...new Set(words)];
        const resumeText = JSON.stringify(resumeData).toLowerCase();
        let matched = 0;
        uniqueWords.forEach(word => { if (resumeText.includes(word)) matched++; });
        const matchPercent = uniqueWords.length > 0 ? Math.round((matched / uniqueWords.length) * 100) : 0;
        if (matchPercent >= 50) checks.push({ text: `Job keyword match: ${matchPercent}% (good)`, pass: true });
        else if (matchPercent >= 25) checks.push({ text: `Job keyword match: ${matchPercent}% (improve)`, pass: 'warn' });
        else checks.push({ text: `Job keyword match: ${matchPercent}% (low)`, pass: false });
    }
    const finalScore = maxScore > 0 ? Math.round((score / maxScore) * 100) : 0;
    updateATSDisplay(finalScore, checks);
}

function updateATSDisplay(score, checks) {
    document.getElementById('atsScoreNav').textContent = score + '%';
    document.getElementById('atsScoreValue').textContent = score;
    const circle = document.getElementById('atsCircle');
    const circumference = 2 * Math.PI * 54;
    const offset = circumference - (score / 100) * circumference;
    circle.style.strokeDashoffset = offset;
    let color = '#e74c3c';
    if (score >= 80) color = '#2ecc71';
    else if (score >= 50) color = '#ffc107';
    circle.style.stroke = color;
    const badge = document.getElementById('atsBadge');
    badge.style.borderColor = color;
    badge.style.color = color;
    const details = document.getElementById('atsDetails');
    details.innerHTML = checks.map(check => { const cls = check.pass === true ? 'pass' : check.pass === 'warn' ? 'warn' : 'fail'; const icon = check.pass === true ? 'bi-check-circle-fill' : check.pass === 'warn' ? 'bi-exclamation-circle-fill' : 'bi-x-circle-fill'; return `<div class="ats-item ${cls}"><i class="bi ${icon} ats-icon"></i><span>${check.text}</span></div>`; }).join('');
}

// ==================== GRAMMAR / SPELLING CHECK ====================
function checkGrammar() {
    const issues = [];
    const weakPhrases = [{ pattern: /\bwas responsible for\b/gi, suggestion: 'Use active verb like "led", "managed", "owned"' }, { pattern: /\bhelped with\b/gi, suggestion: 'Replace with specific action like "contributed to", "collaborated on"' }, { pattern: /\bworked on\b/gi, suggestion: 'Be specific: "developed", "built", "designed", "implemented"' }, { pattern: /\bwas involved in\b/gi, suggestion: 'Replace with active verb: "participated in", "contributed to"' }, { pattern: /\bassisted with\b/gi, suggestion: 'Be more specific: "supported", "facilitated", "enabled"' }, { pattern: /\bresponsible for\b/gi, suggestion: 'Use action verb instead: "managed", "led", "oversaw"' }];
    const firstPersonPatterns = [{ pattern: /\b(I|my|me|myself)\b/gi, suggestion: 'Remove first-person pronouns from resume bullet points' }];
    const textFields = [];
    const summaryVal = document.getElementById('summary') ? document.getElementById('summary').value : '';
    if (summaryVal) textFields.push({ id: 'summary', label: 'Summary', text: summaryVal });
    resumeData.experience.forEach(exp => { if (exp.description) textFields.push({ id: `exp-desc-${exp.id}`, label: `Experience: ${exp.position || exp.company}`, text: exp.description }); });
    resumeData.education.forEach(edu => { if (edu.description) textFields.push({ id: `edu-desc-${edu.id}`, label: `Education: ${edu.school}`, text: edu.description }); });
    resumeData.projects.forEach(proj => { if (proj.description) textFields.push({ id: `proj-desc-${proj.id}`, label: `Project: ${proj.name}`, text: proj.description }); });
    resumeData.awards.forEach(award => { if (award.description) textFields.push({ id: `award-desc-${award.id}`, label: `Award: ${award.title}`, text: award.description }); });
    textFields.forEach(field => {
        const fieldIssues = [];
        const hasNumbers = /\d/.test(field.text);
        if (!hasNumbers && field.text.length > 30) fieldIssues.push({ issue: 'Missing quantification', suggestion: 'Add numbers/metrics (e.g., "improved performance by 30%")' });
        weakPhrases.forEach(({ pattern, suggestion }) => { if (pattern.test(field.text)) { pattern.lastIndex = 0; fieldIssues.push({ issue: 'Weak/passive phrase detected', suggestion }); } });
        firstPersonPatterns.forEach(({ pattern, suggestion }) => { if (pattern.test(field.text)) { pattern.lastIndex = 0; fieldIssues.push({ issue: 'First-person pronoun found', suggestion }); } });
        if (fieldIssues.length > 0) issues.push({ field: field.id, label: field.label, issues: fieldIssues });
    });
    return issues;
}

function checkGrammarSection(section) {
    const allIssues = checkGrammar();
    document.querySelectorAll('[id^="grammar-"]').forEach(el => { el.innerHTML = ''; });
    if (allIssues.length === 0) { showToast('Writing looks great! No issues found.', 'success'); return; }
    allIssues.forEach(({ field, label, issues }) => { const container = document.getElementById('grammar-' + field); if (container) { container.innerHTML = issues.map(i => `<div class="grammar-warning"><i class="bi bi-exclamation-triangle-fill me-1"></i><strong>${i.issue}:</strong> ${i.suggestion}</div>`).join(''); } });
    showToast(`Found ${allIssues.reduce((t, i) => t + i.issues.length, 0)} writing suggestion(s). Check below each field.`, 'warning');
}

// ==================== AUTH SYSTEM ====================
function checkAuth() {
    const currentUser = localStorage.getItem('resumeforge_current_user');
    if (!currentUser) { const modal = new bootstrap.Modal(document.getElementById('loginModal')); modal.show(); }
    else { updateUserDisplay(currentUser); loadFromLocal(); }
}

function switchAuthTab(tab) {
    document.getElementById('loginForm').style.display = tab === 'login' ? 'block' : 'none';
    document.getElementById('registerForm').style.display = tab === 'register' ? 'block' : 'none';
    document.getElementById('loginTabBtn').classList.toggle('active', tab === 'login');
    document.getElementById('registerTabBtn').classList.toggle('active', tab === 'register');
    document.getElementById('loginError').classList.add('d-none');
    document.getElementById('registerError').classList.add('d-none');
}

function loginUser() {
    const username = document.getElementById('loginUsername').value.trim();
    const password = document.getElementById('loginPassword').value;
    const errEl = document.getElementById('loginError');
    if (!username || !password) { errEl.textContent = 'Please enter username and password.'; errEl.classList.remove('d-none'); return; }
    const users = JSON.parse(localStorage.getItem('resumeforge_users') || '[]');
    const user = users.find(u => u.username === username && u.password === password);
    if (!user) { errEl.textContent = 'Invalid username or password.'; errEl.classList.remove('d-none'); return; }
    localStorage.setItem('resumeforge_current_user', username);
    const modal = bootstrap.Modal.getInstance(document.getElementById('loginModal'));
    if (modal) modal.hide();
    updateUserDisplay(username);
    loadFromLocal();
    showToast(`Welcome back, ${user.name || username}!`, 'success');
}

function registerUser() {
    const name = document.getElementById('registerName').value.trim();
    const username = document.getElementById('registerUsername').value.trim();
    const password = document.getElementById('registerPassword').value;
    const errEl = document.getElementById('registerError');
    if (!username || !password) { errEl.textContent = 'Username and password are required.'; errEl.classList.remove('d-none'); return; }
    if (username.length < 3) { errEl.textContent = 'Username must be at least 3 characters.'; errEl.classList.remove('d-none'); return; }
    if (password.length < 4) { errEl.textContent = 'Password must be at least 4 characters.'; errEl.classList.remove('d-none'); return; }
    const users = JSON.parse(localStorage.getItem('resumeforge_users') || '[]');
    if (users.find(u => u.username === username)) { errEl.textContent = 'Username already taken. Choose another.'; errEl.classList.remove('d-none'); return; }
    users.push({ username, password, name });
    localStorage.setItem('resumeforge_users', JSON.stringify(users));
    localStorage.setItem('resumeforge_current_user', username);
    const modal = bootstrap.Modal.getInstance(document.getElementById('loginModal'));
    if (modal) modal.hide();
    updateUserDisplay(username);
    updatePreview();
    showToast(`Account created! Welcome, ${name || username}!`, 'success');
}

function logoutUser() {
    saveToLocal();
    localStorage.removeItem('resumeforge_current_user');
    document.getElementById('userDisplay').classList.add('d-none');
    resumeData = { personal: { firstName: '', lastName: '', title: '', email: '', phone: '', location: '', linkedin: '', github: '', website: '', summary: '' }, experience: [], education: [], skills: [], projects: [], certifications: [], awards: [], coverLetter: { content: '', generated: false } };
    entryCounters = { experience: 0, education: 0, skills: 0, projects: 0, certifications: 0, awards: 0 };
    setPersonalData(resumeData.personal);
    renderExperienceList();
    renderEducationList();
    renderSkillsList();
    renderProjectsList();
    renderCertificationsList();
    renderAwardsList();
    updatePreview();
    const modal = new bootstrap.Modal(document.getElementById('loginModal'));
    modal.show();
}

function updateUserDisplay(username) {
    const users = JSON.parse(localStorage.getItem('resumeforge_users') || '[]');
    const user = users.find(u => u.username === username);
    const displayName = user ? (user.name || username) : username;
    document.getElementById('userNameDisplay').textContent = displayName;
    document.getElementById('userDisplay').classList.remove('d-none');
}

// ==================== SAVE / LOAD ====================
function saveToLocal() {
    resumeData.personal = getPersonalData();
    const saveData = { resumeData, template: currentTemplate, timestamp: new Date().toISOString() };
    const currentUser = localStorage.getItem('resumeforge_current_user');
    const key = currentUser ? `resumeforge_data_${currentUser}` : 'resumeforge_data';
    localStorage.setItem(key, JSON.stringify(saveData));
    showToast('Resume saved to browser storage!', 'success');
}

function loadFromLocal() {
    const currentUser = localStorage.getItem('resumeforge_current_user');
    const key = currentUser ? `resumeforge_data_${currentUser}` : 'resumeforge_data';
    const saved = localStorage.getItem(key);
    if (!saved) {
        const legacy = localStorage.getItem('resumeforge_data');
        if (legacy) { try { const saveData = JSON.parse(legacy); if (saveData.resumeData) { restoreData(saveData); return; } } catch (e) {} }
        updatePreview();
        return;
    }
    try { const saveData = JSON.parse(saved); if (saveData.resumeData) restoreData(saveData); } catch (e) { showToast('Could not load saved data.', 'danger'); }
}

function restoreData(saveData) {
    resumeData = saveData.resumeData;
    if (!resumeData.coverLetter) resumeData.coverLetter = { content: '', generated: false };
    currentTemplate = saveData.template || 'professional';
    entryCounters.experience = resumeData.experience.length > 0 ? Math.max(...resumeData.experience.map(e => e.id)) : 0;
    entryCounters.education = resumeData.education.length > 0 ? Math.max(...resumeData.education.map(e => e.id)) : 0;
    entryCounters.skills = resumeData.skills.length > 0 ? Math.max(...resumeData.skills.map(s => s.id)) : 0;
    entryCounters.projects = resumeData.projects.length > 0 ? Math.max(...resumeData.projects.map(p => p.id)) : 0;
    entryCounters.certifications = resumeData.certifications.length > 0 ? Math.max(...resumeData.certifications.map(c => c.id)) : 0;
    entryCounters.awards = resumeData.awards.length > 0 ? Math.max(...resumeData.awards.map(a => a.id)) : 0;
    setPersonalData(resumeData.personal);
    setTemplate(currentTemplate);
    renderExperienceList();
    renderEducationList();
    renderSkillsList();
    renderProjectsList();
    renderCertificationsList();
    renderAwardsList();
    updatePreview();
}

// ==================== IMPORT / EXPORT JSON ====================
function exportJSON() {
    resumeData.personal = getPersonalData();
    const saveData = { resumeData, template: currentTemplate, exportedAt: new Date().toISOString(), app: 'ResumeForge' };
    const blob = new Blob([JSON.stringify(saveData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${resumeData.personal.firstName || 'resume'}_${resumeData.personal.lastName || 'data'}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('Resume exported as JSON!', 'success');
}

function importJSON(event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function (e) {
        try { const saveData = JSON.parse(e.target.result); if (!saveData.resumeData) throw new Error('Invalid format'); restoreData(saveData); showToast('Resume imported successfully!', 'success'); } catch (err) { showToast('Invalid JSON file. Please use a file exported from ResumeForge.', 'danger'); }
    };
    reader.readAsText(file);
    event.target.value = '';
}

// ==================== PDF EXPORT ====================
function exportPDF() {
    const originalMode = previewMode;
    
    // Helper to get a clean clone without page numbers or extra spans
    function getCleanClone(mode) {
        setPreviewMode(mode);
        return new Promise((resolve) => {
            setTimeout(() => {
                const el = document.getElementById('resumePage');
                const clone = el.cloneNode(true);
                
                // Remove any elements that might be page numbers (common culprits)
                const removeSelectors = [
                    '.page-number', '.page-break', 'footer', 
                    '[class*="page"]', '[class*="Page"]', '.counter'
                ];
                removeSelectors.forEach(selector => {
                    clone.querySelectorAll(selector).forEach(el => el.remove());
                });
                
                // Remove any span/div that contains only digits (page numbers)
                clone.querySelectorAll('span, div, p').forEach(el => {
                    const text = el.textContent.trim();
                    if (text.match(/^\d+$/) && text.length <= 4) {
                        el.remove();
                    }
                });
                
                resolve(clone);
            }, 150);
        });
    }
    
    showToast('Preparing PDF...', 'info');
    
    // Get resume clone
    getCleanClone('resume').then(resumeClone => {
        // If cover letter exists, combine
        if (resumeData.coverLetter && resumeData.coverLetter.content && resumeData.coverLetter.content.trim() !== '') {
            getCleanClone('coverletter').then(coverClone => {
                setPreviewMode(originalMode);
                
                // Create container
                const container = document.createElement('div');
                container.style.background = 'white';
                container.style.padding = '0';
                container.style.margin = '0';
                container.appendChild(resumeClone);
                
                // Page break
                const pageBreak = document.createElement('div');
                pageBreak.style.pageBreakBefore = 'always';
                container.appendChild(pageBreak);
                container.appendChild(coverClone);
                
                const opt = {
                    margin: 0,
                    filename: `${resumeData.personal.firstName || 'Resume'}_${resumeData.personal.lastName || ''}_with_CoverLetter.pdf`,
                    image: { type: 'jpeg', quality: 0.98 },
                    html2canvas: { scale: 2, useCORS: true, logging: false },
                    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
                };
                html2pdf().set(opt).from(container).save()
                    .then(() => showToast('Combined PDF exported!', 'success'))
                    .catch(err => { console.error(err); showToast('Export failed: ' + err.message, 'danger'); });
            });
        } else {
            // Export only resume
            setPreviewMode(originalMode);
            const opt = {
                margin: 0,
                filename: `${resumeData.personal.firstName || 'Resume'}_${resumeData.personal.lastName || ''}.pdf`,
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 2, useCORS: true, logging: false },
                jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
            };
            html2pdf().set(opt).from(resumeClone).save()
                .then(() => showToast('Resume PDF exported!', 'success'))
                .catch(err => { console.error(err); showToast('Export failed: ' + err.message, 'danger'); });
        }
    }).catch(err => {
        setPreviewMode(originalMode);
        showToast('Failed to prepare preview.', 'danger');
        console.error(err);
    });
}
// ==================== SETTINGS (API KEY) ====================
function openSettings() {
    const keyInput = document.getElementById('apiKeyInput');
    keyInput.value = localStorage.getItem('resumeforge_api_key') || '';
    document.getElementById('apiKeySavedMsg').classList.add('d-none');
    const modal = new bootstrap.Modal(document.getElementById('settingsModal'));
    modal.show();
}

function saveApiKeyFromModal() {
    const key = document.getElementById('apiKeyInput').value.trim();
    if (typeof saveApiKey === 'function') saveApiKey(key);
    else localStorage.setItem('resumeforge_api_key', key);
    document.getElementById('apiKeySavedMsg').classList.remove('d-none');
    setTimeout(() => document.getElementById('apiKeySavedMsg').classList.add('d-none'), 2000);
}

function clearApiKey() {
    localStorage.removeItem('resumeforge_api_key');
    document.getElementById('apiKeyInput').value = '';
    if (typeof AI_CONFIG !== 'undefined') AI_CONFIG.apiKey = '';
    showToast('API key cleared.', 'info');
}

function toggleApiKeyVisibility() {
    const input = document.getElementById('apiKeyInput');
    const icon = document.getElementById('apiKeyEyeIcon');
    if (input.type === 'password') { input.type = 'text'; icon.className = 'bi bi-eye-slash'; }
    else { input.type = 'password'; icon.className = 'bi bi-eye'; }
}

// ==================== UTILITIES ====================
function escapeHTML(str) { if (!str) return ''; const div = document.createElement('div'); div.textContent = str; return div.innerHTML; }
function formatMonth(dateStr) { if (!dateStr) return ''; const [year, month] = dateStr.split('-'); const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']; return `${months[parseInt(month) - 1]} ${year}`; }
function formatDateRange(start, end, current) { const startStr = start ? formatMonth(start) : ''; const endStr = current ? 'Present' : (end ? formatMonth(end) : ''); if (startStr && endStr) return `${startStr} — ${endStr}`; if (startStr) return startStr; if (endStr) return endStr; return ''; }
function formatDescription(text) { if (!text) return ''; const lines = text.split('\n').filter(l => l.trim()); const hasBullets = lines.some(l => l.trim().startsWith('- ') || l.trim().startsWith('* ')); if (hasBullets) { const items = lines.map(l => { const cleaned = l.trim().replace(/^[-*]\s*/, ''); return `<li>${escapeHTML(cleaned)}</li>`; }).join(''); return `<ul>${items}</ul>`; } return escapeHTML(text); }
function showToast(message, type) { const toast = document.getElementById('toast'); const body = document.getElementById('toastBody'); body.textContent = message; toast.className = `toast align-items-center border-0 text-bg-${type || 'info'}`; const bsToast = new bootstrap.Toast(toast, { autohide: true, delay: 3000 }); bsToast.show(); }

// ==================== THEME MANAGEMENT ====================
function setTheme(theme) {
    if (theme === 'light') {
        document.body.classList.add('light-theme');
        localStorage.setItem('resumeforge_theme', 'light');
        const btn = document.getElementById('themeToggleBtn');
        if (btn) { btn.innerHTML = '<i class="bi bi-sun-fill"></i>'; btn.title = 'Switch to Dark Theme'; }
    } else {
        document.body.classList.remove('light-theme');
        localStorage.setItem('resumeforge_theme', 'dark');
        const btn = document.getElementById('themeToggleBtn');
        if (btn) { btn.innerHTML = '<i class="bi bi-moon-stars"></i>'; btn.title = 'Switch to Light Theme'; }
    }
}

function toggleTheme() { setTheme(document.body.classList.contains('light-theme') ? 'dark' : 'light'); }
function loadTheme() { const savedTheme = localStorage.getItem('resumeforge_theme'); setTheme(savedTheme === 'light' ? 'light' : 'dark'); }

// ==================== INITIALIZATION ====================
window.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'z' && !e.shiftKey) { e.preventDefault(); undo(); }
        if ((e.ctrlKey && e.key === 'y') || (e.ctrlKey && e.shiftKey && e.key === 'z')) { e.preventDefault(); redo(); }
    });
    window.addEventListener('resize', () => setZoom('fit'));
    checkAuth();
    setTimeout(() => setZoom('fit'), 100);
    loadTheme();
});

// Debug logs
console.log('app.js loaded successfully');
console.log('showSection defined?', typeof showSection);
console.log('addExperience defined?', typeof addExperience);
console.log('setTemplate defined?', typeof setTemplate);