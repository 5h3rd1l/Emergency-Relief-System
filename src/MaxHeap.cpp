#include <iostream>
#include <string>

using namespace std;

class MaxHeap
{
private:
    static const int MAX_SIZE = 100;
    EmergencyReport heap[MAX_SIZE];
    int heapSize;
    
    int parent(int i) 
    { 
        return (i - 1) / 2; 
    }
    
    int leftChild(int i) 
    { 
        return 2 * i + 1; 
    }
    
    int rightChild(int i) 
    { 
        return 2 * i + 2; 
    }
    
    void swap(int i, int j)
    {
        EmergencyReport temp = heap[i];
        heap[i] = heap[j];
        heap[j] = temp;
    }
    
    void heapifyUp(int index)
    {
        while (index > 0 && heap[parent(index)].severityScore < heap[index].severityScore) {
            swap(index, parent(index));
            index = parent(index);
        }
    }
    
    void heapifyDown(int index)
    {
        int maxIndex = index;
        int left = leftChild(index);
        int right = rightChild(index);
        
        if (left < heapSize && heap[left].severityScore > heap[maxIndex].severityScore)
        {
            maxIndex = left;
        }
        
        if (right < heapSize && heap[right].severityScore > heap[maxIndex].severityScore)
        {
            maxIndex = right;
        }
        
        if (index != maxIndex)
        {
            swap(index, maxIndex);
            heapifyDown(maxIndex);
        }
    }
    
public:
    MaxHeap()
    {
        heapSize = 0;
    }
    
    bool insert(EmergencyReport report)
    {
        if (heapSize >= MAX_SIZE) {
            return false;
        }
        
        heap[heapSize] = report;
        heapifyUp(heapSize);
        heapSize++;
        return true;
    }
    
    EmergencyReport extractMax()
    {
        if (heapSize == 0) {
            return EmergencyReport();
        }
        
        EmergencyReport maxReport = heap[0];
        heap[0] = heap[heapSize - 1];
        heapSize--;
        heapifyDown(0);
        
        return maxReport;
    }
    
    EmergencyReport getMax()
    {
        if (heapSize == 0) {
            return EmergencyReport();
        }
        return heap[0];
    }
    
    void buildHeap(EmergencyReport* reports, int count)
    {
        heapSize = 0;
        for (int i = 0; i < count && i < MAX_SIZE; i++)
        {
            heap[i] = reports[i];
            heapSize++;
        }
        
        for (int i = (heapSize / 2) - 1; i >= 0; i--)
        {
            heapifyDown(i);
        }
    }
    
    void rebuildHeap(EmergencyReport* reports, int count)
    {
        buildHeap(reports, count);
    }
    
    void clear() {
        heapSize = 0;
    }
    
    bool isEmpty() 
    { 
        return heapSize == 0; 
    }
    
    int size() 
    { 
        return heapSize; 
    }
    
    void displayHeap() {
        if (heapSize == 0) {
            cout << "EMPTY\n";
            return;
        }
        
        for (int i = 0; i < heapSize; i++)
        {
            cout << "---PRIORITY:" << (i + 1) << "---\n";
            cout << "LOCATION:" << heap[i].locationID << "\n";
            cout << "DISASTER:" << heap[i].disasterType << "\n";
            cout << "SEVERITY:" << heap[i].severityScore << "\n";
        }
    }
};
