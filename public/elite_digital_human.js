// Elite Digital Human Interface - Best in Class Implementation

class EliteDigitalHuman {
    constructor() {
        this.socket = null;
        this.sessionId = null;
        this.avatarMode = 'photorealistic';
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.avatar = null;
        this.mixer = null;
        this.animations = {};
        this.currentEmotion = 'neutral';
        this.isSpeaking = false;
        this.charts = {};
        this.voiceRecognition = null;
        this.speechSynthesis = window.speechSynthesis;
        
        this.init();
    }
    
    async init() {
        // Initialize WebSocket connection
        this.connectWebSocket();
        
        // Initialize premium avatar
        await this.initPhotorealisticAvatar();
        
        // Initialize charts
        this.initCharts();
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Initialize voice features
        this.initVoiceFeatures();
        
        // Apply premium animations
        this.applyPremiumAnimations();
        
        // Load user data
        this.loadUserData();
    }
    
    connectWebSocket() {
        try {
            this.socket = new WebSocket('ws://localhost:8000/ws');
            
            this.socket.onopen = () => {
                console.log('Connected to Digital Human server');
                this.updateStatus('online');
                this.sessionId = this.generateSessionId();
                
                this.socket.send(JSON.stringify({
                    type: 'startSession',
                    sessionId: this.sessionId,
                    premium: true
                }));
            };
            
            this.socket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleResponse(data);
            };
            
            this.socket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.updateStatus('error');
            };
            
