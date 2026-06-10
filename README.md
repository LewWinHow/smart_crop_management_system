# AI Oil Palm Mentor System

Intelligent Oil Palm Management System - A Django-based oil palm plantation management platform with integrated AI assistant and image analysis capabilities.

## 🌟 Project Overview

AI Oil Palm Mentor System is an intelligent management system designed specifically for oil palm plantations, providing the following core features:

- **Employee Management**: Multi-role permission management (Supervisor, Administrator, Viewer)
- **Plantation Monitoring**: Real-time monitoring of oil palm tree health status, nutrient levels, and productivity
- **AI Image Analysis**: Automatic identification of oil palm tree diseases, nutrient deficiencies, and growth conditions
- **AI Assistant**: Intelligent Q&A system that answers farmers' questions about oil palm tree management
- **Data Visualization**: Charts displaying health status distribution, infection rates, and other key metrics

## 🚀 Quick Start

### 1. Requirements

- Python 3.8+
- Django 5.2.12
- SQLite3 (default database)

### 2. Installation Steps

```bash
# Clone or download the project
cd smart_crop_management_system

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

### 3. Access the Application

Open your browser and visit: `http://127.0.0.1:8000/`

## 👤 Default Account

The system comes with a pre-configured Supervisor account for testing:

| Role | Username | Password | Permissions |
|------|----------|----------|-------------|
| Supervisor | lewwinhow | (XiaoHao6070) | Full access to manage all employees and plantation data |

### Other Role Descriptions

- **Supervisor**: Full permissions, can add/edit/delete employees, view all plantation data
- **Administrator**: Can view and manage plantation data, cannot manage employees
- **Viewer**: Read-only access to plantation data, no editing permissions

## 📋 Main Features

### 1. Employee Management

- View all employee list
- Add new employees
- Edit employee information
- Delete employees
- View personal information

**Access Paths**:
- Employee List: `/employee/all_employee/`
- Add Employee: `/employee/add_employee/`
- Personal Information: `/employee/your_information/`

### 2. Plantation Monitoring

#### Monitoring Dashboard
- Display farm overview statistics
- Health status stacked bar chart
- Zone infection rate charts
- Productivity distribution charts

**Access Path**: `/monitoring/`

#### Zone Details
- View tree map for specific zones
- Display tree health status within the zone
- View zone statistics

**Access Path**: `/monitoring/zone/<zone_id>/`

#### Individual Tree Details
- View detailed information for a single tree
- Display health status, disease type, productivity status
- View tree photos and analysis results

**Access Path**: `/monitoring/tree/<tree_id>/`

### 3. AI Image Analysis

Upload oil palm tree photos for automatic analysis:

- **Health Status**: Healthy, Nutrient Deficiency, Sick
- **Disease Type**: None, Ganoderma, Basal Stem Rot, Leaf Spot, Anthracnose
- **Productivity Status**: Producing, Not Producing, Unknown

**Access Path**: `/analyze/oil_palm_tree_analyze/`

**Usage Steps**:
1. Upload a clear photo of the oil palm tree
2. Select the zone where the tree is located
3. Enter row number and column number
4. Click "Upload & Analyze" to start analysis
5. View analysis results and recommendations

### 4. AI Assistant

Intelligent Q&A system that answers farmers' questions about oil palm tree management:

- Disease identification and treatment recommendations
- Nutrient deficiency symptom diagnosis
- Soil and fertilization management
- Irrigation and harvesting guidance
- Pest control methods

**Access Path**: `/ai_assistant/get_chat/`

**Supported Question Types**:
- "How to identify Ganoderma disease in oil palm trees?"
- "What causes yellowing leaves?"
- "When should I apply fertilizer?"
- "How to prevent basal stem rot?"

### 5. Login Logs

Record login information for all users:

- Login record queries
- IP address statistics

**Access Paths**:
- Login Records: `/login_log/all_login_record/`
- IP Statistics: `/login_log/all_login_ip/`

## 🎨 Interface Features

- **Gradient Animation Effects**: Fade-in animations on page load
- **Responsive Design**: Adapts to desktop and mobile devices
- **Icon System**: Uses Bootstrap Icons for enhanced visual appeal
- **Color Coding**:
  - 🟢 Green: Healthy/Normal/Producing
  - 🟡 Yellow: Nutrient Deficiency/Not Producing
  - 🔴 Red: Diseased/Abnormal
  - ⚪ Gray: Unknown status

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 5.2.12
- **Database**: SQLite3
- **REST API**: Django REST Framework
- **Image Processing**: YOLO (Object Detection)
- **AI Model**: LLM (Large Language Model)

