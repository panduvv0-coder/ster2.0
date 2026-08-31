<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>School Marks Tracker (Cloud)</title>
    <style>
        /* --- CSS STYLING --- */
        :root { --primary: #2563eb; --primary-dark: #1d4ed8; --bg: #f3f4f6; --card-bg: #ffffff; --text: #1f2937; --text-light: #6b7280; --danger: #ef4444; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--bg); color: var(--text); margin: 0; padding: 20px; line-height: 1.6; }
        .container { max-width: 1000px; margin: 0 auto; }
        header { text-align: center; margin-bottom: 30px; }
        header h1 { color: var(--primary); margin: 0; font-size: 2.5rem; }
        .card { background: var(--card-bg); border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); padding: 25px; margin-bottom: 25px; }
        .card h2 { margin-top: 0; border-bottom: 2px solid var(--bg); padding-bottom: 10px; color: var(--primary-dark); }
        .form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 15px; }
        .form-group label { display: block; font-weight: 600; margin-bottom: 5px; font-size: 0.9rem; }
        input { width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 1rem; box-sizing: border-box; }
        input:focus { outline: none; border-color: var(--primary); }
        .btn { padding: 12px 24px; border: none; border-radius: 6px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: background 0.2s; }
        .btn-primary { background: var(--primary); color: white; }
        .btn-primary:hover { background: var(--primary-dark); }
        .btn-danger { background: var(--danger); color: white; padding: 6px 12px; font-size: 0.85rem;}
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #e5e7eb; }
        th { background-color: #f9fafb; font-weight: 600; color: var(--text-light); text-transform: uppercase; font-size: 0.8rem; }
        .grade-badge { padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 0.85rem; color: white; }
        .grade-A { background: #10b981; } .grade-B { background: #3b82f6; } .grade-C { background: #f59e0b; } .grade-D { background: #f97316; } .grade-F { background: #ef4444; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .stat-box { background: #f9fafb; padding: 15px; border-radius: 8px; text-align: center; border-left: 4px solid var(--primary); }
        .stat-box h3 { margin: 0; font-size: 1.5rem; color: var(--primary); }
        .stat-box p { margin: 5px 0 0; color: var(--text-light); font-size: 0.9rem; }
        .empty-state { text-align: center; padding: 40px; color: var(--text-light); }
    </style>
</head>
<body>

    <div class="container">
        <header>
            <h1>🎓 School Marks Tracker (Cloud)</h1>
            <p>Real-time synchronized records for all students</p>
        </header>

        <!-- Input Form -->
        <div class="card">
            <h2>Add New Marks</h2>
            <form id="markForm">
                <div class="form-grid">
                    <div class="form-group">
                        <label for="studentName">Student Name</label>
                        <input type="text" id="studentName" placeholder="e.g. John Doe" required>
                    </div>
                    <div class="form-group">
                        <label for="subject">Subject</label>
                        <input type="text" id="subject" placeholder="e.g. Mathematics" required>
                    </div>
                    <div class="form-group">
                        <label for="obtained">Marks Obtained</label>
                        <input type="number" id="obtained" placeholder="e.g. 85" min="0" required>
                    </div>
                    <div class="form-group">
                        <label for="total">Total Marks</label>
                        <input type="number" id="total" placeholder="e.g. 100" min="1" required>
                    </div>
                </div>
                <button type="submit" class="btn btn-primary">Add Record to Cloud</button>
            </form>
        </div>

        <!-- Dashboard / Stats -->
        <div class="card">
            <h2>Dashboard Summary</h2>
            <div class="stats-grid">
                <div class="stat-box"><h3 id="totalEntries">...</h3><p>Total Records</p></div>
                <div class="stat-box"><h3 id="totalStudents">...</h3><p>Unique Students</p></div>
                <div class="stat-box"><h3 id="overallAvg">...</h3><p>Overall Average</p></div>
            </div>
        </div>

        <!-- Records Table -->
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                <h2 style="margin:0; border:none; padding:0;">Student Records</h2>
                <input type="text" id="searchInput" placeholder="Search by Student Name..." style="width: 200px;">
            </div>
            
            <div style="overflow-x: auto;">
                <table id="marksTable">
                    <thead>
                        <tr>
                            <th>Student Name</th>
                            <th>Subject</th>
                            <th>Obtained</th>
                            <th>Total</th>
                            <th>Percentage</th>
                            <th>Grade</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody">
                        <tr><td colspan="7" style="text-align:center; padding:20px;">Loading data from cloud...</td></tr>
                    </tbody>
                </table>
                <div id="emptyState" class="empty-state" style="display:none;">
                    <p>No records found in the database.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- FIREBASE SDK & LOGIC -->
    <script type="module">
        // Import the functions you need from the SDKs you need
        import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.0/firebase-app.js";
        import { getDatabase, ref, push, onValue, remove } from "https://www.gstatic.com/firebasejs/9.22.0/firebase-database.js";

        // YOUR FIREBASE CONFIGURATION
        const firebaseConfig = {
          apiKey: "AIzaSyCc25VI6M1Gasxs_RIHbhn_kpsQJymrGmY",
          authDomain: "ster-b530f.firebaseapp.com",
          databaseURL: "https://ster-b530f-default-rtdb.firebaseio.com",
          projectId: "ster-b530f",
          storageBucket: "ster-b530f.firebasestorage.app",
          messagingSenderId: "242192924542",
          appId: "1:242192924542:web:b41baee70078362b90bd2f"
        };

        // Initialize Firebase
        const app = initializeApp(firebaseConfig);
        const db = getDatabase(app);
        const marksRef = ref(db, 'marks');

        // DOM Elements
        const form = document.getElementById('markForm');
        const tableBody = document.getElementById('tableBody');
        const emptyState = document.getElementById('emptyState');
        const searchInput = document.getElementById('searchInput');
        
        let localMarksData = []; 

        // 1. LISTEN FOR REAL-TIME DATA
        onValue(marksRef, (snapshot) => {
            const data = snapshot.val();
            localMarksData = []; 
            
            if (data) {
                Object.keys(data).forEach(key => {
                    localMarksData.push({ id: key, ...data[key] });
                });
            }
            
            renderTable();
            updateStats();
        });

        // 2. ADD DATA TO FIREBASE
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const studentName = document.getElementById('studentName').value.trim();
            const subject = document.getElementById('subject').value.trim();
            const obtained = parseFloat(document.getElementById('obtained').value);
            const total = parseFloat(document.getElementById('total').value);

            if (obtained > total) {
                alert("Error: Marks Obtained cannot be greater than Total Marks!");
                return;
            }

            push(marksRef, {
                name: studentName,
                subject: subject,
                obtained: obtained,
                total: total,
                timestamp: Date.now()
            })
            .then(() => {
                form.reset();
                alert("Record added successfully!");
            })
            .catch((error) => {
                console.error("Error adding record: ", error);
                alert("Failed to add record. Check console.");
            });
        });

        // 3. DELETE DATA FROM FIREBASE
        window.deleteRecord = function(id) {
            if (confirm('Are you sure you want to delete this record from the cloud?')) {
                const itemRef = ref(db, 'marks/' + id);
                remove(itemRef);
            }
        }

        // 4. RENDER TABLE
        function renderTable() {
            const searchTerm = searchInput.value.toLowerCase();
            const filteredData = localMarksData.filter(mark => 
                mark.name.toLowerCase().includes(searchTerm)
            );

            tableBody.innerHTML = '';

            if (filteredData.length === 0) {
                emptyState.style.display = 'block';
                document.getElementById('marksTable').style.display = 'none';
            } else {
                emptyState.style.display = 'none';
                document.getElementById('marksTable').style.display = 'table';

                filteredData.forEach(mark => {
                    const percentage = ((mark.obtained / mark.total) * 100).toFixed(1);
                    const grade = calculateGrade(percentage);
                    const gradeClass = `grade-${grade.charAt(0)}`;

                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td><strong>${mark.name}</strong></td>
                        <td>${mark.subject}</td>
                        <td>${mark.obtained}</td>
                        <td>${mark.total}</td>
                        <td>${percentage}%</td>
                        <td><span class="grade-badge ${gradeClass}">${grade}</span></td>
                        <td><button class="btn btn-danger" onclick="deleteRecord('${mark.id}')">Delete</button></td>
                    `;
                    tableBody.appendChild(row);
                });
            }
        }

        searchInput.addEventListener('input', renderTable);

        function calculateGrade(percentage) {
            if (percentage >= 90) return 'A+';
            if (percentage >= 80) return 'A';
            if (percentage >= 70) return 'B';
            if (percentage >= 60) return 'C';
            if (percentage >= 50) return 'D';
            return 'F';
        }

        function updateStats() {
            document.getElementById('totalEntries').innerText = localMarksData.length;
            const uniqueStudents = [...new Set(localMarksData.map(mark => mark.name))];
            document.getElementById('totalStudents').innerText = uniqueStudents.length;

            if (localMarksData.length > 0) {
                let totalObtained = 0;
                let totalPossible = 0;
                localMarksData.forEach(mark => {
                    totalObtained += mark.obtained;
                    totalPossible += mark.total;
                });
                const avg = ((totalObtained / totalPossible) * 100).toFixed(1);
                document.getElementById('overallAvg').innerText = avg + '%';
            } else {
                document.getElementById('overallAvg').innerText = '0%';
            }
        }
    </script>
</body>
</html>