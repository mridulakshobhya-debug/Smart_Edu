# E-Learning Routes
from flask import Blueprint, render_template, session, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from ..models import db, Module, Quiz, UserProgress

elearning = Blueprint('elearning', __name__)

# Enhanced course data - 50+ comprehensive courses
COURSES = {
    # Programming Languages (15 courses)
    'python-basics': {'name': 'Python Basics', 'instructor': 'John Smith', 'level': 'Beginner'},
    'python-advanced': {'name': 'Advanced Python Programming', 'instructor': 'John Smith', 'level': 'Advanced'},
    'javascript': {'name': 'JavaScript Mastery', 'instructor': 'Sarah Johnson', 'level': 'Intermediate'},
    'typescript': {'name': 'TypeScript for Developers', 'instructor': 'Sarah Johnson', 'level': 'Intermediate'},
    'java-basics': {'name': 'Java Programming Basics', 'instructor': 'Alex Kumar', 'level': 'Beginner'},
    'java-advanced': {'name': 'Advanced Java Programming', 'instructor': 'Alex Kumar', 'level': 'Advanced'},
    'cpp': {'name': 'C++ Programming', 'instructor': 'Prof. Andrei Alekseyev', 'level': 'Intermediate'},
    'csharp': {'name': 'C# and .NET Development', 'instructor': 'Marcus Johnson', 'level': 'Intermediate'},
    'rust': {'name': 'Rust Programming', 'instructor': 'Emma Wilson', 'level': 'Intermediate'},
    'golang': {'name': 'Go (Golang) Programming', 'instructor': 'David Zhang', 'level': 'Intermediate'},
    'swift': {'name': 'Swift for iOS Development', 'instructor': 'Lisa Park', 'level': 'Intermediate'},
    'kotlin': {'name': 'Kotlin Programming', 'instructor': 'Daniel Lee', 'level': 'Beginner'},
    'php': {'name': 'PHP Web Development', 'instructor': 'Robert Brown', 'level': 'Beginner'},
    'ruby': {'name': 'Ruby on Rails Development', 'instructor': 'Jennifer White', 'level': 'Intermediate'},
    'scala': {'name': 'Scala Functional Programming', 'instructor': 'Victor Chen', 'level': 'Advanced'},
    
    # Web Development (10 courses)
    'web-dev': {'name': 'Full Stack Web Development', 'instructor': 'Mike Chen', 'level': 'Advanced'},
    'html-css': {'name': 'HTML & CSS Fundamentals', 'instructor': 'Nina Patel', 'level': 'Beginner'},
    'responsive-design': {'name': 'Responsive Web Design', 'instructor': 'Nina Patel', 'level': 'Intermediate'},
    'react': {'name': 'React.js Mastery', 'instructor': 'Tom Brady', 'level': 'Intermediate'},
    'angular': {'name': 'Angular Framework', 'instructor': 'Kevin Smith', 'level': 'Intermediate'},
    'vue': {'name': 'Vue.js Development', 'instructor': 'Grace Liu', 'level': 'Beginner'},
    'node-js': {'name': 'Node.js Backend Development', 'instructor': 'Michael Zhang', 'level': 'Intermediate'},
    'express': {'name': 'Express.js & REST APIs', 'instructor': 'Michael Zhang', 'level': 'Intermediate'},
    'webpack': {'name': 'Webpack & Build Tools', 'instructor': 'Alex Rivera', 'level': 'Advanced'},
    'nextjs': {'name': 'Next.js Full Stack', 'instructor': 'Chris Martin', 'level': 'Advanced'},
    
    # Mobile Development (8 courses)
    'mobile-dev': {'name': 'Mobile App Development', 'instructor': 'Lisa Garcia', 'level': 'Advanced'},
    'react-native': {'name': 'React Native Development', 'instructor': 'Amanda Foster', 'level': 'Intermediate'},
    'flutter': {'name': 'Flutter App Development', 'instructor': 'Raj Patel', 'level': 'Intermediate'},
    'android': {'name': 'Android Development', 'instructor': 'James Wilson', 'level': 'Intermediate'},
    'ios-dev': {'name': 'iOS App Development', 'instructor': 'Rachel Green', 'level': 'Intermediate'},
    'xamarin': {'name': 'Xamarin Cross-Platform', 'instructor': 'David Miller', 'level': 'Advanced'},
    'progressive-web': {'name': 'Progressive Web Apps (PWA)', 'instructor': 'Sarah Chen', 'level': 'Intermediate'},
    'mobile-testing': {'name': 'Mobile App Testing', 'instructor': 'Omar Hassan', 'level': 'Intermediate'},
    
    # Data Science & Analytics (10 courses)
    'data-science': {'name': 'Data Science Fundamentals', 'instructor': 'Dr. Patricia Moore', 'level': 'Intermediate'},
    'ml-basics': {'name': 'Machine Learning Fundamentals', 'instructor': 'Dr. Anna Martinez', 'level': 'Beginner'},
    'deep-learning': {'name': 'Deep Learning & Neural Networks', 'instructor': 'Prof. James Wilson', 'level': 'Advanced'},
    'nlp': {'name': 'Natural Language Processing', 'instructor': 'Dr. Lisa Brown', 'level': 'Intermediate'},
    'computer-vision': {'name': 'Computer Vision Basics', 'instructor': 'Dr. Hassan Ahmed', 'level': 'Intermediate'},
    'data-analytics': {'name': 'Data Analytics with Python', 'instructor': 'Sarah Williams', 'level': 'Beginner'},
    'pandas': {'name': 'Pandas for Data Analysis', 'instructor': 'Marcus Thompson', 'level': 'Beginner'},
    'tensorflow': {'name': 'TensorFlow & Keras', 'instructor': 'Dr. Yuki Tanaka', 'level': 'Advanced'},
    'pytorch': {'name': 'PyTorch Deep Learning', 'instructor': 'Dr. Arjun Singh', 'level': 'Advanced'},
    'sklearn': {'name': 'Scikit-Learn for ML', 'instructor': 'Elena Rossi', 'level': 'Intermediate'},
    
    # Computer Science Fundamentals (7 courses)
    'data-structures': {'name': 'Data Structures & Algorithms', 'instructor': 'Dr. Emily White', 'level': 'Intermediate'},
    'algorithms': {'name': 'Algorithm Design & Analysis', 'instructor': 'Prof. Steven Brown', 'level': 'Advanced'},
    'operating-systems': {'name': 'Operating Systems Concepts', 'instructor': 'Dr. Frank Schmidt', 'level': 'Advanced'},
    'databases': {'name': 'Database Systems', 'instructor': 'Prof. David Lee', 'level': 'Intermediate'},
    'sql': {'name': 'SQL Mastery', 'instructor': 'Jennifer Lopez', 'level': 'Beginner'},
    'nosql': {'name': 'NoSQL Databases', 'instructor': "Kevin O'Brien", 'level': 'Intermediate'},
    'system-design': {'name': 'System Design & Architecture', 'instructor': 'Dr. Raj Reddy', 'level': 'Advanced'},
    
    # Cloud & DevOps (7 courses)
    'aws': {'name': 'Amazon Web Services (AWS)', 'instructor': 'Tom Hardy', 'level': 'Intermediate'},
    'azure': {'name': 'Microsoft Azure Cloud', 'instructor': 'Chris Wilson', 'level': 'Intermediate'},
    'gcp': {'name': 'Google Cloud Platform', 'instructor': 'Priya Sharma', 'level': 'Intermediate'},
    'docker': {'name': 'Docker Containerization', 'instructor': 'Marcus Lee', 'level': 'Intermediate'},
    'kubernetes': {'name': 'Kubernetes Orchestration', 'instructor': 'Dmitri Volkov', 'level': 'Advanced'},
    'ci-cd': {'name': 'CI/CD Pipeline Automation', 'instructor': 'Sandra Kim', 'level': 'Intermediate'},
    'devops': {'name': 'DevOps Engineering', 'instructor': 'Ricardo Fernandez', 'level': 'Advanced'},
    
    # Networking & Security (5 courses)
    'networking': {'name': 'Computer Networks', 'instructor': 'Dr. Robert Kim', 'level': 'Advanced'},
    'cybersecurity': {'name': 'Cybersecurity Fundamentals', 'instructor': 'Dr. Eric Johnson', 'level': 'Intermediate'},
    'ethical-hacking': {'name': 'Ethical Hacking & Penetration Testing', 'instructor': 'Marcus Black', 'level': 'Advanced'},
    'cryptography': {'name': 'Cryptography & Encryption', 'instructor': 'Dr. Sophia Turner', 'level': 'Advanced'},
    'web-security': {'name': 'Web Security Essentials', 'instructor': 'Nathan Gray', 'level': 'Intermediate'},
    
    # Academic Subjects (15+ courses)
    'math-basics': {'name': 'Mathematics Fundamentals', 'instructor': 'Prof. Michael Johnson', 'level': 'Beginner'},
    'algebra': {'name': 'Algebra Mastery', 'instructor': 'Prof. Michael Johnson', 'level': 'Beginner'},
    'geometry': {'name': 'Geometry Essentials', 'instructor': 'Dr. Patricia Lewis', 'level': 'Beginner'},
    'calculus': {'name': 'Calculus I & II', 'instructor': 'Prof. Robert Taylor', 'level': 'Intermediate'},
    'statistics': {'name': 'Statistics & Probability', 'instructor': 'Dr. Elena Garcia', 'level': 'Intermediate'},
    'trigonometry': {'name': 'Trigonometry Mastery', 'instructor': 'Prof. David Chen', 'level': 'Beginner'},
    
    'science-basics': {'name': 'Science Fundamentals', 'instructor': 'Dr. Sarah Wilson', 'level': 'Beginner'},
    'physics': {'name': 'Physics: Mechanics & Motion', 'instructor': 'Prof. James Anderson', 'level': 'Intermediate'},
    'chemistry': {'name': 'Chemistry Essentials', 'instructor': 'Dr. Linda Martinez', 'level': 'Beginner'},
    'biology': {'name': 'Biology: Life Sciences', 'instructor': 'Prof. Emma Brown', 'level': 'Beginner'},
    'environmental-science': {'name': 'Environmental Science', 'instructor': 'Dr. Mark Phillips', 'level': 'Intermediate'},
    
    'social-studies': {'name': 'Social Studies Fundamentals', 'instructor': 'Prof. William Harris', 'level': 'Beginner'},
    'history': {'name': 'World History Overview', 'instructor': 'Dr. Thomas White', 'level': 'Beginner'},
    'geography': {'name': 'Geography & Cultures', 'instructor': 'Prof. Christopher Lee', 'level': 'Beginner'},
    'civics': {'name': 'Civics & Government', 'instructor': 'Dr. Nancy Davis', 'level': 'Beginner'},
    'economics': {'name': 'Economics Basics', 'instructor': 'Prof. Richard Miller', 'level': 'Intermediate'},
    
    'english-basics': {'name': 'English Language Fundamentals', 'instructor': 'Dr. Victoria Turner', 'level': 'Beginner'},
    'literature': {'name': 'World Literature & Classics', 'instructor': 'Prof. Caroline King', 'level': 'Intermediate'},
    'writing-skills': {'name': 'Professional Writing Skills', 'instructor': 'Dr. Benjamin Scott', 'level': 'Intermediate'},
    'grammar': {'name': 'Grammar & Composition', 'instructor': 'Prof. Amanda Green', 'level': 'Beginner'},
    'public-speaking': {'name': 'Public Speaking Mastery', 'instructor': 'Dr. Jonathan Blake', 'level': 'Intermediate'},
}

