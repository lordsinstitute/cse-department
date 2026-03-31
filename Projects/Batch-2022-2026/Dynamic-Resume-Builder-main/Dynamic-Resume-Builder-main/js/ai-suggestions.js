/* ============================================
   ResumeForge — AI Suggestions Module
   Using OpenRouter (free models)
   ============================================ */

// ==================== CONFIGURATION ====================
const AI_CONFIG = {
    apiKey: localStorage.getItem('resumeforge_api_key') || '',
    // You can change this to any free model from the list below
    model: 'arcee-ai/trinity-large-preview:free'  // Recommended free model
};

function saveApiKey(key) {
    AI_CONFIG.apiKey = key.trim();
    localStorage.setItem('resumeforge_api_key', AI_CONFIG.apiKey);
}

// ==================== OPENROUTER API CALL ====================
async function callOpenRouter(systemPrompt, userMessage) {
    if (!AI_CONFIG.apiKey) {
        throw new Error('No API key configured. Please add your OpenRouter API key in Settings.');
    }

    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${AI_CONFIG.apiKey}`,   // <-- CORRECT HEADER
            'Content-Type': 'application/json',
            'HTTP-Referer': window.location.origin,
            'X-Title': 'ResumeForge'
        },
        body: JSON.stringify({
            model: AI_CONFIG.model,
            messages: [
                { role: 'system', content: systemPrompt },
                { role: 'user', content: userMessage }
            ],
            max_tokens: 1024,
            temperature: 0.7
        })
    });

    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        const errorMessage = err.error?.message || err.message || `API error ${response.status}`;
        throw new Error(errorMessage);
    }

    const data = await response.json();
    return data.choices[0].message.content;
}

// ==================== AI SUGGESTION ====================
async function getAISuggestion(text, context, sectionType) {
    const systemPrompt = `You are an expert resume writer and career coach.
Your job is to improve resume content to be more impactful, professional, and ATS-friendly.
Guidelines:
- Use strong action verbs (led, developed, built, achieved, managed, designed, implemented, optimized)
- Add quantifiable metrics where possible (numbers, percentages, impact)
- Remove first-person pronouns (I, my, me)
- Write in past tense for past roles, present tense for current role
- Be concise and specific
- Format bullet points starting with action verbs
- Keep the same information but make it sound more impressive
Return ONLY the improved text, no explanations or preamble.`;

    const sectionContext = {
        summary: 'professional summary section',
        experience: 'work experience description',
        project: 'project description',
        education: 'education description',
        award: 'award description'
    };

    const userMessage = `Improve this ${sectionContext[sectionType] || 'resume section'} content. Make it more impactful and professional:

${text}

Return only the improved text. Use bullet points starting with "- " if the content has multiple achievements or responsibilities.`;

    return await callOpenRouter(systemPrompt, userMessage);
}

// ==================== REWRITE SECTION ====================
async function rewriteSection(text, sectionType) {
    const systemPrompt = `You are a professional resume writer. Completely rewrite the given resume content to be outstanding.
Rules:
- Start bullet points with powerful action verbs
- Include or suggest quantifiable metrics with [X] placeholders if unknown
- No first-person pronouns
- ATS-optimized language
- Professional and impactful
Return ONLY the rewritten text.`;

    const userMessage = `Completely rewrite this ${sectionType} content for a resume, making it outstanding:

${text}`;

    return await callOpenRouter(systemPrompt, userMessage);
}

// ==================== SHOW AI SUGGESTION PANEL ====================
function showAISuggestion(targetId, suggestion) {
    const panelId = 'ai-panel-' + targetId;
    const panel = document.getElementById(panelId);
    if (!panel) return;

    panel.innerHTML = `
        <div class="ai-suggestion-text">${escapeHTMLForAI(suggestion)}</div>
        <div class="ai-suggestion-actions">
            <button class="btn btn-sm btn-outline-success" onclick="acceptSuggestion('${targetId}', this)">
                <i class="bi bi-check-lg me-1"></i>Accept
            </button>
            <button class="btn btn-sm btn-outline-secondary" onclick="dismissAISuggestion('${targetId}')">
                <i class="bi bi-x-lg me-1"></i>Dismiss
            </button>
        </div>
    `;
    panel.setAttribute('data-suggestion', suggestion);
    panel.classList.remove('d-none');
}

function showAILoading(targetId) {
    const panelId = 'ai-panel-' + targetId;
    const panel = document.getElementById(panelId);
    if (!panel) return;

    panel.innerHTML = `
        <div class="ai-loading">
            <div class="spinner-border text-info spinner-border-sm" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <span>AI is thinking...</span>
        </div>
    `;
    panel.classList.remove('d-none');
}

function hideAIPanel(targetId) {
    const panelId = 'ai-panel-' + targetId;
    const panel = document.getElementById(panelId);
    if (panel) panel.classList.add('d-none');
}

function dismissAISuggestion(targetId) {
    hideAIPanel(targetId);
}

// ==================== ACCEPT SUGGESTION ====================
function acceptSuggestion(targetId, buttonEl) {
    const panelId = 'ai-panel-' + targetId;
    const panel = document.getElementById(panelId);
    const suggestion = panel ? panel.getAttribute('data-suggestion') : '';

    const textarea = document.getElementById(targetId);
    if (textarea && suggestion) {
        // Save undo state before applying (if function exists)
        if (typeof saveState === 'function') saveState();

        textarea.value = suggestion;
        // Trigger the oninput event to update resume data
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
        hideAIPanel(targetId);

        if (typeof showToast === 'function') {
            showToast('AI suggestion applied!', 'success');
        }
    }
}

// ==================== TRIGGER AI SUGGEST ====================
async function triggerAISuggest(targetId, sectionType) {
    const textarea = document.getElementById(targetId);
    if (!textarea) {
        if (typeof showToast === 'function') showToast('Field not found.', 'warning');
        return;
    }

    const text = textarea.value.trim();
    if (!text) {
        if (typeof showToast === 'function') showToast('Please enter some text first.', 'warning');
        return;
    }

    if (!AI_CONFIG.apiKey) {
        if (typeof showToast === 'function') showToast('Please add your OpenRouter API key in Settings (gear icon).', 'warning');
        if (typeof openSettings === 'function') openSettings();
        return;
    }

    showAILoading(targetId);

    try {
        const suggestion = await getAISuggestion(text, null, sectionType);
        showAISuggestion(targetId, suggestion);
    } catch (err) {
        const panelId = 'ai-panel-' + targetId;
        const panel = document.getElementById(panelId);
        if (panel) {
            panel.innerHTML = `
                <div class="text-danger small">
                    <i class="bi bi-exclamation-triangle-fill me-1"></i>
                    <strong>Error:</strong> ${escapeHTMLForAI(err.message)}
                </div>
                <button class="btn btn-sm btn-outline-secondary mt-1" onclick="dismissAISuggestion('${targetId}')">
                    <i class="bi bi-x-lg me-1"></i>Dismiss
                </button>
            `;
        }
        if (typeof showToast === 'function') showToast('AI suggestion failed: ' + err.message, 'danger');
    }
}
// ==================== AI SKILL SUGGESTIONS (trigger) ====================
async function suggestSkills() {
    if (!AI_CONFIG.apiKey) {
        showToast('Please add your API key in Settings.', 'warning');
        openSettings();
        return;
    }

    const jobTitle = document.getElementById('title').value.trim();
    const jobDesc = document.getElementById('jobDescription').value.trim();

    if (!jobTitle && !jobDesc) {
        showToast('Enter a job title or paste a job description first.', 'warning');
        return;
    }

    const prompt = `You are a career expert. Based on the following ${jobTitle ? 'job title: "'+jobTitle+'"' : ''} ${jobDesc ? 'and job description: "'+jobDesc+'"' : ''}, suggest 10-15 relevant skills for a resume. Return only a JSON array of objects with "name" and "level" (Beginner/Intermediate/Advanced/Expert). No other text.`;

    showToast('Generating skill suggestions...', 'info');

    try {
        const suggestion = await callOpenRouter(
            'You are a helpful assistant that outputs only valid JSON.',
            prompt
        );

        // Parse the AI response
        const skills = JSON.parse(suggestion);
        if (!Array.isArray(skills)) throw new Error('Invalid response');

        // Show the multi‑select modal
        showSkillSuggestions(skills);
    } catch (err) {
        showToast('Failed to get suggestions: ' + err.message, 'danger');
    }
}
// ==================== AI SKILL SUGGESTIONS (Multi‑select) ====================

// Global functions for skill selection (they need to be accessible from inline onclick)
function toggleSelectSkill(btn) {
    btn.classList.toggle('btn-selected');
    const isSelected = btn.classList.contains('btn-selected');
    btn.setAttribute('data-selected', isSelected ? 'true' : 'false');
}

function addSelectedSkills() {
    const modal = document.getElementById('skillSuggestModal');
    if (!modal) return;

    const selectedButtons = modal.querySelectorAll('.btn-outline-warning.btn-selected');
    if (selectedButtons.length === 0) {
        showToast('No skills selected.', 'info');
        return;
    }

    selectedButtons.forEach(btn => {
        const name = btn.getAttribute('data-name');
        const level = btn.getAttribute('data-level');
        addSkill({ name, level });
    });

    // Close the modal
    const modalInstance = bootstrap.Modal.getInstance(modal);
    if (modalInstance) modalInstance.hide();

    showToast(`${selectedButtons.length} skill(s) added!`, 'success');
}

function showSkillSuggestions(skills) {
    // Remove any existing modal with the same ID
    const existing = document.getElementById('skillSuggestModal');
    if (existing) existing.remove();

    // Build skill buttons with data attributes
    const skillButtons = skills.map(s => 
        `<button class="btn btn-outline-warning btn-sm" 
            data-name="${escapeHTML(s.name)}" 
            data-level="${escapeHTML(s.level)}" 
            data-selected="false"
            onclick="toggleSelectSkill(this)">
            ${escapeHTML(s.name)} (${escapeHTML(s.level)})
        </button>`
    ).join('');

    const modalHtml = `
        <div class="modal fade" id="skillSuggestModal" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content login-modal-content">
                    <div class="modal-header border-0">
                        <h6 class="modal-title"><i class="bi bi-stars text-warning"></i> Suggested Skills</h6>
                        <button class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p class="small text-muted">Click skills to select/deselect. Then click Done to add all selected.</p>
                        <div class="d-flex flex-wrap gap-2">
                            ${skillButtons}
                        </div>
                    </div>
                    <div class="modal-footer border-0">
                        <button class="btn btn-sm btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button class="btn btn-sm btn-warning" onclick="addSelectedSkills()">
                            <i class="bi bi-check-lg me-1"></i>Done
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('skillSuggestModal'));
    modal.show();
}

