// Form and results elements
const form = document.getElementById('assessment-form');
const resultsContainer = document.getElementById('results');
const submitBtn = form.querySelector('.submit-btn');

// Handle form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Show loading state
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
    
    // Collect form data
    const formData = new FormData(form);
    const data = {};
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    try {
        // Send data to server
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error('Failed to get prediction');
        }
        
        const result = await response.json();
        
        // Show results
        displayResults(result);
        
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    } finally {
        // Reset button state
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
    }
});

// Display results
function displayResults(result) {
    // Hide form and show results
    form.style.display = 'none';
    resultsContainer.classList.remove('hidden');
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    // Display risk level
    const riskLevel = document.getElementById('risk-level');
    const riskPercentage = document.getElementById('risk-percentage');
    const riskFill = document.getElementById('risk-fill');
    
    riskLevel.textContent = getRiskLevelText(result.risk_level);
    riskLevel.className = `risk-level ${result.risk_level}`;
    
    const percentage = Math.round(result.probability * 100);
    riskPercentage.textContent = `${percentage}%`;
    
    // Animate risk bar
    setTimeout(() => {
        riskFill.style.width = `${percentage}%`;
    }, 100);
    
    // Display risk factors
    displayRiskFactors(result.risk_factors);
    
    // Display recommendations
    displayRecommendations(result.recommendations);
}

// Get risk level text
function getRiskLevelText(level) {
    const texts = {
        'critical': 'Critical Risk',
        'high': 'High Risk',
        'moderate': 'Moderate Risk',
        'low': 'Low Risk',
        'minimal': 'Minimal Risk'
    };
    return texts[level] || level;
}

// Display risk factors
function displayRiskFactors(factors) {
    const container = document.getElementById('risk-factors');
    container.innerHTML = '';
    
    if (factors.length === 0) {
        container.innerHTML = '<p class="no-factors">No significant risk factors identified.</p>';
        return;
    }
    
    factors.forEach((factor, index) => {
        const element = document.createElement('div');
        element.className = `risk-factor ${factor.severity}`;
        element.style.animationDelay = `${index * 0.1}s`;
        
        element.innerHTML = `
            <h3>${factor.factor}</h3>
            <p>${factor.description}</p>
        `;
        
        container.appendChild(element);
    });
}

// Display recommendations
function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendations');
    container.innerHTML = '<h3 style="margin-bottom: 1rem; font-size: 1.25rem;">Recommendations</h3>';
    
    recommendations.forEach((rec, index) => {
        const element = document.createElement('div');
        element.className = `recommendation ${rec.priority}`;
        element.style.animationDelay = `${(index + 3) * 0.1}s`;
        
        const icon = getRecommendationIcon(rec.priority);
        
        element.innerHTML = `
            <div class="recommendation-icon">${icon}</div>
            <div class="recommendation-content">
                <h4>${rec.action}</h4>
                <p>${rec.description}</p>
            </div>
        `;
        
        container.appendChild(element);
    });
}

// Get recommendation icon
function getRecommendationIcon(priority) {
    const icons = {
        'high': '🚨',
        'medium': '⚠️',
        'low': 'ℹ️'
    };
    return icons[priority] || '📌';
}

// Reset form
function resetForm() {
    // Show form and hide results
    form.style.display = 'block';
    resultsContainer.classList.add('hidden');
    
    // Reset form fields
    form.reset();
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Add input animations
const inputs = form.querySelectorAll('input, select');
inputs.forEach((input, index) => {
    input.style.animationDelay = `${index * 0.05}s`;
    input.style.animation = 'fadeInUp 0.5s ease forwards';
    
    input.addEventListener('focus', function() {
        this.parentElement.style.transform = 'scale(1.02)';
        this.parentElement.style.transition = 'transform 0.2s ease';
    });
    
    input.addEventListener('blur', function() {
        this.parentElement.style.transform = 'scale(1)';
    });
});

// Keyboard navigation
form.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.target.tagName !== 'BUTTON') {
        e.preventDefault();
        const formElements = Array.from(form.elements).filter(el => 
            el.tagName === 'INPUT' || el.tagName === 'SELECT' || el.tagName === 'BUTTON'
        );
        const currentIndex = formElements.indexOf(e.target);
        const nextElement = formElements[currentIndex + 1];
        
        if (nextElement) {
            nextElement.focus();
        }
    }
});

// Auto-save form data
let autoSaveTimer;
form.addEventListener('input', () => {
    clearTimeout(autoSaveTimer);
    autoSaveTimer = setTimeout(() => {
        const formData = new FormData(form);
        const data = {};
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        localStorage.setItem('mental_health_form_data', JSON.stringify(data));
    }, 1000);
});

// Load saved form data
window.addEventListener('load', () => {
    const savedData = localStorage.getItem('mental_health_form_data');
    if (savedData) {
        const data = JSON.parse(savedData);
        Object.keys(data).forEach(key => {
            const input = form.elements[key];
            if (input) {
                input.value = data[key];
            }
        });
    }
});

// Clear saved data on successful submission
form.addEventListener('submit', () => {
    localStorage.removeItem('mental_health_form_data');
});

// Add stats display (optional)
async function loadStats() {
    try {
        const response = await fetch('/stats');
        const stats = await response.json();
        console.log('Assessment stats:', stats);
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

// Load stats on page load
loadStats();