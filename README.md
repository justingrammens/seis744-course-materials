# SEIS 744: IoT with Machine Learning
**University of St. Thomas - Fall 2025**  
**Instructor:** Justin Grammens  
**Course Materials Repository**

---

## 📋 Course Overview

Welcome to SEIS 744: IoT with Machine Learning! This repository contains course-specific materials that complement Andy King's book **"Programming the Internet of Things: An Introduction to Building Integrated, Device-to-Cloud IoT Solutions"**.

This course takes a hands-on, progressive approach to learning IoT and Machine Learning integration. You'll build real IoT systems from device to cloud while incorporating ML capabilities at the edge and in the cloud.

---

## 🎯 Learning Approach

### **Fork-Based Development Model**
Unlike traditional courses, you'll work directly with professional-grade repositories:

1. **Fork Andy King's Official Repositories** - Get real-world, production-quality code
2. **Follow Progressive Exercises** - Each chapter builds on the previous
3. **Add ML Enhancements** - Integrate machine learning throughout your development
4. **Build Professional Portfolio** - Create industry-ready code repositories

### **"Learn as You Build" Philosophy**
You'll construct an end-to-end IoT+ML solution step by step, understanding both the technical implementation and architectural principles.

---

## 🚀 Getting Started

### **Step 1: Set Up Your Development Environment**

#### **Required Software:**
- **Python 3.8+** with pip
- **Java 11+** (OpenJDK recommended)
- **Git** (command line)
- **IDE**: Eclipse with PyDev, or VS Code
- **Arduino IDE** (for hardware work)

#### **Installation Verification:**
```bash
# Verify installations
python3 --version    # Should be 3.8+
java --version       # Should be 11+
git --version        # Any recent version
```

### **Step 2: Fork the Core Repositories**

#### **Required Forks:**
1. **Python Components (CDA - Constrained Device Application):**
   - **Original:** https://github.com/programming-the-iot/python-components
   - **Fork to:** `https://github.com/{your-username}/piot-python-components`

2. **Java Components (GDA - Gateway Device Application):**
   - **Original:** https://github.com/programming-the-iot/java-components  
   - **Fork to:** `https://github.com/{your-username}/piot-java-components`

#### **How to Fork:**
1. Navigate to each repository above
2. Click the "Fork" button (top right)
3. Select your GitHub account as the destination
4. Wait for GitHub to create your fork

### **Step 3: Clone Your Forks Locally**

```bash
# Create working directory
mkdir ~/programmingtheiot
cd ~/programmingtheiot

# Clone your forks (replace {your-username})
git clone https://github.com/{your-username}/piot-python-components.git
git clone https://github.com/{your-username}/piot-java-components.git

# Clone this course materials repository
git clone https://github.com/ust-seis744/seis744-course-materials.git
```

### **Step 4: Set Up Upstream Remotes**

This allows you to pull updates from Andy King's original repositories:

```bash
# Python components
cd piot-python-components
git remote add upstream https://github.com/programming-the-iot/python-components.git

# Java components  
cd ../piot-java-components
git remote add upstream https://github.com/programming-the-iot/java-components.git

# Verify remotes
git remote -v
# Should show: origin (your fork) and upstream (Andy's original)
```

---

## 📖 Working with Andy King's Book

### **Primary Reference: Programming the IoT Kanban Board**
**🔗 https://github.com/orgs/programming-the-iot/projects/5**

This is your primary source for exercise requirements. Each exercise follows the format:
- **PIOT-CDA-XX-YYY** (Python/Constrained Device)
- **PIOT-GDA-XX-YYY** (Java/Gateway Device)

Where:
- **XX** = Chapter number (01, 02, 03...)
- **YYY** = Exercise sequence (001, 002, 003...)

### **Weekly Development Workflow**

#### **For Each Chapter:**

1. **Create Chapter Branch:**
   ```bash
   cd piot-python-components
   git checkout main
   git pull origin main
   git checkout -b chapter02  # Replace with current chapter
   ```

2. **Follow Official Exercises:**
   - Open Andy King's Kanban board
   - Find exercises for current chapter (e.g., PIOT-CDA-02-001)
   - Implement requirements exactly as specified
   - Run all unit tests to verify implementation

3. **Add Course-Specific Enhancements:**
   - Integrate ML components where specified
   - Add hardware integration points
   - Include data visualization elements

4. **Test and Commit:**
   ```bash
   # Run tests frequently
   python3 -m pytest src/test/python/
   
   # Commit working code
   git add .
   git commit -m "Implement PIOT-CDA-02-001: Basic sensor simulation"
   ```

5. **Submit for Review:**
   ```bash
   # Push chapter branch
   git push origin chapter02
   
   # Create Pull Request on GitHub:
   # - From: chapter02 branch
   # - To: main branch
   # - Include: Exercise completion summary
   ```

---

## 🤖 Machine Learning Integration

### **Course-Specific ML Components**

As you progress through the exercises, you'll add ML capabilities:

#### **Week 8+: Hardware Integration**
- **Arduino Tiny ML Kit** setup and programming
- **Real sensor data** collection and processing
- **Edge inference** with TensorFlow Lite

#### **Week 10: Data Visualization**  
- **ThingSpeak** dashboards with ML insights
- **Real-time analytics** and anomaly detection
- **Cloud-based model training**

#### **Week 12: Edge ML Deployment**
- **Edge Impulse** model development
- **On-device inference** optimization
- **Model performance monitoring**

### **ML Integration Points in Your Code**

You'll add these directories to your forked repositories:

