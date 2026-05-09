#include "EmergencyReport.cpp"
#include "LinkedList.cpp"
#include "MaxHeap.cpp"
#include "Queue.cpp"
#include "Logger.cpp"
#include <fstream>

using namespace std;
ReportLinkedList reportList;
MaxHeap priorityQueue;
DispatchQueue dispatchQueue;
AuditLogger logger;

void rebuildPriorityQueue()
{
    int count;
    EmergencyReport* reports = reportList.getAllReports(count);
    priorityQueue.rebuildHeap(reports, count);
    if (reports)
        delete[] reports;
}

string getShortageLabel(int val)
{
    if (val >= 8) return "CRITICAL";
    if (val >= 5) return "HIGH";
    if (val >= 3) return "MODERATE";
    return "LOW";
}

void generateReports()
{
    ofstream pendingFile("Pending_Emergencies_Report.txt");
    if (pendingFile.is_open())
    {
        pendingFile << "========================================================================================================================\n";
        pendingFile << "                                               PENDING EMERGENCY REPORT\n";
        pendingFile << "========================================================================================================================\n";
        pendingFile << left << setw(20) << "LOCATION" 
                   << setw(15) << "DISASTER" 
                   << setw(10) << "POP" 
                   << setw(10) << "INJURED"
                   << setw(15) << "FOOD NEED"
                   << setw(15) << "MED NEED"
                   << setw(15) << "WATER NEED"
                   << setw(15) << "SEVERITY" 
                   << setw(25) << "REPORTED TIME" << "\n";
        pendingFile << "------------------------------------------------------------------------------------------------------------------------\n";
        
        MaxHeap tempHeap = priorityQueue; // Copy for non-destructive iteration
        
        while (!tempHeap.isEmpty())
        {
            EmergencyReport r = tempHeap.extractMax();
            pendingFile << left << setw(20) << r.locationID 
                       << setw(15) << r.disasterType
                       << setw(10) << r.populationAffected
                       << setw(10) << r.injuredCount
                       << setw(15) << getShortageLabel(r.foodShortage)
                       << setw(15) << getShortageLabel(r.medicalShortage)
                       << setw(15) << getShortageLabel(r.waterShortage)
                       << setw(15) << r.getSeverityLabel()
                       << setw(25) << r.getTimeString() << "\n";
        }
        
        pendingFile << "------------------------------------------------------------------------------------------------------------------------\n";
        pendingFile << "TOTAL PENDING: " << priorityQueue.size() << "\n";
        pendingFile.close();
    }
    
    cout << "STATUS=OK\nMSG=Reports generated successfully\n";
}

void handleAdd(string locationID, string disaster, int pop, int injured, 
               int food, int medical, int water)
{
    if (reportList.exists(locationID)) {
        cout << "STATUS=ERROR\nMSG=Location already exists\n";
        return;
    }
    
    EmergencyReport report(locationID, disaster, pop, injured, food, medical, water);
    
    if (!isValidReport(report)) {
        cout << "STATUS=ERROR\nMSG=Invalid report data\n";
        return;
    }
    
    report.severityScore = calculateSeverity(report);
    reportList.insert(report);
    rebuildPriorityQueue();
    logger.addLog("ADD", locationID + " (" + disaster + ")");
    
    cout << "STATUS=OK\n";
    cout << "SEVERITY_LABEL=" << report.getSeverityLabel() << "\n"; 
    cout << "MSG=Emergency Reported. Standby for dispatch.\n";
}

void handleUpdate(string locationID, string disaster, int pop, int injured, 
                  int food, int medical, int water)
{
    if (!reportList.exists(locationID)) {
        cout << "STATUS=ERROR\nMSG=Location not found\n";
        return;
    }
    
    EmergencyReport report(locationID, disaster, pop, injured, food, medical, water);
    
    if (!isValidReport(report)) {
        cout << "STATUS=ERROR\nMSG=Invalid report data\n";
        return;
    }
    
    report.severityScore = calculateSeverity(report);
    reportList.update(report);
    rebuildPriorityQueue();
    logger.addLog("UPDATE", locationID + " Severity: " + to_string(report.severityScore));
    
    cout << "STATUS=OK\n";
    cout << "SEVERITY_LABEL=" << report.getSeverityLabel() << "\n";
    cout << "MSG=Report updated successfully\n";
}

void handleViewTop()
{
    if (priorityQueue.isEmpty()) {
        cout << "STATUS=EMPTY\n";
        return;
    }
    
    EmergencyReport top = priorityQueue.getMax();
    cout << "STATUS=OK\n";
    cout << "TOP_LOC=" << top.locationID << "\n";
    cout << "TOP_DISASTER=" << top.disasterType << "\n";
    cout << "TOP_SEVERITY_LABEL=" << top.getSeverityLabel() << "\n";
    cout << "TOP_TIME=" << top.getTimeString() << "\n";
    
    cout << "TOP_POP=" << top.populationAffected << "\n";
    cout << "TOP_INJ=" << top.injuredCount << "\n";
    cout << "TOP_FOOD=" << top.foodShortage << "\n";
    cout << "TOP_MED=" << top.medicalShortage << "\n";
    cout << "TOP_WATER=" << top.waterShortage << "\n";
}

