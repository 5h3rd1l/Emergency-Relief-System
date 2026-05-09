#include <iostream>
#include <string>

using namespace std;

class LogEntry
{
public:
    string action;
    string details;
    
    LogEntry()
    {
        action = "";
        details = "";
    }
    LogEntry(string act, string det)
    {
        action = act;
        details = det;
    }
};

class AuditLogger
{
private:
    static const int MAX_LOGS = 500;
    LogEntry logs[MAX_LOGS];
    int logCount;
    
public:
    AuditLogger()
    {
        logCount = 0;
    }
    
    bool addLog(string action, string details)
    {
        if (logCount >= MAX_LOGS) {
            return false;
        }
        
        logs[logCount] = LogEntry(action, details);
        logCount++;
        return true;
    }
    
    void display()
    {
        if (logCount == 0) {
            cout << "EMPTY\n";
            return;
        }
        
        for (int i = 0; i < logCount; i++)
        {
            cout << "---LOG:" << (i + 1) << "---\n";
            cout << "ACTION:" << logs[i].action << "\n";
            cout << "DETAILS:" << logs[i].details << "\n";
        }
    }
    
    int getCount() 
    { 
        return logCount; 
    }
    
    void clear()
    {
        logCount = 0;
    }
};