```
piot-python-components/
├── src/main/python/programmingtheiot/
│   ├── cda/
│   │   ├── ml/                    # NEW: ML components
│   │   │   ├── EdgeImpulseConnector.py
│   │   │   ├── TensorFlowLiteInference.py
│   │   │   └── ModelManager.py
│   │   ├── embedded/              # NEW: Hardware integration
│   │   │   ├── ArduinoConnector.py
│   │   │   └── SensorManager.py
│   │   └── ...existing code...
```

---

## 🛠️ Hardware Components

### **Required Hardware: Arduino Tiny ML Kit**
**🛒 Purchase Link:** https://www.digikey.com/en/products/detail/arduino/AKX00028/13982273

#### **Kit Contents:**
- Arduino Nano 33 BLE Sense board
- OV7675 camera module  
- Tiny ML shield
- Various sensors (accelerometer, gyroscope, microphone, etc.)

#### **Setup Instructions:**
Detailed setup guides are in `/hardware-guides/` directory of this repository.

---

## 📝 Assignments and Assessment

### **Weekly Structure:**

#### **Every Week:**
- **Technical Exercises:** Complete assigned chapters from Programming the Internet of Things book
- **Article Discussion:** Find and share one IoT/ML article (post to Canvas)
- **Code Commits:** Regular commits showing progressive development

#### **Major Deliverables:**
- **Week 7:** Midterm Examination (20%)
- **Week 12+:** Term Paper (15%) - 300+ words on IoT/ML topic
- **Week 15:** Capstone Project Presentation (50%)

### **Grading Breakdown:**
- **In-class Exercises, Articles, Homework:** 15%
- **Midterm Examination:** 20%  
- **Term Paper:** 15%
- **Capstone Project:** 50%

### **Code Quality Expectations:**
- **Clean Commits:** Meaningful commit messages
- **Working Tests:** All unit tests must pass
- **Documentation:** README files and code comments
- **Professional Standards:** Industry-ready code organization

---

## 🔗 Essential Resources

### **Primary Resources:**
- **📚 Textbook:** [Programming the Internet of Things (O'Reilly)](https://learning.oreilly.com/library/view/programming-the-internet/9781492081401/)
- **📋 Official Kanban Board:** https://github.com/orgs/programming-the-iot/projects/5
- **💻 Course Book Website:** https://labbenchstudios.com/programming-the-iot-book/

### **Development Tools:**
- **🔧 Arduino Tiny ML Kit Documentation:** https://docs.arduino.cc/hardware/nano-33-ble-sense
- **🧠 Edge Impulse Platform:** https://edgeimpulse.com/
- **📊 ThingSpeak IoT Platform:** https://thingspeak.com/
- **☁️ AWS IoT Core:** https://aws.amazon.com/iot-core/ (optional)

### **Course-Specific Resources:**
- **📖 Course Syllabus:** Latest version in Canvas
- **🔨 Hardware Setup Guides:** `/hardware-guides/`
- **🤖 ML Integration Examples:** `/machine-learning-extensions/`
- **📊 Assessment Rubrics:** `/assessment-rubrics/`

---

## 💡 Success Tips

### **Code Development Best Practices:**
1. **Commit Early and Often** - Small, working commits are better than large, broken ones
2. **Follow the Kanban Board** - Don't skip ahead; each exercise builds on the previous
3. **Test Continuously** - Run unit tests after each implementation
4. **Document Your Learning** - Keep notes on challenges and solutions
5. **Ask Questions Early** - Don't struggle alone; use office hours and Canvas discussions

### **Professional Development:**
- **GitHub Profile:** Your repositories become part of your professional portfolio
- **Industry Standards:** You're learning real-world IoT development practices
- **Network Building:** Connect with classmates and industry professionals
- **Continuous Learning:** IoT and ML evolve rapidly; stay curious and keep learning

---

## 🆘 Getting Help

### **Office Hours:**
- **Thursdays:** 5:00-5:40 PM and 9:00-9:30 PM (OSS 228)
- **By Appointment:** Email jlgrammens@stthomas.edu

### **Online Resources:**
- **Canvas Discussions:** Course-specific questions and article sharing
- **GitHub Issues:** Technical problems with repositories
- **Programming the IoT Community:** Andy King's GitHub discussions

### **Emergency Contacts:**
- **Email:** jlgrammens@stthomas.edu
- **Phone:** 612-208-8663 (work)
- **Response Time:** Within 24 hours (faster during weekdays)

---

## 🎓 Course Philosophy

> *"The Internet of Things and Machine Learning are new technologies still being developed and far from perfect. There is no 'right answer'. We will derive our answers from sharing knowledge with each other."*
> 
> — Course Instructor

This course emphasizes:
- **Hands-on Learning** over theoretical study
- **Professional Development** over academic exercises  
- **Collaborative Problem-Solving** over individual competition
- **Real-World Applications** over toy examples
- **Continuous Improvement** over perfect solutions

---

## 📄 License and Usage

This course materials repository is for **SEIS 744 students only**. Please respect intellectual property:

- **Andy King's Code:** Licensed under his terms (see individual repositories)
- **Course Materials:** For educational use in SEIS 744 only
- **Student Code:** Your forks become your intellectual property
- **Sharing:** Feel free to showcase your work professionally after course completion

---

**Welcome to an exciting journey into the future of connected, intelligent systems! Let's build something amazing together.** 🚀

---

*Last Updated: August 2025*  
*Questions? Contact: jlgrammens@stthomas.edu*