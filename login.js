// Login/Signup Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Tab switching functionality
    const authTabs = document.querySelectorAll('.auth-tab');
    const authForms = document.querySelectorAll('.auth-form');
    
    authTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetForm = tab.getAttribute('data-tab');
            
            // Remove active class from all tabs and forms
            authTabs.forEach(t => t.classList.remove('active'));
            authForms.forEach(f => f.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding form
            tab.classList.add('active');
            document.getElementById(`${targetForm}-form`).classList.add('active');
        });
    });
    
    // Form submissions
    const loginForm = document.getElementById('loginEmailForm');
    const signupForm = document.getElementById('signupEmailForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    if (signupForm) {
        signupForm.addEventListener('submit', handleSignup);
    }
    
    // Social login buttons
    const googleLoginBtns = document.querySelectorAll('.google-btn');
    const appleLoginBtns = document.querySelectorAll('.apple-btn');
    
    googleLoginBtns.forEach(btn => {
        btn.addEventListener('click', handleGoogleAuth);
    });
    
    appleLoginBtns.forEach(btn => {
        btn.addEventListener('click', handleAppleAuth);
    });
    
    // Password confirmation validation
    const confirmPasswordField = document.getElementById('confirmPassword');
    const signupPasswordField = document.getElementById('signupPassword');
    
    if (confirmPasswordField && signupPasswordField) {
        confirmPasswordField.addEventListener('input', validatePasswordMatch);
        signupPasswordField.addEventListener('input', validatePasswordMatch);
    }
});

// Handle email login
async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const rememberMe = document.getElementById('rememberMe').checked;
    const submitBtn = e.target.querySelector('.auth-submit-btn');
    
    // Add loading state
    submitBtn.classList.add('loading');
    submitBtn.textContent = 'Signing In...';
    
    try {
        // Simulate API call
        await simulateAuthRequest();
        
        // Store auth data (in real app, use secure storage)
        const authData = {
            email: email,
            loginTime: new Date().toISOString(),
            rememberMe: rememberMe
        };
        
        if (rememberMe) {
            localStorage.setItem('transverse_auth', JSON.stringify(authData));
        } else {
            sessionStorage.setItem('transverse_auth', JSON.stringify(authData));
        }
        
        // Show success message
        showAuthMessage('Login successful! Redirecting...', 'success');
        
        // Redirect to main app after delay
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 1500);
        
    } catch (error) {
        showAuthMessage('Login failed. Please check your credentials.', 'error');
    } finally {
        // Remove loading state
        submitBtn.classList.remove('loading');
        submitBtn.textContent = 'Sign In';
    }
}

// Handle email signup
async function handleSignup(e) {
    e.preventDefault();
    
    const name = document.getElementById('signupName').value;
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const agreeTerms = document.getElementById('agreeTerms').checked;
    const submitBtn = e.target.querySelector('.auth-submit-btn');
    
    // Validation
    if (password !== confirmPassword) {
        showAuthMessage('Passwords do not match.', 'error');
        return;
    }
    
    if (!agreeTerms) {
        showAuthMessage('Please agree to the Terms of Service and Privacy Policy.', 'error');
        return;
    }
    
    if (password.length < 8) {
        showAuthMessage('Password must be at least 8 characters long.', 'error');
        return;
    }
    
    // Add loading state
    submitBtn.classList.add('loading');
    submitBtn.textContent = 'Creating Account...';
    
    try {
        // Simulate API call
        await simulateAuthRequest();
        
        // Store auth data
        const authData = {
            name: name,
            email: email,
            loginTime: new Date().toISOString(),
            isNewUser: true
        };
        
        sessionStorage.setItem('transverse_auth', JSON.stringify(authData));
        
        // Show success message
        showAuthMessage('Account created successfully! Redirecting...', 'success');
        
        // Redirect to main app after delay
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 1500);
        
    } catch (error) {
        showAuthMessage('Signup failed. Please try again.', 'error');
    } finally {
        // Remove loading state
        submitBtn.classList.remove('loading');
        submitBtn.textContent = 'Create Account';
    }
}

