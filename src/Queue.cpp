#include <iostream>
#include <string>

using namespace std;

class DispatchNode
{
public:
    string locationID;
    string disasterType;
    double severityScore;
    string status;
    DispatchNode* next;
    
    DispatchNode(string loc, string disaster, double severity, string stat)
    {
        locationID = loc;
        disasterType = disaster;
        severityScore = severity;
        status = stat;
        next = nullptr;
    }
};

class DispatchQueue
{
private:
    DispatchNode* front;
    DispatchNode* rear;
    int size;
    
public:
    DispatchQueue()
    {
        front = nullptr;
        rear = nullptr;
        size = 0;
    }
    
    void enqueue(string locationID, string disasterType, double severity, string status)
    {
        DispatchNode* newNode = new DispatchNode(locationID, disasterType, severity, status);
        
        if (rear == nullptr)
        {
            front = rear = newNode;
        }
        else
        {
            rear->next = newNode;
            rear = newNode;
        }
        size++;
    }
    
    bool dequeue()
    {
        if (front == nullptr) {
            return false;
        }
        
        DispatchNode* temp = front;
        front = front->next;
        
        if (front == nullptr)
        {
            rear = nullptr;
        }
        
        delete temp;
        size--;
        return true;
    }
    
    void display()
    {
        if (front == nullptr) {
            cout << "EMPTY\n";
            return;
        }
        
        DispatchNode* current = front;
        while (current != nullptr)
        {
            cout << "---DISPATCH---\n";
            cout << "LOCATION:" << current->locationID << "\n";
            cout << "DISASTER:" << current->disasterType << "\n";
            cout << "SEVERITY:" << current->severityScore << "\n";
            cout << "STATUS:" << current->status << "\n";
            current = current->next;
        }
    }
    
    bool isEmpty() 
    { 
        return front == nullptr; 
    }
    
    int getSize() 
    { 
        return size; 
    }
    
    void clear()
    {
        while (!isEmpty()) {
            dequeue();
        }
    }
    
    ~DispatchQueue()
    {
        while (front != nullptr) {
            dequeue();
        }
    }
};
