#include <iostream>
#include <string>
#include <cmath>
#include <ctime>
#include <sstream>
#include <iomanip>

using namespace std;

class EmergencyReport 
{
public:
    string locationID;
    string disasterType;
    int populationAffected;
    int injuredCount;
    int foodShortage;
    int medicalShortage;
    int waterShortage;
    double severityScore;
    time_t timestamp;
    
    EmergencyReport()
    {
        locationID = "";
        disasterType = "";
        populationAffected = 0;
        injuredCount = 0;
        foodShortage = 0;
        medicalShortage = 0;
        waterShortage = 0;
        severityScore = 0.0;
        timestamp = time(0);
    }
    
    EmergencyReport(string loc, string disaster, int pop, int injured, 
                   int food, int medical, int water)
    {
        locationID = loc;
        disasterType = disaster;
        populationAffected = pop;
        injuredCount = injured;
        foodShortage = food;
        medicalShortage = medical;
        waterShortage = water;
        severityScore = 0.0;
        timestamp = time(0);
    }
    
    // Get formatted timestamp string
    string getTimeString() const
    {
        struct tm* timeinfo;
        char buffer[80];
        timeinfo = localtime(&timestamp);
        strftime(buffer, 80, "%Y-%m-%d %H:%M:%S", timeinfo);
        return string(buffer);
    }
    
    string getSeverityLabel() const
    {
        if (severityScore >= 100) return "CRITICAL";
        if (severityScore >= 60) return "HIGH";
        if (severityScore >= 30) return "MODERATE";
        return "LOW";
    }
};

double calculateSeverity(const EmergencyReport& report)
{
    double disasterWeight = 0.0;
    string disaster = report.disasterType;
    
    if (disaster == "Earthquake" || disaster == "earthquake") disasterWeight = 50.0;
    else if (disaster == "Flood" || disaster == "flood") disasterWeight = 30.0;
    else if (disaster == "Fire" || disaster == "fire") disasterWeight = 20.0;
    
    double severity = (report.populationAffected * 0.001) + // Adjusted weight for realistic scores
                     (report.injuredCount * 0.5) +
                     (report.foodShortage * 2.0) +
                     (report.medicalShortage * 3.0) +
                     (report.waterShortage * 2.5) +
                     disasterWeight;
                     
    return severity;
}

bool isValidReport(const EmergencyReport& report)
{
    if (report.locationID.empty()) return false;
    if (report.disasterType.empty()) return false;
    if (report.populationAffected < 0) return false;
    if (report.injuredCount < 0) return false;
    return true;
}

void displayReport(const EmergencyReport& report)
{
    cout << "LOC=" << report.locationID << "\n";
    cout << "DISASTER=" << report.disasterType << "\n";
    cout << "SEVERITY=" << report.severityScore << "\n";
    cout << "LABEL=" << report.getSeverityLabel() << "\n";
    cout << "TIME=" << report.getTimeString() << "\n";
}
