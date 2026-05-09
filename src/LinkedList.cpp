#include <iostream>
#include <string>
#include "EmergencyReport.cpp"

using namespace std;

class ReportNode
{
public:
    EmergencyReport data;
    ReportNode* next;
    
    ReportNode(EmergencyReport report)
    {
        data = report;
        next = nullptr;
    }
};

class ReportLinkedList
{
private:
    ReportNode* head;
    int size;
    
public:
    ReportLinkedList()
    {
        head = nullptr;
        size = 0;
    }
    
    void insert(EmergencyReport report)
    {
        ReportNode* newNode = new ReportNode(report);
        newNode->next = head;
        head = newNode;
        size++;
    }
    
    ReportNode* search(string locationID)
    {
        ReportNode* current = head;
        while (current != nullptr) {
            if (current->data.locationID == locationID) {
                return current;
            }
            current = current->next;
        }
        return nullptr;
    }
    
    bool update(EmergencyReport report)
    {
        ReportNode* node = search(report.locationID);
        if (node != nullptr)
        {
            node->data = report;
            return true;
        }
        return false;
    }
    
    bool deleteReport(string locationID)
    {
        if (head == nullptr) return false;
        
        if (head->data.locationID == locationID)
        {
            ReportNode* temp = head;
            head = head->next;
            delete temp;
            size--;
            return true;
        }
        
        // Search for node to delete
        ReportNode* current = head;
        while (current->next != nullptr)
        {
            if (current->next->data.locationID == locationID) {
                ReportNode* temp = current->next;
                current->next = current->next->next;
                delete temp;
                size--;
                return true;
            }
            current = current->next;
        }
        
        return false;
    }
    
    EmergencyReport* getAllReports(int& count)
    {
        count = size;
        if (size == 0) return nullptr;
        
        EmergencyReport* reports = new EmergencyReport[size];
        ReportNode* current = head;
        int index = 0;
        
        while (current != nullptr)
        {
            reports[index++] = current->data;
            current = current->next;
        }
        
        return reports;
    }
    
    bool exists(string locationID)
    {
        return search(locationID) != nullptr;
    }
    
    int getSize() 
    { 
        return size; 
    }
    
    bool isEmpty() 
    { 
        return head == nullptr; 
    }
    
    void displayAll()
    {
        if (head == nullptr) {
            cout << "EMPTY\n";
            return;
        }
        
        ReportNode* current = head;
        while (current != nullptr)
        {
            cout << "---REPORT---\n";
            cout << "LOCATION:" << current->data.locationID << "\n";
            cout << "DISASTER:" << current->data.disasterType << "\n";
            cout << "POPULATION:" << current->data.populationAffected << "\n";
            cout << "INJURED:" << current->data.injuredCount << "\n";
            cout << "FOOD:" << current->data.foodShortage << "\n";
            cout << "MEDICAL:" << current->data.medicalShortage << "\n";
            cout << "WATER:" << current->data.waterShortage << "\n";
            cout << "SEVERITY:" << current->data.severityScore << "\n";
            current = current->next;
        }
    }
    
    ~ReportLinkedList()
    {
        ReportNode* current = head;
        while (current != nullptr) {
            ReportNode* temp = current;
            current = current->next;
            delete temp;
        }
    }
};
