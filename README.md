CSV Source ───────────┐
                      │
REST API Source ──────┤
                      │
SQLite Database ──────┤
                      │
MongoDB Database ─────┘
                      │
                      ▼
                   Extract
                      │
                      ▼
             Source Validation
                      │
                      ▼
                Standardize
                      │
                      ▼
                 Integrate
                      │
                      ▼
                   Clean
                  /     \\
                 /       \\
                ▼         ▼
       Clean Records   Rejected Records
                │         │
                │         ▼
                │    rejected_records.csv
                │
                ▼
             Transform
                │
                ▼
          Final Validation
                │
           ┌────┴────┐
           ▼         ▼
       CSV Output  MongoDB Output
           │         │
           ▼         ▼
   final_dataset.csv
   processed_students