const examsList = document.getElementById("examsList");
const createExamForm = document.getElementById("createExamForm");
const message = document.getElementById("message");

if (!getToken()) {
  window.location.href = "login.html";
}

async function loadExams() {
  try {
    const response = await fetch(`${API_BASE_URL}/exams`, {
      method: "GET",
      headers: getAuthHeaders()
    });

    const data = await response.json();

    if (!response.ok) {
      message.textContent = data.detail || "Failed to load exams";
      return;
    }

    examsList.innerHTML = "";

    if (data.length === 0) {
      examsList.innerHTML = "<p>No exams available.</p>";
      return;
    }

    data.forEach(exam => {
      const examCard = document.createElement("div");
      examCard.className = "card";

      examCard.innerHTML = `
        <h3>${exam.title}</h3>
        <p>${exam.description || "No description"}</p>
        <p><strong>Duration:</strong> ${exam.duration_minutes} minutes</p>
        <div class="actions">
          <button onclick="deleteExam(${exam.id})">Delete</button>
        </div>
      `;

      examsList.appendChild(examCard);
    });

  } catch (error) {
    message.textContent = "Server error. Please try again.";
  }
}

if (examsList) {
  loadExams();
}

if (createExamForm) {
  createExamForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const examData = {
      title: document.getElementById("title").value,
      description: document.getElementById("description").value,
      duration_minutes: Number(document.getElementById("duration").value)
    };

    try {
      const response = await fetch(`${API_BASE_URL}/exams`, {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify(examData)
      });

      const data = await response.json();

      if (!response.ok) {
        message.textContent = data.detail || "Failed to create exam";
        return;
      }

      message.style.color = "green";
      message.textContent = "Exam created successfully.";

      setTimeout(() => {
        window.location.href = "exams.html";
      }, 1000);

    } catch (error) {
      message.textContent = "Server error. Please try again.";
    }
  });
}

async function deleteExam(examId) {
  const confirmDelete = confirm("Are you sure you want to delete this exam?");

  if (!confirmDelete) {
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/exams/${examId}`, {
      method: "DELETE",
      headers: getAuthHeaders()
    });

    if (!response.ok) {
      const data = await response.json();
      alert(data.detail || "Failed to delete exam");
      return;
    }

    alert("Exam deleted successfully");
    loadExams();

  } catch (error) {
    alert("Server error. Please try again.");
  }
}