// Handle Google authentication
async function handleGoogleAuth(e) {
    e.preventDefault();
    const btn = e.currentTarget;
    const originalText = btn.textContent;
    
    btn.style.opacity = '0.7';
    btn.style.pointerEvents = 'none';
    btn.textContent = 'Connecting to Google...';
    
    try {
        // In a real app, this would integrate with Google OAuth
        // For demo purposes, we'll simulate the process
        await simulateAuthRequest();
        
        showAuthMessage('Google authentication not yet implemented. This is a demo.', 'info');
        
        // Simulate successful auth for demo
        const authData = {
            email: 'user@gmail.com',
            name: 'Google User',
            provider: 'google',
            loginTime: new Date().toISOString()
        };
        
        sessionStorage.setItem('transverse_auth', JSON.stringify(authData));
        
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 2000);
        
    } catch (error) {
        showAuthMessage('Google authentication failed.', 'error');
    } finally {
        btn.style.opacity = '1';
        btn.style.pointerEvents = 'auto';
        btn.textContent = originalText;
    }
}

// Handle Apple authentication
async function handleAppleAuth(e) {
    e.preventDefault();
    const btn = e.currentTarget;
    const originalText = btn.textContent;
    
    btn.style.opacity = '0.7';
    btn.style.pointerEvents = 'none';
    btn.textContent = 'Connecting to Apple...';
    
    try {
        // In a real app, this would integrate with Apple Sign In
        // For demo purposes, we'll simulate the process
        await simulateAuthRequest();
        
        showAuthMessage('Apple Sign In not yet implemented. This is a demo.', 'info');
        
        // Simulate successful auth for demo
        const authData = {
            email: 'user@icloud.com',
            name: 'Apple User',
            provider: 'apple',
            loginTime: new Date().toISOString()
        };
        
        sessionStorage.setItem('transverse_auth', JSON.stringify(authData));
        
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 2000);
        
    } catch (error) {
        showAuthMessage('Apple authentication failed.', 'error');
    } finally {
        btn.style.opacity = '1';
        btn.style.pointerEvents = 'auto';
        btn.textContent = originalText;
    }
}

// Validate password matching
function validatePasswordMatch() {
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const confirmField = document.getElementById('confirmPassword');
    
    if (confirmPassword && password !== confirmPassword) {
        confirmField.style.borderColor = '#e74c3c';
        confirmField.style.boxShadow = '0 0 0 3px rgba(231, 76, 60, 0.1)';
    } else {
        confirmField.style.borderColor = '#e1e5e9';
        confirmField.style.boxShadow = 'none';
    }
}

// Show authentication messages
function showAuthMessage(message, type = 'info') {
    // Remove existing messages
    const existingMessage = document.querySelector('.auth-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `auth-message auth-message-${type}`;
    messageDiv.textContent = message;
    
    // Style the message
    messageDiv.style.cssText = `
        position: fixed;
        top: 100px;
        left: 50%;
        transform: translateX(-50%);
        padding: 1rem 1.5rem;
        border-radius: 14px;
        font-family: 'Anonymous Pro', monospace;
        font-size: 0.9rem;
        font-weight: 500;
        z-index: 1000;
        max-width: 400px;
        text-align: center;
        animation: slideDown 0.3s ease;
    `;
    
    // Set colors based on type
    switch (type) {
        case 'success':
            messageDiv.style.background = '#d4edda';
            messageDiv.style.color = '#155724';
            messageDiv.style.border = '1px solid #c3e6cb';
            break;
        case 'error':
            messageDiv.style.background = '#f8d7da';
            messageDiv.style.color = '#721c24';
            messageDiv.style.border = '1px solid #f5c6cb';
            break;
        case 'info':
            messageDiv.style.background = '#d1ecf1';
            messageDiv.style.color = '#0c5460';
            messageDiv.style.border = '1px solid #bee5eb';
            break;
    }
    
    // Add to page
    document.body.appendChild(messageDiv);
    
    // Remove after delay
    setTimeout(() => {
        messageDiv.style.animation = 'slideUp 0.3s ease';
        setTimeout(() => messageDiv.remove(), 300);
    }, 4000);
}

// Simulate authentication request
function simulateAuthRequest() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            // Simulate 90% success rate
            if (Math.random() > 0.1) {
                resolve();
            } else {
                reject(new Error('Authentication failed'));
            }
        }, 1500);
    });
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateX(-50%) translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
    }
    
    @keyframes slideUp {
        from {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
        to {
            opacity: 0;
            transform: translateX(-50%) translateY(-20px);
        }
    }
`;
document.head.appendChild(style);
