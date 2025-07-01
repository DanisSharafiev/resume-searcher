const API_CONFIG = {
    baseUrl: 'http://localhost:8006',
    endpoints: {
        search: '/api/v1/search',
        resume: '/api/v1/resume'
    }
};


const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');
const loadingIndicator = document.getElementById('loadingIndicator');
const searchResults = document.getElementById('searchResults');
const expandedResume = document.getElementById('expandedResume');
const llmResponse = document.getElementById('llmResponse');
const resumeText = document.getElementById('resumeText');
const closeExpanded = document.getElementById('closeExpanded');

let currentQuery = '';
let selectedCandidateId = null;

document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    focusSearchInput();
});

function initializeEventListeners() {
    searchButton.addEventListener('click', handleSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });
    closeExpanded.addEventListener('click', closeExpandedResume);
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeExpandedResume();
        }
    });
}

function focusSearchInput() {
    searchInput.focus();
}

async function handleSearch() {
    const query = searchInput.value.trim();
    if (!query) {
        showError('Please enter keywords for search');
        return;
    }
    currentQuery = query;
    await performSearch(query);
}

async function performSearch(query) {
    try {
        showLoading(true);
        hideExpandedResume();
        clearResults();

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000);

        const response = await fetch(`${API_CONFIG.baseUrl}${API_CONFIG.endpoints.search}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const candidates = await response.json();
        console.log('Response from server:', candidates);
        console.log('Type of candidates:', typeof candidates);
        console.log('Is candidates array?', Array.isArray(candidates));
        console.log('candidates.results:', candidates.results);
        console.log('Is candidates.results array?', Array.isArray(candidates.results));
        
        showLoading(false);
        // Гарантируем, что в displaySearchResults всегда передается массив
        let candidatesArr = [];
        if (Array.isArray(candidates)) {
            candidatesArr = candidates;
        } else if (candidates && Array.isArray(candidates.results)) {
            candidatesArr = candidates.results;
        } else {
            console.error('Neither candidates nor candidates.results is an array!');
            candidatesArr = [];
        }
        console.log('Final candidates array:', candidatesArr);
        console.log('Final array length:', candidatesArr.length);
        displaySearchResults(candidatesArr);
    } catch (error) {
        console.error('Search error:', error);
        showLoading(false);
        showError('Error while searching resumes. ' + (error.message || 'Check server connection.'));
    }
}

function displaySearchResults(candidates) {
    console.log('displaySearchResults called with:', candidates, 'isArray:', Array.isArray(candidates));
    
    // Принудительно преобразуем в массив
    if (!Array.isArray(candidates)) {
        console.warn('candidates is not an array, converting to array');
        candidates = [];
    }
    
    if (candidates.length === 0) {
        showEmptyState();
        return;
    }
    
    try {
        const resultsHTML = candidates.map(candidate => `
            <div class="result-card" data-candidate-id="${candidate.id}" onclick="selectCandidate(${candidate.id})">
                <div class="candidate-name">${escapeHtml(candidate.name)}</div>
                <div class="candidate-position">${escapeHtml(candidate.position)}</div>
            </div>
        `).join('');
        searchResults.innerHTML = resultsHTML;
    } catch (error) {
        console.error('Error in displaySearchResults:', error);
        showError('Error displaying search results: ' + error.message);
    }
}

async function selectCandidate(candidateId) {
    try {
        updateSelectedCard(candidateId);
        showExpandedLoading();
        const response = await fetch(`${API_CONFIG.baseUrl}${API_CONFIG.endpoints.resume}/${candidateId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const resumeData = await response.json();
        selectedCandidateId = candidateId;
        showExpandedResume(resumeData);
    } catch (error) {
        console.error('Resume fetch error:', error);
        showError('Error while searching resumes. ' + (error.message || 'Check server connection.'));
        hideExpandedResume();
    }
}

function updateSelectedCard(candidateId) {
    document.querySelectorAll('.result-card').forEach(card => {
        card.classList.remove('selected');
    });
    const selectedCard = document.querySelector(`[data-candidate-id="${candidateId}"]`);
    if (selectedCard) {
        selectedCard.classList.add('selected');
    }
}

function showExpandedResume(resumeData) {
    // Логируем для отладки
    console.log('showExpandedResume received:', resumeData);
    // Если есть ошибка
    if (resumeData.error) {
        showError('Error loading resume: ' + resumeData.error);
        return;
    }
    // Если backend вернул content как строку (старый/простой вариант)
    if (typeof resumeData.content === 'string') {
        llmResponse.textContent = resumeData.content;
        resumeText.textContent = '';
        expandedResume.classList.remove('hidden');
        expandedResume.scrollIntoView({ behavior: 'smooth', block: 'start' });
        return;
    }
    // Если backend вернул объект с llm_response_markdown и resume_plain
    if (resumeData.content && typeof resumeData.content === 'object') {
        llmResponse.textContent = resumeData.content.llm_response_markdown || '';
        resumeText.textContent = resumeData.content.resume_plain || 'Resume not found';
        expandedResume.classList.remove('hidden');
        expandedResume.scrollIntoView({ behavior: 'smooth', block: 'start' });
        return;
    }
    // Если backend вернул llm_response_markdown и resume_plain на верхнем уровне
    llmResponse.textContent = resumeData.llm_response_markdown || '';
    resumeText.textContent = resumeData.resume_plain || 'Resume not found';
    expandedResume.classList.remove('hidden');
    expandedResume.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function showExpandedLoading() {
    llmResponse.innerHTML = '<div class="loading"><div class="spinner"></div><span>Loading details...</span></div>';
    resumeText.textContent = '';
    expandedResume.classList.remove('hidden');
    expandedResume.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function closeExpandedResume() {
    expandedResume.classList.add('hidden');
    selectedCandidateId = null;
    document.querySelectorAll('.result-card').forEach(card => {
        card.classList.remove('selected');
    });
}

function hideExpandedResume() {
    expandedResume.classList.add('hidden');
}

function showLoading(show) {
    if (show) {
        loadingIndicator.classList.remove('hidden');
        searchButton.disabled = true;
        searchButton.textContent = 'Searching...';
    } else {
        loadingIndicator.classList.add('hidden');
        searchButton.disabled = false;
        searchButton.textContent = 'Search';
    }
}

function clearResults() {
    searchResults.innerHTML = '';
}

function showEmptyState() {
    searchResults.innerHTML = `
        <div class="empty-state">
            <div class="empty-state-icon">📋</div>
            <div>No results for "${escapeHtml(currentQuery)}"</div>
            <div style="margin-top: 10px; font-size: 16px; color: #999;">
                Try changing your keywords
            </div>
        </div>
    `;
}

function showError(message) {
    const errorHTML = `
        <div class="error-message">
            ⚠️ ${escapeHtml(message)}
        </div>
    `;
    searchResults.innerHTML = errorHTML;
    setTimeout(() => {
        const errorElement = document.querySelector('.error-message');
        if (errorElement) {
            errorElement.remove();
        }
    }, 5000);
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        handleSearch,
        selectCandidate,
        showError,
        escapeHtml
    };
}
