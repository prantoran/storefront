
## VSCode Django Debug Setup

Click VSCode's Debug panel and create a launch.json for python->Django. This will create .vscode/launch.json:
```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Django",
            "type": "debugpy",  
            "request": "launch",
            "args": [
                "runserver",
                "9000"
            ],
            "django": true,
            "autoStartBrowser": false,
            "program": "${workspaceFolder}/manage.py"
        }
    ]
}
```


VSCode Shortcuts:
F5: Start server with debugger
Ctrl+F5: Start server without debugger