void handleDispatch(int foodSupply, int medSupply, int waterSupply)
{
    if (priorityQueue.isEmpty()) {
        cout << "STATUS=ERROR\nMSG=No emergencies to service\n";
        return;
    }
    
    EmergencyReport highest = priorityQueue.extractMax();
    int foodFulfilled = min(foodSupply, highest.foodShortage);
    int medFulfilled = min(medSupply, highest.medicalShortage);
    int waterFulfilled = min(waterSupply, highest.waterShortage);
    
    highest.foodShortage -= foodFulfilled;
    highest.medicalShortage -= medFulfilled;
    highest.waterShortage -= waterFulfilled;
    
    string status = "Complete";
    bool complete = (highest.foodShortage == 0 && highest.medicalShortage == 0 && highest.waterShortage == 0);
    
    if (complete)
    {
        reportList.deleteReport(highest.locationID);
        status = "Complete";
        dispatchQueue.enqueue(highest.locationID, highest.disasterType, highest.severityScore, "Complete");
        logger.addLog("DISPATCH_FULL", highest.locationID);
        cout << "STATUS=COMPLETE\n";
    }
    else
    {
        highest.severityScore = calculateSeverity(highest);
        reportList.update(highest);
        status = "Partial";
        dispatchQueue.enqueue(highest.locationID, highest.disasterType, highest.severityScore, "Partial");
        logger.addLog("DISPATCH_PARTIAL", highest.locationID);
        cout << "STATUS=PARTIAL\n";
        rebuildPriorityQueue(); 
    }
    
    ofstream history("Dispatch_History_Report.txt", ios::app);
    if (history.is_open())
    {
        history << left << setw(20) << highest.locationID 
               << setw(15) << highest.disasterType 
               << setw(15) << highest.getSeverityLabel()
               << setw(15) << status
               << setw(25) << highest.getTimeString() << "\n";
        history.close();
    }

    cout << "DISPATCHED_LOC=" << highest.locationID << "\n";
    cout << "MSG=Relief dispatched (" << status << ")\n";
}

void handleViewLog()
{
    logger.display(); 
}

void handleViewPendingList()
{
    if (priorityQueue.isEmpty()) {
        cout << "STATUS=EMPTY\n";
        cout << "DEBUG_HEAP_SIZE=" << priorityQueue.size() << "\n";
        return;
    }
    
    MaxHeap temp = priorityQueue;
    cout << "STATUS=OK\n";
    cout << "DEBUG_HEAP_SIZE=" << priorityQueue.size() << "\n";
    
    while (!temp.isEmpty())
    {
        EmergencyReport r = temp.extractMax();
        cout << "ITEM=" << r.locationID << "|" << r.disasterType << "|" << r.getSeverityLabel() << "\n";
    }
}

void handleViewDetails(string locID)
{
    ReportNode* node = reportList.search(locID);
    if (!node)
    {
        cout << "STATUS=ERROR\nMSG=Report not found\n";
        return;
    }
    EmergencyReport* report = &(node->data);
    
    cout << "STATUS=OK\n";
    cout << "LOC=" << report->locationID << "\n";
    cout << "DISASTER=" << report->disasterType << "\n";
    cout << "SEVERITY_LABEL=" << report->getSeverityLabel() << "\n";
    cout << "TIME=" << report->getTimeString() << "\n";
    cout << "POP=" << report->populationAffected << "\n";
    cout << "INJ=" << report->injuredCount << "\n";
    cout << "FOOD=" << report->foodShortage << "\n";
    cout << "MED=" << report->medicalShortage << "\n";
    cout << "WATER=" << report->waterShortage << "\n";
}

void processCommand(string command)
{
    if (command == "VIEW_TOP") handleViewTop(); 
    else if (command == "VIEW_PENDING_LIST") handleViewPendingList();
    else if (command.substr(0, 12) == "VIEW_DETAILS") {
        string loc;
        cin >> loc;
        handleViewDetails(loc);
    }
    else if (command == "GENERATE_REPORTS")
        generateReports();
    else if (command == "VIEW_LOG") handleViewLog();
    else if (command == "EXIT") cout << "STATUS=EXIT\n";
    else if (command.substr(0, 3) == "ADD") {
        string loc, dis; int p, i, f, m, w;
        cin >> loc >> dis >> p >> i >> f >> m >> w;
        handleAdd(loc, dis, p, i, f, m, w);
    }
    else if (command.substr(0, 6) == "UPDATE")
    {
        string loc, dis; int p, i, f, m, w;
        cin >> loc >> dis >> p >> i >> f >> m >> w;
        handleUpdate(loc, dis, p, i, f, m, w);
    }
    else if (command.substr(0, 8) == "DISPATCH")
    {
        int f, m, w;
        cin >> f >> m >> w;
        handleDispatch(f, m, w);
    }
    else
    {
        cout << "STATUS=ERROR\nMSG=Unknown command\n";
    }
    cout.flush();
}

int main()
{
    string command;
    while (cin >> command)
    {
        processCommand(command);
        if (command == "EXIT")
            break;
        cout << "---END---\n";
        cout.flush();
    }
    return 0;
}