// Note: The old addSuggestedSkill function is no longer needed, but we keep it for backward compatibility if any other code calls it.
// If you want to remove it, you can delete the function.
function addSuggestedSkill(name, level) {
    addSkill({ name, level });
}
// ==================== AI KEYWORD GAP ANALYSIS ====================
async function analyzeKeywordGap() {
    const jobDesc = document.getElementById('jobDescription').value.trim();
    if (!jobDesc) {
        showToast('Paste a job description first.', 'warning');
        return;
    }

    if (!AI_CONFIG.apiKey) {
        showToast('API key required.', 'warning');
        openSettings();
        return;
    }

    // Build resume text from all sections
    const resumeText = `
        ${resumeData.personal.summary || ''}
        ${resumeData.experience.map(e => e.description || '').join(' ')}
        ${resumeData.education.map(e => e.description || '').join(' ')}
        ${resumeData.projects.map(p => p.description || '').join(' ')}
        ${resumeData.skills.map(s => s.name || '').join(', ')}
    `.toLowerCase();

    const prompt = `Compare the following job description with the candidate's resume text. Identify the top 10 most important keywords or phrases that appear in the job description but are missing or underrepresented in the resume. For each, suggest a brief way to incorporate it (e.g., "Add to skills section" or "Mention in experience description"). Return the result as a JSON array of objects with "keyword" and "suggestion". No other text.

Job Description:
${jobDesc}

Resume Text:
${resumeText}`;

    showToast('Analyzing keyword gap...', 'info');

    try {
        const response = await callOpenRouter(
            'You output only valid JSON.',
            prompt
        );
        const gaps = JSON.parse(response);

        const resultsDiv = document.getElementById('keywordGapResults');
        if (!gaps || gaps.length === 0) {
            resultsDiv.innerHTML = '<p class="text-success">✅ No major keyword gaps found!</p>';
        } else {
            resultsDiv.innerHTML = '<p class="text-warning mb-1">🔍 Missing keywords:</p><ul class="list-unstyled">' +
                gaps.map(g => `<li class="mb-1"><span class="badge bg-secondary me-1">${escapeHTML(g.keyword)}</span> <span class="text-muted">${escapeHTML(g.suggestion)}</span></li>`).join('') +
                '</ul>';
        }
    } catch (err) {
        showToast('Analysis failed: ' + err.message, 'danger');
    }
}

// ==================== UTILITY ====================
function escapeHTMLForAI(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;')
        .replace(/\n/g, '<br>');
}