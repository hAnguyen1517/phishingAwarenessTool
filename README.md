# Phishing Training Platform

Welcome to the **Phishing Training Platform**, a web-based application designed to educate and train users in identifying and preventing phishing attacks. This platform offers interactive simulations, real-time reporting, and comprehensive training modules to empower organizations and individuals with cutting-edge phishing awareness and prevention skills.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [User Roles](#user-roles)
- [File Structure](#file-structure)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)

## Project Overview
The Phishing Training Platform is built to address the growing threat of phishing attacks by providing a secure, user-friendly environment for training. This is the frontend-template starter setup for all group members to follow so that we can take the shortest time in designing the platform.
The platform is designed with a responsive interface, ensuring accessibility across devices.

## Features (will be implemented when we start integrating django)
- **Interactive Simulations** - Engage in realistic phishing scenarios to build practical skills.
- **Real-Time Reporting** - Track progress and performance with detailed analytics and customizable reports.
- **Comprehensive Training** - Access a library of courses covering phishing awareness, prevention, and best practices.
- **Role-Based Access** - Supports administrators, regular users, and superusers with specific privileges.
- **Secure Design** - Implements encryption and secure access controls to protect user data.

## Installation

### Prerequisites
- Python
- Git
- A modern web browser (Chrome, Firefox, Edge)

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/phishing-training-platform.git
   cd phishing-training-platform
   ```

2. **Install Dependencies** (will be implemented when we start integrating django)
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   - Run it
   ```bash
   python manage.py runserver
   ```

## Usage
- **Sign Up**: Visit the landing page (`index.html`) and click "Sign Up" to create an account.
- **Sign In**: Use your credentials to log in and access training modules, quizzes, or reports.
- **Administrators**: Navigate to "Reports" or "Settings" to manage users and generate analytics.
- **Superusers**: Contact support for elevated access to oversee system logs and perform maintenance.
- **Documentation**: Refer to `documentation.html` for detailed system information and technical requirements.

## User Roles
- **Administrators**: Manage user accounts, configure training, and generate system-wide reports.
- **Regular Users**: Access training and quizzes, view personal progress, and update profiles.
- **Special Accounts (Superusers)**: Oversee all activities, perform system maintenance, and troubleshoot issues.

## File Structure
```
phishing-training-platform/
├── assets
│   ├── fonts
│   ├── icons
│   └── images
├── dashboard
│   ├── dashboard.html (done)
│   ├── profile.html
│   ├── quiz.html
│   ├── report.html
│   ├── settings.html
│   ├── template.html (done)
│   └── training.html
├── scripts
│   └── main.js
├── styles
│   ├── dashboard.css (done)
│   ├── index.css
│   ├── profile.css
│   ├── quiz.css
│   ├── report.css
│   ├── responsive.css (the root styles for responsive) *don't edit
│   ├── settings.css
│   ├── signin.css (done)
│   ├── signup.css (done)
│   ├── styles.css (the root styles) *don't edit
│   └── training.css
├── README.md
├── index.html (done)
├── signin.html (done)
├── signup.html (done)
```

## Technologies Used
- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Django
- **Database**: SQLite/MYSQL
- **Hosting**: Pythoneverywhere
- **Security**: SSL encryption, JWT authentication

## Contributing
I have only made the starter part so it's upon each individual memebers to take care of your own parts.
For example if you're taking care the quiz page, you will write the codes in quiz.html (copy the html structure of the template.html then paste them into the quiz.html file) then add your own codes from where it has been indicated.

![alt text](image.png)

Add your styles into the training.css file.
After your page looks good then do the following:

1. **Create a New Branch**
   - Use the following command to create and switch to a new branch.
    ```bash
    git checkout -b new-branch-name
    ```

2. **Make Changes**
   - Implement your changes or bug fixes.

3. **Add and Commit Changes**
   ```bash
   git add .
   ```

4. **Commit Your Changes**
   ```bash
   git commit -m "Description of your changes"
   ```

5. **Push the New Branch to Remote**
    - Push the new branch to the remote repository:
    ```bash
    git push -u origin new-branch-name
    ```
    - The `-u` flag sets up tracking, so future pushes can simply be done with `git push`.
    ```bash
    git checkout new-branch-name
    ```

6. **Code Standards**
   - Follow the existing code style (e.g., use CSS variables, consistent indentation).
   - Write clear commit messages and comments.

7. **Testing**
   - Test your changes across different screen sizes and browsers.