# Enhanced module data with information, videos, and quizzes
MODULES = {
    'module1': {'name': 'Module 1: Fundamentals & Getting Started', 'lessons': 4},
    'module2': {'name': 'Module 2: Intermediate Techniques & Best Practices', 'lessons': 4},
    'module3': {'name': 'Module 3: Advanced Concepts & Optimization', 'lessons': 4},
    'module4': {'name': 'Module 4: Frameworks & Tools', 'lessons': 4},
    'module5': {'name': 'Module 5: Case Studies & Real-World Applications', 'lessons': 4},
    'module6': {'name': 'Module 6: Mastery & Capstone Project', 'lessons': 4},
}

# Module details with information, videos, and quiz questions
MODULE_DETAILS = {
    'module1': {
        'title': 'Fundamentals & Getting Started',
        'description': 'Learn the core concepts and fundamentals',
        'information': '''<h3>Module Overview</h3>
<p>In this module, you'll master the foundational concepts essential to this subject. We'll cover:</p>
<ul>
<li>Core principles and theory</li>
<li>Basic terminology and concepts</li>
<li>Practical applications</li>
<li>Best practices for beginners</li>
</ul>
<h3>What You'll Accomplish</h3>
<p>By the end of this module, you'll be able to:</p>
<ul>
<li>✅ Understand core concepts</li>
<li>✅ Apply theory to practice</li>
<li>✅ Solve basic problems</li>
<li>✅ Complete hands-on exercises</li>
</ul>''',
        'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        'video_duration': '45 minutes',
        'learning_objectives': [
            'Understand the fundamentals and core concepts',
            'Learn industry standards and best practices',
            'Apply theoretical knowledge practically',
            'Complete foundational exercises'
        ],
        'quiz_questions': [
            {
                'question': 'What is the primary focus of this module?',
                'options': ['Advanced concepts', 'Fundamental principles', 'Specialized tools', 'Case studies'],
                'correct': 1,
                'explanation': 'This module focuses on building a strong foundation with fundamental principles.'
            },
            {
                'question': 'Which learning outcome is emphasized?',
                'options': ['Complex problem solving', 'Core concept understanding', 'Expert-level skills', 'Advanced applications'],
                'correct': 1,
                'explanation': 'The module emphasizes understanding core concepts before moving to advanced topics.'
            },
            {
                'question': 'What type of content is included?',
                'options': ['Only videos', 'Videos, reading, and exercises', 'Theory only', 'Practice problems only'],
                'correct': 1,
                'explanation': 'The module includes videos, reading materials, and practical exercises.'
            },
            {
                'question': 'How much time should you allocate?',
                'options': ['1-2 hours', '3-5 hours', '5-7 hours', '10+ hours'],
                'correct': 2,
                'explanation': 'This module requires approximately 5-7 hours of dedicated study.'
            }
        ]
    },
    'module2': {
        'title': 'Intermediate Techniques & Best Practices',
        'description': 'Advance your skills with practical techniques',
        'information': '''<h3>Building on Fundamentals</h3>
<p>Now that you've mastered the basics, it's time to explore intermediate techniques and industry best practices.</p>
<ul>
<li>Advanced techniques and methodologies</li>
<li>Real-world best practices</li>
<li>Optimization strategies</li>
<li>Common pitfalls and how to avoid them</li>
</ul>
<h3>Practical Skills</h3>
<p>You'll develop practical skills including:</p>
<ul>
<li>✅ Implement intermediate techniques</li>
<li>✅ Apply best practices effectively</li>
<li>✅ Optimize your approach</li>
<li>✅ Solve intermediate problems</li>
</ul>''',
        'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        'video_duration': '60 minutes',
        'learning_objectives': [
            'Master intermediate techniques',
            'Apply industry best practices',
            'Optimize your workflow',
            'Solve complex problems'
        ],
        'quiz_questions': [
            {
                'question': 'What makes intermediate techniques different from basics?',
                'options': ['They are more complex', 'They optimize efficiency', 'Both A and B', 'Neither A nor B'],
                'correct': 2,
                'explanation': 'Intermediate techniques are both more complex and focus on optimization.'
            },
            {
                'question': 'Why are best practices important?',
                'options': ['They save time', 'They improve quality', 'They prevent errors', 'All of the above'],
                'correct': 3,
                'explanation': 'Best practices benefit all aspects: time, quality, and error prevention.'
            },
            {
                'question': 'How should you approach optimization?',
                'options': ['Randomly try techniques', 'Follow a systematic approach', 'Copy from others', 'Guess and check'],
                'correct': 1,
                'explanation': 'A systematic approach to optimization ensures consistent improvements.'
            }
        ]
    },
    'module3': {
        'title': 'Advanced Concepts & Optimization',
        'description': 'Master advanced topics and optimization strategies',
        'information': '''<h3>Advanced Mastery</h3>
<p>Take your skills to the next level with advanced concepts and deep optimization strategies.</p>
<ul>
<li>Complex problem-solving approaches</li>
<li>Advanced optimization techniques</li>
<li>Performance tuning</li>
<li>Scalability considerations</li>
</ul>
<h3>Expert-Level Outcomes</h3>
<p>You'll achieve expert-level competency in:</p>
<ul>
<li>✅ Advanced problem analysis</li>
<li>✅ Strategic optimization</li>
<li>✅ Performance excellence</li>
<li>✅ Complex system design</li>
</ul>''',
        'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        'video_duration': '90 minutes',
        'learning_objectives': [
            'Master advanced concepts',
            'Implement optimization strategies',
            'Analyze complex problems',
            'Design scalable solutions'
        ],
        'quiz_questions': [
            {
                'question': 'What is the focus of advanced optimization?',
                'options': ['Speed only', 'Memory only', 'Multiple factors', 'User interface'],
                'correct': 2,
                'explanation': 'Advanced optimization considers multiple factors including speed, memory, and scalability.'
            },
            {
                'question': 'How should complex problems be approached?',
                'options': ['Quick solutions', 'Systematic analysis', 'Trial and error', 'Copy existing solutions'],
                'correct': 1,
                'explanation': 'Complex problems require systematic analysis and strategic thinking.'
            }
        ]
    },
    'module4': {
        'title': 'Frameworks & Tools',
        'description': 'Explore relevant frameworks and professional tools',
        'information': '''<h3>Framework Ecosystem</h3>
<p>Learn about popular frameworks and tools used in professional environments.</p>
<ul>
<li>Popular frameworks overview</li>
<li>Tool comparison and selection</li>
<li>Integration strategies</li>
<li>Real-world projects</li>
</ul>
<h3>Professional Development</h3>
<p>Prepare for professional work with:</p>
<ul>
<li>✅ Framework proficiency</li>
<li>✅ Tool expertise</li>
<li>✅ Integration knowledge</li>
<li>✅ Project management</li>
</ul>''',
        'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        'video_duration': '75 minutes',
        'learning_objectives': [
            'Understand major frameworks',
            'Master essential tools',
            'Integrate technologies effectively',
            'Develop professional projects'
        ],
        'quiz_questions': [
            {
                'question': 'What is the benefit of using established frameworks?',
                'options': ['Faster development', 'Better practices', 'Community support', 'All of the above'],
                'correct': 3,
                'explanation': 'Frameworks provide all these benefits: speed, best practices, and community.'
            }
        ]
    },
    'module5': {
        'title': 'Case Studies & Real-World Applications',
        'description': 'Learn from real-world case studies and applications',
        'information': '''<h3>Real-World Learning</h3>
<p>Explore how industry leaders apply these concepts in real-world scenarios.</p>
<ul>
<li>Industry case studies</li>
<li>Success stories</li>
<li>Lessons learned</li>
<li>Practical applications</li>
</ul>
<h3>Practical Experience</h3>
<p>Gain practical insights through:</p>
<ul>
<li>✅ Analyze real projects</li>
<li>✅ Learn from experts</li>
<li>✅ Understand challenges</li>
<li>✅ Apply lessons to your work</li>
</ul>''',
        'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        'video_duration': '60 minutes',
        'learning_objectives': [
            'Analyze real-world case studies',
            'Learn industry best practices',
            'Understand practical challenges',
            'Apply lessons to projects'
        ],
        'quiz_questions': [
            {
                'question': 'Why are case studies valuable?',
                'options': ['They are entertaining', 'They provide real-world context', 'They fill time', 'They are required'],
                'correct': 1,
                'explanation': 'Case studies provide valuable real-world context for learning.'
            }
        ]
    },
    'module6': {
        'title': 'Mastery & Capstone Project',
        'description': 'Complete your journey with a capstone project',
        'information': '''<h3>Final Mastery</h3>
<p>Demonstrate your complete understanding by completing a comprehensive capstone project.</p>
<ul>
<li>Project planning and scope</li>
<li>Implementation strategies</li>
<li>Quality assurance</li>
<li>Presentation and documentation</li>
</ul>
<h3>Achievement Goals</h3>
<p>Upon completion, you will have:</p>
<ul>
<li>✅ Completed a professional project</li>
<li>✅ Demonstrated mastery</li>
<li>✅ Built a portfolio piece</li>
<li>✅ Earned course certification</li>
</ul>''',
        'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        'video_duration': '45 minutes',
        'learning_objectives': [
            'Plan and design a capstone project',
            'Implement all learned concepts',
            'Apply quality standards',
            'Complete professional documentation'
        ],
        'quiz_questions': [
            {
                'question': 'What is the purpose of a capstone project?',
                'options': ['Fill time', 'Demonstrate mastery', 'Make it hard', 'Entertain students'],
                'correct': 1,
                'explanation': 'A capstone project demonstrates your complete understanding and mastery.'
            }
        ]
    }
}

