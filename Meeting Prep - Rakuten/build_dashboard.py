import os
import sys

# DIR is always the folder this script lives in — safe to copy to any Meeting Prep folder.
DIR = os.path.dirname(os.path.abspath(__file__))

# Derive company name from the folder name automatically
folder_name = os.path.basename(DIR)
COMPANY_NAME = folder_name.replace('Meeting Prep - ', '').strip() or 'Meeting Prep'

def read_file(path):
    try:
        with open(os.path.join(DIR, path), 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""

briefing = read_file('01_briefing_doc.md').replace("</script>", "<\\/script>")
intel = read_file('03_competitive_intel.md').replace("</script>", "<\\/script>")
research = read_file('02_deep_research_report.md').replace("</script>", "<\\/script>")

# Escape for JS template literal
quiz = read_file('06_pre_call_quiz.md').replace("\\\\", "\\\\\\\\").replace("`", "\\\\`").replace("$", "\\\\$").replace("</script>", "<\\/script>")
flashcards = read_file('07_flashcards.md').replace("\\\\", "\\\\\\\\").replace("`", "\\\\`").replace("$", "\\\\$").replace("</script>", "<\\/script>")

template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meeting Prep - {{COMPANY_NAME}}</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        darkBg: '#08080c',
                        primary: '#1d4ed8', // blue-700
                        accent: '#eab308', // gold/yellow-500
                    },
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    }
                }
            }
        }
    </script>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Marked.js -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    
    <style>
        body {
            background-color: #08080c;
            color: #f3f4f6;
            background-image: radial-gradient(circle at 15% 50%, rgba(29, 78, 216, 0.15), transparent 25%),
                              radial-gradient(circle at 85% 30%, rgba(234, 179, 8, 0.1), transparent 25%);
            background-attachment: fixed;
        }
        .glass {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        /* Markdown Styling */
        .markdown-content h1 { font-size: 2rem; font-weight: 700; margin-bottom: 1rem; color: #eab308; }
        .markdown-content h2 { font-size: 1.5rem; font-weight: 600; margin-top: 2rem; margin-bottom: 0.75rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem; color: #60a5fa;}
        .markdown-content h3 { font-size: 1.25rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem; }
        .markdown-content p { margin-bottom: 1rem; line-height: 1.6; }
        .markdown-content ul { list-style-type: disc; padding-left: 1.5rem; margin-bottom: 1rem; }
        .markdown-content li { margin-bottom: 0.5rem; }
        .markdown-content strong { color: #fff; font-weight: 600; }
        .markdown-content a { color: #60a5fa; text-decoration: underline; }
        .markdown-content table { width: 100%; border-collapse: collapse; margin-top: 1rem; margin-bottom: 1.5rem; }
        .markdown-content th, .markdown-content td { border: 1px solid rgba(255,255,255,0.1); padding: 0.75rem; text-align: left; }
        .markdown-content th { background-color: rgba(255,255,255,0.05); font-weight: 600; color: #eab308; }
        
        /* Flashcard 3D */
        .perspective-1000 { perspective: 1000px; }
        .transform-style-3d { transform-style: preserve-3d; }
        .backface-hidden { backface-visibility: hidden; }
        .rotate-y-180 { transform: rotateY(180deg); }
        .card-transition { transition: transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1); }
        
        /* Audio Visualizer */
        .bar {
            width: 4px;
            height: 10px;
            background-color: #60a5fa;
            margin: 0 2px;
            border-radius: 2px;
            display: inline-block;
            animation: bounce 1s infinite alternate;
        }
        .bar:nth-child(even) { animation-delay: 0.3s; background-color: #eab308; }
        .bar:nth-child(3n) { animation-delay: 0.6s; }
        @keyframes bounce {
            0% { transform: scaleY(1); }
            100% { transform: scaleY(3); }
        }
        .paused .bar { animation-play-state: paused; }
    </style>
</head>
<body class="min-h-screen flex flex-col font-sans">
    <!-- Navbar -->
    <nav class="glass flex justify-between items-center px-6 py-4 sticky top-0 z-50">
        <div class="flex items-center space-x-3">
            <div class="w-8 h-8 rounded bg-gradient-to-br from-primary to-accent flex items-center justify-center text-white font-bold text-lg"><i class="fa-solid fa-rocket"></i></div>
            <span class="text-xl font-bold tracking-wider">ANTIGRAVITY <span class="text-accent font-light">OS</span></span>
        </div>
        <div class="flex items-center space-x-4">
            <span class="px-3 py-1 rounded-full bg-blue-900/40 text-blue-300 text-sm border border-blue-500/30 flex items-center"><i class="fa-regular fa-calendar mr-2"></i> Upcoming Meeting</span>
            <button class="bg-white/10 hover:bg-white/20 transition px-4 py-2 rounded text-sm flex items-center shadow" onclick="window.print()">
                <i class="fa-solid fa-file-pdf mr-2 text-accent"></i> Export PDF
            </button>
        </div>
    </nav>

    <!-- Header -->
    <header class="glass mx-6 mt-6 p-8 rounded-xl flex flex-col md:flex-row justify-between items-center relative overflow-hidden">
        <div class="absolute right-0 top-0 w-64 h-64 bg-accent/10 rounded-full filter blur-3xl -z-10 translate-x-1/2 -translate-y-1/4"></div>
        <div class="z-10 mb-6 md:mb-0">
            <h1 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-accent mb-2">{{COMPANY_NAME}}</h1>
            <p class="text-gray-400 text-lg">Meeting Preparation & Intelligence Dashboard</p>
        </div>
        <div class="glass p-4 rounded-lg flex items-center space-x-4 z-10 w-full md:w-auto">
            <button id="playBtn" class="w-12 h-12 rounded-full bg-gradient-to-r from-primary to-blue-600 flex items-center justify-center text-white hover:scale-105 transition shadow-lg shadow-blue-500/30">
                <i class="fa-solid fa-play" id="playIcon"></i>
            </button>
            <div>
                <p class="text-sm text-gray-300 mb-1 font-medium">AI Audio Briefing</p>
                <div class="flex items-end h-6 paused" id="visualizer">
                    <div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div>
                </div>
            </div>
            <audio id="audioElement" src="audio_briefing.mp3"></audio>
        </div>
    </header>

    <!-- Main Content -->
    <div class="flex-1 mx-6 mt-6 mb-12 flex flex-col md:flex-row gap-6">
        <!-- Sidebar -->
        <aside class="w-full md:w-64 flex-shrink-0">
            <div class="glass rounded-xl p-3 flex flex-col space-y-1 sticky top-24">
                <button class="tab-btn active w-full text-left px-4 py-3 rounded-lg flex items-center text-gray-300 hover:bg-white/5 transition" data-target="briefing">
                    <i class="fa-solid fa-file-signature w-6 text-blue-400 mr-3"></i> Executive Briefing
                </button>
                <button class="tab-btn w-full text-left px-4 py-3 rounded-lg flex items-center text-gray-300 hover:bg-white/5 transition" data-target="intel">
                    <i class="fa-solid fa-chess-knight w-6 text-accent mr-3"></i> Competitive Intel
                </button>
                <button class="tab-btn w-full text-left px-4 py-3 rounded-lg flex items-center text-gray-300 hover:bg-white/5 transition" data-target="research">
                    <i class="fa-solid fa-microscope w-6 text-purple-400 mr-3"></i> Deep Research
                </button>
                <div class="h-px bg-white/10 my-2"></div>
                <button class="tab-btn w-full text-left px-4 py-3 rounded-lg flex items-center text-gray-300 hover:bg-white/5 transition" data-target="infographic">
                    <i class="fa-solid fa-chart-line w-6 text-emerald-400 mr-3"></i> Market Infographic
                </button>
                <div class="h-px bg-white/10 my-2"></div>
                <button class="tab-btn w-full text-left px-4 py-3 rounded-lg flex items-center text-gray-300 hover:bg-white/5 transition" data-target="quiz">
                    <i class="fa-solid fa-clipboard-question w-6 text-orange-400 mr-3"></i> Knowledge Quiz
                </button>
                <button class="tab-btn w-full text-left px-4 py-3 rounded-lg flex items-center text-gray-300 hover:bg-white/5 transition" data-target="flashcards">
                    <i class="fa-solid fa-layer-group w-6 text-indigo-400 mr-3"></i> Flashcards
                </button>
            </div>
        </aside>

        <!-- Content Area -->
        <main class="glass flex-1 rounded-xl p-8 min-h-[600px] relative overflow-hidden">
            <!-- Briefing -->
            <div id="content-briefing" class="tab-content block markdown-content"></div>
            <!-- Intel -->
            <div id="content-intel" class="tab-content hidden markdown-content"></div>
            <!-- Research -->
            <div id="content-research" class="tab-content hidden markdown-content"></div>
            
            <!-- Infographic -->
            <div id="content-infographic" class="tab-content hidden">
                <h2 class="text-2xl font-bold mb-6 text-accent">Market Landscape Infographic</h2>
                <div class="rounded-xl overflow-hidden border border-white/10 bg-white/5 p-4 flex justify-center">
                    <img src="04_market_infographic.png" alt="Market Infographic" class="max-w-full h-auto rounded drop-shadow-2xl">
                </div>
            </div>

            <!-- Quiz -->
            <div id="content-quiz" class="tab-content hidden h-full flex flex-col">
                <h2 class="text-2xl font-bold mb-6 text-accent">Knowledge Readiness Test</h2>
                <div id="quiz-container" class="max-w-3xl mx-auto w-full flex-1">
                    <!-- Quiz dynamically rendered here -->
                </div>
            </div>

            <!-- Flashcards -->
            <div id="content-flashcards" class="tab-content hidden h-full flex flex-col items-center justify-center">
                <h2 class="text-2xl font-bold mb-8 text-accent self-start w-full">Rapid Review Flashcards</h2>
                
                <div class="relative w-full max-w-2xl aspect-[3/2] perspective-1000 cursor-pointer mx-auto" id="flashcard-container" onclick="flipCard()">
                    <div id="flashcard-inner" class="w-full h-full relative transform-style-3d card-transition shadow-2xl">
                        <!-- Front -->
                        <div class="absolute w-full h-full backface-hidden rounded-2xl bg-gradient-to-br from-blue-900 to-indigo-900 border border-blue-500/30 p-10 flex flex-col items-center justify-center text-center">
                            <span class="absolute top-4 left-4 text-blue-400/50 text-sm font-bold uppercase tracking-widest">Question</span>
                            <i class="fa-regular fa-circle-question text-4xl text-blue-400/30 mb-6"></i>
                            <h3 id="fc-question" class="text-3xl font-semibold leading-relaxed text-white">Loading...</h3>
                            <span class="absolute bottom-4 text-gray-400 text-sm"><i class="fa-solid fa-hand-pointer mr-1"></i> Click to flip</span>
                        </div>
                        <!-- Back -->
                        <div class="absolute w-full h-full backface-hidden rotate-y-180 rounded-2xl bg-gradient-to-br from-yellow-900 to-orange-900 border border-yellow-500/30 p-10 flex flex-col items-center justify-center text-center overflow-y-auto">
                            <span class="absolute top-4 left-4 text-yellow-400/50 text-sm font-bold uppercase tracking-widest">Answer</span>
                            <i class="fa-regular fa-lightbulb text-4xl text-yellow-400/30 mb-6"></i>
                            <p id="fc-answer" class="text-2xl leading-relaxed text-white">Loading...</p>
                        </div>
                    </div>
                </div>
                
                <div class="flex items-center space-x-8 mt-10">
                    <button onclick="prevCard()" class="w-12 h-12 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition focus:outline-none"><i class="fa-solid fa-chevron-left"></i></button>
                    <div class="text-lg font-medium"><span id="fc-current" class="text-accent">1</span> / <span id="fc-total">10</span></div>
                    <button onclick="nextCard()" class="w-12 h-12 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition focus:outline-none"><i class="fa-solid fa-chevron-right"></i></button>
                </div>
                <!-- Progress dots -->
                <div id="fc-dots" class="flex space-x-2 mt-6"></div>
            </div>
        </main>
    </div>

    <!-- Data Injection -->
    <script type="text/markdown" id="md-briefing">{{BRIEFING_MD}}</script>
    <script type="text/markdown" id="md-intel">{{INTEL_MD}}</script>
    <script type="text/markdown" id="md-research">{{RESEARCH_MD}}</script>

    <script>
        // Data parsed from python injection
        const rawQuiz = `{{QUIZ_MD}}`;
        const rawFlashcards = `{{FLASHCARDS_MD}}`;

        // 1. Markdown Parsing
        document.getElementById('content-briefing').innerHTML = marked.parse(document.getElementById('md-briefing').textContent);
        document.getElementById('content-intel').innerHTML = marked.parse(document.getElementById('md-intel').textContent);
        document.getElementById('content-research').innerHTML = marked.parse(document.getElementById('md-research').textContent);

        // 2. Tab Navigation
        const tabs = document.querySelectorAll('.tab-btn');
        const contents = document.querySelectorAll('.tab-content');

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                tabs.forEach(t => {
                    t.classList.remove('active', 'bg-white/10', 'border-l-4', 'border-accent');
                });
                tab.classList.add('active', 'bg-white/10', 'border-l-4', 'border-accent');
                
                contents.forEach(c => c.classList.add('hidden'));
                document.getElementById('content-' + tab.dataset.target).classList.remove('hidden');
            });
        });

        // Initialize first tab
        tabs[0].classList.add('active', 'bg-white/10', 'border-l-4', 'border-accent');

        // 3. Audio Player Logic
        const audio = document.getElementById('audioElement');
        const playBtn = document.getElementById('playBtn');
        const playIcon = document.getElementById('playIcon');
        const visualizer = document.getElementById('visualizer');

        playBtn.addEventListener('click', () => {
            if (audio.paused) {
                audio.play();
                playIcon.classList.remove('fa-play');
                playIcon.classList.add('fa-pause');
                visualizer.classList.remove('paused');
            } else {
                audio.pause();
                playIcon.classList.remove('fa-pause');
                playIcon.classList.add('fa-play');
                visualizer.classList.add('paused');
            }
        });

        // 4. Parser for Quiz & Flashcards
        function parseQA(text) {
            const pairs = [];
            // Handle specific format from NotebookLM
            let combined = text.replace(/\\*\\*Question.*?\\*\\*|Q:|Question:|\\*\\*Q.*?\\*\\*/gi, '%%%Q%%%');
            combined = combined.replace(/\\*\\*Answer.*?\\*\\*|A:|Answer:|\\*\\*A.*?\\*\\*/gi, '%%%A%%%');
            
            let parts = combined.split('%%%Q%%%');
            for(let i=1; i<parts.length; i++) {
                let qaPart = parts[i].split('%%%A%%%');
                if(qaPart.length >= 2) {
                    let q = qaPart[0].trim().replace(/^[^a-zA-Z0-9]+/, '');
                    let a = qaPart[1].split('%%%Q%%%')[0].trim().replace(/^[^a-zA-Z0-9]+/, '');
                    pairs.push({q, a});
                }
            }
            if(pairs.length === 0) {
                let chunks = text.split('\\n\\n').filter(x => x.trim().length > 10);
                for(let i=0; i<chunks.length-1; i+=2) {
                    pairs.push({q: chunks[i], a: chunks[i+1]});
                }
            }
            return pairs.length > 0 ? pairs : [{q: "Could not parse flashcards.", a: "Check the raw markdown file."}];
        }

        function parseQuiz(text) {
            let questions = [];
            let parts = text.split(/\\*\\*Question [0-9]+.*?\\*\\*|Question [0-9]+:|^[0-9]+\\./gm).filter(x => x.trim().length > 10);
            
            if(parts.length < 2) return [];
            
            for(let p of parts) {
                if(p.toLowerCase().includes("answer key") || p.toLowerCase().includes("answers:")) continue;
                
                let lines = p.trim().split('\\n').filter(l => l.trim().length > 0);
                let title = lines[0];
                let options = [];
                let correctOpt = -1; 
                
                for(let i=1; i<lines.length; i++) {
                    let l = lines[i].trim();
                    if(l.match(/^[A-E][\\.\\)]|^- /i)) {
                        let isCorrect = l.includes('**') || l.includes('Correct');
                        let cleanText = l.replace(/^[A-E][\\.\\)]|^- |\\*\\*/gi, '').trim();
                        options.push(cleanText);
                        if(isCorrect) correctOpt = options.length - 1;
                    }
                }
                
                if(options.length > 0) {
                    if(correctOpt === -1) correctOpt = 0; 
                    questions.push({q: title, opts: options, ans: correctOpt});
                }
            }
            
            return questions;
        }

        // Initialize Flashcards
        const fcData = parseQA(rawFlashcards);
        let currFc = 0;
        let isFlipped = false;
        
        function updateFC() {
            document.getElementById('fc-question').innerHTML = marked.parseInline(fcData[currFc].q);
            document.getElementById('fc-answer').innerHTML = marked.parseInline(fcData[currFc].a);
            document.getElementById('fc-current').innerText = currFc + 1;
            document.getElementById('fc-total').innerText = fcData.length;
            
            const dots = document.getElementById('fc-dots');
            dots.innerHTML = '';
            for(let i=0; i<fcData.length; i++) {
                dots.innerHTML += `<div class="w-2 h-2 rounded-full ${i===currFc ? 'bg-accent' : 'bg-white/20'} transition-colors"></div>`;
            }
        }
        
        window.flipCard = function() {
            isFlipped = !isFlipped;
            const inner = document.getElementById('flashcard-inner');
            if(isFlipped) {
                inner.classList.add('rotate-y-180');
            } else {
                inner.classList.remove('rotate-y-180');
            }
        };
        
        window.nextCard = function(e) {
            if (e) e.stopPropagation();
            if(isFlipped) { flipCard(); setTimeout(() => changeFC(1), 300); }
            else changeFC(1);
        };
        
        window.prevCard = function(e) {
            if (e) e.stopPropagation();
            if(isFlipped) { flipCard(); setTimeout(() => changeFC(-1), 300); }
            else changeFC(-1);
        };

        function changeFC(dir) {
            currFc = (currFc + dir + fcData.length) % fcData.length;
            updateFC();
        }
        
        updateFC();

        // Initialize Quiz
        const quizData = parseQuiz(rawQuiz);
        const quizContainer = document.getElementById('quiz-container');
        
        if(quizData.length === 0) {
            quizContainer.innerHTML = `<div class="glass p-8 rounded-xl"><p>Please view the raw 06_pre_call_quiz.md file for the complete quiz context.</p></div>`;
        } else {
            let qHTML = '';
            quizData.forEach((q, idx) => {
                qHTML += `
                <div class="glass p-6 rounded-xl mb-6">
                    <h3 class="text-xl font-semibold mb-4 text-blue-200">${idx+1}. ${q.q}</h3>
                    <div class="space-y-3">
                `;
                q.opts.forEach((opt, oidx) => {
                    qHTML += `
                        <button class="quiz-opt-${idx} w-full text-left p-4 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 transition flex items-center justify-between" onclick="selectOpt(${idx}, ${oidx}, ${q.ans}, this)">
                            <span>${opt}</span>
                            <i class="fa-solid fa-circle-check text-green-500 opacity-0 transition-opacity"></i>
                            <i class="fa-solid fa-circle-xmark text-red-500 opacity-0 transition-opacity absolute right-4"></i>
                        </button>
                    `;
                });
                qHTML += `</div></div>`;
            });
            quizContainer.innerHTML = qHTML;
        }

        window.selectOpt = function(qIdx, oIdx, cIdx, btn) {
            const opts = document.querySelectorAll(`.quiz-opt-${qIdx}`);
            opts.forEach((o, i) => {
                o.disabled = true;
                o.classList.remove('hover:bg-white/10', 'cursor-pointer');
                if(i === cIdx) {
                    o.classList.add('bg-green-500/20', 'border-green-500/50');
                    o.querySelector('.fa-circle-check').classList.remove('opacity-0');
                } else if(i === oIdx && i !== cIdx) {
                    o.classList.add('bg-red-500/20', 'border-red-500/50');
                    o.querySelector('.fa-circle-xmark').classList.remove('opacity-0');
                    o.querySelector('.fa-circle-xmark').classList.remove('absolute', 'right-4');
                }
            });
        };
    </script>
</body>
</html>
"""

template = template.replace('{{BRIEFING_MD}}', briefing)
template = template.replace('{{INTEL_MD}}', intel)
template = template.replace('{{RESEARCH_MD}}', research)
template = template.replace('{{QUIZ_MD}}', quiz)
template = template.replace('{{FLASHCARDS_MD}}', flashcards)
template = template.replace('{{COMPANY_NAME}}', COMPANY_NAME)

with open(os.path.join(DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(template)

print("Dashboard generated successfully.")
