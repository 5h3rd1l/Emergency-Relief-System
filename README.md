# 🚨 Emergency Relief Command Center

> A deployment-ready emergency relief prioritization system with a professional Python/Tkinter GUI powered by a high-performance C++ backend — no STL containers used.

---

## 📌 Overview

The Emergency Relief Command Center is a full-stack disaster response application designed for non-technical operators. Field staff interact with a clean, guided dashboard while the backend silently handles all data structure operations — calculating severity scores, sorting by priority, and dispatching relief in the right order.

No command line. No technical jargon. No frozen UI.

---

## 🏗️ System Architecture

The system is split into two layers that communicate via a strict `KEY=VALUE` machine protocol.

```
┌─────────────────────────────────┐
│   Python / Tkinter Frontend     │  ← Operator interacts here
│  - Status Dashboard             │
│  - GPS Location Input           │
│  - Crisis Assessment Sliders    │
│  - Dispatch Button              │
└────────────┬────────────────────┘
             │  KEY=VALUE Protocol
             │  (temp_input.txt)
┌────────────▼────────────────────┐
│     C++ Backend Engine          │  ← Runs silently
│  - Linked List (storage)        │
│  - Max Heap (priority)          │
│  - Queue (dispatch order)       │
│  - Merge Sort (ranking)         │
│  - Severity Calculator          │
└─────────────────────────────────┘
```

### Frontend (Python/Tkinter)
- **Status Dashboard** — Color-coded, auto-refreshing severity monitor
- **Location Intelligence** — Accepts Lat/Lon coordinates, generates internal IDs
- **Crisis Assessment** — Simple sliders for resource shortage levels
- **Threaded Core** — UI never freezes during backend calculations

### Backend (C++)
- Runs silently with no user interaction
- Outputs strict `KEY=VALUE` machine protocol
- Manages all data structures manually — no STL containers

---

## 🏗️ Data Structures Implemented

All data structures are built from scratch.

| Structure | Implementation | Purpose |
|---|---|---|
| Singly Linked List | Pointer-based nodes | Dynamic storage of emergency reports |
| Max Heap | Array-based | Priority queue — highest severity first |
| Queue | Linked list-based | FIFO relief package dispatch order |

---

## 🔧 Algorithms

| Algorithm | Time Complexity | Space | Notes |
|---|---|---|---|
| Merge Sort | O(n log n) | O(n) | Primary sort — stable, divide-and-conquer |
| Selection Sort | O(n²) | O(1) | Included for educational comparison |
| Heap Insert | O(log n) | — | heapifyUp |
| Heap Extract Max | O(log n) | — | heapifyDown |

---

## 📊 Severity Calculation

```
Base Score = (Population / 1000 × 0.3)
           + (Injured       × 2.0)
           + (Food Shortage × 5.0)
           + (Med Shortage  × 8.0)
           + (Water Shortage× 7.0)

Final Score = Base Score × Disaster Multiplier
```

**Disaster Multipliers:**
- 🌍 Earthquake — `1.5×` (structural damage, aftershock risk)
- 🌊 Flood — `1.3×` (displacement, disease spread)
- 🔥 Fire — `1.2×` (rapid spread, smoke inhalation)

**Weight Rationale:**
- Medical Shortage `(8)` — most critical for survival
- Water Shortage `(7)` — essential for life
- Food Shortage `(5)` — important but less immediate
- Injured Count `(2)` — direct medical burden
- Population `(0.3)` — normalized context factor

---

## 🎛️ Features at a Glance

| Feature | User Experience | Backend Reality |
|---|---|---|
| **Prioritization** | Status panel turns Red / Orange | Max Heap re-sorts O(log n) |
| **Locations** | GPS Coordinates (Lat/Lon) | Internal string IDs |
| **Dispatch** | "Dispatch Resources" button | ExtractMax + Queue update |
| **Audit** | Read-only action log | Logger class storage |

---

## 🔄 System Workflow

```
Operator enters report (GUI)
        │
        ▼
C++ Backend stores in Linked List
        │
        ▼
Severity Score calculated via formula
        │
        ▼
Merge Sort ranks all reports (descending)
        │
        ▼
Max Heap built for priority extraction
        │
        ▼
Operator clicks "Dispatch" (GUI)
        │
        ▼
ExtractMax → Relief Queue (FIFO dispatch)
        │
        ▼
Dashboard updates with delivery order
```

---

## 🗂️ Code Structure

```
EmergencyReliefSystem/
├── src/
│   └── main.cpp
│       ├── EmergencyReport         (struct)
│       ├── ReportLinkedList        (class)
│       │   ├── insert()
│       │   ├── display()
│       │   ├── toArray()
│       │   └── fromArray()
│       ├── MaxHeap                 (class)
│       │   ├── insert()
│       │   ├── extractMax()
│       │   ├── heapifyUp()
│       │   └── heapifyDown()
│       ├── ReliefQueue             (class)
│       │   ├── enqueue()
│       │   ├── dequeue()
│       │   └── display()
│       ├── Sorter                  (class)
│       │   ├── mergeSort()
│       │   └── selectionSort()
│       ├── SeverityCalculator      (class)
│       │   └── calculateSeverity()
│       └── EmergencyReliefSystem   (class)
│           └── run()
├── gui.py                          ← Python/Tkinter frontend
└── temp_input.txt                  ← Inter-language communication bridge
```

---

## ⚙️ Build & Run

### Prerequisites
- `g++` (GCC) with C++11 support
- Python 3.x with Tkinter

### Step 1 — Compile the Backend Engine
```bash
g++ -o ReliefSystem.exe src/main.cpp -std=c++11
```

### Step 2 — Launch the Command Center
```bash
python gui.py
```

The GUI handles everything from here. No further terminal interaction needed.

---

## 📝 Sample

**Operator Input (via GUI sliders & fields):**
```
Location:        Lat 33.6, Lon 73.1
Disaster Type:   Earthquake
Population:      5000
Injured:         150
Food Shortage:   8 / 10
Medical:         9 / 10
Water:           7 / 10
```

**Severity Score (calculated by backend):**
```
Base  = 1.5 + 300 + 40 + 72 + 49 = 462.5
Final = 462.5 × 1.5 = 693.75  →  🔴 CRITICAL
```

---

## ✅ Requirements Met

- No STL containers (`vector`, `queue`, `priority_queue`, `list`, etc.)
- No `<algorithm>` header — all sorting implemented manually
- Headers used: `<iostream>`, `<string>`, `<cmath>` only
- Full OOP design with encapsulated classes
- Threaded Python frontend — UI never blocks
- Clean inter-language communication via file protocol

---

## 📚 Concepts Demonstrated

- Dynamic memory management (pointers, `new`/`delete`)
- Recursion (merge sort)
- Tree properties (heap structure and heapify operations)
- Big-O complexity analysis
- Inter-language communication (C++ ↔ Python)
- UX-first software design & separation of concerns

---

## 📄 License

Educational project — free to use for learning purposes.