@elearning.route('/')
def index():
    return render_template('elearning.html')

@elearning.route('/course/<course_id>')
def course_detail(course_id):
    course = COURSES.get(course_id, {})
    course_name = course.get('name', 'Course Not Found')
    
    if not course:
        return render_template('course_detail.html', course_name='Course Not Found'), 404
    
    # Check if user is enrolled
    if 'enrolled_courses' not in session:
        session['enrolled_courses'] = []
    
    is_enrolled = course_id in session['enrolled_courses']
    
    return render_template('course_detail.html', 
                         course_name=course_name, 
                         course_id=course_id,
                         is_enrolled=is_enrolled)

@elearning.route('/course/<course_id>/enroll')
def enroll_course(course_id):
    if 'enrolled_courses' not in session:
        session['enrolled_courses'] = []
    
    if course_id not in session['enrolled_courses']:
        session['enrolled_courses'].append(course_id)
        session.modified = True
    
    return render_template('course_detail.html', 
                         course_name=COURSES.get(course_id, {}).get('name', 'Course'),
                         course_id=course_id,
                         is_enrolled=True)

@elearning.route('/course/<course_id>/module/<module_id>')
def module_detail(course_id, module_id):
    """Display module details with information, video, and quiz"""
    course = COURSES.get(course_id, {})
    course_name = course.get('name', 'Course Not Found')
    
    if not course:
        return render_template('course_detail.html', course_name='Course Not Found'), 404
    
    # Check if user is enrolled - but allow preview if not enrolled
    if 'enrolled_courses' not in session:
        session['enrolled_courses'] = []
    
    is_enrolled = course_id in session['enrolled_courses']
    
    module = MODULES.get(module_id, {'name': 'Module Not Found'})
    module_info = MODULE_DETAILS.get(module_id, {})
    
    return render_template('module_detail.html',
                         course_name=course_name,
                         course_id=course_id,
                         module_name=module.get('name'),
                         module_id=module_id,
                         module_info=module_info,
                         is_enrolled=is_enrolled)