            this.socket.onclose = () => {
                console.log('Disconnected from server');
                this.updateStatus('offline');
                setTimeout(() => this.connectWebSocket(), 3000);
            };
        } catch (error) {
            console.error('Failed to connect:', error);
            this.updateStatus('error');
        }
    }
    
    async initPhotorealisticAvatar() {
        const container = document.getElementById('premiumAvatar');
        
        // Initialize Three.js scene
        this.scene = new THREE.Scene();
        this.scene.background = null; // Transparent background
        
        // Premium lighting setup
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
        this.scene.add(ambientLight);
        
        const keyLight = new THREE.DirectionalLight(0xffffff, 0.8);
        keyLight.position.set(0.5, 1, 0.5);
        keyLight.castShadow = true;
        keyLight.shadow.mapSize.width = 2048;
        keyLight.shadow.mapSize.height = 2048;
        this.scene.add(keyLight);
        
        const fillLight = new THREE.DirectionalLight(0x88ccff, 0.5);
        fillLight.position.set(-0.5, 0.5, -0.5);
        this.scene.add(fillLight);
        
        const rimLight = new THREE.DirectionalLight(0xffffff, 0.3);
        rimLight.position.set(0, 0.5, -1);
        this.scene.add(rimLight);
        
        // Camera setup
        this.camera = new THREE.PerspectiveCamera(
            35,
            container.clientWidth / container.clientHeight,
            0.1,
            1000
        );
        this.camera.position.set(0, 0.6, 2.5);
        this.camera.lookAt(0, 0.5, 0);
        
        // Renderer with premium settings
        this.renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: true,
            powerPreference: "high-performance"
        });
        this.renderer.setSize(container.clientWidth, container.clientHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.renderer.outputEncoding = THREE.sRGBEncoding;
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 1.2;
        container.appendChild(this.renderer.domElement);
        
        // Load photorealistic avatar
        await this.loadPremiumAvatar();
        
        // Start animation loop
        this.animate();
        
        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());
    }
    
    async loadPremiumAvatar() {
        // Create a more realistic head shape
        const headGeometry = new THREE.SphereGeometry(0.45, 64, 64);
        headGeometry.scale(1, 1.2, 0.95); // Make head more oval
        
        // Enhanced skin material with better realism
        const skinMaterial = new THREE.MeshPhysicalMaterial({
            color: 0xffd4b3,
            roughness: 0.4,
            metalness: 0,
            clearcoat: 0.05,
            clearcoatRoughness: 0.4,
            reflectivity: 0.3,
            sheen: 0.5,
            sheenColor: 0xffc896,
            envMapIntensity: 0.3
        });
        
        this.avatar = new THREE.Group();
        
        // Head
        const head = new THREE.Mesh(headGeometry, skinMaterial);
        head.position.set(0, 0.1, 0);
        this.avatar.add(head);
        
        // Neck
        const neckGeometry = new THREE.CylinderGeometry(0.15, 0.2, 0.3, 16);
        const neck = new THREE.Mesh(neckGeometry, skinMaterial);
        neck.position.set(0, -0.35, 0);
        this.avatar.add(neck);
        
        this.avatar.position.set(0, 0.3, 0);
        this.scene.add(this.avatar);
        
        // Add facial features
        this.createFacialFeatures();
        
        // Initialize animation mixer
        this.mixer = new THREE.AnimationMixer(this.avatar);
        
        // Create basic animations
        this.createAnimations();
    }
    
    createFacialFeatures() {
        // Get the head mesh (first child of avatar group)
        const head = this.avatar.children[0];
        
        // Eyes
        const eyeGeometry = new THREE.SphereGeometry(0.08, 32, 32);
        const eyeMaterial = new THREE.MeshPhysicalMaterial({
            color: 0xffffff,
            roughness: 0.2,
            metalness: 0.1,
            clearcoat: 0.8,
            clearcoatRoughness: 0
        });
        
        const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        leftEye.position.set(-0.13, 0.15, 0.38);
        head.add(leftEye);
        
        const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        rightEye.position.set(0.13, 0.15, 0.38);
        head.add(rightEye);
        
        // Iris
        const irisGeometry = new THREE.SphereGeometry(0.05, 16, 16);
        const irisMaterial = new THREE.MeshPhysicalMaterial({ 
            color: 0x4a90e2,
            roughness: 0.3,
            metalness: 0.2
        });
        
        const leftIris = new THREE.Mesh(irisGeometry, irisMaterial);
        leftIris.position.set(0, 0, 0.04);
        leftEye.add(leftIris);
        
        const rightIris = new THREE.Mesh(irisGeometry, irisMaterial);
        rightIris.position.set(0, 0, 0.04);
        rightEye.add(rightIris);
        
        // Pupils
        const pupilGeometry = new THREE.SphereGeometry(0.02, 16, 16);
        const pupilMaterial = new THREE.MeshBasicMaterial({ color: 0x000000 });
        
        const leftPupil = new THREE.Mesh(pupilGeometry, pupilMaterial);
        leftPupil.position.set(0, 0, 0.02);
        leftIris.add(leftPupil);
        
        const rightPupil = new THREE.Mesh(pupilGeometry, pupilMaterial);
        rightPupil.position.set(0, 0, 0.02);
        rightIris.add(rightPupil);
        
        // Mouth
        const mouthGeometry = new THREE.BoxGeometry(0.2, 0.03, 0.1);
        const mouthMaterial = new THREE.MeshPhysicalMaterial({
            color: 0xcc9988,
            roughness: 0.8
        });
        
        const mouth = new THREE.Mesh(mouthGeometry, mouthMaterial);
        mouth.position.set(0, -0.15, 0.38);
        head.add(mouth);
        
        // Nose
        const noseGeometry = new THREE.ConeGeometry(0.04, 0.1, 4);
        const noseMaterial = new THREE.MeshPhysicalMaterial({
            color: 0xffd4b3,
            roughness: 0.4
        });
        const nose = new THREE.Mesh(noseGeometry, noseMaterial);
        nose.position.set(0, 0, 0.45);
        nose.rotation.x = Math.PI / 2;
        head.add(nose);
        
        // Store references for animation
        this.facialFeatures = {
            leftEye,
            rightEye,
            leftIris,
            rightIris,
            leftPupil,
            rightPupil,
            mouth,
            head
        };
    }
    
    createAnimations() {
        // Idle animation
        const idleTrack = new THREE.VectorKeyframeTrack(
            '.position',
            [0, 2, 4],
            [0, 0.5, 0, 0, 0.52, 0, 0, 0.5, 0]
        );
        
        const idleClip = new THREE.AnimationClip('idle', 4, [idleTrack]);
        this.animations.idle = this.mixer.clipAction(idleClip);
        this.animations.idle.play();
        
        // Speaking animation
        const speakingTrack = new THREE.VectorKeyframeTrack(
            '.scale',
            [0, 0.1, 0.2],
            [1, 1, 1, 1.02, 0.98, 1, 1, 1, 1]
        );
        
        const speakingClip = new THREE.AnimationClip('speaking', 0.2, [speakingTrack]);
        this.animations.speaking = this.mixer.clipAction(speakingClip);
        this.animations.speaking.setLoop(THREE.LoopRepeat);
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        const delta = this.clock ? this.clock.getDelta() : 0.016;
        
        if (this.mixer) {
            this.mixer.update(delta);
        }
        
        // Subtle head movement
        if (this.avatar) {
            this.avatar.rotation.y = Math.sin(Date.now() * 0.0005) * 0.1;
            this.avatar.rotation.x = Math.sin(Date.now() * 0.0007) * 0.05;
        }
        
        // Eye tracking (follows mouse)
        this.updateEyeTracking();
        
        // Render scene
        if (this.renderer && this.scene && this.camera) {
            this.renderer.render(this.scene, this.camera);
        }
    }
    
    updateEyeTracking() {
        if (!this.facialFeatures) return;
        
        // Get mouse position
        const mouse = this.getMousePosition();
        
        // Calculate eye rotation
        const lookX = mouse.x * 0.3;
        const lookY = mouse.y * 0.3;
        
        // Rotate eyes
        this.facialFeatures.leftEye.rotation.y = lookX * 0.2;
        this.facialFeatures.leftEye.rotation.x = -lookY * 0.1;
        
        this.facialFeatures.rightEye.rotation.y = lookX * 0.2;
        this.facialFeatures.rightEye.rotation.x = -lookY * 0.1;
    }
    
    initCharts() {
        // Performance Chart
        const performanceCtx = document.getElementById('performanceChart').getContext('2d');
        this.charts.performance = new Chart(performanceCtx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Portfolio Value',
                    data: [2400000, 2420000, 2380000, 2450000, 2480000, 2470000, 2451329],
                    borderColor: '#0066FF',
                    backgroundColor: 'rgba(0, 102, 255, 0.1)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        ticks: {
                            callback: (value) => '$' + (value / 1000000).toFixed(1) + 'M',
                            color: '#8B92A9'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        }
                    },
                    x: {
                        ticks: { color: '#8B92A9' },
                        grid: { display: false }
                    }
                }
            }
        });
        
        // Allocation Chart
        const allocationCtx = document.getElementById('allocationChart').getContext('2d');
        this.charts.allocation = new Chart(allocationCtx, {
            type: 'doughnut',
            data: {
                labels: ['Stocks', 'Bonds', 'Real Estate', 'Crypto', 'Cash'],
                datasets: [{
                    data: [45, 25, 15, 10, 5],
                    backgroundColor: [
                        '#0066FF',
                        '#00D4AA',
                        '#FF6B00',
                        '#FFB800',
                        '#8B92A9'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#8B92A9',
                            padding: 20
                        }
                    }
                }
            }
        });
    }
    
    setupEventListeners() {
        // Chat input
        const chatInput = document.getElementById('chatInput');
        const sendBtn = document.getElementById('sendBtn');
        
        sendBtn.addEventListener('click', () => this.sendMessage());
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
        
        // Voice button
        const micBtn = document.getElementById('micBtn');
        micBtn.addEventListener('click', () => this.toggleVoiceInput());
        
        // Settings
        const settingsBtn = document.getElementById('settingsBtn');
        const settingsPanel = document.getElementById('settingsPanel');
        const closeSettings = document.getElementById('closeSettings');
        
        settingsBtn.addEventListener('click', () => {
            settingsPanel.style.display = 'block';
            gsap.fromTo(settingsPanel, 
                { opacity: 0, x: 50 }, 
                { opacity: 1, x: 0, duration: 0.3 }
            );
        });
        
        closeSettings.addEventListener('click', () => {
            gsap.to(settingsPanel, {
                opacity: 0,
                x: 50,
                duration: 0.3,
                onComplete: () => settingsPanel.style.display = 'none'
            });
        });
        
        // Avatar mode toggle
        const avatarModeBtn = document.getElementById('avatarModeBtn');
        avatarModeBtn.addEventListener('click', () => this.toggleAvatarMode());
        
        // Quick actions
        document.querySelectorAll('.action-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.currentTarget.querySelector('span').textContent;
                this.handleQuickAction(action);
            });
        });
        
        // Suggestion chips
        document.querySelectorAll('.suggestion-chip').forEach(chip => {
            chip.addEventListener('click', (e) => {
                chatInput.value = e.target.textContent;
                this.sendMessage();
            });
        });
    }
    
    sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message to chat
        this.addMessage('user', message);
        
        // Clear input
        input.value = '';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        // Send to server
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({
                type: 'message',
                content: message,
                sessionId: this.sessionId,
                timestamp: new Date().toISOString()
            }));
        } else {
            console.warn('WebSocket not connected, using demo response');
            // Demo response if not connected
            setTimeout(() => {
                this.handleResponse({
                    type: 'response',
                    content: `I understand you're asking about "${message}". Let me analyze your portfolio and provide insights.`,
                    emotion: 'thinking'
                });
            }, 1000);
        }
        
        // Trigger speaking animation
        this.setSpeaking(true);
    }
    
    addMessage(sender, content) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender} fade-in slide-up`;
        
        const avatar = sender === 'user' ? 'You' : 'AI';
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                <p class="message-text">${content}</p>
                <span class="message-time">${time}</span>
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    handleResponse(data) {
        // Hide typing indicator
        this.hideTypingIndicator();
        
        // Stop speaking animation
        this.setSpeaking(false);
        
        if (data.type === 'response') {
            this.addMessage('ai', data.content);
            
            // Speak response if voice is enabled
            if (this.voiceEnabled) {
                this.speak(data.content);
            }
            
            // Update emotion based on response
            if (data.emotion) {
                this.setEmotion(data.emotion);
            }
        }
        
        // Update charts if data is provided
        if (data.chartData) {
            this.updateCharts(data.chartData);
        }
    }
    
    setSpeaking(isSpeaking) {
        this.isSpeaking = isSpeaking;
        
        if (isSpeaking && this.animations.speaking) {
            this.animations.speaking.play();
        } else if (this.animations.speaking) {
            this.animations.speaking.stop();
        }
    }
    
    setEmotion(emotion) {
        this.currentEmotion = emotion;
        
        // Adjust avatar appearance based on emotion
        if (this.avatar) {
            switch(emotion) {
                case 'happy':
                    gsap.to(this.avatar.material.color, { r: 1, g: 0.9, b: 0.8 });
                    break;
                case 'concerned':
                    gsap.to(this.avatar.material.color, { r: 0.9, g: 0.85, b: 0.8 });
                    break;
                case 'neutral':
                default:
                    gsap.to(this.avatar.material.color, { r: 1, g: 0.86, b: 0.68 });
            }
        }
    }
    
    speak(text) {
        if (!this.speechSynthesis) return;
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.volume = 0.9;
        
        // Premium voice selection
        const voices = this.speechSynthesis.getVoices();
        const premiumVoice = voices.find(voice => 
            voice.name.includes('Samantha') || 
            voice.name.includes('Alex') ||
            voice.quality === 'premium'
        );
        
        if (premiumVoice) {
            utterance.voice = premiumVoice;
        }
        
        utterance.onstart = () => this.setSpeaking(true);
        utterance.onend = () => this.setSpeaking(false);
        
        this.speechSynthesis.speak(utterance);
    }
    
    initVoiceFeatures() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.voiceRecognition = new SpeechRecognition();
            this.voiceRecognition.continuous = false;
            this.voiceRecognition.interimResults = true;
            
            this.voiceRecognition.onresult = (event) => {
                const transcript = Array.from(event.results)
                    .map(result => result[0].transcript)
                    .join('');
                
                document.getElementById('chatInput').value = transcript;
                
                if (event.results[0].isFinal) {
                    this.sendMessage();
                }
            };
        }
    }
    
    toggleVoiceInput() {
        if (!this.voiceRecognition) return;
        
        const micBtn = document.getElementById('micBtn');
        
        if (this.isListening) {
            this.voiceRecognition.stop();
            micBtn.classList.remove('active');
            this.isListening = false;
        } else {
            this.voiceRecognition.start();
            micBtn.classList.add('active');
            this.isListening = true;
            
            // Show voice visualization
            const voiceViz = document.getElementById('voiceViz');
            voiceViz.style.display = 'flex';
            
            this.animateVoiceVisualization();
        }
    }
    
    animateVoiceVisualization() {
        const bars = document.querySelectorAll('.voice-bar');
        
        bars.forEach((bar, index) => {
            gsap.to(bar, {
                scaleY: Math.random() * 2 + 0.5,
                duration: 0.2,
                repeat: -1,
                yoyo: true,
                delay: index * 0.1,
                ease: 'power2.inOut'
            });
        });
    }
    
    applyPremiumAnimations() {
        // Animate logo on hover
        const logo = document.querySelector('.logo');
        logo.addEventListener('mouseenter', () => {
            gsap.to(logo, { scale: 1.1, duration: 0.3, ease: 'power2.out' });
        });
        logo.addEventListener('mouseleave', () => {
            gsap.to(logo, { scale: 1, duration: 0.3, ease: 'power2.out' });
        });
        
        // Animate cards on scroll
        gsap.utils.toArray('.chart-container').forEach(container => {
            gsap.fromTo(container,
                { y: 30, opacity: 0 },
                {
                    y: 0,
                    opacity: 1,
                    duration: 0.8,
                    stagger: 0.2,
                    ease: 'power3.out',
                    scrollTrigger: {
                        trigger: container,
                        start: 'top 90%'
                    }
                }
            );
        });
        
        // Hover effects for buttons
        document.querySelectorAll('.action-btn, .control-btn').forEach(btn => {
            btn.addEventListener('mouseenter', () => {
                gsap.to(btn, { scale: 1.05, duration: 0.2 });
            });
            btn.addEventListener('mouseleave', () => {
                gsap.to(btn, { scale: 1, duration: 0.2 });
            });
        });
    }
    
    showTypingIndicator() {
        const indicator = document.querySelector('.typing-indicator');
        indicator.style.display = 'flex';
        
        // Animate dots
        gsap.to('.typing-indicator .dot', {
            y: -10,
            duration: 0.4,
            stagger: 0.1,
            repeat: -1,
            yoyo: true,
            ease: 'power2.inOut'
        });
    }
    
    hideTypingIndicator() {
        const indicator = document.querySelector('.typing-indicator');
        indicator.style.display = 'none';
        gsap.killTweensOf('.typing-indicator .dot');
    }
    
    onWindowResize() {
        const container = document.getElementById('premiumAvatar');
        this.camera.aspect = container.clientWidth / container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(container.clientWidth, container.clientHeight);
    }
    
    getMousePosition() {
        // For eye tracking
        return {
            x: (this.mouseX || 0) / window.innerWidth * 2 - 1,
            y: -(this.mouseY || 0) / window.innerHeight * 2 + 1
        };
    }
    
    loadUserData() {
        // Load premium user data
        fetch('/api/user/premium-data')
            .then(response => response.json())
            .then(data => {
                // Update UI with user data
                if (data.portfolio) {
                    this.updatePortfolioDisplay(data.portfolio);
                }
            })
            .catch(error => {
                console.log('Loading with demo data');
                this.loadDemoData();
            });
    }
    
    loadDemoData() {
        // Premium demo data
        const demoData = {
            portfolio: {
                value: 2451329,
                change: 0.125,
                changeAmount: 274891
            },
            performance: {
                daily: [2400000, 2420000, 2380000, 2450000, 2480000, 2470000, 2451329]
            }
        };
        
        this.updatePortfolioDisplay(demoData.portfolio);
    }
    
    updatePortfolioDisplay(portfolio) {
        const valueElement = document.querySelector('.portfolio-value');
        const changeElement = document.querySelector('.portfolio-change');
        
        if (valueElement) {
            valueElement.textContent = this.formatCurrency(portfolio.value);
        }
        
        if (changeElement) {
            const isPositive = portfolio.change >= 0;
            changeElement.className = `portfolio-change ${isPositive ? '' : 'negative'}`;
            changeElement.innerHTML = `
                <i class="fas fa-trending-${isPositive ? 'up' : 'down'}"></i>
                <span>${isPositive ? '+' : ''}${(portfolio.change * 100).toFixed(1)}% ($${this.formatNumber(Math.abs(portfolio.changeAmount))})</span>
            `;
        }
    }
    
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount);
    }
    
    formatNumber(num) {
        return new Intl.NumberFormat('en-US').format(num);
    }
    
    generateSessionId() {
        return 'premium_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    updateStatus(status) {
        const statusDot = document.querySelector('.status-dot');
        const statusText = document.querySelector('.status-text');
        
        switch(status) {
            case 'online':
                statusDot.style.background = '#00D4AA';
                statusText.textContent = 'AI Assistant Active';
                break;
            case 'offline':
                statusDot.style.background = '#8B92A9';
                statusText.textContent = 'Reconnecting...';
                break;
            case 'error':
                statusDot.style.background = '#FF4757';
                statusText.textContent = 'Connection Error';
                break;
        }
    }
    
    handleQuickAction(action) {
        const actionMap = {
            'Analyze': 'Perform a comprehensive analysis of my portfolio',
            'Rebalance': 'Suggest optimal portfolio rebalancing',
            'Tax Report': 'Generate tax optimization report',
            'Risk Analysis': 'Conduct risk assessment of my investments'
        };
        
        const message = actionMap[action] || `Execute ${action}`;
        document.getElementById('chatInput').value = message;
        this.sendMessage();
    }
}

// Initialize premium interface
document.addEventListener('DOMContentLoaded', () => {
    window.eliteDigitalHuman = new EliteDigitalHuman();
    
    // Add premium visual effects
    gsap.fromTo('.elite-header', 
        { y: -100, opacity: 0 }, 
        { y: 0, opacity: 1, duration: 1, ease: 'power3.out' }
    );
    
    gsap.fromTo('.premium-sidebar',
        { x: -100, opacity: 0 },
        { x: 0, opacity: 1, duration: 0.8, delay: 0.2, ease: 'power3.out' }
    );
    
    gsap.fromTo('.chat-section',
        { x: 100, opacity: 0 },
        { x: 0, opacity: 1, duration: 0.8, delay: 0.3, ease: 'power3.out' }
    );
    
    gsap.fromTo('.avatar-section',
        { scale: 0.9, opacity: 0 },
        { scale: 1, opacity: 1, duration: 1, delay: 0.4, ease: 'power3.out' }
    );
});

// Premium mouse tracking for avatar
document.addEventListener('mousemove', (e) => {
    if (window.eliteDigitalHuman) {
        window.eliteDigitalHuman.mouseX = e.clientX;
        window.eliteDigitalHuman.mouseY = e.clientY;
    }
});

// Initialize clock for animations
if (window.eliteDigitalHuman) {
    window.eliteDigitalHuman.clock = new THREE.Clock();
}