### Frontend
- **Template Engine**: Django Templates
- **CSS Framework**: Bootstrap 5.3.0
- **Icon Library**: Bootstrap Icons 1.11.3
- **Chart Library**: Chart.js
- **JavaScript**: Vanilla JS + jQuery

### AI Features
- **Image Analysis**: YOLO Object Detection + VLM Vision-Language Model
- **RAG System**: Retrieval Augmented Generation, combining local knowledge base with web search
- **Natural Language Processing**: LLM conversational system

## 📁 Project Structure

```
smart_crop_management_system/
├── account/                    # Account management
├── ai_assistant/               # AI assistant module
├── analyze/                    # AI image analysis module
├── employee/                   # Employee management module
├── login_log/                  # Login log module
├── media/                      # Media file storage
│   ├── oil_palm_tree/          # Oil palm tree photos
│   └── profile_image/          # Employee profile images
├── middleware/                 # Middleware
├── monitoring/                 # Plantation monitoring module
├── smart_crop_management/      # Project configuration
├── templates/                  # HTML templates
│   ├── account/                # Login page
│   ├── ai_assistant/           # AI assistant chat interface
│   ├── anaylze/                # Image analysis page
│   ├── employee/               # Employee management pages
│   ├── login_log/              # Login log pages
│   ├── monitoring/             # Monitoring pages
│   ├── background.html         # Background template
│   ├── navigation_bar.html     # Navigation bar template
│   └── hint_message.html       # Hint message template
├── utils/                      # Utility functions
│   ├── agricultural_knowledge.py  # Agricultural knowledge base
│   ├── llm.py                  # LLM integration
│   ├── rag.py                  # RAG retrieval system
│   ├── audio_to_text.py        # Speech to text
│   └── ...
├── db.sqlite3                  # Database file
└── manage.py                   # Django management script
```

## 🔧 Configuration

### Database Configuration

The project uses SQLite3 as the default database. Configuration is located in `smart_crop_management/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Media File Configuration

User-uploaded images are stored in the `media/` directory:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### AI Model Configuration

LLM model configuration is in `utils/llm.py`:

```python
def llm(prompt, model='gpt-oss:120b-cloud', temperature=0.3):
    # LLM call logic
```

## 📊 Data Models

### Employee
- username: Username
- password: Password (encrypted storage)
- first_name: First name
- last_name: Last name
- email: Email
- phone: Phone number
- birth_date: Date of birth
- age: Age
- gender: Gender (1=Male, 2=Female)
- permission: Permission level (1=Supervisor, 2=Administrator, 3=Viewer)
- is_active: Active status
- profile_image: Profile picture

### Zone
- zone_name: Zone name
- n_value: Nitrogen content
- p_value: Phosphorus content
- k_value: Potassium content
- ph: pH level

### OilPalmTree
- zone: Associated zone (foreign key)
- row: Row number
- column: Column number
- status: Health status (1=Healthy, 2=Nutrient Deficiency, 3=Sick)
- disease: Disease type (1=None, 2=Ganoderma, 3=Basal Stem Rot, 4=Leaf Spot, 5=Anthracnose)
- productivity: Productivity status (1=Producing, 2=Not Producing, 3=Unknown)
- describe: Description
- image_path: Image path

### Chat
- employee: User (foreign key)
- message: Message content
- sender: Sender (1=User, 2=AI)

## 🐛 Troubleshooting

### 1. Cannot Log In
- Verify username and password are correct
- Confirm account is active (is_active=True)
- Try using the default account: lewwinhow / (XiaoHao6070)

### 2. Image Upload Fails
- Check if file size exceeds limits
- Verify file format (JPG, PNG, WEBP)
- Ensure the media directory has write permissions

### 3. AI Analysis Results Are Inaccurate
- Ensure you upload clear oil palm tree photos
- Avoid obscured or blurry images
- Try capturing from different angles

### 4. AI Assistant Not Responding
- Check network connection
- Verify LLM service is running properly
- Try simplifying your question

## 📝 Changelog

### v1.0.0 (2026-05-26)
- ✅ Completed employee management module
- ✅ Implemented plantation monitoring functionality
- ✅ Integrated AI image analysis
- ✅ Developed AI assistant Q&A system
- ✅ Optimized frontend interface and user experience
- ✅ Unified brand name to "AI Oil Palm Mentor System"
- ✅ Fixed form field naming conventions

## 👥 Development Team

This project is maintained by the Intelligent Agriculture Management System development team.

## 📄 License

This project is for educational and research purposes only.

## 🙏 Acknowledgments

Thanks to the following open-source projects for their support:
- Django
- Bootstrap
- Chart.js
- Bootstrap Icons
- YOLO
- LLM Models

---

**Feel free to provide feedback if you have any questions or suggestions!**