@elearning.route('/course/<course_id>/module/<module_id>/lesson/<lesson_id>')
def lesson(course_id, module_id, lesson_id):
    course = COURSES.get(course_id, {})
    course_name = course.get('name', 'Course Not Found')
    
    # Track enrollment in session if needed, but don't block access
    if 'enrolled_courses' not in session:
        session['enrolled_courses'] = []
    
    module = MODULES.get(module_id, {'name': 'Module Not Found'})
    module_info = MODULE_DETAILS.get(module_id, {})
    
    return render_template('module_lesson.html',
                         course_name=course_name,
                         course_id=course_id,
                         module_name=module.get('name'),
                         module_id=module_id,
                         lesson_title=f'Lesson {lesson_id}',
                         lesson_id=lesson_id,
                         module_info=module_info,
                         progress=int(lesson_id) * 33)

@elearning.route('/api/course/<course_id>/module/<module_id>/submit-quiz', methods=['POST'])
def submit_quiz(course_id, module_id):
    """API endpoint to submit quiz answers"""
    data = request.json
    answers = data.get('answers', [])
    module_info = MODULE_DETAILS.get(module_id, {})
    quiz_questions = module_info.get('quiz_questions', [])
    
    if not quiz_questions:
        return jsonify({'error': 'No quiz found'}), 404
    
    # Calculate score
    correct_count = 0
    results = []
    
    for i, answer in enumerate(answers):
        if i < len(quiz_questions):
            question = quiz_questions[i]
            is_correct = answer == question['correct']
            if is_correct:
                correct_count += 1
            
            results.append({
                'question_index': i,
                'is_correct': is_correct,
                'explanation': question.get('explanation', '')
            })
    
    score = int((correct_count / len(quiz_questions)) * 100) if quiz_questions else 0
    
    return jsonify({
        'score': score,
        'correct_count': correct_count,
        'total_questions': len(quiz_questions),
        'results': results,
        'passed': score >= 70
    })

