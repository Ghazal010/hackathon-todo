// Script to fix the TodoApp.tsx file to include user_id property
const fs = require('fs');
const path = require('path');

// Path to the TodoApp.tsx file that's causing the build error
const todoAppPath = '/Users/user/Desktop/hackathon-todo/src/app/components/TodoApp.tsx';

if (fs.existsSync(todoAppPath)) {
    let content = fs.readFileSync(todoAppPath, 'utf8');

    // Look for the task creation that's missing user_id
    const taskCreationPattern = /const task: Task = \{([\s\S]*?)(?=};)/g;

    let updatedContent = content.replace(taskCreationPattern, (match) => {
        // Check if user_id is already present
        if (match.includes('user_id')) {
            return match;
        }

        // Add user_id to the task object
        return match + ',\n        user_id: user?.id || 1  // Add required user_id field';
    });

    fs.writeFileSync(todoAppPath, updatedContent);
    console.log('Fixed TodoApp.tsx to include user_id property');
} else {
    console.log('TodoApp.tsx file not found at expected location');
}